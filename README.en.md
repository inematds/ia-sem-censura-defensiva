# Uncensored AI, the right way — your own model for defensive security

[![Uncensored AI, the right way](guia/assets/banner-en.jpg)](https://inematds.github.io/ia-sem-censura-defensiva/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

This is a free INEMA kit, in Portuguese, for people studying security who want an open AI model that
doesn’t refuse technical questions — so-called *abliterated* models, from which refusal has been removed. It
shows how to connect this model to DeepSeek Harness (an open source agent) through an API, a GPU
rented on RunPod, or LM Studio on your computer. It includes ready-to-use prompts, scripts that verify whether text,
tools, and images work, a fake lab for training, and a guard that stops an idle GPU. You
need an assistant that can read files, Python 3.10+, and, depending on the route, an API or GPU account — and
permission for everything you test.

## 📖 User guide

Full guide (landing page + step-by-step instructions): **https://inematds.github.io/ia-sem-censura-defensiva/guia/en/**

## ⚠️ Defensive use

**Only your own systems or systems whose owner has given written permission.** Record the scope before the first request,
start with a synthetic lab, use non-destructive checks and proportionate proof, and keep credentials out of chat and
git. A downloaded model runs without tools first; isolation comes from the operating system and container —
a prompt is not a fence. Local endpoints must use `127.0.0.1`; cloud endpoints must always use authentication. On RunPod,
stop the Pod and check for **EXITED**: storage is still billed. Complete rules in
[`kit/USO-DEFENSIVO.md`](kit/USO-DEFENSIVO.md) (in Portuguese).

## The three routes

| Route | Best for | You pay for | Prompts |
|---|---|---|---|
| Hosted API (e.g., Abliteration, OrcaRouter) | getting started quickly, no GPU | API usage | 01 → 02 → 03 → 09 |
| Rented GPU on RunPod | choosing the model and runtime | GPU hours + storage | 01 → 04 → 05 → 06 → 03 → 09 |
| Local with LM Studio | a machine with memory to spare | electricity, disk, time | 01 → 07 → 08 → 03 → 09 |

Example models (checked Oct 26, 2026; subject to change): local **Huihui Qwen3.6 35B-A3B abliterated GGUF Q4_K**
(~21.7 GB + ~0.9 GB vision projector); cloud **Huihui Qwen3.5 9B abliterated Q6_K** with a vision projector.

## The process, start to finish

Who does what: 🧠 you in a session with the assistant · ⚙️ kit script · 🤖 agent/model.

| # | Step | Command / file | Who does it |
|---|---|---|---|
| 1 | Read the rules | [`kit/USO-DEFENSIVO.md`](kit/USO-DEFENSIVO.md) (in Portuguese) | 🧠 |
| 2 | Check the machine | `python3 kit/scripts/doutor.py` | ⚙️ |
| 3 | Run the offline tests | `python3 -m unittest discover -s kit/testes -v` | ⚙️ |
| 4 | Lab + scoped check | `python3 kit/scripts/laboratorio.py` and `python3 kit/scripts/checagem_segura.py --lab-local-autorizado` | ⚙️ |
| 5 | Fix and retest | `laboratorio.py --corrigido` + the same check → `"achados": []` | ⚙️ |
| 6 | Choose a route | [`kit/guias/1-escolha-da-rota.md`](kit/guias/1-escolha-da-rota.md) (in Portuguese) | 🧠 |
| 7 | Give the kit to the assistant | request in [`kit/CONFIGURA-COM-ASSISTENTE.md`](kit/CONFIGURA-COM-ASSISTENTE.md) (in Portuguese) | 🧠 → 🤖 |
| 8 | Install/connect the model for the chosen route | prompts 01, 02 / 04-05 / 07-08 in [`kit/prompts/`](kit/prompts/) (in Portuguese) (cost always approved first) | 🤖, approved by 🧠 |
| 9 | Verify text, function, and image | `python3 kit/scripts/checa_endpoint.py --base-url ... --modelo ... --funcao --imagem kit/exemplos/teste-visao.png` | ⚙️ |
| 10 | Add tools (Playwright, Firecrawl, Nuclei) | prompt 03 + `kit/config/dsh-mcp.exemplo.yml` + `kit/exemplos/nuclei-cabecalhos-lab.yaml` only in the lab | 🤖, checked by 🧠 |
| 11 | RunPod: idle guard | `python3 kit/scripts/guarda_ociosa.py --upstream ... --ocioso 900` (simulation → real stop with ID and name) | ⚙️ + 🧠 checks EXITED |
| 12 | Your app, with written scope | prompt 09 + completed copy of `kit/exemplos/escopo-autorizado.exemplo.json` | 🧠 → 🤖 |

### Where this repository’s guide and video are

| Item | Where | Who does it |
|---|---|---|
| Guide (PT/EN/ES) | `guia/index.html`, `guia/en/`, `guia/es/` → https://inematds.github.io/ia-sem-censura-defensiva/guia/en/ | 🧠 INEMA session → ⚙️ GitHub Pages via Actions |
| Explainer video | MP4 outside the repo; release `video-v1.0.0` + player in `videos/` → https://inematds.github.io/ia-sem-censura-defensiva/videos/ | ⚙️ `python3 scripts/publica.py` |

## Structure

```
kit/
├── COMECE-AQUI.md · USO-DEFENSIVO.md · CONFIGURA-COM-ASSISTENTE.md
├── guia-rapido.pdf  the whole kit as a PDF to read and print, in Portuguese (`python3 scripts/gera_pdf.py` rebuilds it)
├── prompts/      01..09 (each with the FRONTEIRAS block) + TODOS-OS-PROMPTS.md
├── guias/        1 route choice · 2 hosted · 3 runpod · 4 local · 5 tools
│                 6 model security · 7 runpod cost · 8 common problems
├── config/       .env.exemplo · campos-do-provedor.json · dsh-mcp.exemplo.yml · mcp.exemplo.json · modelos-de-exemplo.json
├── scripts/      doutor · checa_endpoint · laboratorio · checagem_segura · guarda_ociosa · comum · gera_imagem_teste
├── testes/       test_kit.py (offline, 127.0.0.1)
├── exemplos/     sample scope · findings report · passive Nuclei template · teste-visao.png
└── verificacao/  STATUS.md · checklist.md
guia/       user guide page (PT, en/, es/)
videos/     explainer video player
scripts/    publica.py (uploads the video as a release and generates the player)
```

## Status (Oct 26, 2026)

- **Tested by INEMA:** all 25 offline script tests and the lab → finding → fix cycle via the command line.
- **Observed, not repeated in this version:** local Q4_K model in LM Studio — text ✔, function ✔, **image ✘** in that runtime.
- **Not tested:** paid provider, GPU on RunPod, real Pod shutdown, installed Harness/MCPs/Nuclei. These depend on your account.

Details in [`kit/verificacao/STATUS.md`](kit/verificacao/STATUS.md) (in Portuguese). Nothing here is a security certification.

## License

[MIT](LICENSE) — text, prompts, scripts, and examples by INEMA. DeepSeek Harness, LM Studio, RunPod, Nuclei,
Playwright, Firecrawl, and the cited models belong to their respective authors and are subject to their own terms.

---

Open and free content from **[INEMA.CLUB](https://inema.club)**.