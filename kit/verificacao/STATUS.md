# Status da verificação — 26/10/2026

Testes com limite claro. Não é certificação de segurança.

| Camada | Status | Quem rodou |
|---|---|---|
| Testes offline dos scripts (`kit/testes/`) | **25 testes passando**: escopo negado, alvo remoto recusado, escopo vencido, janela sem fuso, limite de pedidos, achado sintético + correção, servidor que não é o laboratório, URL e permissão de chave, relógio ocioso (simulação, pedido em andamento, falha de parada), parada de Pod contra API falsa (nome errado, EXITED confirmado, sem EXITED), proxy (sem token, origem de navegador, rota estranha, só loopback), checador de endpoint contra modelo falso | INEMA, em 127.0.0.1, sem internet |
| Laboratório + checagem segura pela linha de comando | achados aparecem; com `--corrigido` somem; escopo de exemplo e alvo remoto recusados | INEMA |
| Modelo local Huihui Qwen3.6 35B-A3B abliterated Q4_K no LM Studio | resultado **observado em 26/10/2026** numa instalação existente: texto em 2 turnos ✔, função inofensiva ✔, **imagem ✘** nesse runtime. **Não foi repetido nesta versão do kit** | — |
| Modelo na nuvem Huihui Qwen3.5 9B abliterated Q6_K | **não implantado**: nenhuma GPU paga foi alugada para este kit | — |
| Provedor hospedado pago | **não testado**: depende da conta e da chave de quem usa | — |
| Parada real de Pod na RunPod | só testada contra API falsa; a parada real exige o seu Pod e a sua chave | — |
| Template Nuclei passivo | escrito para o laboratório; **não executado** pelo INEMA (Nuclei não instalado na máquina de teste) | — |
| DeepSeek Harness, Playwright MCP, Firecrawl MCP | configuração de exemplo; **não instalados** pelo INEMA nesta versão | — |
| Windows / macOS / Linux | instruções incluídas; sem prova de instalação nova em cada sistema | — |

Use o [checklist](checklist.md) na sua instalação. Link de documentação não é teste ao vivo.
