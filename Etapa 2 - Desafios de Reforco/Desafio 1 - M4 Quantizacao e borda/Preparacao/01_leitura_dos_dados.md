# Leitura descritiva de `relatos_de_campo.csv` (antes do critério)

> Só estatística descritiva do arquivo (contagens, comprimentos, padrões de texto). **Nenhum modelo foi treinado nem medido**, porque o critério de aceite vem antes do teste.
> Fonte: `squad-05-ufc/desafio-1-m4/dados/relatos_de_campo.csv`. Contagens feitas com Python puro (`csv`, `re`) em 09/11/2026.

## Visão geral
- **3.000 relatos**, de 01/06/2026 a 30/06/2026. Colunas: `id`, `data`, `equipamento`, `texto`, `classe`. Conjunto **sintético**.
- **Textos curtos:** 13,4 palavras em média (mediana 13, máximo 28); no máximo 181 caracteres. Com `max_length=64` tokens no notebook, praticamente nada deve ser truncado (confirmar no tokenizador).
- **Ruído de digitação proposital:** abreviações (`mot.`, `bba`, `c/`, `s/`, `equip.`), erros (`rolate`, `perot`, `paienl`, `cntator`, `etqiuetagem`) e textos em CAIXA ALTA.
- **8 textos duplicados**, todos com o mesmo rótulo. Um par pode cair em treino e teste ao mesmo tempo, mas o efeito é desprezível.

## Distribuição das classes

| Classe | Relatos | % | ~na amostra de 300 |
|---|---:|---:|---:|
| eletrica | 902 | 30,1% | ~90 |
| mecanica | 842 | 28,1% | ~84 |
| hidraulica | 499 | 16,6% | ~50 |
| instrumentacao | 439 | 14,6% | ~44 |
| seguranca | 318 | 10,6% | ~32 |

As classes são desbalanceadas, e **`seguranca` é a menor e a mais cara de errar**. Por isso o F1 macro deve entrar no critério ao lado da acurácia.

## Equipamento × classe
Sete tipos de equipamento, de 360 a 471 relatos cada. Todas as classes aparecem em todos os equipamentos, **exceto `hidraulica` em `motor`** (zero). Os relatos de "ar comprimido" ou pneumáticos (121) são majoritariamente `hidraulica` (102), como a situação define, mas 14 estão em `mecanica` e 5 em `instrumentacao`.

## ⚠️ Achado para levar ao E1: relatos com dois problemas e rótulo inconsistente
Muitos relatos juntam **duas ocorrências** num texto só (separadas por `;`, `.`, ` e `). O caso crítico é quando **um dos problemas é de segurança**:

- 252 relatos têm pista clara de segurança (aterramento rompido, guarda-corpo solto, proteção removida, sem bloqueio e etiquetagem).
- Destes, **51 também têm pista elétrica** (disjuntor, isolamento, borne, inversor, contator, fase...). O rótulo se divide: **26 `eletrica` × 25 `seguranca`**.
- Mais 12 relatos com pista de segurança estão como `eletrica` ou `mecanica` e trazem um segundo problema, como "relé térmico atuando" ou "botoeira sem resposta".

Exemplos (rótulo | texto):
- `eletrica` | *prensa sem bloqueio e etiquetagem na intervencao; prensa hidraulica c/ corrente alta, rele termico atuando*
- `eletrica` | *guarda-corpo perto do gerador de vapor solto; gerador de vapor com corrente alta, rele termico atuando*
- `seguranca` | *disjuntor do caldeira a gas desarmando na partida; aterramento do caldeira rompido - linha parada*

**Consequências (hipóteses, não conclusões):**
1. **Teto de acurácia:** se o rótulo de relatos mistos não segue regra fixa, nenhum dos três caminhos acerta todos. Parte da "perda" pode ser ruído do rótulo, e não efeito da quantização.
2. **Risco operacional:** um relato com risco de segurança classificado como `eletrica` aciona o eletricista e não a segurança. É o erro mais caro.
3. **Pergunta ao instrutor no E1:** existe regra de prioridade quando o relato tem dois problemas (por exemplo, segurança sempre prevalece)? Se não existe, registrar como incerteza no KIT-003 e no KIT-007.
4. Isso liga o desafio ao **M3 Data-centric** (qualidade de rótulo, error analysis por recorte). Na defesa, vale olhar os erros dos três modelos **nos relatos mistos** separadamente.

## O que isso muda no rascunho do critério
- Manter **F1 macro**, não só acurácia.
- A tolerância de perda deve ficar **acima do ruído da amostra** (1 relato = 0,33 p.p.).
- Comparar a perda **entre modelos**, contra a referência BERTimbau float32, e não contra 100%: o teto real é menor por causa do rótulo.
