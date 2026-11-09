# 2b. Rota Venice (API hospedada, sem GPU)

> Uso defensivo: só sistemas seus ou com permissão por escrito. Credenciais fora do chat.
> **Status: rota documentada pela documentação pública da Venice (lida em 09/11/2026), ainda não testada
> com conta pelo INEMA.** Preços e modelos mudam: confira antes de pagar.

## Por que esta rota

A Venice é um provedor de API que já serve modelos sem filtro prontos, inclusive um DeepSeek rápido e
barato. Você não precisa de GPU nem de instalar modelo: cria a conta, coloca crédito e liga no Harness
como "Custom model API". A API segue o padrão OpenAI.

| Modelo (ID exato) | Entrada / saída (US$ por 1M tokens) | Contexto | Privacidade |
|---|---|---|---|
| `deepseek-v4-1-flash-1017-uncensored` (DeepSeek V4.1 Flash Uncensored) | 0,33 / 1,32 | 1M | Private |
| `e2ee-deepseek-v4-1-flash-1017-abliterated` | 0,375 / 1,50 | 1M | E2EE |
| `venice-uncensored-1-2` (Venice Uncensored 1.2) | 0,20 / 0,90 | 128K | Private |
| `gemma-4-uncensored` | 0,1625 / 0,50 | 256K | Private |
| `olafangensan-glm-4.7-flash-heretic` | 0,07 / 0,40 | 200K | Private |

Comece pelo **DeepSeek V4.1 Flash Uncensored**: rápido, barato e com contexto grande para código.

**Privacidade, em uma linha cada** (segundo a Venice): *Private* = o provedor diz não guardar o conteúdo;
*E2EE* = criptografado de ponta a ponta, nem a Venice lê; *Anonymized* = vai para um provedor terceiro
sem o seu nome, e esse terceiro pode ver o conteúdo. Para dado sensível, prefira Private ou E2EE.

**Conta e pagamento:** e-mail ou carteira; crédito por cartão (não expira), cripto, ou o token DIEM.
A documentação lida não fala em verificação de identidade, o que não prova que ela nunca será pedida.

## Antes

1. Rode o prompt **01** (Harness pronto).
2. Crie a conta em venice.ai e coloque **só o crédito que você aceita gastar no teste** (US$ 5 bastam
   para centenas de pedidos curtos). O crédito pré-pago é o seu teto.
3. Gere uma chave de API **só para este teste**. Não reaproveite chave de outro projeto.

## Conectar (prompt 10 faz isso com você)

1. No Harness: **Settings > Models > Add model provider > Custom model API**.
2. Preencha com [`kit/config/venice.exemplo.json`](../config/venice.exemplo.json):
   URL base `https://api.venice.ai/api/v1`, protocolo `openai-completions`, ID `deepseek-v4-1-flash-1017-uncensored`.
3. Digite a chave direto no app (nunca no chat do assistente).
4. Abra **uma sessão nova** na pasta de teste.

## Verificar

```sh
mkdir -p ~/.segredos && chmod 700 ~/.segredos
nano ~/.segredos/chave-venice      # cole a chave, salve; uma linha só
chmod 600 ~/.segredos/chave-venice
export INEMA_CHAVE_MODELO_ARQ=~/.segredos/chave-venice
python3 kit/scripts/checa_endpoint.py --base-url https://api.venice.ai/api/v1 --modelo deepseek-v4-1-flash-1017-uncensored --funcao
```

O checador manda só textos inventados e gasta poucos centavos. Confira no painel da Venice que o
saldo caiu o esperado e que o modelo listado é o que você escolheu.

## Modelo sem filtro faz, assinatura confere

Modelo sem filtro alucina mais que um modelo de ponta. Use os dois juntos:

1. O modelo da Venice trabalha numa **pasta separada** (nunca na pasta do seu projeto real).
2. O seu Claude Code ou Codex, **pela assinatura**, revisa o que foi feito nessa pasta: lê o código,
   roda os testes, compara com o pedido e marca o que ficou **não testado**.
3. Só depois você copia para o projeto real.

Assim o modelo sem filtro destrava o pedido e o modelo da assinatura garante a qualidade.

## Desfazer

Feche a sessão, desative o provedor criado no Harness e **revogue a chave** no painel da Venice.
Desinstalar o Harness não revoga chave nem devolve crédito.

Documentação oficial: [Venice API](https://docs.venice.ai) · [modelos e preços](https://docs.venice.ai/overview/pricing) ·
[privacidade](https://docs.venice.ai/overview/privacy)
