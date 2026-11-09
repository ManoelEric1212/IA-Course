# Resumo do Desafio — Encontro 1 (caso Aroeira)

> Preparo pessoal antes do encontro. Não é o Mapa Técnico do Problema nem a Hipótese Técnica — esses instrumentos são produzidos em squad, em sala, com proveniência citada célula a célula. Isto aqui é munição para chegar com hipóteses melhores que "o pedido como está".

## O que o Encontro 1 exige de mim hoje

Produzir, em squad, 3 instrumentos (critério de pronto completo em `.claude/skills/projeto-aroeira/references/encontro-1.md`):
1. **Acordo de squad** (papéis, rodízio, decisão sem consenso, canal, pasta)
2. **Mapa Técnico do Problema** — enunciado como raiz (não sintoma), sintomas×causas, dados e qualidade, restrições em 3+ dimensões, oportunidades de IA candidatas **sem escolher nenhuma**
3. **Hipótese Técnica** — abordagem + condição + critério de teste, com a tarefa/paradigma (M0) nomeados e justificados

Regra de ouro do arco inteiro: **nenhuma tecnologia é escolhida hoje.** E toda afirmação precisa de proveniência (`C0-xx` do dossiê ou `conjunto.campo` dos dados) — "porque faz sentido" não entra.

## O pedido tal como chegou (C0-05) — e por que ele é uma armadilha

> *"Um assistente conversacional com IA para os técnicos de campo, capaz de responder em linguagem natural sobre histórico do equipamento, manuais e procedimentos, e capaz de abrir a ordem de serviço e solicitar a peça sem sair da conversa."*

Justificativa da diretoria, em três partes — e é nelas que a análise precisa bater:
1. Tempo médio de atendimento subiu no painel de serviço.
2. Entraram técnicos sem experiência na série CP.
3. Há reincidência de chamados no mesmo equipamento.

O erro clássico (já visto nos slides do curso base, módulo M1: "o reflexo do mais novo", e módulo M2: "tratar a arquitetura agentic como default moderno") é aceitar a solução pedida como se fosse o problema. Um assistente conversacional resolve *falta de acesso a informação*. Os dados abaixo testam se é isso mesmo que está faltando.

## O que a análise dos dados (D1–D4) mostra — hipótese por hipótese

### 1. "Tempo médio de atendimento subiu" — confirmado e explicado com precisão (atualizado com a camada 1)
A camada 1 trouxe o indicador **real** do painel (C1-02): **"tempo médio de atendimento" = média de `duracao_horas` sobre TODAS as ordens abertas no mês** (corretiva + preventiva + inspeção + comissionamento), não só as corretivas. Valor oficial: **3,4h (set/2025) → 4,5h (ago/2026)**, média do período 4,0h.

> **Correção de rota**: a primeira versão desta análise tinha calculado a duração só sobre ordens corretivas (5,64h → 6,08h, alta de ~8%) — um erro de escopo. Reproduzindo o indicador exatamente como o painel define (sobre todas as ordens), a série bate com a oficial quase ponto a ponto (3,40 / 3,69 / 3,89 / 3,77 / 3,66 / 4,16 / 4,17 / 3,85 / 4,28 / 4,42 / 4,16 / 4,46 — ver `analise.py::indicador_painel_oficial`).

O mecanismo real, agora confirmado:
- A duração média **de cada tipo de ordem**, isoladamente, fica **estável** o ano inteiro: corretiva ~5,6–6,1h, preventiva ~2,4–2,6h, inspeção ~1,3–1,4h.
- O que muda é o **mix**: a proporção de corretivas sobe de **36,9% para 59,0%** das ordens do mês, enquanto preventivas caem de **35,2% para 23,0%** e inspeções de 24,6% para 15,6%.
- Como corretiva demora ~2,4x mais que preventiva, um mix com mais corretiva **puxa a média geral para cima mecanicamente** — mesmo sem nenhum atendimento individual ficando mais lento.
- Volume absoluto também cresceu (122 → 244 ordens/mês, ~2x no total; 3,2x só nas corretivas) — ou seja, há dois efeitos simultâneos: mais trabalho no total, e proporcionalmente mais trabalho reativo (corretivo) em vez de preventivo.

**Leitura candidata (agora bem mais específica)**: o sintoma "tempo médio subiu" é real e **mecanicamente explicado pelo mix de ordens**, não por lentidão de atendimento. A pergunta que o Mapa Técnico precisa levantar não é "por que o técnico demora mais", e sim **"por que a proporção de corretivas está crescendo em relação às preventivas"** — hipótese de um ciclo: menos tempo para manutenção preventiva → mais falhas → mais corretivas → ainda menos tempo para preventiva.

### Depoimentos dos técnicos (C1-03, C1-04) — cruzamento qualitativo com os dados
- **Iran**: o que consome tempo não é o serviço em si, é **chegar sem saber o que já foi feito naquele equipamento** (histórico espalhado entre técnicos) e **buscar o procedimento certo num manual extenso no celular**, no meio do atendimento. Dor específica de **acesso à informação já existente**, não de decisão.
- **Kleber**: em algumas plantas, ele já **sabe informalmente** qual peça vai trocar antes de abrir o equipamento — reconhece um padrão de recorrência — mas **não tem registro nem número pra mostrar isso**. Essa fala **valida qualitativamente** o achado quantitativo de reincidência concentrada (seção 3 abaixo): o que os dados mostram agregado, o técnico mais experiente já percebe individualmente, sem conseguir provar.

### 2. "Técnicos novos sem experiência na série CP" — não verificável com os dados disponíveis
- Os 14 `id_tecnico` aparecem todos entre 01/set e 02/out/2025 — não há um grupo claramente "mais novo" entrando depois, pelo menos não de forma visível em D3.
- Correlação entre ordem de entrada do técnico e duração média do atendimento: **≈ 0** (−0,057). Correlação com proporção de causa não identificada: fraca (0,20, amostra de 14 técnicos).
- **Leitura candidata**: a afirmação da diretoria pode ser verdadeira, mas **os dados fornecidos não permitem testá-la** — falta um campo de data de contratação/senioridade por técnico. Isso é, em si, um achado: uma restrição de dados a declarar no Mapa (dimensão "dados e qualidade"), não um fato a aceitar ou negar sem evidência.

### 3. "Reincidência de chamados no mesmo equipamento" — confirmada, e concentrada
- 179 equipamentos tiveram ao menos 1 corretiva; mediana de 6 corretivas por equipamento ao longo do ano, alguns com até 12.
- Olhando pares consecutivos de corretiva no mesmo equipamento (905 pares): **18,9%** repetem a mesma causa do atendimento anterior; **7,7%** repetem a mesma causa **dentro de 30 dias** (reincidência "quente" — sugere reparo que não eliminou a causa raiz).
- Essa reincidência quente se concentra em 3 causas: **falha_eletrica, vazamento_oleo, contaminacao_particulado** — as três causas mais frequentes do dataset inteiro.
- **Leitura candidata**: a reincidência existe e é real, mas aponta para **qualidade/eficácia do reparo nessas 3 causas específicas**, não para falta de informação do técnico no momento do atendimento.

## Achados adicionais que os slides/pedido não mencionam (e que valem a pena levar)

- **A hipótese ambiental mais óbvia não se sustenta**: `contaminacao_particulado` como causa **não é mais frequente** em plantas de `classe_ambiente = particulado_alto` (22,8%) do que em `particulado_baixo` (30,5%) — o oposto do que se esperaria. Vale desconfiar de explicações "óbvias" sem checar o dado.
- **Telemetria tem sinal de alerta, mas só para parte das causas**: nos 7 dias antes de uma corretiva, a temperatura máxima de descarga sobe acima da linha de base (30–60 dias antes) em **+7,95°C para `falha_valvula_admissao`** (n=5 amostras) e **+7,40°C para `falha_vedacao`** (n=11) — sinal de desgaste gradual, candidato real a manutenção preditiva, mas com amostra pequena, tratar como pista. Já para `falha_eletrica` (n=181), `vazamento_oleo` (n=175) e `contaminacao_particulado` (n=182) — as 3 causas mais frequentes e mais reincidentes, com amostra grande e confiável — **não há esse aviso prévio** (delta ≈ 0,08–0,30°C): são falhas mais súbitas, telemetria de temperatura não ajuda a prever essas três.
- **Garantia é um ponto de atrito separado**: 34% dos pedidos são negados (majoritariamente por "uso fora de especificação"), e a taxa de contestação do cliente é 5x maior numa decisão negativa (20,6%) do que numa total (4%). Não é o que a diretoria pediu, mas é um sintoma correlato que pode voltar na Matriz de Riscos/Validação mais adiante.

## Reframe para levar ao squad (ponto de partida, não resposta fechada)

O pedido original mira **acesso à informação durante o atendimento** (chatbot). Com a camada 1, os três sintomas citados ficam mais nítidos — dois confirmados com mecanismo preciso, um ainda não testável:
- tempo subindo → **confirmado e explicado**: mix de ordens migrando de preventiva para corretiva (36,9%→59,0%), não atendimento mais lento — a pergunta real é por que a preventiva está perdendo espaço;
- técnico novo sem experiência → **ainda não testável com os dados atuais**, é lacuna, não fato;
- reincidência → **real, concentrada em 3 causas, e corroborada qualitativamente** por Kleber (que já percebe o padrão informalmente, sem conseguir prová-lo).

O depoimento de Iran dá um recorte **mais preciso** do próprio pedido original: não é "assistente conversacional genérico", é especificamente **acesso ao histórico de atendimentos anteriores do mesmo equipamento entre técnicos diferentes** + **busca rápida no manual** — um problema de recuperação de informação concreto, não um chatbot aberto.

Candidatas de IA a levar para o Mapa (sem escolher nenhuma ainda — isso é regra do Encontro 1):
1. Manutenção preditiva seletiva via telemetria, para as causas com sinal de alerta (válvula/vedação).
2. Apoio ao diagnóstico de causa raiz nas 3 causas reincidentes (classificação/triagem a partir do relato técnico + histórico do equipamento) — captura sistematizada do que Kleber já sabe tacitamente.
3. Ferramenta de consulta rápida ao histórico do equipamento + busca no manual, no momento do atendimento — recorte mais preciso do pedido original, ancorado no depoimento de Iran.
4. Investigar por que o mix está migrando para corretiva (gestão/alocação de manutenção preventiva) — não é bem "IA generativa", mas é uma leitura de dados que precisa entrar no Mapa como alternativa ao pedido original.

Use o notebook `notebook_analise_exploratoria.ipynb` (ou os scripts em `analise/`) para reproduzir, aprofundar ou contestar qualquer um desses números antes de levar ao squad — e lembre de registrar `conjunto.campo` como proveniência de cada célula que vier daqui.
