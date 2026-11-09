# Hipótese Técnica (KIT-003) — versão 2, revisada para o Encontro 2

> ⚠ **Camada 2:** o argumento da H1, "poucos casos positivos (7 e 12) → detecção de anomalia", **cai com a C2-01**: os casos reais são ~92. **Não corrijam isso aqui em silêncio.** A queda deve ser registrada na Decisão Justificada (ver `06_camada2_impacto.md`). Este arquivo corrige só os erros que já existiam antes da camada 2.

> Copiar para o docx do KIT-003 e subir na pasta da turma. Os **[MUDOU]** explicam cada alteração e devem ser apagados antes de copiar.

**Identificação:** Squad 5 – UFC · Data: 01/10/2026 (revisado em __/10/2026) · Caso: caso da Aroeira · Escrita: Rhuan Nunes · Apresenta: Manoel Eric · Pasta: Rhuan Nunes

## 1. Hipóteses técnicas

| # | Abordagem | Condição (sob que circunstância) | Resultado esperado | Critério de teste |
|---|---|---|---|---|
| **H1** | Detecção de anomalia na telemetria. **Tarefa:** detecção de anomalia (classificação binária normal/alerta). **Paradigma:** não supervisionado, aprendendo o "normal" de cada equipamento. | Equipamento **com telemetria** e falhas de desgaste gradual: `falha_valvula_admissao` e `falha_vedacao` | Alerta de alta de `temp_descarga_maxima` dias antes da corretiva, permitindo antecipá-la como preventiva | Nos eventos históricos dessas 2 causas, alerta com ≥3 dias de antecedência em ≥ 60% dos casos, com ≤ 1 falso alarme por equipamento a cada 30 dias |
| **H2a** | Consulta estruturada do histórico por `id_equipamento`. **Não é IA**: é uma consulta a banco. | Equipamento que já teve ordem anterior, atendida por **outro técnico** | Técnico chega sabendo as últimas ordens: causa, peças trocadas, relato | 100% das visitas com ordem anterior exibem as 3 últimas ordens. O efeito esperado é a queda da reincidência de mesma causa em ≤30 dias, cuja linha de base é 70 em 905 pares (7,7%). |
| **H2b** | RAG sobre o manual da série CP. **Tarefa:** recuperação. **Paradigma:** auto-supervisionado (embeddings pré-treinados). | Técnico precisa de um procedimento durante o atendimento | Trecho certo do manual em segundos, com citação da seção | Num conjunto de perguntas por causa (10 causas), o trecho correto aparece entre os 3 primeiros em ≥ 80% das perguntas (recall@3 ≥ 0,8) |
| **H3** | Workflow com chamada pontual de modelo, compondo H2a + H2b (e H1 onde houver telemetria). **Tarefa:** composição de tarefas, **não** agente. | Abertura de uma OS corretiva | Ao abrir a OS, o técnico recebe histórico + procedimento + alerta (se houver) | Fluxo executa sem decisão em tempo de execução. O efeito medido é a reincidência das 3 causas principais, cuja linha de base é 65 casos em ≤30 dias. |

**[MUDOU]**
- **H1:** a tabela dizia "classificação supervisionada", mas a seção 3 concluía "detecção de anomalia", então a tabela foi alinhada. A condição agora inclui as 2 causas. "Reduzir reincidências" saiu, porque a telemetria não avisa as 3 causas que reincidem. "Recall > 80%" foi trocado por um critério com antecedência e falso alarme: com 7 e 12 casos, um recall sozinho não diz nada.
- **H2** foi dividida em duas. Histórico é consulta, manual é recuperação. São dois problemas diferentes.
- **H3:** "reduzir tempo de atendimento corretivo" saiu, porque a duração da corretiva é estável e o problema é o volume.
- Todos os critérios agora têm **número e linha de base**, o que é exigido no E3: o critério é fixado antes do teste.

## 2. Justificativa (por que esta hipótese, e não um palpite)
- **H1:** nos 7 dias antes de uma corretiva, `temp_descarga_maxima` sobe ~+7,9°C (válvula, n=5) e ~+7,4°C (vedação, n=11) sobre a linha de base. Para `falha_eletrica`, `vazamento_oleo` e `contaminacao_particulado` o delta é ≈ 0,1–0,3°C, sem sinal (`d2_telemetria.temp_descarga_maxima` × `d3_ordens.causa_registrada`). O escopo é pequeno: 23 de 1084 corretivas.
- **H2a/H2b:** Iran diz que perde tempo por não saber o que o colega fez e por não achar o procedimento no manual (C1-03). Os dados confirmam: em 93% das visitas consecutivas ao mesmo equipamento o técnico é outro, e 67 das 70 reincidências rápidas foram atendidas por um técnico diferente do anterior (`d3_ordens.id_tecnico`).
- **H3:** surge da composição de H1 e H2. O fluxo é sempre o mesmo, então não há o que um agente decida (T2.1 do M2).

## 3. Este é um problema de X e não de Y?
- **H1 é detecção de anomalia, e não classificação supervisionada**, porque há só 7 e 12 positivos, poucos para treinar e validar um classificador. Também **não é regressão de vida útil**: não há rótulo de "tempo até a falha", só o sinal de alerta.
- **H2a é consulta, e não IA:** a resposta é um filtro exato por `id_equipamento`, e não há o que inferir.
- **H2b é recuperação, e não geração:** a resposta já existe no manual. O sistema deve devolver o trecho com a fonte, e não redigir um procedimento novo, o que traria risco de alucinação (T1.2).
- **H3 é workflow, e não agente:** o caminho é fixo (OS aberta → busca histórico → busca manual → alerta se houver). Nenhum passo depende de interpretação para escolher o próximo (branching dinâmico baixo, T2.1).

**Critério de pronto:** ☑ abordagem + condição + critério de teste · ☑ X e não Y com evidência · ☑ justificativa
