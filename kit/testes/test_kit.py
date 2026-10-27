"""Testes offline do kit. Tudo roda em 127.0.0.1 com servidores falsos; nenhuma chave real, nenhuma internet.

  python3 -m unittest discover -s kit/testes -v
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))

import checa_endpoint  # noqa: E402
import checagem_segura  # noqa: E402
import comum  # noqa: E402
import guarda_ociosa  # noqa: E402
import laboratorio  # noqa: E402


def subir(servidor: ThreadingHTTPServer) -> str:
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{servidor.server_port}/"


def pedir(url: str, metodo: str = "GET", corpo: bytes | None = None, cab: dict | None = None):
    req = urllib.request.Request(url, data=corpo, method=metodo, headers=cab or {})
    abridor = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return abridor.open(req, timeout=10)


class TestEscopoELaboratorio(unittest.TestCase):
    def setUp(self):
        self.srv = laboratorio.criar_servidor(0)
        self.alvo = subir(self.srv)
        self.escopo = checagem_segura.escopo_lab_local(self.alvo)

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()

    def test_exemplo_de_escopo_e_negado(self):
        exemplo = json.loads((RAIZ / "exemplos" / "escopo-autorizado.exemplo.json").read_text(encoding="utf-8"))
        with self.assertRaises(comum.ErroDeSeguranca):
            checagem_segura.validar_escopo(exemplo, self.alvo)

    def test_sem_registro_de_permissao_e_negado(self):
        self.escopo["registro_da_permissao"] = ""
        with self.assertRaises(comum.ErroDeSeguranca):
            checagem_segura.validar_escopo(self.escopo, self.alvo)

    def test_alvo_remoto_recusado(self):
        porta = self.srv.server_port
        for alvo in ["https://exemplo.com.br/", "http://10.0.0.5:8181/", f"http://localhost:{porta}/",
                     f"http://127.0.0.1.exemplo.test:{porta}/", f"http://x@127.0.0.1:{porta}/",
                     f"http://127.0.0.1:{porta}/admin", f"http://127.0.0.1:{porta}/?q=1", "http://127.0.0.1/"]:
            with self.subTest(alvo=alvo), self.assertRaises(comum.ErroDeSeguranca):
                checagem_segura.validar_escopo(self.escopo, alvo)

    def test_alvo_fora_da_lista_recusado(self):
        outro = f"http://127.0.0.1:{self.srv.server_port + 1}/"
        with self.assertRaises(comum.ErroDeSeguranca):
            checagem_segura.validar_escopo(self.escopo, outro)

    def test_escopo_vencido_recusado(self):
        self.escopo["janela"]["fim"] = "2020-01-01T00:00:00+00:00"
        with self.assertRaises(comum.ErroDeSeguranca):
            checagem_segura.validar_escopo(self.escopo, self.alvo)

    def test_janela_sem_fuso_recusada(self):
        self.escopo["janela"]["inicio"] = "2026-01-01T00:00:00"
        with self.assertRaises(comum.ErroDeSeguranca):
            checagem_segura.validar_escopo(self.escopo, self.alvo)

    def test_limite_de_requisicoes_diferente_de_um_recusado(self):
        self.escopo["limites"]["max_requisicoes"] = 50
        with self.assertRaises(comum.ErroDeSeguranca):
            checagem_segura.validar_escopo(self.escopo, self.alvo)

    def test_achado_sintetico_e_depois_correcao(self):
        antes = checagem_segura.checar(self.escopo, self.alvo)
        self.assertEqual({a["cabecalho"] for a in antes["achados"]}, {"X-Content-Type-Options", "Referrer-Policy"})
        self.assertEqual(antes["requisicoes"], 1)
        corrigido = laboratorio.criar_servidor(0, corrigido=True)
        try:
            alvo2 = subir(corrigido)
            depois = checagem_segura.checar(checagem_segura.escopo_lab_local(alvo2), alvo2)
            self.assertEqual(depois["achados"], [])
        finally:
            corrigido.shutdown()
            corrigido.server_close()

    def test_recusa_servidor_que_nao_e_o_laboratorio(self):
        class Outro(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"<h1>outro site</h1>")

        srv = ThreadingHTTPServer(("127.0.0.1", 0), Outro)
        try:
            alvo = subir(srv)
            with self.assertRaises(comum.ErroDeSeguranca):
                checagem_segura.checar(checagem_segura.escopo_lab_local(alvo), alvo)
        finally:
            srv.shutdown()
            srv.server_close()

    def test_cli_sem_escopo_recusa(self):
        self.assertEqual(checagem_segura.main(["--alvo", self.alvo]), 2)


class TestUrlEChave(unittest.TestCase):
    def test_url_base(self):
        self.assertEqual(comum.validar_url_base("http://127.0.0.1:1234/v1/"), "http://127.0.0.1:1234/v1")
        self.assertEqual(comum.validar_url_base("https://api.exemplo.com/v1"), "https://api.exemplo.com/v1")
        for url in ["http://api.exemplo.com/v1", "https://chave@api.exemplo.com/v1",
                    "https://api.exemplo.com/v1?key=abc", "ftp://127.0.0.1/", "https:///v1"]:
            with self.subTest(url=url), self.assertRaises(comum.ErroDeSeguranca):
                comum.validar_url_base(url)

    @unittest.skipIf(os.name == "nt", "permissão de arquivo é do Linux/macOS")
    def test_chave_com_permissao_aberta_recusada(self):
        with tempfile.TemporaryDirectory() as d:
            arq = Path(d) / "chave"
            arq.write_text("valor-falso\n")
            os.chmod(arq, 0o644)
            os.environ["INEMA_TESTE_ARQ"] = str(arq)
            try:
                with self.assertRaises(comum.ErroDeSeguranca):
                    comum.ler_segredo("INEMA_TESTE_ARQ")
                os.chmod(arq, 0o600)
                self.assertEqual(comum.ler_segredo("INEMA_TESTE_ARQ"), "valor-falso")
            finally:
                del os.environ["INEMA_TESTE_ARQ"]


class TestRelogioOcioso(unittest.TestCase):
    def test_simulacao_avisa_uma_vez_e_nova_atividade_reinicia(self):
        t = [0.0]
        r = guarda_ociosa.Relogio(60, agora=lambda: t[0])
        t[0] = 59
        self.assertIsNone(r.verificar())
        t[0] = 61
        self.assertEqual(r.verificar(), guarda_ociosa.SIMULACAO)
        self.assertIsNone(r.verificar())
        self.assertTrue(r.entrar())
        r.sair()
        t[0] = 100
        self.assertIsNone(r.verificar())
        t[0] = 122
        self.assertEqual(r.verificar(), guarda_ociosa.SIMULACAO)

    def test_requisicao_em_andamento_impede_parada(self):
        t = [0.0]
        chamadas = []
        r = guarda_ociosa.Relogio(60, parar=lambda: chamadas.append(1) or True, agora=lambda: t[0])
        self.assertTrue(r.entrar())
        t[0] = 1000
        self.assertIsNone(r.verificar())
        self.assertEqual(chamadas, [])
        r.sair()
        t[0] = 1061
        self.assertEqual(r.verificar(), guarda_ociosa.PARADO)
        self.assertEqual(len(chamadas), 1)
        self.assertFalse(r.entrar())  # depois de parado, não aceita mais pedidos

    def test_falha_de_parada_nao_vira_sucesso(self):
        for parar in (lambda: False, lambda: 1 / 0):
            t = [0.0]
            r = guarda_ociosa.Relogio(60, parar=parar, agora=lambda: t[0])
            t[0] = 61
            with self.subTest(parar=parar):
                self.assertEqual(r.verificar(), guarda_ociosa.FALHOU)
                self.assertFalse(r.encerrado)
                self.assertTrue(r.entrar())
                r.sair()


class RunPodFalsa(BaseHTTPRequestHandler):
    estado = {"id": "pod-teste-01", "name": "meu-pod-defensivo", "desiredStatus": "RUNNING"}
    paradas = []
    responde_exited = True

    def log_message(self, *a):
        pass

    def _json(self, dados):
        bruto = json.dumps(dados).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(bruto)))
        self.end_headers()
        self.wfile.write(bruto)

    def do_GET(self):
        self._json(self.estado)

    def do_POST(self):
        RunPodFalsa.paradas.append(self.path)
        if RunPodFalsa.responde_exited:
            RunPodFalsa.estado = {**RunPodFalsa.estado, "desiredStatus": "EXITED"}
        self._json({})


class TestPararPod(unittest.TestCase):
    def setUp(self):
        RunPodFalsa.estado = {"id": "pod-teste-01", "name": "meu-pod-defensivo", "desiredStatus": "RUNNING"}
        RunPodFalsa.paradas = []
        RunPodFalsa.responde_exited = True
        self.srv = ThreadingHTTPServer(("127.0.0.1", 0), RunPodFalsa)
        self.api = subir(self.srv) + "v1"

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()

    def test_nome_diferente_nao_para_nada(self):
        with self.assertRaises(comum.ErroDeSeguranca):
            guarda_ociosa.parar_pod("pod-teste-01", "outro-pod", "chave-falsa", api=self.api)
        self.assertEqual(RunPodFalsa.paradas, [])

    def test_para_e_confirma_exited(self):
        self.assertTrue(guarda_ociosa.parar_pod("pod-teste-01", "meu-pod-defensivo", "chave-falsa", api=self.api))
        self.assertEqual(RunPodFalsa.paradas, ["/v1/pods/pod-teste-01/stop"])

    def test_sem_exited_devolve_falso(self):
        RunPodFalsa.responde_exited = False
        ok = guarda_ociosa.parar_pod("pod-teste-01", "meu-pod-defensivo", "chave-falsa", api=self.api,
                                     tentativas=2, espera_s=0)
        self.assertFalse(ok)

    def test_id_invalido_recusado(self):
        with self.assertRaises(comum.ErroDeSeguranca):
            guarda_ociosa.parar_pod("../todos", "x", "chave-falsa", api=self.api)


class ModeloFalso(BaseHTTPRequestHandler):
    """Imita um endpoint compatível com OpenAI, para testar o checador e o proxy sem internet."""

    def log_message(self, *a):
        pass

    def _json(self, dados, codigo=200):
        bruto = json.dumps(dados).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(bruto)))
        self.end_headers()
        self.wfile.write(bruto)

    def do_GET(self):
        if self.path.endswith("/models"):
            return self._json({"data": [{"id": "modelo-falso"}]})
        self._json({}, 404)

    def do_POST(self):
        corpo = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        msgs = corpo["messages"]
        ultima = msgs[-1]
        if isinstance(ultima.get("content"), list):
            msg = {"role": "assistant", "content": checa_endpoint.CODIGO_DA_IMAGEM}
        elif ultima["role"] == "tool":
            msg = {"role": "assistant", "content": "25 °C são 77 °F."}
        elif corpo.get("tools"):
            msg = {"role": "assistant", "content": None, "tool_calls": [{"id": "c1", "type": "function", "function": {
                "name": "celsius_para_fahrenheit", "arguments": json.dumps({"celsius": 25})}}]}
        elif len(msgs) >= 3:
            msg = {"role": "assistant", "content": checa_endpoint.PALAVRA_SECRETA}
        else:
            msg = {"role": "assistant", "content": "ok"}
        self._json({"choices": [{"message": msg}]})


class TestChecaEndpointEProxy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modelo = ThreadingHTTPServer(("127.0.0.1", 0), ModeloFalso)
        cls.upstream = subir(cls.modelo) + "v1"
        cls.relogio = guarda_ociosa.Relogio(900)
        cls.proxy = guarda_ociosa.montar_servidor(cls.upstream, "token-local-de-teste", None, cls.relogio, porta=0)
        cls.base = f"http://127.0.0.1:{cls.proxy.server_port}"
        threading.Thread(target=cls.proxy.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        for s in (cls.proxy, cls.modelo):
            s.shutdown()
            s.server_close()

    def test_checador_passa_texto_funcao_e_imagem(self):
        rel = checa_endpoint.executar(self.upstream, "modelo-falso", None, True,
                                      str(RAIZ / "exemplos" / "teste-visao.png"))
        self.assertTrue(rel["passou_tudo"], rel)
        self.assertEqual(len(rel["resultados"]), 4)

    def test_imagem_do_kit_e_pequena(self):
        self.assertLess((RAIZ / "exemplos" / "teste-visao.png").stat().st_size, checa_endpoint.LIMITE_IMAGEM)

    def test_proxy_sem_token_recusa(self):
        with self.assertRaises(urllib.error.HTTPError) as e:
            pedir(self.base + "/v1/models")
        self.assertEqual(e.exception.code, 401)
        with self.assertRaises(urllib.error.HTTPError) as e:
            pedir(self.base + "/v1/models", cab={"Authorization": "Bearer errado"})
        self.assertEqual(e.exception.code, 401)

    def test_proxy_recusa_origem_de_navegador_e_rota_estranha(self):
        ok = {"Authorization": "Bearer token-local-de-teste"}
        casos = [("/v1/models", "GET", {**ok, "Origin": "https://site-qualquer.example"}, 403),
                 ("/v1/admin", "GET", ok, 404),
                 ("/v1/models?x=1", "GET", ok, 404),
                 ("/v1/chat/completions", "GET", ok, 405)]
        for caminho, metodo, cab, codigo in casos:
            with self.subTest(caminho=caminho), self.assertRaises(urllib.error.HTTPError) as e:
                pedir(self.base + caminho, metodo, cab=cab)
            self.assertEqual(e.exception.code, codigo)

    def test_proxy_com_token_encaminha_e_marca_uso(self):
        self.relogio.ultimo_uso = -10_000
        with pedir(self.base + "/v1/models", cab={"Authorization": "Bearer token-local-de-teste"}) as r:
            self.assertEqual(json.load(r)["data"][0]["id"], "modelo-falso")
        self.assertGreater(self.relogio.ultimo_uso, 0)
        self.assertEqual(self.relogio.em_andamento, 0)

    def test_proxy_escuta_so_em_loopback(self):
        self.assertEqual(self.proxy.server_address[0], "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
