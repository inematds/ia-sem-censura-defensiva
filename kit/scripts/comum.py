"""Funções comuns dos scripts do kit INEMA "IA sem censura, do jeito certo".

Só biblioteca padrão do Python 3.10+. Nada aqui chama a internet sozinho.
"""
from __future__ import annotations

import ipaddress
import os
import stat
import urllib.parse
import urllib.request
from pathlib import Path

# Nomes de loopback aceitos para HTTP sem TLS (endpoint no seu próprio computador).
LOOPBACK = {"127.0.0.1", "localhost", "::1"}


class ErroDeSeguranca(ValueError):
    """Pedido recusado por uma regra de segurança do kit."""


class SemRedirecionar(urllib.request.HTTPRedirectHandler):
    """Nunca segue redirecionamento: uma chave ou um teste não podem ir parar em outro host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        raise ErroDeSeguranca(f"redirecionamento {code} recusado")


def abridor_seguro() -> urllib.request.OpenerDirector:
    """Abridor HTTP sem proxy do sistema e sem redirecionamento."""
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), SemRedirecionar())


def eh_loopback(host: str | None) -> bool:
    if not host:
        return False
    if host in LOOPBACK:
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def validar_url_base(url: str) -> str:
    """Aceita https://... em qualquer host, ou http:// só em loopback.

    Recusa usuário/senha embutidos, query string e fragmento (lugares onde chave costuma vazar).
    """
    partes = urllib.parse.urlsplit(url.strip())
    if partes.username or partes.password:
        raise ErroDeSeguranca("não coloque usuário ou senha dentro da URL")
    if partes.query or partes.fragment:
        raise ErroDeSeguranca("a URL base não pode ter ?query nem #fragmento")
    if not partes.hostname:
        raise ErroDeSeguranca("URL sem host")
    if partes.scheme == "https":
        pass
    elif partes.scheme == "http" and eh_loopback(partes.hostname):
        pass
    else:
        raise ErroDeSeguranca("use https://, ou http:// só no seu próprio computador (127.0.0.1)")
    return url.strip().rstrip("/")


def ler_segredo(variavel: str, obrigatorio: bool = False) -> str | None:
    """Lê UM segredo do arquivo cujo caminho está na variável de ambiente `variavel`.

    O valor nunca vem por argumento de linha de comando (fica no histórico e na lista de processos).
    No Linux/macOS o arquivo precisa estar com permissão 600.
    """
    caminho = os.environ.get(variavel, "").strip()
    if not caminho:
        if obrigatorio:
            raise ErroDeSeguranca(f"defina {variavel} com o caminho de um arquivo privado")
        return None
    arq = Path(caminho).expanduser()
    if not arq.is_file():
        raise ErroDeSeguranca(f"{variavel} não aponta para um arquivo")
    if os.name != "nt":
        modo = stat.S_IMODE(arq.stat().st_mode)
        if modo & (stat.S_IRWXG | stat.S_IRWXO):
            raise ErroDeSeguranca(f"o arquivo de {variavel} está aberto para outros usuários; rode chmod 600")
    linhas = [l.strip() for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(linhas) != 1:
        raise ErroDeSeguranca(f"o arquivo de {variavel} deve ter exatamente um valor, numa linha")
    return linhas[0]
