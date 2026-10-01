# analise/ — código de apoio à análise de dados do caso Aroeira

Código Python independente do notebook, para rodar local (fora do Colab) e reutilizar em qualquer encontro do arco. Testa, com dado, as três justificativas do pedido da diretoria (C0-05) e levanta achados adicionais — ver `../RESUMO_DESAFIO_1.md` para a leitura narrativa dos resultados.

## Arquivos
- `carregar_dados.py` — lê os 4 CSVs de `../Dados/` com os tipos corretos e valida as regras de consistência da camada 0 (ex.: equipamento sem telemetria não deve aparecer em D2, pedido de garantia só sobre ordem corretiva).
- `analise.py` — uma função por hipótese/achado: tendência de duração e volume, perfil de técnicos, reincidência por equipamento, contaminação x ambiente, alerta de telemetria antes de corretiva, panorama de garantia.
- `relatorio.py` — roda tudo e imprime um relatório texto, hipótese por hipótese.

## Como rodar
```bash
pip install -r requirements.txt
python relatorio.py
```

## Como usar em outro script ou notebook
```python
from carregar_dados import carregar_tudo
from analise import tendencia_duracao_e_volume

dados = carregar_tudo()  # usa ../Dados por padrão
tabela = tendencia_duracao_e_volume(dados)
```

Cada função devolve um `DataFrame`/`Series` pronto para citar como proveniência (`conjunto.campo`) num instrumento do encontro — ex.: "D3.duracao_horas, agregado por mês" ou "D2.temp_descarga_maxima, comparado 7 dias antes vs. baseline".

Este código é instrumento de preparo pessoal, não substitui a produção colaborativa do Mapa Técnico do Problema e da Hipótese Técnica em sala — ele só chega com hipóteses melhor embasadas que "o pedido como está".
