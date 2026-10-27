# 6. Antes de dar ferramentas a um modelo baixado

> Uso defensivo: só sistemas seus ou com permissão por escrito. Credenciais fora do chat.

Leitura recomendada: [ProjectDiscovery — How abliterated models can get you pwned](https://projectdiscovery.io/research/how-abliterated-models-can-get-you-pwned).
O texto mostra um modelo de pesquisa com porta dos fundos colocada de propósito. Ele **não** diz que os
modelos de exemplo deste kit estão comprometidos; mostra por que confiar com cuidado.

**Pesos e ferramentas são duas decisões de confiança separadas.**

1. **Anote a procedência:** quem publicou, repositório, revisão exata, hash do arquivo, formato e licença.
   Nome conhecido e muitos downloads não garantem nada; um antivírus não certifica comportamento.
2. **Primeiro sem ferramentas e sem arquivos pessoais.** Converse, veja como responde.
3. **Depois, o mínimo de ferramentas** para uma tarefa sintética, se possível num ambiente descartável.
4. **Isolamento é do sistema, não do prompt.** Dizer "não leia segredos" não é cerca. Use usuário separado,
   contêiner, pasta de trabalho dedicada. `127.0.0.1` impede acesso pela rede, mas não impede o Harness de
   ler os arquivos que você deixou ao alcance.
5. **Nada real na pasta de teste:** sem credencial verdadeira, sem dado de produção. Ferramenta de pesquisa
   recebe só URL pública.
6. **Desconfie de pedidos estranhos do modelo:** baixar e rodar script remoto, mostrar chave, desligar
   proteção, aumentar escopo. Pare e investigue. Não teste payload malicioso na sua máquina de trabalho.
7. **Mudou algo, teste de novo:** pesos, projetor, template de chat, runtime ou permissões.

Documentação oficial: [SAFETY.md do Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md) ·
[segurança no Hugging Face](https://huggingface.co/docs/hub/security)
