#!/usr/bin/env python3
"""Laboratório sintético do INEMA: uma página falsa, só em 127.0.0.1, para treinar uma checagem defensiva.

Não tem usuário real, banco de dados nem falha explorável. A única "falha" é de configuração:
faltam dois cabeçalhos de proteção do navegador. Com --corrigido, a página passa a enviá-los.

  python3 kit/scripts/laboratorio.py              # porta 8181, versão com os achados
  python3 kit/scripts/laboratorio.py --corrigido  # mesma página, já corrigida
"""
from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORTA_PADRAO = 8181
MARCA = "laboratorio-sintetico-inema"  # a checagem segura confere esta marca antes de analisar
CABECALHOS_CORRECAO = {
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
}
PAGINA = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="{MARCA}" content="1">
<title>Laboratório sintético INEMA</title></head>
<body><h1>Laboratório sintético INEMA</h1>
<p>Tudo aqui é inventado. Pratique uma checagem não destrutiva e depois a correção.</p>
<p>Cliente de exemplo: Maria Exemplo, pedido nº 0000 (dado falso).</p>
</body></html>""".encode("utf-8")


class Laboratorio(BaseHTTPRequestHandler):
    corrigido = False
    server_version = "LabINEMA/1"
    sys_version = ""

    def log_message(self, *args):  # sem log de requisições
        return

    def do_GET(self):
        if self.path not in ("/", ""):
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGINA)))
        if self.corrigido:
            for nome, valor in CABECALHOS_CORRECAO.items():
                self.send_header(nome, valor)
        self.end_headers()
        self.wfile.write(PAGINA)

    def do_POST(self):  # o laboratório não aceita escrita
        self.send_error(405)


def criar_servidor(porta: int = PORTA_PADRAO, corrigido: bool = False) -> ThreadingHTTPServer:
    classe = type("LaboratorioConfigurado", (Laboratorio,), {"corrigido": corrigido})
    return ThreadingHTTPServer(("127.0.0.1", porta), classe)


def main() -> None:
    ap = argparse.ArgumentParser(description="Laboratório sintético só em 127.0.0.1.")
    ap.add_argument("--porta", type=int, default=PORTA_PADRAO)
    ap.add_argument("--corrigido", action="store_true", help="envia os cabeçalhos de proteção")
    a = ap.parse_args()
    srv = criar_servidor(a.porta, a.corrigido)
    estado = "corrigido" if a.corrigido else "com achados"
    print(f"Laboratório sintético em http://127.0.0.1:{a.porta}/ ({estado}). Ctrl+C para parar.", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
