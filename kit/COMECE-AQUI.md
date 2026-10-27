# Comece aqui

> **Uso defensivo.** Só sistemas seus ou com permissão por escrito do dono. Credenciais fora do chat.
> Confira o que a IA encontrar antes de agir.

Este kit liga um modelo de IA "sem censura" (abliterated) ao **DeepSeek Harness** por uma de três rotas —
API hospedada, GPU alugada na RunPod ou LM Studio no seu computador — e dá ferramentas para provar que cada
parte funciona, praticar num laboratório falso e não deixar a GPU cobrando à toa.

## Caminho mais curto

1. Leia [USO-DEFENSIVO.md](USO-DEFENSIVO.md) (5 minutos). É a parte mais importante.
2. Escolha a rota: [guias/1-escolha-da-rota.md](guias/1-escolha-da-rota.md). Hospedada tem menos passos;
   local não tem conta de GPU, se a sua máquina aguentar.
3. Abra [CONFIGURA-COM-ASSISTENTE.md](CONFIGURA-COM-ASSISTENTE.md), copie o pedido e entregue ao seu
   assistente junto com esta pasta.
4. Siga os [prompts](prompts/LEIA-ME.md) da sua rota, na ordem. Chave você digita direto no app ou num
   arquivo privado, nunca no chat.
5. Rode os testes de modelo e o laboratório antes de ligar ferramentas a qualquer coisa que importe.
6. Na RunPod: teste a guarda de custo e confira o Pod **EXITED**. Armazenamento cobra mesmo parado.

## O que você precisa

- Um assistente que leia arquivos (Claude Code, Codex ou similar).
- Node.js na versão pedida pelo Harness e pelos servidores MCP.
- Python 3.10 ou mais novo para os scripts do kit (só biblioteca padrão; o Pillow só para recriar a imagem de teste).
- Na rota hospedada: conta e crédito de API. Na RunPod: conta e crédito. Assinatura de chat não inclui nada disso.

## O que tem aqui

| Pasta / arquivo | Para quê |
|---|---|
| `prompts/` | 9 prompts em português, cada um com o bloco FRONTEIRAS |
| `guias/` | escolha da rota, as 3 rotas, ferramentas, segurança do modelo, custo, problemas comuns |
| `config/` | exemplos sem credencial: campos do provedor, MCP, modelos de exemplo, nomes de variáveis |
| `scripts/doutor.py` | confere o que está instalado, sem instalar nada |
| `scripts/checa_endpoint.py` | testa texto em 2 turnos, função inofensiva e imagem sintética |
| `scripts/laboratorio.py` + `checagem_segura.py` | laboratório falso em 127.0.0.1 e a checagem com escopo |
| `scripts/guarda_ociosa.py` | guarda de tempo ocioso para o SEU Pod da RunPod (simulação por padrão) |
| `exemplos/` | escopo de exemplo, relatório de achados, template Nuclei passivo, imagem de teste |
| `testes/` | testes offline dos scripts |
| `verificacao/` | o que foi testado e o checklist para a sua instalação |

O kit **não** traz pesos de modelo, não aluga GPU e não chama nenhum serviço sozinho. Modelos e preços são
exemplos conferidos em 26/10/2026 e mudam.
