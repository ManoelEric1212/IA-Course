# Hipótese Técnica (KIT-003)

> Instrumento do kit de formação, preenchido pelo squad **durante o Encontro 1** (o template original traz "Encontro 2" na capa porque pertence ao kit de 5 encontros — no mapa de instrumentos deste arco de 3 encontros, KIT-022 §1.2, a Hipótese Técnica é produzida no **Encontro 1**, logo depois do Mapa Técnico do Problema). **Como preencher**: uma hipótese = abordagem + condição + resultado esperado + critério de teste.
>
> **Decisão do squad**: das hipóteses levantadas na discussão (classificação de causa raiz, alerta de telemetria, recuperação de histórico+manual, regressão de demanda, clustering de equipamentos), o squad fechou em **três**: alerta de telemetria (H1), recuperação de histórico+manual (H2), e a composição das duas como workflow determinístico (H3). As demais ficam registradas como descartadas, não escolhidas por capricho.

## Identificação

| Campo | Preenchimento |
|---|---|
| Squad / Polo | *(preencher)* |
| Data | *(preencher — data do Encontro 1)* |
| Caso / Desafio | caso da Aroeira |
| Integrantes e papéis do dia (quem registra / quem apresenta) | *(preencher)* |

## 1. Hipótese(s) técnica(s)

| # | Abordagem | Condição (sob que circunstância) | Resultado esperado | Critério de teste |
|---|---|---|---|---|
| **H1** | Sinalizar risco elevado de falha nos próximos dias a partir de sinais de telemetria recentes (`temp_descarga_maxima`, `pressao_descarga_media`) comparados à linha de base do próprio equipamento | Restrita a equipamentos com telemetria (68% da frota) e às causas com sinal de alerta já identificado (`falha_valvula_admissao`, `falha_vedacao`) | O modelo sinaliza risco com antecedência útil para essas 2 causas; **não** se espera que funcione para as 3 causas mais frequentes (sem sinal de alerta nos dados) | Recall na detecção antecipada vs. taxa de falso alarme — **amostra pequena (5 e 11 casos)**, tratar como sinal preliminar, não validação definitiva |
| **H2** | Sistema de recuperação que, dado uma pergunta do técnico em campo, retorna os trechos mais relevantes do manual técnico e/ou do histórico de atendimentos anteriores do mesmo equipamento | Quando o técnico atende um equipamento já visitado por outro colega, ou precisa consultar um procedimento específico do manual | O técnico encontra a informação relevante mais rápido que no processo atual (busca manual no celular / ligar para colega — relato de Iran, C1-03) | Taxa de acerto do trecho recuperado (contém a informação certa) sobre um conjunto de perguntas-teste; comparar tempo até encontrar a informação, antes/depois |
| **H3** | **Workflow determinístico que compõe H1 + H2**: pipeline de 2 passos fixos — (1) checagem periódica do sinal de telemetria vs. linha de base do próprio equipamento (= H1); (2) se ultrapassar o limiar de alerta, aciona automaticamente a recuperação do procedimento relevante no manual + histórico do equipamento (= H2), e notifica o técnico | Restrita a equipamentos com telemetria e às causas com sinal validado (`falha_valvula_admissao`, `falha_vedacao`) — fora disso, o workflow fica inativo | O técnico chega no próximo atendimento já com o procedimento certo em mãos, antes de pedir — reduzindo a dor relatada por Iran (C1-03) nos casos em que o alerta é confiável | Precisão do gatilho (proporção de alertas que de fato antecedem corretiva real nessas 2 causas) + tempo economizado na consulta ao procedimento, vs. fluxo manual atual |

## 2. Justificativa (por que esta hipótese, e não um palpite)

> **H1** nasce do achado de que a telemetria mostra sinal de alerta (alta de temperatura de descarga, +7,95°C e +7,40°C acima da linha de base) especificamente para `falha_valvula_admissao`/`falha_vedacao`, e não para as demais causas — a hipótese é deliberadamente restrita a essas duas, não generalizada para toda a frota.
>
> **H2** nasce diretamente do relato de Iran (C1-03): a dor relatada não é "falta de inteligência artificial", é acesso a informação que já existe mas está espalhada/difícil de buscar — um recorte mais preciso do pedido original da diretoria (C0-05).
>
> **H3** não é uma terceira ideia solta: é H1 encadeada com H2, na mesma lógica do relato de Iran — "procurar o procedimento certo no meio do atendimento é ruim". Em vez de dois sistemas autônomos decidindo cada um por conta própria, o fluxo é sempre o mesmo e conhecido de antemão: verificar → se disparar, buscar e notificar. O "se disparar" é uma condição programada (limiar numérico), não uma interpretação aberta — por isso H3 é tratada como **composição de tarefas** dentro de um workflow, e não como um agente.

## 3. Este é um problema de X e não de Y?

| Hipótese | Evidência que distingue |
|---|---|
| **H1** | É problema de **classificação supervisionada em princípio**, mas a amostra positiva é escassa (5 e 11 casos) — isso aproxima a prática de **detecção de anomalia** (não supervisionado), que exige menos exemplos rotulados da classe rara. Não é regressão de vida útil restante: os dados não sustentam estimar "quantas horas até falhar" (número contínuo), só um sinal de alerta categórico. |
| **H2** | É problema de **recuperação**, não de **classificação** nem de **geração**: a resposta certa já existe literalmente no manual ou no histórico — queremos localizar o trecho existente, não prever uma categoria fechada nem sintetizar conteúdo novo. |
| **H3** | É problema de **workflow determinista**, não de **agente**: o caminho é fixo e conhecido de antemão (verificar → se disparar, buscar e notificar) — não há branching dinâmico dependente de interpretação a cada passo (critério central do módulo M2 para distinguir os dois). A recuperação (H2) é chamada num ponto específico do fluxo; não decide o que fazer em seguida. E não é uma tarefa única: é **composição de tarefas** (classificação do alerta + recuperação do procedimento), no mesmo sentido em que o M0 descreve RAG como composição de recuperação + geração — o workflow em si não tem tarefa própria, herda as de cada passo. |

## Tarefa e paradigma de cada hipótese (exigido pelo guia do aluno, além do template oficial)

| # | Tarefa (M0) | Paradigma (M0) | Observação |
|---|---|---|---|
| H1 | Classificação | Supervisionado em princípio, mas na prática beira **detecção de anomalia** | Amostra positiva escassa (5 e 11 casos) — poucos exemplos da classe rara favorece enquadrar como anomalia, não classificação supervisionada clássica |
| H2 | Recuperação | Auto-supervisionado | Embeddings pré-treinados (padrão RAG do M1) — não exige rotulagem manual de cada par pergunta-resposta |
| H3 | **Composição de tarefas** (classificação + recuperação) — o workflow em si não tem tarefa própria | Não se aplica ao workflow — herda os paradigmas de H1 (classificação/anomalia) e H2 (auto-supervisionado) | A ramificação (dispara ou não) é um limiar programado (determinístico), não uma decisão aprendida — distinção central do M2 entre workflow e agente |

## Critério de pronto (autoverificação do squad antes de avançar)

- [ ] Cada hipótese tem abordagem + condição + critério de teste
- [ ] A distinção "problema de X e não de Y" está feita com evidência
- [ ] Justificativa registrada

## Devolutiva do mentor (evidência → interpretação → próximo passo → prazo)

| Campo | Registro |
|---|---|
| Evidência observada | *(preenchido em sala)* |
| Interpretação técnica | *(preenchido em sala)* |
| Próximo passo | *(preenchido em sala)* |
| Prazo / momento de revisão | *(preenchido em sala)* |
