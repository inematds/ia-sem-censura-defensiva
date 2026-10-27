#!/usr/bin/env python3
"""Gera kit/guia-rapido.pdf: o kit em português num PDF para ler e imprimir.

Junta os Markdown do kit (comece aqui, uso defensivo, os 8 guias, configuração com assistente, prompts e
verificação) numa página HTML de papel (padrão INEMA: títulos Sora, corpo Inter, amarelo só como preenchimento)
e imprime com o Chromium headless do Playwright.

Uso: python3 scripts/gera_pdf.py   (precisa do módulo `markdown` e de um chromium/headless_shell)
Os Markdown continuam sendo a fonte editável; o PDF é só a versão de leitura."""
import base64, glob, html, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

import markdown

R = Path(__file__).resolve().parent.parent
K = R / "kit"
SAIDA = K / "guia-rapido.pdf"

# (arquivo, título da seção no sumário); prompts entram com o texto inteiro
ORDEM = [
    ("COMECE-AQUI.md", "Comece aqui"),
    ("USO-DEFENSIVO.md", "Uso defensivo"),
    ("guias/1-escolha-da-rota.md", "Escolha a rota"),
    ("guias/2-rota-hospedada.md", "Rota 1: API hospedada"),
    ("guias/3-rota-runpod.md", "Rota 2: GPU na RunPod"),
    ("guias/4-rota-local.md", "Rota 3: LM Studio no seu computador"),
    ("guias/5-ferramentas.md", "Ferramentas"),
    ("guias/6-seguranca-do-modelo.md", "Segurança do modelo baixado"),
    ("guias/7-custo-runpod.md", "Custo da RunPod sob controle"),
    ("guias/8-problemas-comuns.md", "Problemas comuns"),
    ("CONFIGURA-COM-ASSISTENTE.md", "Configurar com o seu assistente"),
    ("verificacao/STATUS.md", "O que foi testado"),
    ("verificacao/checklist.md", "Checklist da sua instalação"),
]

CSS = """
@page { size: A4; margin: 18mm 17mm 20mm; }
:root { --tinta:#16161d; --suave:#4b4b57; --linha:#e3e1da; --papel:#ffffff; --dica:#FEF9C3; --filete:#EAB308;
        --amarelo:#FACC15; --link:#854d0e; --codigo:#f5f4ef; }
* { box-sizing: border-box; }
html, body { background: var(--papel); color: var(--tinta); }
body { font: 10.5pt/1.55 Inter, system-ui, sans-serif; margin: 0; }
h1, h2, h3 { font-family: Sora, Inter, sans-serif; line-height: 1.2; color: var(--tinta); }
h1 { font-size: 21pt; margin: 0 0 4mm; padding-bottom: 2mm; border-bottom: 3px solid var(--amarelo); }
h2 { font-size: 14pt; margin: 6mm 0 2mm; }
h3 { font-size: 11.5pt; margin: 5mm 0 1.5mm; }
p, li { orphans: 3; widows: 3; }
a { color: var(--link); text-decoration: underline; text-decoration-color: var(--amarelo); text-decoration-thickness: 2px; }
blockquote { margin: 3mm 0; padding: 2.5mm 4mm; background: var(--dica); border-left: 4px solid var(--filete); border-radius: 6px; }
blockquote p { margin: 1mm 0; }
code { font: 9pt/1.4 "JetBrains Mono", ui-monospace, monospace; background: var(--codigo); padding: .3mm 1mm; border-radius: 3px; }
pre { background: var(--codigo); border: 1px solid var(--linha); border-radius: 8px; padding: 3mm; white-space: pre-wrap;
      word-break: break-word; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 8.6pt; }
table { border-collapse: collapse; width: 100%; margin: 3mm 0; font-size: 9.5pt; page-break-inside: avoid; }
th, td { border: 1px solid var(--linha); padding: 1.6mm 2.2mm; text-align: left; vertical-align: top; }
th { background: #faf9f5; font-family: Sora, Inter, sans-serif; }
.secao { page-break-before: always; }
.capa { height: 257mm; display: flex; flex-direction: column; justify-content: space-between; }
.capa img { width: 100%; border-radius: 12px; }
.capa .kicker { font: 600 9pt Sora, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: var(--suave); }
.capa h1 { font-size: 30pt; border: 0; margin: 4mm 0 2mm; }
.capa .marca { background: linear-gradient(transparent 55%, var(--amarelo) 55%); }
.capa .sub { font-size: 12.5pt; color: var(--suave); max-width: 150mm; }
.capa .aviso { background: var(--dica); border-left: 4px solid var(--filete); border-radius: 6px; padding: 3mm 4mm; font-size: 10pt; }
.capa .rodape { font-size: 9pt; color: var(--suave); display: flex; justify-content: space-between; }
.sumario ol { columns: 2; column-gap: 10mm; padding-left: 5mm; }
.sumario li { margin: 1mm 0; }
h1, h2, h3 { break-after: avoid; page-break-after: avoid; }
.prompt + .prompt { page-break-before: always; }
.prompt pre { page-break-inside: auto; }
.prompt h3 { margin-top: 4mm; }
"""


def md_html(texto):
    # links internos .md viram texto (no PDF não há para onde ir); externos ficam
    texto = re.sub(r"\[([^\]]+)\]\((?!https?:)[^)]+\)", r"**\1**", texto)
    return markdown.markdown(texto, extensions=["tables", "fenced_code", "sane_lists"])


def chrome():
    for c in [os.environ.get("CHROME"), *sorted(glob.glob(os.path.expanduser(
            "~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell")), reverse=True),
              shutil.which("chromium"), shutil.which("google-chrome")]:
        if c and os.path.exists(c):
            return c
    sys.exit("sem chromium: defina CHROME=<caminho>")


def main():
    capa = base64.b64encode((R / "capa" / "capa.png").read_bytes()).decode()
    partes = [f"""<section class="capa">
  <div><div class="kicker">INEMA.CLUB · kit em português · outubro de 2026</div>
  <h1>IA <span class="marca">sem censura</span>, do jeito certo</h1>
  <p class="sub">Seu próprio modelo para testar a segurança do <b>seu</b> app: três rotas no DeepSeek Harness
  (API hospedada, GPU na RunPod, LM Studio local), ferramentas, laboratório local e custo sob controle.</p></div>
  <img src="data:image/png;base64,{capa}" alt="">
  <div class="aviso"><b>Uso defensivo.</b> Só sistemas seus ou com permissão por escrito do dono, dentro do escopo
  combinado. Credenciais fora do chat. Confira o que a IA encontrar antes de agir.</div>
  <div class="rodape"><span>github.com/inematds/ia-sem-censura-defensiva</span><span>inema.club</span></div>
</section>"""]
    itens = "".join(f"<li>{html.escape(t)}</li>" for _, t in ORDEM) + "<li>Os 9 prompts</li>"
    partes.append(f'<section class="secao sumario"><h1>O que tem aqui</h1><ol>{itens}</ol>'
                  "<p>Os arquivos editáveis (Markdown, prompts, scripts e testes) estão no repositório. Este PDF é a "
                  "versão de leitura do mesmo conteúdo.</p></section>")
    for arq, _ in ORDEM:
        partes.append(f'<section class="secao">{md_html((K / arq).read_text(encoding="utf-8"))}</section>')
    prompts = sorted(p for p in (K / "prompts").glob("0*.txt"))
    corpo = "".join(f'<div class="prompt"><h3>{html.escape(p.stem)}</h3><pre><code>'
                    f'{html.escape(p.read_text(encoding="utf-8").strip())}</code></pre></div>' for p in prompts)
    partes.append(f'<section class="secao"><h1>Os 9 prompts</h1><p>Copie na ordem da sua rota. Cada um traz o '
                  f'bloco de segurança; não tire.</p>{corpo}</section>')
    pagina = ("<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>IA sem censura, do jeito certo</title>"
              "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Sora:wght@600;700&"
              "family=JetBrains+Mono&display=swap' rel='stylesheet'>"
              f"<style>{CSS}</style></head><body>{''.join(partes)}</body></html>")
    with tempfile.TemporaryDirectory() as d:
        h = Path(d) / "guia.html"
        h.write_text(pagina, encoding="utf-8")
        subprocess.run([chrome(), "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=8000", f"--print-to-pdf={SAIDA}", h.as_uri()],
                       check=True, capture_output=True, timeout=120)
    print(SAIDA, SAIDA.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
