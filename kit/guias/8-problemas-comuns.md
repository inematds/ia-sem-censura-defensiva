# 8. Problemas comuns: conserte a menor camada

> Uso defensivo: só sistemas seus ou com permissão por escrito. Credenciais fora do chat.

| Sintoma | Confira primeiro | Próximo passo |
|---|---|---|
| Conexão recusada | o servidor está ligado na porta certa? | ver o status do servidor; manter 127.0.0.1 igual em todo lugar |
| Erro 401 ou 403 | chave certa e conta com permissão? | digitar a chave de novo no lugar privado; nunca colar no relatório |
| Lista de modelos vazia | o endpoint tem `/v1/models`? | ler a documentação e digitar o ID exato |
| Responde "oi" mas a função falha | modelo e runtime suportam chamada de função? | rodar `checa_endpoint.py --funcao`; olhar o template de chat |
| Ignora a imagem | visão ligada e projetor certo? | rodar só o teste `--imagem` |
| Modelo não carrega | memória livre e runtime compatível? | contexto ou modelo menor; não forçar sem memória |
| Harness continua com o modelo antigo | sessões antigas guardam o modelo | abrir sessão nova e conferir |
| MCP aparece mas não faz nada | uma chamada real deu certo? | olhar a inicialização do servidor MCP e fazer um teste pequeno |
| A nuvem continua cobrando | parou o Pod ou só o app? | conferir EXITED; olhar o armazenamento à parte |
| Guarda ociosa não fez nada | todo pedido passou por ela? ela estava rodando? | manter parada manual e alerta de orçamento |
| `checagem_segura.py` recusou | é o laboratório em 127.0.0.1 e o escopo está valendo? | ler o motivo no JSON; a recusa é proposital |

Deu errado? Desfaça só o que você mudou. Guarde os perfis que funcionam. Nunca resolva conexão abrindo um
endpoint sem autenticação, nem colando chave numa issue pública.
