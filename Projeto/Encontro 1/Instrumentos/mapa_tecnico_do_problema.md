# Mapa Técnico do Problema (KIT-001)

> Instrumento do kit de formação, preenchido pelo squad **durante o Encontro 1**. Como preencher: completar durante o encontro. **Não escolher tecnologia ainda** — o objetivo é entender o problema.
>
> O conteúdo abaixo nas seções 1–5 é uma **proposta inicial, baseada na análise de dados já feita** (`RESUMO_DESAFIO_1.md` e `notebook_analise_exploratoria.ipynb`) — leve para a discussão do squad, conteste, ajuste a redação e confirme a proveniência antes de considerar pronto. Célula sem proveniência é devolvida pelo mentor.

## Identificação

| Campo | Preenchimento |
|---|---|
| Squad / Polo | *(preencher)* |
| Data | *(preencher — data do Encontro 1)* |
| Caso / Desafio | caso da Aroeira |
| Integrantes e papéis do dia (quem registra / quem apresenta) | *(preencher)* |

## 1. Problema técnico delimitado (raiz, não sintoma)

> Teste: se a frase começa com "usar IA para…", ainda é solução, não problema.

**Enunciado (1 a 2 frases) — proposta (atualizada com a camada 1):**

> A proporção de ordens corretivas em relação às preventivas vem crescendo (36,9%→59,0% das ordens no período), o que explica mecanicamente a alta do indicador de tempo médio de atendimento do painel — e não um atendimento individual mais lento; ao mesmo tempo, parte das causas de falha mais frequentes (elétrica, vazamento de óleo, contaminação por particulado) se repete no mesmo equipamento pouco tempo depois do reparo anterior, um padrão que o próprio técnico já percebe informalmente mas sem registro sistemático.

*(Passa no teste: não cita "assistente", "chatbot" nem nenhuma tecnologia — descreve o fenômeno, não a solução.)*

## 2. Sintomas × Causas

| Sintomas observáveis | Causas prováveis |
|---|---|
| Tempo médio de atendimento subindo no painel de serviço (C0-05, C1-02: 3,4h→4,5h) | **Confirmado e explicado**: duração de cada tipo de ordem é estável no tempo (corretiva ~5,6–6,1h, preventiva ~2,4–2,6h); o que sobe é a **proporção de corretivas no mix** (36,9%→59,0%), que puxa a média geral para cima mecanicamente — pergunta real é por que a preventiva está perdendo espaço (`D3.tipo_ordem`, `D3.duracao_horas`, `D3.data_abertura`) |
| Reincidência de chamados no mesmo equipamento (C0-05), corroborada pelo relato de Kleber (C1-04) | **7,7%** dos atendimentos consecutivos no mesmo equipamento repetem a mesma causa em até 30 dias — concentrado em `falha_eletrica`, `vazamento_oleo`, `contaminacao_particulado`; técnico já reconhece o padrão informalmente mas "não tem número pra mostrar" (`D3.causa_registrada`, `D3.data_abertura`, `D3.id_equipamento`) |
| Técnico relata dificuldade de acesso à informação durante o atendimento (C1-03, Iran) | Dor específica e dupla: (1) **histórico do equipamento** não é visível entre técnicos diferentes quando um atende um equipamento já visitado por outro; (2) **manual extenso, não indexado**, difícil de buscar no celular durante o atendimento — recorte mais preciso do pedido original (C0-05), não um chatbot genérico |
| Diretoria aponta "técnicos sem experiência na série CP" (C0-05) | **Não verificável** com os dados atuais: os 14 técnicos em `D3.id_tecnico` aparecem todos já no 1º mês do período; correlação entre ordem de entrada e duração média ≈ 0 — lacuna de dado, não causa confirmada nem descartada |

## 3. Dados disponíveis e qualidade

| Dado | Disponível? | Qualidade | Observação |
|---|---|---|---|
| D1 — frota (184 equipamentos) | sim | alta | 9 campos, sem inconsistência encontrada na validação de integridade |
| D2 — telemetria diária (42.458 linhas) | parcial | média | só 126/184 equipamentos (68%) têm módulo; há dias de transmissão incompleta (indicador explícito) e séries mais curtas por instalação recente — as duas situações não devem ser confundidas (C0-08) |
| D3 — ordens de serviço (2.122 linhas) | sim | alta | causa em lista fechada (10 valores); relato técnico em texto livre existe mas ainda não explorado |
| D4 — pedidos de garantia (712 linhas) | sim | média | só existe sobre ordem corretiva; 34% das decisões são negativas, majoritariamente por "uso fora de especificação" (achado paralelo ao pedido original) |
| Painel de serviço — indicador oficial (C1-02) | sim (12 valores mensais) | alta | reproduzido com precisão a partir de `D3.duracao_horas` médio por mês, sobre todas as ordens — não é um dataset novo, é a definição do indicador que faltava |
| Relatos de técnicos (C1-03, C1-04) | sim (2 depoimentos) | qualitativa | não é dado numérico, mas corrobora achados quantitativos (reincidência) e aponta uma dor específica de acesso à informação |
| Dado de senioridade/data de contratação do técnico | **não** | — | não existe em nenhum dos 4 conjuntos — é a lacuna que impede testar a hipótese "técnicos sem experiência" |

## 4. Restrições

| Dimensão | Conteúdo — proposta |
|---|---|
| **Técnicas** | Telemetria cobre só 68% da frota, com séries de tamanho variável (11 a 365 dias) e sem campo de tempo de espera/fila; painel de serviço só expõe o indicador agregado por mês, sem abertura por tipo de ordem/causa/equipamento (C1-02) — qualquer diagnóstico mais fino exige recalcular a partir de D3, não do painel |
| **Éticas / regulatórias** | Decisões de garantia podem ser contestadas pelo cliente (C0-04); análise leva até 30 dias corridos e usa o registro do atendimento quando não há medição (C1-01); cláusula de "uso fora de especificação" cobre regime de trabalho, temperatura/pressão, qualidade do ar aspirado e manutenção com insumos homologados — qualquer solução que toque avaliação/triagem de causa precisa manter rastreabilidade e justificativa auditável |
| **Operacionais (prazo, infraestrutura, orçamento)** | Equipe de 14 técnicos estável durante todo o período de alta de volume; proporção de corretivas crescendo em relação a preventivas (36,9%→59,0%); arco de 3 encontros (prazo do laboratório); orçamento de 4 perguntas ao squad no Encontro 1 |

## 5. Oportunidades candidatas de IA (sem juízo ainda)

> Listar ao menos duas, sem escolher nenhuma — a escolha vem nos Encontros 2 e 3.

**Abordagens possíveis — proposta:**
1. **Manutenção preditiva seletiva via telemetria** — sinal de alerta (alta de temperatura de descarga) existe para falhas de válvula/vedação, mas não para as 3 causas mais frequentes/reincidentes (amostra pequena, cautela)
2. **Apoio ao diagnóstico de causa raiz** nas 3 causas mais reincidentes, a partir do relato técnico + histórico do equipamento — sistematiza o que Kleber já percebe tacitamente (C1-04)
3. **Ferramenta de consulta rápida ao histórico do equipamento e ao manual**, no momento do atendimento — recorte mais preciso do pedido original (C0-05), ancorado diretamente no relato de Iran (C1-03)
4. **Investigar a migração do mix preventiva→corretiva** (gestão/alocação de manutenção preventiva) — não é bem "IA generativa", mas é a leitura de dados que mais explica o sintoma citado pela diretoria

## Critério de pronto (autoverificação do squad antes de avançar)

- [ ] Problema enunciado como raiz, não sintoma
- [ ] Sintomas e causas diferenciados
- [ ] Dados e qualidade registrados
- [ ] Restrições em ao menos três dimensões
- [ ] Oportunidades de IA como candidatas, sem escolha

## Devolutiva do mentor (evidência → interpretação → próximo passo → prazo)

| Campo | Registro |
|---|---|
| Evidência observada | *(preenchido em sala)* |
| Interpretação técnica | *(preenchido em sala)* |
| Próximo passo | *(preenchido em sala)* |
| Prazo / momento de revisão | *(preenchido em sala)* |
