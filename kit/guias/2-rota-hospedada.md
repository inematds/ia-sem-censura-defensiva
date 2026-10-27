# 2. Rota API hospedada

> Uso defensivo: só sistemas seus ou com permissão por escrito. Credenciais fora do chat.

## Antes

Rode o prompt **01** (Harness pronto) e depois o **02**. Você precisa de uma conta num provedor que aceite
uso defensivo e sirva um modelo com protocolo compatível com o Harness. Pode haver verificação de
identidade e cobrança separada da sua assinatura de chat. Exemplos de provedor: Abliteration e OrcaRouter.
Termos, modelos e preços mudam: confira no site de cada um (conferido em 26/10/2026).

## Conectar

1. Na documentação oficial do provedor, copie a **URL base** e o **protocolo** (normalmente "OpenAI compatible").
2. Crie uma chave só para teste e, se o provedor deixar, um **limite de gasto**.
3. No Harness: **Settings > Models > Add model provider > Custom model API**. Use
   [`kit/config/campos-do-provedor.json`](../config/campos-do-provedor.json) como folha de preenchimento.
4. Busque a lista de modelos ou digite o ID exato. Nome na tela e ID podem ser diferentes.
5. Abra **uma sessão nova** na pasta de teste. Sessões antigas podem continuar com o modelo anterior.

## Verificar

Guarde a chave num arquivo privado e aponte a variável para ele:

```sh
mkdir -p ~/.segredos && chmod 700 ~/.segredos
nano ~/.segredos/chave-modelo      # cole a chave, salve; uma linha só
chmod 600 ~/.segredos/chave-modelo
export INEMA_CHAVE_MODELO_ARQ=~/.segredos/chave-modelo
python3 kit/scripts/checa_endpoint.py --base-url https://SEU-PROVEDOR/v1 --modelo SEU-ID --funcao
```

O checador manda só textos inventados e gasta um pouco de uso da API. Para imagem, acrescente
`--imagem kit/exemplos/teste-visao.png`. Depois repita a função inofensiva dentro do próprio Harness.

## Desfazer

Feche a sessão de teste, desative só o provedor que você criou e revogue a chave de teste. Olhe o painel
de uso do provedor. Desinstalar o Harness **não** cancela cobrança nem revoga chave.

Documentação oficial: [provedores no Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md) ·
[Abliteration](https://abliteration.ai) · [OrcaRouter](https://orcarouter.com)
