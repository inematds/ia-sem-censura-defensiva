#!/usr/bin/env python3
"""Guarda ociosa da RunPod: um proxy local que conta o tempo sem uso e, se você ligar, para o SEU Pod.

Regras de fábrica:
  - escuta só em 127.0.0.1 (nunca na rede);
  - exige um token local (arquivo em INEMA_TOKEN_LOCAL_ARQ) em toda requisição;
  - recusa requisição de navegador (cabeçalho Origin) e qualquer rota fora de /v1/models e /v1/chat/completions;
  - começa em SIMULAÇÃO: só avisa "simulacao_pararia";
  - só para de verdade com --parar-de-verdade + --pod-id + --pod-nome exatos + chave de controle em
    INEMA_CHAVE_RUNPOD_ARQ; confere ID e nome antes e confirma EXITED depois;
  - nunca cria, liga ou apaga Pod.

Ela não é teto de cobrança: se o computador dormir, o processo cair ou outro cliente falar direto com o Pod,
ela não vê. Armazenamento continua cobrando com o Pod parado.

  python3 kit/scripts/guarda_ociosa.py --upstream https://SEU-ENDPOINT/v1 --ocioso 900
"""
from __future__ import annotations

import argparse
import hmac
import http.client
import json
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import ErroDeSeguranca, abridor_seguro, ler_segredo, validar_url_base  # noqa: E402

PORTA_PADRAO = 8282
API_RUNPOD = "https://rest.runpod.io/v1"
ROTAS = {"/v1/models": "GET", "/v1/chat/completions": "POST"}
MAX_CORPO = 4 * 1024 * 1024

SIMULACAO = "simulacao_pararia"
PARADO = "parado_confirmado"
FALHOU = "parada_falhou_ou_nao_confirmada"


class Relogio:
    """Conta requisições em andamento e o instante do último uso."""

    def __init__(self, limite_s: float, parar: Callable[[], bool] | None = None,
                 agora: Callable[[], float] = time.monotonic):
        self.limite_s = limite_s
        self.parar = parar
        self.agora = agora
        self.ultimo_uso = agora()
        self.em_andamento = 0
        self.ocupado = False      # uma tentativa de parada está rodando
        self.encerrado = False    # Pod confirmado parado
        self.avisou = False       # já avisou neste período ocioso
        self._trava = threading.Lock()

    def entrar(self) -> bool:
        with self._trava:
            if self.ocupado or self.encerrado:
                return False
            self.em_andamento += 1
            self.ultimo_uso = self.agora()
            self.avisou = False
            return True

    def sair(self) -> None:
        with self._trava:
            self.em_andamento = max(0, self.em_andamento - 1)
            self.ultimo_uso = self.agora()

    def verificar(self) -> str | None:
        with self._trava:
            ocioso = self.agora() - self.ultimo_uso
            if self.em_andamento or self.ocupado or self.encerrado or self.avisou or ocioso < self.limite_s:
                return None
            self.ocupado = True
        try:
            if self.parar is None:
                with self._trava:
                    self.avisou = True
                return SIMULACAO
            try:
                ok = bool(self.parar())
            except Exception:  # noqa: BLE001
                ok = False
            with self._trava:
                if ok:
                    self.encerrado = True
                    self.avisou = True
                else:
                    self.ultimo_uso = self.agora()  # tenta de novo depois de outro período ocioso
            return PARADO if ok else FALHOU
        finally:
            with self._trava:
                self.ocupado = False


def parar_pod(pod_id: str, pod_nome: str, chave: str, api: str = API_RUNPOD,
              tentativas: int = 10, espera_s: float = 3.0) -> bool:
    """Para UM Pod depois de conferir ID e nome. Devolve True só se ler EXITED depois."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{4,64}", pod_id or ""):
        raise ErroDeSeguranca("ID de Pod inválido")
    if not pod_nome:
        raise ErroDeSeguranca("informe o nome exato do Pod")
    base = validar_url_base(api) + "/pods/" + pod_id
    abridor = abridor_seguro()

    def chamar(metodo: str, url: str) -> dict:
        req = urllib.request.Request(url, method=metodo, headers={"Authorization": f"Bearer {chave}"})
        with abridor.open(req, timeout=30) as r:
            bruto = r.read()
        return json.loads(bruto) if bruto else {}

    antes = chamar("GET", base)
    if antes.get("id") != pod_id or antes.get("name") != pod_nome:
        raise ErroDeSeguranca("o Pod encontrado não tem o ID e o nome informados; nada foi parado")
    if antes.get("desiredStatus") == "EXITED":
        return True
    chamar("POST", base + "/stop")
    for _ in range(tentativas):
        depois = chamar("GET", base)
        if depois.get("id") == pod_id and depois.get("desiredStatus") == "EXITED":
            return True
        time.sleep(espera_s)
    return False


class Encaminhador(BaseHTTPRequestHandler):
    relogio: Relogio
    upstream: str
    chave_upstream: str | None = None
    token_local: str = ""

    def log_message(self, *args):  # não registra pedidos, respostas nem chaves
        return

    def do_GET(self):
        self._tratar()

    def do_POST(self):
        self._tratar()

    def _recusar(self, codigo: int, motivo: str = "") -> None:
        self.send_error(codigo, motivo or None)

    def _tratar(self) -> None:
        if self.headers.get("Origin"):
            return self._recusar(403, "pedido de navegador recusado")
        esperado = f"Bearer {self.token_local}"
        if not self.token_local or not hmac.compare_digest(self.headers.get("Authorization", ""), esperado):
            return self._recusar(401)
        rota = urllib.parse.urlsplit(self.path)
        if rota.query or rota.fragment or self.path not in ROTAS:
            return self._recusar(404)
        if ROTAS[self.path] != self.command:
            return self._recusar(405)
        if self.headers.get("Transfer-Encoding"):
            return self._recusar(411)
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self._recusar(400)
        if tamanho < 0 or tamanho > MAX_CORPO:
            return self._recusar(413)
        if self.command == "POST" and not self.headers.get("Content-Type", "").lower().startswith("application/json"):
            return self._recusar(415)
        if not self.relogio.entrar():
            return self._recusar(503, "Pod parado ou parando")
        conexao = None
        try:
            corpo = self.rfile.read(tamanho) if tamanho else None
            alvo = urllib.parse.urlsplit(self.upstream)
            Classe = http.client.HTTPSConnection if alvo.scheme == "https" else http.client.HTTPConnection
            conexao = Classe(alvo.hostname, alvo.port, timeout=300)
            cab = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
            if self.chave_upstream:
                cab["Authorization"] = f"Bearer {self.chave_upstream}"
            caminho = alvo.path.rstrip("/") + self.path[len("/v1"):]
            conexao.request(self.command, caminho, body=corpo, headers=cab)
            resp = conexao.getresponse()
            if 300 <= resp.status < 400:  # nunca seguir redirecionamento levando a chave
                return self._recusar(502, "redirecionamento do upstream recusado")
            self.send_response(resp.status)
            self.send_header("Content-Type", resp.getheader("Content-Type", "application/json"))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "close")
            self.end_headers()
            while True:  # repassa em pedaços: resposta em streaming conta como "em uso" até fechar
                pedaco = resp.read1(16384)
                if not pedaco:
                    break
                self.wfile.write(pedaco)
                self.wfile.flush()
        except Exception:  # noqa: BLE001
            self.close_connection = True
        finally:
            if conexao:
                conexao.close()
            self.relogio.sair()


def montar_servidor(upstream: str, token_local: str, chave_upstream: str | None, relogio: Relogio,
                    porta: int = PORTA_PADRAO) -> ThreadingHTTPServer:
    if not token_local:
        raise ErroDeSeguranca("token local vazio")
    classe = type("EncaminhadorConfigurado", (Encaminhador,), {
        "relogio": relogio, "upstream": validar_url_base(upstream),
        "chave_upstream": chave_upstream, "token_local": token_local,
    })
    srv = ThreadingHTTPServer(("127.0.0.1", porta), classe)
    srv.daemon_threads = True
    return srv


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Proxy local com guarda de tempo ocioso (simulação por padrão).")
    ap.add_argument("--upstream", required=True, help="endpoint autenticado do modelo, terminando em /v1")
    ap.add_argument("--porta", type=int, default=PORTA_PADRAO)
    ap.add_argument("--ocioso", type=int, default=900, help="segundos sem uso antes de agir (mínimo 60)")
    ap.add_argument("--parar-de-verdade", action="store_true", help="sai da simulação e para o Pod indicado")
    ap.add_argument("--pod-id")
    ap.add_argument("--pod-nome")
    a = ap.parse_args(argv)
    if a.ocioso < 60:
        ap.error("use pelo menos 60 segundos")
    try:
        token = ler_segredo("INEMA_TOKEN_LOCAL_ARQ", obrigatorio=True)
        chave_modelo = ler_segredo("INEMA_CHAVE_MODELO_ARQ")
        parar = None
        if a.parar_de_verdade:
            if not a.pod_id or not a.pod_nome:
                raise ErroDeSeguranca("para parar de verdade, informe --pod-id e --pod-nome exatos")
            chave_runpod = ler_segredo("INEMA_CHAVE_RUNPOD_ARQ", obrigatorio=True)
            parar = lambda: parar_pod(a.pod_id, a.pod_nome, chave_runpod)  # noqa: E731
        relogio = Relogio(a.ocioso, parar)
        srv = montar_servidor(a.upstream, token, chave_modelo, relogio, a.porta)
    except Exception as erro:  # noqa: BLE001
        print(f"Configuração recusada: {erro}", file=sys.stderr)
        return 2
    fim = threading.Event()

    def vigiar() -> None:
        while not fim.wait(5):
            evento = relogio.verificar()
            if evento:
                print(json.dumps({"guarda_ociosa": evento}), flush=True)

    threading.Thread(target=vigiar, daemon=True).start()
    modo = "PARADA REAL" if a.parar_de_verdade else "SIMULAÇÃO"
    print(json.dumps({"escutando": f"http://127.0.0.1:{a.porta}/v1", "modo": modo, "ocioso_s": a.ocioso},
                     ensure_ascii=False), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        fim.set()
        srv.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
