#!/usr/bin/env python3
"""Checagem segura de cabeçalhos — só no laboratório sintético em 127.0.0.1, só com escopo registrado.

Antes de mandar UMA requisição GET, confere o arquivo de escopo:
  - status "AUTORIZADO_LAB_LOCAL" e registro de permissão preenchido
  - o alvo é exatamente o listado em "alvos_permitidos" (e é http://127.0.0.1:<porta>/)
  - dados "sinteticos"
  - a janela de teste tem fuso horário e está valendo agora
  - limite de no máximo 1 requisição por execução
Recusa host remoto, nome (localhost), redirecionamento, proxy do sistema e caminho fora da raiz.

  python3 kit/scripts/checagem_segura.py --lab-local-autorizado
  python3 kit/scripts/checagem_segura.py --escopo meu-escopo.json --alvo http://127.0.0.1:8181/
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import ErroDeSeguranca, abridor_seguro  # noqa: E402
from laboratorio import CABECALHOS_CORRECAO, MARCA, PORTA_PADRAO  # noqa: E402

STATUS_OK = "AUTORIZADO_LAB_LOCAL"


def normalizar_alvo(alvo: str) -> str:
    p = urllib.parse.urlsplit(alvo.strip())
    # IP numérico evita truques de DNS; só a raiz do laboratório.
    if p.scheme != "http" or p.hostname != "127.0.0.1":
        raise ErroDeSeguranca("alvo recusado: esta checagem só roda em http://127.0.0.1 (laboratório local)")
    if p.username or p.password or p.query or p.fragment or p.path not in ("", "/"):
        raise ErroDeSeguranca("alvo recusado: use só a raiz do laboratório, sem usuário, query ou fragmento")
    if not p.port:
        raise ErroDeSeguranca("alvo recusado: informe a porta do laboratório")
    return f"http://127.0.0.1:{p.port}/"


def _data(texto: str, campo: str) -> dt.datetime:
    try:
        valor = dt.datetime.fromisoformat(texto)
    except (TypeError, ValueError):
        raise ErroDeSeguranca(f"escopo: '{campo}' não é uma data ISO válida") from None
    if valor.tzinfo is None:
        raise ErroDeSeguranca(f"escopo: '{campo}' precisa de fuso horário (ex.: -03:00)")
    return valor


def validar_escopo(escopo: dict, alvo: str, agora: dt.datetime | None = None) -> str:
    alvo_ok = normalizar_alvo(alvo)
    if escopo.get("status") != STATUS_OK:
        raise ErroDeSeguranca("escopo negado: status não é AUTORIZADO_LAB_LOCAL")
    if not str(escopo.get("registro_da_permissao", "")).strip() or "PREENCHA" in str(escopo.get("registro_da_permissao")):
        raise ErroDeSeguranca("escopo negado: falta o registro da permissão")
    permitidos = [normalizar_alvo(a) for a in escopo.get("alvos_permitidos", [])]
    if permitidos != [alvo_ok]:
        raise ErroDeSeguranca("escopo negado: o alvo não é exatamente o único alvo permitido")
    if escopo.get("dados") != "sinteticos":
        raise ErroDeSeguranca("escopo negado: o laboratório precisa ter só dados sintéticos")
    janela = escopo.get("janela") or {}
    inicio, fim = _data(janela.get("inicio"), "inicio"), _data(janela.get("fim"), "fim")
    agora = agora or dt.datetime.now(dt.timezone.utc)
    if not (inicio <= agora < fim):
        raise ErroDeSeguranca("escopo vencido ou ainda não começou: a janela de teste não vale agora")
    if (escopo.get("limites") or {}).get("max_requisicoes") != 1:
        raise ErroDeSeguranca("escopo negado: esta checagem exige limite de exatamente 1 requisição")
    return alvo_ok


def escopo_lab_local(alvo: str, minutos: int = 10) -> dict:
    agora = dt.datetime.now(dt.timezone.utc)
    return {
        "status": STATUS_OK,
        "registro_da_permissao": "laboratório sintético no meu próprio computador",
        "alvos_permitidos": [normalizar_alvo(alvo)],
        "dados": "sinteticos",
        "janela": {"inicio": agora.isoformat(), "fim": (agora + dt.timedelta(minutes=minutos)).isoformat()},
        "limites": {"max_requisicoes": 1},
    }


def checar(escopo: dict, alvo: str) -> dict:
    alvo_ok = validar_escopo(escopo, alvo)
    req = urllib.request.Request(alvo_ok, method="GET", headers={"User-Agent": "checagem-segura-inema/1"})
    with abridor_seguro().open(req, timeout=5) as resp:
        corpo = resp.read(8192)
        if MARCA.encode() not in corpo:
            raise ErroDeSeguranca("parei: isto não é o laboratório sintético do kit")
        recebidos = {k.lower(): v for k, v in resp.headers.items()}
    achados = []
    for nome, esperado in CABECALHOS_CORRECAO.items():
        valor = recebidos.get(nome.lower(), "")
        if valor.lower() != esperado:
            achados.append({
                "cabecalho": nome,
                "observado": valor or "(ausente)",
                "correcao": f"configurar o servidor para enviar {nome}: {esperado}",
            })
    return {
        "alvo": alvo_ok,
        "requisicoes": 1,
        "laboratorio_sintetico": True,
        "achados": achados,
        "leitura": "Observação de configuração (endurecimento). Não prova invasão nem vazamento.",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Checagem de cabeçalhos só no laboratório local, com escopo.")
    ap.add_argument("--alvo", default=f"http://127.0.0.1:{PORTA_PADRAO}/")
    ap.add_argument("--escopo", help="arquivo JSON de escopo (veja kit/exemplos/escopo-autorizado.exemplo.json)")
    ap.add_argument("--lab-local-autorizado", action="store_true",
                    help="eu autorizo testar o MEU laboratório sintético local pelos próximos 10 minutos")
    a = ap.parse_args(argv)
    try:
        if a.lab_local_autorizado:
            escopo = escopo_lab_local(a.alvo)
        elif a.escopo:
            escopo = json.loads(Path(a.escopo).read_text(encoding="utf-8"))
        else:
            raise ErroDeSeguranca("sem escopo, sem teste: use --escopo ou --lab-local-autorizado")
        print(json.dumps(checar(escopo, a.alvo), ensure_ascii=False, indent=2))
        return 0
    except Exception as erro:  # noqa: BLE001
        print(json.dumps({"recusado": True, "motivo": str(erro) or type(erro).__name__}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
