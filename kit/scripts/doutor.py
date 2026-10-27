#!/usr/bin/env python3
"""Doutor do kit: confere o que já está instalado. Só lê versões; não instala nada e não abre chave nenhuma.

  python3 kit/scripts/doutor.py
"""
from __future__ import annotations

import json
import platform
import shutil
import socket
import subprocess
import sys


def versao(*comando: str) -> str:
    if not shutil.which(comando[0]):
        return "não instalado"
    try:
        r = subprocess.run(comando, capture_output=True, text=True, timeout=15)
        linhas = (r.stdout or r.stderr).strip().splitlines()
        return linhas[0] if linhas else "instalado (sem versão)"
    except Exception:  # noqa: BLE001
        return "instalado (não respondeu à versão)"


def porta_livre(porta: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", porta)) != 0


def diagnostico() -> dict:
    return {
        "sistema": f"{platform.system()} {platform.release()} ({platform.machine()})",
        "python": platform.python_version(),
        "python_ok_3_10": sys.version_info >= (3, 10),
        "node": versao("node", "--version"),
        "deepseek_harness_dsh": versao("dsh", "--version"),
        "lm_studio_cli_lms": "encontrado" if shutil.which("lms") else "não encontrado",
        "nuclei": versao("nuclei", "-version"),
        "portas_livres": {
            "8181 laboratório": porta_livre(8181),
            "8282 guarda ociosa": porta_livre(8282),
            "1234 LM Studio": porta_livre(1234),
        },
        "lembrete": "Leia o guia da sua rota antes de instalar qualquer coisa. Nenhuma chave foi lida.",
    }


if __name__ == "__main__":
    print(json.dumps(diagnostico(), ensure_ascii=False, indent=2))
