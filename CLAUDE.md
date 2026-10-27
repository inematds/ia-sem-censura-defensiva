# CLAUDE.md — ia-sem-censura-defensiva

Kit do INEMA para ligar um modelo abliterated ao DeepSeek Harness (API, RunPod ou LM Studio) para
segurança **defensiva**, com scripts próprios (checador de endpoint, laboratório sintético, checagem com
escopo, guarda ociosa), prompts PT e guia PT/EN/ES.

## Regras do repo

- **Autor de todo commit:** `inematds <inematds@gmail.com>` (author e committer). Conferir `git config user.email`.
- **Push:** remoto SSH `git@github.com:inematds/ia-sem-censura-defensiva.git` (o token HTTPS da inematds não tem escopo `workflow`).
- **Sem fonte de terceiros:** nada de link para vídeo, curso, autor, comunidade ou loja de onde a ideia veio. O kit é do INEMA.
  Ferramentas (Harness, LM Studio, RunPod, Nuclei, Playwright, Firecrawl, Hugging Face, provedores de exemplo) podem ser citadas como ferramentas.
- **Código e texto próprios:** não colar trechos de kits de terceiros; escrever do zero.
- **Só defensivo:** nenhum payload ofensivo, nenhum exemplo contra alvo real. Testes só offline/127.0.0.1.
- **Status honesto:** não afirmar que o INEMA rodou modelo, GPU ou provedor que não rodou. Datas e preços com "conferido em" e aviso de que mudam.
- **PT é a fonte.** EN/ES (README e guia) só pelo tradutor central `inema-traduz`.
- Antes do push: `grep -riE "you[t]ube\.com/watch|you[t]u\.be|sk[o]ol|gum[r]oad|kash[e]f|early[a]idopters|early a[i]|coach[v]ault|refe[r][eê]ncia|referen[c]e video|recor[d]ed|trans[c]ri" --exclude-dir=.git .` tem que voltar vazio.
- Testes: `python3 -m unittest discover -s kit/testes -v` passando antes de todo commit que mexe em `kit/scripts/`.
- Mudou o fluxo? Atualizar a seção "O processo, do início ao fim" dos 3 READMEs no mesmo commit.

## Self-learning

When I correct you, or you catch yourself making a mistake: before continuing, add the lesson as a one-line rule at the TOP of [LESSONS.md](LESSONS.md) (not here), so it never happens again.

## Lessons

As lições ficam em [LESSONS.md](LESSONS.md). Ler antes de mexer no kit ou no guia.
