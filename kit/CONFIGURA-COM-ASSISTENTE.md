# Configure com o seu assistente

> Uso defensivo: só sistemas seus ou com permissão por escrito. Credenciais fora do chat.

Entregue ao seu assistente (Claude Code, Codex ou similar) a pasta deste repositório e cole o pedido abaixo.
Se o assistente não abre links, anexe os arquivos citados.

```text
Me ajude a usar o kit "IA sem censura, do jeito certo" para estudo de segurança defensiva autorizado.
Leia primeiro: kit/COMECE-AQUI.md, kit/USO-DEFENSIVO.md, kit/verificacao/STATUS.md e kit/guias/1-escolha-da-rota.md.
Pergunte: qual rota eu quero, meu sistema e memória livre, se preciso de imagem e qual é o meu orçamento.
Reaproveite o que já está instalado. Nunca me peça para colar chave neste chat.
Use os prompts numerados da rota escolhida (kit/prompts/). Antes de mudar configuração, confira a
documentação oficial e a versão instalada e me mostre os arquivos e as mudanças. Não sobrescreva
provedores nem MCPs que já existem.
Não crie nada pago sem meu OK explícito para a GPU exata, o preço por hora, o armazenamento e o tempo máximo.
Prove de verdade: uma resposta, uma conversa de dois turnos e uma função inofensiva
(python3 kit/scripts/checa_endpoint.py ... --funcao). Imagem só se eu pedir, em teste separado.
Falhou? Diga que falhou; item na lista não é item funcionando.
Testes de segurança só no laboratório sintético (kit/scripts/laboratorio.py + kit/scripts/checagem_segura.py).
Para qualquer outro alvo: minha posse ou permissão escrita, escopo exato, limites e condições de parada.
Faltou algo, pare.
No fim, me entregue: modelo e versão, endpoint, onde ficaram as credenciais (sem os valores), resultado de
cada teste e como ligar, parar e desinstalar.
```

Depois de colar, acompanhe: o assistente deve **mostrar** antes de **fazer**, e parar antes de gastar.
