# IA sem censura, do jeito certo — seu próprio modelo para segurança defensiva

[![IA sem censura, do jeito certo](guia/assets/banner.jpg)](https://inematds.github.io/ia-sem-censura-defensiva/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Este é um kit gratuito do INEMA, em português, para quem estuda segurança e quer um modelo de IA aberto que
não recuse perguntas técnicas — os chamados modelos *abliterated*, dos quais a recusa foi removida. Ele
mostra como ligar esse modelo ao DeepSeek Harness (um agente de código aberto) por uma API, por uma GPU
alugada na RunPod ou pelo LM Studio no seu computador. Traz prompts prontos, scripts que provam se texto,
ferramenta e imagem funcionam, um laboratório falso para treinar e uma guarda que para a GPU ociosa. Você
precisa de um assistente que leia arquivos, Python 3.10+ e, conforme a rota, uma conta de API ou de GPU — e
de permissão para tudo o que for testar.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/ia-sem-censura-defensiva/guia/**

## ⚠️ Uso defensivo

**Só sistemas seus ou com permissão por escrito do dono.** Escopo registrado antes do primeiro pedido,
laboratório sintético primeiro, checagens não destrutivas, prova proporcional, credenciais fora do chat e do
git. Modelo baixado roda primeiro sem ferramentas; o isolamento é do sistema operacional e do contêiner —
prompt não é cerca. Endpoint local só em `127.0.0.1`; endpoint na nuvem sempre com autenticação. Na RunPod,
pare o Pod e confira **EXITED**: o armazenamento ainda cobra. Regras completas em
[`kit/USO-DEFENSIVO.md`](kit/USO-DEFENSIVO.md).

## As três rotas

| Rota | Combina com | Você paga | Prompts |
|---|---|---|---|
| API hospedada (ex.: Abliteration, OrcaRouter) | começar rápido, sem GPU | uso da API | 01 → 02 → 03 → 09 |
| GPU alugada na RunPod | escolher modelo e runtime | hora de GPU + armazenamento | 01 → 04 → 05 → 06 → 03 → 09 |
| Local no LM Studio | máquina com memória sobrando | luz, disco, tempo | 01 → 07 → 08 → 03 → 09 |

Modelos de exemplo (conferidos em 26/10/2026; mudam): local **Huihui Qwen3.6 35B-A3B abliterated GGUF Q4_K**
(~21,7 GB + projetor de visão ~0,9 GB); nuvem **Huihui Qwen3.5 9B abliterated Q6_K** com projetor de visão.

## O processo, do início ao fim

Quem faz: 🧠 você numa sessão com o assistente · ⚙️ script do kit · 🤖 agente/modelo.

| # | Passo | Comando / arquivo | Quem faz |
|---|---|---|---|
| 1 | Ler as regras | [`kit/USO-DEFENSIVO.md`](kit/USO-DEFENSIVO.md) | 🧠 |
| 2 | Conferir a máquina | `python3 kit/scripts/doutor.py` | ⚙️ |
| 3 | Rodar os testes offline | `python3 -m unittest discover -s kit/testes -v` | ⚙️ |
| 4 | Laboratório + checagem com escopo | `python3 kit/scripts/laboratorio.py` e `python3 kit/scripts/checagem_segura.py --lab-local-autorizado` | ⚙️ |
| 5 | Corrigir e retestar | `laboratorio.py --corrigido` + a mesma checagem → `"achados": []` | ⚙️ |
| 6 | Escolher a rota | [`kit/guias/1-escolha-da-rota.md`](kit/guias/1-escolha-da-rota.md) | 🧠 |
| 7 | Entregar o kit ao assistente | pedido de [`kit/CONFIGURA-COM-ASSISTENTE.md`](kit/CONFIGURA-COM-ASSISTENTE.md) | 🧠 → 🤖 |
| 8 | Instalar/ligar o modelo pela rota | prompts 01, 02 / 04-05 / 07-08 em [`kit/prompts/`](kit/prompts/) (custo sempre aprovado antes) | 🤖, aprovado por 🧠 |
| 9 | Provar texto, função e imagem | `python3 kit/scripts/checa_endpoint.py --base-url ... --modelo ... --funcao --imagem kit/exemplos/teste-visao.png` | ⚙️ |
| 10 | Dar ferramentas (Playwright, Firecrawl, Nuclei) | prompt 03 + `kit/config/dsh-mcp.exemplo.yml` + `kit/exemplos/nuclei-cabecalhos-lab.yaml` só no laboratório | 🤖, conferido por 🧠 |
| 11 | RunPod: guarda ociosa | `python3 kit/scripts/guarda_ociosa.py --upstream ... --ocioso 900` (simulação → parada real com ID e nome) | ⚙️ + 🧠 confere EXITED |
| 12 | Seu app, com escopo escrito | prompt 09 + cópia preenchida de `kit/exemplos/escopo-autorizado.exemplo.json` | 🧠 → 🤖 |

### Onde ficam o guia e o vídeo deste repositório

| Peça | Onde | Quem faz |
|---|---|---|
| Guia (PT/EN/ES) | `guia/index.html`, `guia/en/`, `guia/es/` → https://inematds.github.io/ia-sem-censura-defensiva/guia/ | 🧠 sessão INEMA → ⚙️ GitHub Pages via Actions |
| Vídeo explicativo | MP4 fora do repo; release `video-v1.0.0` + player em `videos/` → https://inematds.github.io/ia-sem-censura-defensiva/videos/ | ⚙️ `python3 scripts/publica.py` |

## Estrutura

```
kit/
├── COMECE-AQUI.md · USO-DEFENSIVO.md · CONFIGURA-COM-ASSISTENTE.md
├── guia-rapido.pdf  o kit inteiro em PDF para ler e imprimir (`python3 scripts/gera_pdf.py` refaz)
├── prompts/      01..09 (cada um com o bloco FRONTEIRAS) + TODOS-OS-PROMPTS.md
├── guias/        1 escolha da rota · 2 hospedada · 3 runpod · 4 local · 5 ferramentas
│                 6 segurança do modelo · 7 custo runpod · 8 problemas comuns
├── config/       .env.exemplo · campos-do-provedor.json · dsh-mcp.exemplo.yml · mcp.exemplo.json · modelos-de-exemplo.json
├── scripts/      doutor · checa_endpoint · laboratorio · checagem_segura · guarda_ociosa · comum · gera_imagem_teste
├── testes/       test_kit.py (offline, 127.0.0.1)
├── exemplos/     escopo de exemplo · relatório de achados · template Nuclei passivo · teste-visao.png
└── verificacao/  STATUS.md · checklist.md
guia/       página de uso (PT, en/, es/)
videos/     player do vídeo explicativo
scripts/    publica.py (sobe o vídeo como release e gera o player)
```

## Status (26/10/2026)

- **Testado pelo INEMA:** os 25 testes offline dos scripts e o ciclo laboratório → achado → correção pela linha de comando.
- **Observado, não repetido nesta versão:** modelo local Q4_K no LM Studio — texto ✔, função ✔, **imagem ✘** naquele runtime.
- **Não testado:** provedor pago, GPU na RunPod, parada real de Pod, Harness/MCPs/Nuclei instalados. Dependem da sua conta.

Detalhes em [`kit/verificacao/STATUS.md`](kit/verificacao/STATUS.md). Nada aqui é certificação de segurança.

## Licença

[MIT](LICENSE) — texto, prompts, scripts e exemplos do INEMA. DeepSeek Harness, LM Studio, RunPod, Nuclei,
Playwright, Firecrawl e os modelos citados são de seus autores, cada um com os seus termos.

---

Conteúdo aberto e gratuito do **[INEMA.CLUB](https://inema.club)**.
