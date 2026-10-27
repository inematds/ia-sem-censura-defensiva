# Uso defensivo — as regras do kit

Este kit serve para aprender, achar fraquezas em sistemas **seus** ou que você tem **permissão por escrito**
para testar, e confirmar correções. Ele não dá permissão para testar nada.

## 1. Escopo antes de tudo

Registre: dono do sistema, como a permissão foi dada (e onde está escrita), o host ou app exato, as ações
permitidas, a janela de horário, o limite de pedidos e as condições de parada. Faltou algo? Resolva antes
de mandar o primeiro pedido.

URL pública, login que funciona ou chave de API **não são permissão**. Permissão para um app não cobre
serviços ligados a ele, outras contas, hosts vizinhos nem a infraestrutura do provedor.

Modelo de escopo: [exemplos/escopo-autorizado.exemplo.json](exemplos/escopo-autorizado.exemplo.json).
Do jeito que vem, o kit recusa — de propósito.

## 2. Laboratório sintético primeiro

Comece no laboratório do kit (`scripts/laboratorio.py`, só em 127.0.0.1, dados inventados) ou num ambiente
de homologação com dados falsos. Primeiro as checagens que não mudam nada.

## 3. Prova proporcional

Junte só a evidência necessária para confirmar o achado. Não baixe banco de dados, não exiba credencial
real, não mexa em conta de outra pessoa, não guarde dado pessoal à toa. Mascare antes de compartilhar.

**Pare** quando o próximo passo sair do combinado, afetar a disponibilidade, expor registro sensível ou
exigir mudança destrutiva. Anote o que aconteceu e peça autorização específica. Nada de persistência,
disfarce ou acesso além do escopo.

## 4. Proteja o seu próprio ambiente

- Credencial em arquivo privado (`chmod 600`) ou cofre de segredos. Nunca em prompt, commit ou captura de tela.
- Credenciais de teste, limitadas, revogadas no fim.
- Modelo baixado roda **primeiro sem ferramentas**; depois só com o acesso a arquivos, rede e ferramentas que a tarefa pede.
- **Prompt não é cerca.** O isolamento é imposto pelo sistema operacional, pelo contêiner e pelas permissões.
- Endpoint local preso em `127.0.0.1`. Endpoint na nuvem **sempre com autenticação**.
- Antes de subir GPU, revise preço por hora, armazenamento e como parar. No fim, **pare o Pod e confira EXITED**. Armazenamento ainda cobra.

## 5. Resultado de IA é para conferir

A IA inventa achados e comandos errados. Scanner deixa passar falha e acusa o que não existe. Confira a
evidência, reproduza com segurança, aplique uma correção revisada e reteste. Nada neste kit é certificação,
garantia ou substituto de uma avaliação de segurança independente.

## 6. Ao publicar

Não publique credencial de terceiros, dado privado, log bruto de sessão nem alvo real sem permissão.
Confira licenças antes de redistribuir código, imagem ou arquivo de modelo.

---

Material educativo, fornecido "como está", sem garantia. Você responde por permissões, cópias de segurança,
credenciais, dados pessoais, termos de terceiros e cobranças.
