# Checklist da sua instalação

> Uso defensivo. Cada item contra o SEU laboratório ou o SEU endpoint aprovado.

- [ ] Anotei sistema, versões de Python / Node / Harness / runtime e o ID exato do modelo.
- [ ] `python3 kit/scripts/doutor.py`
- [ ] `python3 -m unittest discover -s kit/testes -v` (testes offline, sem internet)
- [ ] Terminal 1: `python3 kit/scripts/laboratorio.py` · Terminal 2: `python3 kit/scripts/checagem_segura.py --lab-local-autorizado` → aparecem 2 achados
- [ ] Parei o laboratório, liguei com `--corrigido`, repeti a checagem → `"achados": []`
- [ ] `checa_endpoint.py` com o ID exato: texto, função e imagem são **resultados separados**
- [ ] Repeti uma função inofensiva dentro do Harness
- [ ] Nuvem: pedido **sem chave** é recusado
- [ ] Guarda ociosa em simulação: pedido zera o relógio; pedido em andamento impede parada; aparece `simulacao_pararia`
- [ ] Primeira parada real conferida no painel (EXITED); liguei de novo e o modelo continua lá
- [ ] Anotei o que **não** testei. Teste com API falsa não prova conta real, GPU paga nem integração no app.
