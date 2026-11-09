# Decisão Justificada (KIT-007) — ESBOÇO, já com a camada 2

> O template diz "Encontro 3", mas neste arco é feito no Encontro 2. A escolha precisa **citar as células da Matriz**.

**Identificação:** Squad 5 – UFC · Data: __/10/2026 · Caso: caso da Aroeira · Registra: Rhuan Nunes · Apresenta: Isac

## 1. Abordagem escolhida
**Assistente conversacional em fases, com motor em workflow (não agente).**
- **No dia 90 (em operação):** o técnico consulta, em linguagem natural, o histórico do equipamento e o manual. O sistema responde citando a OS e a seção do manual. Antes de entrar no histórico, a causa de cada ordem é **corrigida pela peça trocada** (VS-212 → vedação, VA-118 → válvula). (Matriz A1)
- **No dia 90 (modo sombra):** alerta de alta de temperatura para vedação e válvula nos equipamentos com telemetria, só registrado, sem gerar visita. (Matriz A2)
- **Depois:** abrir OS e pedir peça pela conversa (Matriz A3), condicionado à medição do piloto.

## 2. Justificativa (critérios que pesaram)
- **Viabilidade no prazo** (Matriz, viabilidade; C2-02): a A1 não exige treino nem integração de escrita e cabe em 90 dias. A A3 não cabe.
- **Aderência** (Matriz, aderência): a A1 ataca a troca de técnico. 93% das visitas consecutivas mudam de técnico, e 67 de 70 reincidências rápidas envolvem troca (`d3_ordens.id_tecnico`, C1-03).
- **Evidência nova** (C2-01): vedação e válvula são ~92 corretivas, não 23, e todas têm assinatura de temperatura (41 de 43 > 3°C). Por isso a A2 entra já no piloto, em sombra.
- **Auditoria** (Matriz, explicabilidade; T2.1): a OS alimenta a garantia (C0-04, C1-01). Um workflow com fonte citada é auditável, um laço agêntico não é.
- **Custo aceito:** no dia 90 o assistente **não** abre OS nem pede peça, embora isso esteja no pedido original. A verba continua atendida, porque o produto **é** o assistente conversacional (C2-02), entregue na fase que a evidência sustenta.

## 3. Premissas assumidas
1. A diretoria aceita um piloto somente leitura como "assistente conversacional" (C2-02). *A confirmar com o Nelson.*
2. O manual da série CP existe em formato digital indexável (C1-03).
3. A regra peça→causa do Wagner vale para todas as genéricas, e não só para as 60 revisadas (C2-01).
4. O técnico tem conexão ao abrir a OS (antes do deslocamento).
5. Menos reincidência → menos corretivas → indicador do painel menor (C1-02).

## 4. Pontos de incerteza
- **Célula do Encontro 1 que caiu (C2-01):** Hipótese §3/H1. Justificamos detecção de anomalia por haver "5 e 11 casos positivos", mas a revisão do Wagner mostrou 23 de 60 genéricas reclassificadas para vedação/válvula. Pela mesma regra, os eventos sobem de 23 para ~92, com a mesma assinatura de temperatura. O argumento da raridade caiu.
  - Também caíram: Mapa §3 (qualidade de Ordens "Alta") e Mapa §2 (reincidência medida por `causa_registrada`).
- **Célula que ficou incompleta (C2-02):** Mapa §4, restrições operacionais, que não registrava prazo nem orçamento. Agora há 90 dias e verba atrelada ao assistente conversacional.
- **Sugestão de IA recebida e rejeitada:** a "Sugestão IA" do Mapa do E1 dizia que "a proporção de preventivas vem caindo" e explicava o problema por isso. **Rejeitada:** as preventivas são estáveis em número (316 → 340), e quem cresce são as corretivas (411 → 673) (`d3_ordens.tipo_ordem` por semestre).
- 16 ordens de `contaminacao_particulado` trocaram VS-212. Podem ser vedação mal registrada, mas a revisão não cobriu causas específicas.
- Falso alarme da A2 (~6–8% nos grupos sem sinal no histórico) ainda não medido em operação.
- Disponibilidade do manual para teste.

**Critério de pronto:** ☐ escolha vinculada à Matriz · ☐ premissas · ☐ incertezas (com a célula que caiu e a sugestão de IA rejeitada)
