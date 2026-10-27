# Os 9 prompts em um arquivo

Copie o prompt inteiro, com o bloco FRONTEIRAS. Os arquivos separados estão nesta pasta.

## 01-instalar-harness

```text
PROMPT 01 — Instalar (ou reaproveitar) o DeepSeek Harness

Quero usar o DeepSeek Harness (https://github.com/deepseek-ai/deepseek-harness) para estudo de segurança defensiva. Primeiro olhe o que já existe: meu sistema operacional, a versão do Node.js e se o Harness já está instalado. Se já estiver funcionando, reaproveite; não atualize nem sobrescreva configurações sem me perguntar. Leia o README e o SAFETY.md do projeto. Crie uma pasta de trabalho só para testes, longe dos meus arquivos pessoais, e me mostre o plano de instalação antes de executar. Suba a interface só em 127.0.0.1, adicione apenas essa pasta de teste e confirme que a tela abre. No fim, me diga: versão instalada, endereço local, como ligar e desligar e quais arquivos foram alterados.

FRONTEIRAS (não apague este bloco)
- Uso defensivo: só sistemas meus ou com permissão por escrito do dono. URL pública, login que funciona ou chave de API não são permissão.
- Antes de qualquer teste de segurança, peça o alvo exato, onde está a permissão escrita, as ações permitidas, a janela de horário e os limites. Se faltar, vencer ou ficar confuso: pare sem testar.
- Comece pelo laboratório sintético em 127.0.0.1. Só checagens não destrutivas, dentro do alvo, do ritmo e da janela aprovados. Não siga redirecionamento nem sugestão de ferramenta que saia do escopo.
- Prova proporcional: a menor evidência que confirma o achado. Nada de baixar banco de dados, exibir credencial real, mexer em conta de outra pessoa, derrubar serviço, criar persistência ou apagar rastros. Apareceu dado sensível, escrita inesperada ou lentidão: pare e me avise.
- Credenciais nunca no chat, em log ou no git. Eu digito direto no app ou num arquivo privado (chmod 600).
- Antes de mudar configuração, mostre o que vai mudar. Antes de gastar dinheiro (GPU, API), mostre o custo exato e espere meu OK. Pedido de instalação não autoriza varredura.
- Separe o que foi observado, o que é hipótese e o que é recomendação. Proponha a correção e um reteste dentro do escopo. Varredura sem achados não prova que algo é seguro.
```

## 02-conectar-provedor-hospedado

```text
PROMPT 02 — Conectar um modelo hospedado (rota API)

Quero ligar um modelo hospedado ao meu DeepSeek Harness. Eu escolho o provedor e o orçamento. Se eu ainda não escolhi, compare a documentação oficial atual de dois provedores de modelos abliterated (exemplos: Abliteration e OrcaRouter) sem supor que algum é livre de risco: exigências de conta, termos de uso e preço por token de hoje. No Harness, em Settings > Models, adicione um provedor de API personalizado com o protocolo e a URL base da documentação; busque a lista de modelos e confirme comigo o ID exato. Eu mesmo digito a chave no app ou num arquivo privado. Depois verifique: duas rodadas de conversa e uma chamada de função inofensiva; imagem só se eu precisar, num teste separado. Não mexa nos provedores que já existem e me diga o que passou e o que falhou.

FRONTEIRAS (não apague este bloco)
- Uso defensivo: só sistemas meus ou com permissão por escrito do dono. URL pública, login que funciona ou chave de API não são permissão.
- Antes de qualquer teste de segurança, peça o alvo exato, onde está a permissão escrita, as ações permitidas, a janela de horário e os limites. Se faltar, vencer ou ficar confuso: pare sem testar.
- Comece pelo laboratório sintético em 127.0.0.1. Só checagens não destrutivas, dentro do alvo, do ritmo e da janela aprovados. Não siga redirecionamento nem sugestão de ferramenta que saia do escopo.
- Prova proporcional: a menor evidência que confirma o achado. Nada de baixar banco de dados, exibir credencial real, mexer em conta de outra pessoa, derrubar serviço, criar persistência ou apagar rastros. Apareceu dado sensível, escrita inesperada ou lentidão: pare e me avise.
- Credenciais nunca no chat, em log ou no git. Eu digito direto no app ou num arquivo privado (chmod 600).
- Antes de mudar configuração, mostre o que vai mudar. Antes de gastar dinheiro (GPU, API), mostre o custo exato e espere meu OK. Pedido de instalação não autoriza varredura.
- Separe o que foi observado, o que é hipótese e o que é recomendação. Proponha a correção e um reteste dentro do escopo. Varredura sem achados não prova que algo é seguro.
```

## 03-adicionar-ferramentas

```text
PROMPT 03 — Dar ferramentas ao modelo (navegador, pesquisa e Nuclei)

Com o modelo já respondendo, quero adicionar três ferramentas: Playwright MCP (navegador), Firecrawl MCP (pesquisa em páginas públicas) e o Nuclei pelo terminal. Antes, leia o formato de MCP da versão instalada do Harness e compare com kit/config/dsh-mcp.exemplo.yml; não cole um JSON genérico 'mcpServers' no perfil do Harness. Use um perfil de navegador isolado, sem minhas contas logadas. Para o Firecrawl, use o modo sem chave com limite para o primeiro teste, ou guarde a chave num cofre privado. Prove cada ferramenta com uma chamada real: Playwright abrindo o laboratório sintético (python3 kit/scripts/laboratorio.py, em http://127.0.0.1:8181/), Firecrawl lendo uma página pública de documentação, e Nuclei com 'nuclei -version' mais o template passivo kit/exemplos/nuclei-cabecalhos-lab.yaml SÓ contra o laboratório local. Nada de conjuntos grandes de templates. Ferramenta aparecer na lista não é ferramenta funcionando. Se precisar desfazer, remova só o que você criou.

FRONTEIRAS (não apague este bloco)
- Uso defensivo: só sistemas meus ou com permissão por escrito do dono. URL pública, login que funciona ou chave de API não são permissão.
- Antes de qualquer teste de segurança, peça o alvo exato, onde está a permissão escrita, as ações permitidas, a janela de horário e os limites. Se faltar, vencer ou ficar confuso: pare sem testar.
- Comece pelo laboratório sintético em 127.0.0.1. Só checagens não destrutivas, dentro do alvo, do ritmo e da janela aprovados. Não siga redirecionamento nem sugestão de ferramenta que saia do escopo.
- Prova proporcional: a menor evidência que confirma o achado. Nada de baixar banco de dados, exibir credencial real, mexer em conta de outra pessoa, derrubar serviço, criar persistência ou apagar rastros. Apareceu dado sensível, escrita inesperada ou lentidão: pare e me avise.
- Credenciais nunca no chat, em log ou no git. Eu digito direto no app ou num arquivo privado (chmod 600).
- Antes de mudar configuração, mostre o que vai mudar. Antes de gastar dinheiro (GPU, API), mostre o custo exato e espere meu OK. Pedido de instalação não autoriza varredura.
- Separe o que foi observado, o que é hipótese e o que é recomendação. Proponha a correção e um reteste dentro do escopo. Varredura sem achados não prova que algo é seguro.
```

## 04-pesquisar-modelos-nuvem

```text
PROMPT 04 — Escolher um modelo para a nuvem (só pesquisa, sem gastar)

Pesquise três modelos abliterated no Hugging Face que caibam numa GPU pequena da RunPod e falem com o DeepSeek Harness por uma API compatível com a OpenAI. Preciso de texto, chamada de função e, se possível, imagem. Compare: quem publicou, repositório, revisão e arquivo exatos, suporte no runtime, memória necessária (incluindo contexto e cache), projetor de visão, custo por hora da GPU e do armazenamento, disponibilidade, licença e dúvidas de procedência. Use kit/config/modelos-de-exemplo.json só como ponto de partida datado, não como preço atual. Pergunte meu teto por hora, o orçamento total e quanto tempo vou usar. Velocidade estimada é estimativa: diga isso. Recomende um e explique por que o segundo perdeu. Não crie nenhum recurso pago.

FRONTEIRAS (não apague este bloco)
- Uso defensivo: só sistemas meus ou com permissão por escrito do dono. URL pública, login que funciona ou chave de API não são permissão.
- Antes de qualquer teste de segurança, peça o alvo exato, onde está a permissão escrita, as ações permitidas, a janela de horário e os limites. Se faltar, vencer ou ficar confuso: pare sem testar.
- Comece pelo laboratório sintético em 127.0.0.1. Só checagens não destrutivas, dentro do alvo, do ritmo e da janela aprovados. Não siga redirecionamento nem sugestão de ferramenta que saia do escopo.
- Prova proporcional: a menor evidência que confirma o achado. Nada de baixar banco de dados, exibir credencial real, mexer em conta de outra pessoa, derrubar serviço, criar persistência ou apagar rastros. Apareceu dado sensível, escrita inesperada ou lentidão: pare e me avise.
- Credenciais nunca no chat, em log ou no git. Eu digito direto no app ou num arquivo privado (chmod 600).
- Antes de mudar configuração, mostre o que vai mudar. Antes de gastar dinheiro (GPU, API), mostre o custo exato e espere meu OK. Pedido de instalação não autoriza varredura.
- Separe o que foi observado, o que é hipótese e o que é recomendação. Proponha a correção e um reteste dentro do escopo. Varredura sem achados não prova que algo é seguro.
```

## 05-subir-modelo-nuvem

```text
PROMPT 05 — Subir na RunPod o modelo que eu aprovei

Suba na RunPod apenas o modelo, a GPU e o runtime que aprovei depois do prompt 04. Antes de criar qualquer coisa, reconfirme comigo: preço por hora, custo do armazenamento, região e o tempo máximo de uso. Não mexa em Pods que já existem. Fixe a revisão do modelo e o projetor de visão compatível; guarde modelo e configuração de inicialização no armazenamento persistente. Crie um endpoint compatível com OpenAI COM autenticação e prove que uma requisição sem chave é recusada. A chave de controle da RunPod é diferente da chave do modelo e as duas ficam fora do chat. Conecte o ID exato no Harness. Teste: duas rodadas de conversa, uma função inofensiva e a imagem sintética kit/exemplos/teste-visao.png. Depois siga kit/guias/custo-runpod.md: pare, confira EXITED, ligue de novo e confirme que os arquivos continuam lá. Me entregue endpoint, versões, resultado de cada teste, o que continua cobrando e como parar ou apagar ESTE Pod. Se alguma capacidade prometida falhar, não diga que terminou.

FRONTEIRAS (não apague este bloco)
- Uso defensivo: só sistemas meus ou com permissão por escrito do dono. URL pública, login que funciona ou chave de API não são permissão.
- Antes de qualquer teste de segurança, peça o alvo exato, onde está a permissão escrita, as ações permitidas, a janela de horário e os limites. Se faltar, vencer ou ficar confuso: pare sem testar.
- Comece pelo laboratório sintético em 127.0.0.1. Só checagens não destrutivas, dentro do alvo, do ritmo e da janela aprovados. Não siga redirecionamento nem sugestão de ferramenta que saia do escopo.
- Prova proporcional: a menor evidência que confirma o achado. Nada de baixar banco de dados, exibir credencial real, mexer em conta de outra pessoa, derrubar serviço, criar persistência ou apagar rastros. Apareceu dado sensível, escrita inesperada ou lentidão: pare e me avise.
- Credenciais nunca no chat, em log ou no git. Eu digito direto no app ou num arquivo privado (chmod 600).
- Antes de mudar configuração, mostre o que vai mudar. Antes de gastar dinheiro (GPU, API), mostre o custo exato e espere meu OK. Pedido de instalação não autoriza varredura.
- Separe o que foi observado, o que é hipótese e o que é recomendação. Proponha a correção e um reteste dentro do escopo. Varredura sem achados não prova que algo é seguro.
```

## 06-guarda-ociosa

```text
PROMPT 06 — Ligar e provar a guarda de tempo ocioso

Para o Pod que eu aprovar, configure a guarda local kit/scripts/guarda_ociosa.py seguindo kit/guias/custo-runpod.md. Comece em simulação. Faça TODO pedido ao modelo passar por ela (http://127.0.0.1:8282/v1). Prove três coisas: um pedido zera o relógio; um pedido em andamento ou em streaming impede a parada; depois do tempo ocioso aparece 'simulacao_pararia'. Só depois do meu OK, ligue a parada real com --parar-de-verdade, --pod-id e --pod-nome exatos e a chave de controle num arquivo privado. Confira ID e nome antes de parar e confirme EXITED depois; ligue de novo num teste separado. Explique que a guarda não vê clientes que falam direto com o Pod, que computador dormindo ou processo caído não param a GPU, e que o armazenamento continua cobrando. Mantenha a parada manual e o alerta de orçamento do provedor. Nunca crie nem apague Pod, e nunca pare um Pod que não seja este.

FRONTEIRAS (não apague este bloco)
- Uso defensivo: só sistemas meus ou com permissão por escrito do dono. URL pública, login que funciona ou chave de API não são permissão.
- Antes de qualquer teste de segurança, peça o alvo exato, onde está a permissão escrita, as ações permitidas, a janela de horário e os limites. Se faltar, vencer ou ficar confuso: pare sem testar.
- Comece pelo laboratório sintético em 127.0.0.1. Só checagens não destrutivas, dentro do alvo, do ritmo e da janela aprovados. Não siga redirecionamento nem sugestão de ferramenta que saia do escopo.
- Prova proporcional: a menor evidência que confirma o achado. Nada de baixar banco de dados, exibir credencial real, mexer em conta de outra pessoa, derrubar serviço, criar persistência ou apagar rastros. Apareceu dado sensível, escrita inesperada ou lentidão: pare e me avise.
- Credenciais nunca no chat, em log ou no git. Eu digito direto no app ou num arquivo privado (chmod 600).
- Antes de mudar configuração, mostre o que vai mudar. Antes de gastar dinheiro (GPU, API), mostre o custo exato e espere meu OK. Pedido de instalação não autoriza varredura.
- Separe o que foi observado, o que é hipótese e o que é recomendação. Proponha a correção e um reteste dentro do escopo. Varredura sem achados não prova que algo é seguro.
```

## 07-pesquisar-modelos-locais

```text
PROMPT 07 — Escolher um modelo para o meu computador

Veja meu sistema, CPU, GPU, disco livre e memória disponível, sem abrir meus arquivos pessoais. Encontre três modelos abliterated no Hugging Face que caibam com folga para contexto, cache e projetor de visão (se eu precisar de imagem). Preciso de texto e chamada de função. Compare: quem publicou, revisão, quantização, licença, procedência, suporte no runtime e tamanho do download. Se eu já tiver um modelo compatível baixado, prefira ele. Tokens por segundo são estimativas não testadas: deixe isso claro. Lembre que popularidade e antivírus não provam que um modelo é seguro. Recomende um, explique por que os outros perderam e pergunte antes de qualquer download grande.

FRONTEIRAS (não apague este bloco)
- Uso defensivo: só sistemas meus ou com permissão por escrito do dono. URL pública, login que funciona ou chave de API não são permissão.
- Antes de qualquer teste de segurança, peça o alvo exato, onde está a permissão escrita, as ações permitidas, a janela de horário e os limites. Se faltar, vencer ou ficar confuso: pare sem testar.
- Comece pelo laboratório sintético em 127.0.0.1. Só checagens não destrutivas, dentro do alvo, do ritmo e da janela aprovados. Não siga redirecionamento nem sugestão de ferramenta que saia do escopo.
- Prova proporcional: a menor evidência que confirma o achado. Nada de baixar banco de dados, exibir credencial real, mexer em conta de outra pessoa, derrubar serviço, criar persistência ou apagar rastros. Apareceu dado sensível, escrita inesperada ou lentidão: pare e me avise.
- Credenciais nunca no chat, em log ou no git. Eu digito direto no app ou num arquivo privado (chmod 600).
- Antes de mudar configuração, mostre o que vai mudar. Antes de gastar dinheiro (GPU, API), mostre o custo exato e espere meu OK. Pedido de instalação não autoriza varredura.
- Separe o que foi observado, o que é hipótese e o que é recomendação. Proponha a correção e um reteste dentro do escopo. Varredura sem achados não prova que algo é seguro.
```

## 08-conectar-modelo-local

```text
PROMPT 08 — Ligar o modelo local do LM Studio ao Harness

Use o modelo local que aprovei no LM Studio e ligue ao DeepSeek Harness. Confira as versões do LM Studio e do runtime. Reaproveite o que já foi baixado, escolha um contexto modesto que caiba com folga e deixe o servidor preso em 127.0.0.1. Confirme com quem publicou o modelo qual projetor de visão combina com ele. Adicione um provedor separado no Harness sem apagar o que existe. Rode kit/scripts/checa_endpoint.py com o ID exato do modelo e --funcao; se eu precisar de imagem, rode também com --imagem kit/exemplos/teste-visao.png. Não dê terminal nem acesso livre a arquivos ao modelo só para testar chamada de função. Informe os tempos observados junto com hardware, contexto e limite de saída, sem chamar isso de benchmark. Me dê os comandos para descarregar o modelo e parar o servidor, e desligue tudo no fim se eu pedir.

FRONTEIRAS (não apague este bloco)
- Uso defensivo: só sistemas meus ou com permissão por escrito do dono. URL pública, login que funciona ou chave de API não são permissão.
- Antes de qualquer teste de segurança, peça o alvo exato, onde está a permissão escrita, as ações permitidas, a janela de horário e os limites. Se faltar, vencer ou ficar confuso: pare sem testar.
- Comece pelo laboratório sintético em 127.0.0.1. Só checagens não destrutivas, dentro do alvo, do ritmo e da janela aprovados. Não siga redirecionamento nem sugestão de ferramenta que saia do escopo.
- Prova proporcional: a menor evidência que confirma o achado. Nada de baixar banco de dados, exibir credencial real, mexer em conta de outra pessoa, derrubar serviço, criar persistência ou apagar rastros. Apareceu dado sensível, escrita inesperada ou lentidão: pare e me avise.
- Credenciais nunca no chat, em log ou no git. Eu digito direto no app ou num arquivo privado (chmod 600).
- Antes de mudar configuração, mostre o que vai mudar. Antes de gastar dinheiro (GPU, API), mostre o custo exato e espere meu OK. Pedido de instalação não autoriza varredura.
- Separe o que foi observado, o que é hipótese e o que é recomendação. Proponha a correção e um reteste dentro do escopo. Varredura sem achados não prova que algo é seguro.
```

## 09-checar-meu-app

```text
PROMPT 09 — Checar o MEU app com escopo autorizado

Quero examinar um app de teste meu. Comece pelo laboratório sintético do kit, nunca por um site público. Leia kit/USO-DEFENSIVO.md. No laboratório: rode python3 kit/scripts/laboratorio.py num terminal e python3 kit/scripts/checagem_segura.py --lab-local-autorizado em outro; explique os achados usando kit/exemplos/relatorio-de-achados.exemplo.md; depois rode o laboratório com --corrigido e faça o reteste. Para um app real, ANTES de qualquer pedido: registre a permissão escrita, o alvo exato, as ações permitidas, a janela, o limite de ritmo e as condições de parada (modelo em kit/exemplos/escopo-autorizado.exemplo.json) e me mostre um plano não destrutivo para eu aprovar. Colete só a evidência mínima, com dados mascarados, separe achado confirmado de hipótese, proponha correções e um reteste limitado. Nada de varredura automática fora do escopo aprovado.

FRONTEIRAS (não apague este bloco)
- Uso defensivo: só sistemas meus ou com permissão por escrito do dono. URL pública, login que funciona ou chave de API não são permissão.
- Antes de qualquer teste de segurança, peça o alvo exato, onde está a permissão escrita, as ações permitidas, a janela de horário e os limites. Se faltar, vencer ou ficar confuso: pare sem testar.
- Comece pelo laboratório sintético em 127.0.0.1. Só checagens não destrutivas, dentro do alvo, do ritmo e da janela aprovados. Não siga redirecionamento nem sugestão de ferramenta que saia do escopo.
- Prova proporcional: a menor evidência que confirma o achado. Nada de baixar banco de dados, exibir credencial real, mexer em conta de outra pessoa, derrubar serviço, criar persistência ou apagar rastros. Apareceu dado sensível, escrita inesperada ou lentidão: pare e me avise.
- Credenciais nunca no chat, em log ou no git. Eu digito direto no app ou num arquivo privado (chmod 600).
- Antes de mudar configuração, mostre o que vai mudar. Antes de gastar dinheiro (GPU, API), mostre o custo exato e espere meu OK. Pedido de instalação não autoriza varredura.
- Separe o que foi observado, o que é hipótese e o que é recomendação. Proponha a correção e um reteste dentro do escopo. Varredura sem achados não prova que algo é seguro.
```
