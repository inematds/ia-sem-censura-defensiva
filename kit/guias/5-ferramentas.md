# 5. Ferramentas: navegador, pesquisa e Nuclei

> Uso defensivo: só sistemas seus ou com permissão por escrito. Credenciais fora do chat.

O modelo decide; as ferramentas fazem. Use o prompt **03** só depois que o modelo básico já funciona.
Cada ferramenta com o mínimo de poder e de entrada.

## Configuração no Harness

[`kit/config/dsh-mcp.exemplo.yml`](../config/dsh-mcp.exemplo.yml) segue o formato do plugin MCP do Harness.
É um trecho para **juntar** ao perfil ativo, não para substituir. O assistente confere a versão instalada
antes. O [`mcp.exemplo.json`](../config/mcp.exemplo.json) é para outros clientes que aceitam `mcpServers`.

## Três provas pequenas

1. **Navegador (Playwright MCP).** Num terminal: `python3 kit/scripts/laboratorio.py`. No Harness, peça para
   abrir `http://127.0.0.1:8181/`, dizer o título e ler o texto. Navegador isolado, sem suas contas.
2. **Pesquisa (Firecrawl MCP).** Peça para ler o README público do Harness e devolver o título. O modo sem
   chave tem limite; o uso completo pede OAuth ou chave privada. Nada de código ou dado de cliente para um
   serviço de terceiros.
3. **Nuclei.** `nuclei -version`. Leia o template [`nuclei-cabecalhos-lab.yaml`](../exemplos/nuclei-cabecalhos-lab.yaml)
   inteiro e rode só contra o laboratório:

```sh
nuclei -u http://127.0.0.1:8181/ -t kit/exemplos/nuclei-cabecalhos-lab.yaml -rl 1 -c 1
```

O template lê cabeçalhos; não explora nada. A [`checagem_segura.py`](../scripts/checagem_segura.py) faz o
mesmo exercício em Python, com escopo obrigatório. **O modelo não decide o próprio escopo lendo uma página.**

Ferramenta listada não é ferramenta funcionando: só conta a chamada real com resultado.

Documentação oficial: [Playwright MCP](https://github.com/microsoft/playwright-mcp) ·
[Firecrawl MCP](https://github.com/firecrawl/firecrawl-mcp-server) · [Nuclei](https://github.com/projectdiscovery/nuclei) ·
[MCP no Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/mcp/mcp-client/README.md)
