# 7. Custo na RunPod: parar de verdade

> Uso defensivo: só o seu Pod aprovado. Credenciais fora do chat.

Parar o app não é parar a GPU. Confira sempre o Pod **EXITED** no painel. O armazenamento persistente
continua cobrando com o Pod parado.

## Primeiro, o limite manual

Anote ID e nome exatos do Pod, preço por hora aprovado, custo do armazenamento e a hora de parar. Ligue os
alertas de orçamento da conta, se houver. No fim, pare **esse** Pod no painel e leia o status. Só apague
depois de decidir o que guardar.

## Guarda ociosa (opcional)

[`guarda_ociosa.py`](../scripts/guarda_ociosa.py) é um proxy local: repassa os pedidos ao modelo e mede o
tempo sem uso. Escuta só em `127.0.0.1:8282`, exige um token local, não registra pedidos nem chaves e começa
em **simulação**. Só para um Pod se você mandar, com ID e nome exatos. Nunca cria, liga ou apaga Pod.

É ajuda, não garantia: não vê clientes que falam direto com o Pod; se o computador dormir, o processo cair
ou a rede falhar, ela não para a GPU. Use junto com a parada manual e o alerta do provedor.

```sh
mkdir -p ~/.segredos && chmod 700 ~/.segredos
python3 -c "import secrets;print(secrets.token_urlsafe(32))" > ~/.segredos/token-guarda
chmod 600 ~/.segredos/token-guarda
export INEMA_TOKEN_LOCAL_ARQ=~/.segredos/token-guarda
export INEMA_CHAVE_MODELO_ARQ=~/.segredos/chave-modelo     # a chave do endpoint do modelo (chmod 600)
python3 kit/scripts/guarda_ociosa.py --upstream https://SEU-ENDPOINT/v1 --ocioso 900
```

1. No Harness, aponte o provedor para `http://127.0.0.1:8282/v1` e use o **token local** (não a chave da
   RunPod). ID do modelo continua o original. **Todo** pedido passa por aqui.
2. Mande um pedido, espere, mande outro: o relógio zera. Um pedido em andamento ou em streaming impede a
   parada. Depois do tempo ocioso o terminal mostra `{"guarda_ociosa": "simulacao_pararia"}`.
3. Para ligar a parada real, guarde a chave de controle da RunPod em arquivo privado e reinicie:

```sh
export INEMA_CHAVE_RUNPOD_ARQ=~/.segredos/chave-runpod     # chmod 600
python3 kit/scripts/guarda_ociosa.py --upstream https://SEU-ENDPOINT/v1 --ocioso 900 \
  --parar-de-verdade --pod-id SEU_POD_ID --pod-nome "NOME-EXATO-DO-POD"
```

A guarda lê o Pod, confere ID **e** nome, pede a parada e espera `desiredStatus: EXITED`. Se não confirmar,
mostra `parada_falhou_ou_nao_confirmada` e tenta de novo só depois de outro período ocioso. Na primeira vez,
confira você mesmo no painel: pedido de parada não é prova.

## Ligar de novo e remover

Ligue o Pod pelo painel, confirme endpoint e autenticação, e só então reinicie a guarda. Ela não liga GPU
paga sozinha, de propósito. Para remover: pare o processo, volte o provedor do Harness ao endpoint
original e revogue a chave de controle.

Pedidos de lista de modelos também contam como uso: um cliente que consulta a lista de tempos em tempos
pode manter o Pod acordado. A guarda foi feita para um usuário num Pod dedicado.

Documentação oficial: [parar Pod](https://docs.runpod.io/api-reference/pods/POST/pods/podId/stop) ·
[status do Pod](https://docs.runpod.io/api-reference/pods/GET/pods/podId) · [armazenamento](https://docs.runpod.io/pods/storage/types)
