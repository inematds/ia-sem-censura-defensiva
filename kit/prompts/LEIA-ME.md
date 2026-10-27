# Prompts do kit

Nove prompts em português, para colar no seu assistente (Claude Code, Codex ou o próprio Harness), na ordem da sua rota:

| Rota | Prompts |
|---|---|
| API hospedada | 01 → 02 → 03 → 09 |
| GPU na RunPod | 01 → 04 → 05 → 06 → 03 → 09 |
| Local no LM Studio | 01 → 07 → 08 → 03 → 09 |

Todos terminam com o bloco **FRONTEIRAS**. Não apague: é ele que lembra o assistente de pedir escopo,
parar antes de gastar e não colocar chave no chat. Mesmo assim, o bloco é instrução, não cerca: o
isolamento de verdade vem do sistema operacional, do contêiner e das permissões que você dá.

Todos juntos: [TODOS-OS-PROMPTS.md](TODOS-OS-PROMPTS.md).
