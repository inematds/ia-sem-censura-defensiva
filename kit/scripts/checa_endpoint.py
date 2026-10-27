#!/usr/bin/env python3
"""Checa um endpoint compatível com a API da OpenAI, uma capacidade por vez.

1. lista de modelos (o ID que você digitou existe?)
2. conversa em 2 turnos (o modelo lembra do turno anterior?)
3. --funcao: uma chamada de função inofensiva (converter 25 °C para Fahrenheit) com ida e volta
4. --imagem: lê um número de uma imagem sintética

Só manda textos inventados. Não dá terminal nem arquivos ao modelo. Não é benchmark.
A chave vem do arquivo apontado por INEMA_CHAVE_MODELO_ARQ (opcional para endpoint local).

Exemplo:
  python3 kit/scripts/checa_endpoint.py --base-url http://127.0.0.1:1234/v1 --modelo meu-modelo \
      --funcao --imagem kit/exemplos/teste-visao.png
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import ErroDeSeguranca, abridor_seguro, ler_segredo, validar_url_base  # noqa: E402

PALAVRA_SECRETA = "JABUTI-582"
CODIGO_DA_IMAGEM = "4826"  # o número desenhado em kit/exemplos/teste-visao.png
LIMITE_IMAGEM = 1_500_000

FERRAMENTA = {
    "type": "function",
    "function": {
        "name": "celsius_para_fahrenheit",
        "description": "Converte uma temperatura de teste de Celsius para Fahrenheit.",
        "parameters": {
            "type": "object",
            "properties": {"celsius": {"type": "number"}},
            "required": ["celsius"],
            "additionalProperties": False,
        },
    },
}


class Cliente:
    def __init__(self, base: str, chave: str | None, tempo_limite: int = 180):
        self.base = validar_url_base(base)
        self.chave = chave
        self.tempo_limite = tempo_limite
        self.abridor = abridor_seguro()

    def pedir(self, caminho: str, corpo: dict | None = None) -> dict:
        import urllib.request

        cab = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.chave:
            cab["Authorization"] = f"Bearer {self.chave}"
        dados = json.dumps(corpo).encode() if corpo is not None else None
        req = urllib.request.Request(self.base + caminho, data=dados, headers=cab)
        with self.abridor.open(req, timeout=self.tempo_limite) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def conversar(self, modelo: str, mensagens: list, **extra) -> dict:
        corpo = {"model": modelo, "messages": mensagens, "temperature": 0, "max_tokens": 512, **extra}
        return self.pedir("/chat/completions", corpo)["choices"][0]["message"]


def texto(msg: dict) -> str:
    return (msg.get("content") or "").strip()


def checar_lista(cli: Cliente, modelo: str) -> bool:
    ids = [m.get("id") for m in cli.pedir("/models").get("data", [])]
    return modelo in ids


def checar_dois_turnos(cli: Cliente, modelo: str) -> bool:
    conversa = [{"role": "user", "content": f"Guarde esta palavra para a próxima mensagem: {PALAVRA_SECRETA}. Responda só: ok."}]
    conversa.append({"role": "assistant", "content": texto(cli.conversar(modelo, conversa))})
    conversa.append({"role": "user", "content": "Qual era a palavra? Responda só com ela."})
    return PALAVRA_SECRETA in texto(cli.conversar(modelo, conversa)).upper()


def checar_funcao(cli: Cliente, modelo: str) -> bool:
    conversa = [{"role": "user", "content": "Use a ferramenta celsius_para_fahrenheit com celsius=25 e me diga o resultado."}]
    resp = cli.conversar(modelo, conversa, tools=[FERRAMENTA], tool_choice="required")
    chamadas = resp.get("tool_calls") or []
    if len(chamadas) != 1 or chamadas[0].get("function", {}).get("name") != "celsius_para_fahrenheit":
        return False
    try:
        args = json.loads(chamadas[0]["function"].get("arguments") or "{}")
    except json.JSONDecodeError:
        return False
    if float(args.get("celsius", -999)) != 25:
        return False
    conversa.append(resp)
    conversa.append({"role": "tool", "tool_call_id": chamadas[0].get("id", "t1"), "content": json.dumps({"fahrenheit": 77})})
    final = texto(cli.conversar(modelo, conversa, tools=[FERRAMENTA]))
    return "77" in final


def checar_imagem(cli: Cliente, modelo: str, caminho: str) -> bool:
    bruto = Path(caminho).read_bytes()
    if len(bruto) > LIMITE_IMAGEM:
        raise ErroDeSeguranca("use uma imagem sintética pequena (até 1,5 MB)")
    url = "data:image/png;base64," + base64.b64encode(bruto).decode()
    conteudo = [
        {"type": "text", "text": "Qual é o número grande de quatro dígitos na imagem? Responda só os dígitos."},
        {"type": "image_url", "image_url": {"url": url}},
    ]
    return CODIGO_DA_IMAGEM in texto(cli.conversar(modelo, [{"role": "user", "content": conteudo}]))


def executar(base: str, modelo: str, chave: str | None, funcao: bool, imagem: str | None) -> dict:
    cli = Cliente(base, chave)
    relatorio: dict = {"modelo": modelo, "tipo": "teste de fumaça com dados inventados; não é benchmark", "resultados": {}}
    r = relatorio["resultados"]
    inicio = time.monotonic()
    r["modelo_na_lista"] = checar_lista(cli, modelo)
    r["conversa_dois_turnos"] = checar_dois_turnos(cli, modelo)
    relatorio["segundos_dois_turnos"] = round(time.monotonic() - inicio, 1)
    if funcao:
        r["funcao_inofensiva_ida_e_volta"] = checar_funcao(cli, modelo)
    if imagem:
        r["imagem_sintetica"] = checar_imagem(cli, modelo, imagem)
    relatorio["passou_tudo"] = all(r.values())
    return relatorio


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Checa texto, função e imagem de um endpoint compatível com OpenAI.")
    ap.add_argument("--base-url", required=True, help="ex.: http://127.0.0.1:1234/v1")
    ap.add_argument("--modelo", required=True, help="o ID exato que o servidor devolve em /models")
    ap.add_argument("--funcao", action="store_true", help="testa uma chamada de função inofensiva")
    ap.add_argument("--imagem", help="caminho da imagem sintética (kit/exemplos/teste-visao.png)")
    ap.add_argument("--saida", help="grava o relatório JSON neste arquivo")
    a = ap.parse_args(argv)
    try:
        rel = executar(a.base_url, a.modelo, ler_segredo("INEMA_CHAVE_MODELO_ARQ"), a.funcao, a.imagem)
    except Exception as erro:  # noqa: BLE001
        # Não imprime corpo de resposta, URL completa nem chave: só o tipo do erro.
        rel = {"passou_tudo": False, "erro": type(erro).__name__,
               "dica": "Confira endpoint, chave, ID do modelo e se o modelo suporta o recurso. Nada secreto foi impresso."}
        if isinstance(erro, ErroDeSeguranca):
            rel["motivo"] = str(erro)
    saida = json.dumps(rel, ensure_ascii=False, indent=2)
    print(saida)
    if a.saida:
        Path(a.saida).write_text(saida + "\n", encoding="utf-8")
    return 0 if rel.get("passou_tudo") else 1


if __name__ == "__main__":
    sys.exit(main())
