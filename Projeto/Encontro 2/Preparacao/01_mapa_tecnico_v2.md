# Mapa Técnico do Problema (KIT-001) — versão 2, revisada para o Encontro 2

> Copiar para o docx do KIT-001 e subir na pasta da turma. Em **[MUDOU]**: o que foi alterado em relação à versão entregue no E1 e por quê. Apagar essas marcações antes de copiar.

**Frase de abertura do Encontro 2 (o problema em 1 frase, para falar em voz alta):**
> As ordens corretivas cresceram 64% de um semestre para o outro enquanto as preventivas ficaram estáveis, e boa parte disso é a mesma falha voltando no mesmo equipamento, atendida por um técnico que não sabe o que foi feito na visita anterior.

---

**Identificação:** Squad 5 – UFC · Data: 01/10/2026 (revisado em __/10/2026) · Caso: caso da Aroeira · Registra: Rhuan Nunes · Apresenta: Manoel Eric

## 1. Problema técnico delimitado (raiz, não sintoma)

> O volume de ordens **corretivas** cresceu de 411 (set/25–fev/26) para 673 (mar–ago/26), +64%, enquanto as **preventivas** ficaram estáveis (316 → 340). Como a corretiva dura mais que a preventiva, esse aumento puxa para cima o tempo médio do painel (C1-02; `d3_ordens.tipo_ordem`, `d3_ordens.duracao_horas`). Parte desse aumento é **reincidência**: a mesma causa volta no mesmo equipamento em até 30 dias (70 casos, 65 deles em `falha_eletrica`, `vazamento_oleo` e `contaminacao_particulado`). Em 93% das visitas consecutivas ao mesmo equipamento o técnico é outro, sem acesso ao que foi feito antes (C1-03, C1-04; `d3_ordens.id_equipamento`, `data_abertura`, `causa_registrada`, `id_tecnico`).

**[MUDOU]**
- Ficou um enunciado só. A "Nossa formulação" era uma lista de sintomas, e a "Sugestão IA" dizia que as preventivas caíam, o que os dados não confirmam: elas caíram só em proporção.
- Entrou o número que liga a reincidência à troca de técnico.

## 2. Sintomas × Causas

| Sintomas observáveis | Causas prováveis |
|---|---|
| Tempo médio de atendimento subindo no painel (C0-05, C1-02; `d3_ordens.duracao_horas`) | Aumento do **volume de corretivas** (+64%) com preventivas estáveis. A duração de cada tipo de ordem não mudou (corretiva ~5,6–6,1h; preventiva ~2,4–2,6h), então o que muda é o mix (`d3_ordens.tipo_ordem`). |
| Reincidência de chamados no mesmo equipamento (C0-05, C1-04; `d3_ordens.causa_registrada`) | O reparo não elimina a causa: 70 repetições da mesma causa em ≤30 dias, concentradas em 3 causas. O registro é pobre: a causa vem de lista fechada (C0-02), e 126 de 1084 corretivas estão como `corretiva_geral` ou `causa_nao_identificada`. O padrão não é sistematizado (C1-04). |
| Técnico chega sem saber o que já foi feito; procurar no manual é difícil (C1-03) | O histórico existe (`d3_ordens.pecas_trocadas`, `relato_tecnico`), mas não está acessível em campo. O técnico muda em 93% das visitas consecutivas (`d3_ordens.id_tecnico`). O manual é um documento único, extenso e não indexado (C1-03). |
| "Entraram técnicos sem experiência na série CP" (C0-05) | **Não sustentado pelos dados:** os 14 técnicos aparecem desde o 1º mês (`d3_ordens.id_tecnico`). Fica registrado como sintoma relatado e não confirmado. |

**[MUDOU]**
- A linha da reincidência repetia o sintoma como causa.
- Entrou a justificativa 2 da diretoria (técnicos novos), que antes estava escondida em "restrições".

## 3. Dados disponíveis e qualidade

| Dado | Disponível? | Qualidade | Observação |
|---|---|---|---|
| Frota (C0-07; d1) | Sim | Alta | 184 equipamentos, sem campos vazios. `ano_instalacao` bate com `data_inicio_garantia` em todos. Só 126 (68%) têm telemetria (`d1_frota.tem_telemetria`). |
| Telemetria diária (C0-08; d2) | Parcial | Média | Só para equipamentos com módulo. Há dias com `transmissao_incompleta=1` (6 campos vazios) e séries curtas de equipamentos instalados no período (C0-08). O envio depende da rede do cliente (C0-03). |
| Ordens de serviço (C0-09; d3) | Sim | Média | Estrutura completa, mas `causa_registrada` é lista fechada escolhida às pressas (C1-04): 12% das corretivas estão em causa genérica. `relato_tecnico` é curto (~66 caracteres), genérico e às vezes não bate com a causa marcada. |
| Pedidos de garantia (C0-10; d4) | Sim | Média | Só existe sobre ordem corretiva, e 34% das corretivas não têm pedido. 243 negativas, 155 delas por `uso_fora_de_especificacao`, cláusula que inclui a **qualidade do ar aspirado** (C1-01). |
| Manual técnico da série CP (C1-03) | **Não** (para o squad) | — | Existe para os técnicos, mas não foi disponibilizado como dado. É lacuna para qualquer abordagem que dependa dele. |

**[MUDOU]**
- "Inconsistências" na Frota foi removido: não há nenhuma.
- A qualidade das Ordens caiu de Alta para Média.
- O código das Ordens passou de CO-02 para C0-09.
- O manual entrou como dado ausente.

## 4. Restrições
- **Técnicas:** telemetria em só 68% da frota e dependente da rede do cliente (C0-03, C0-08); manual indisponível para o squad e não indexado (C1-03); histórico de texto curto e pouco informativo (`d3_ordens.relato_tecnico`).
- **Éticas / regulatórias:** decisões de garantia têm efeito contratual. Qualquer saída usada como evidência de garantia precisa ser auditável (C0-04, C1-01). Os dados operacionais da planta pertencem ao cliente (C0-03). `id_tecnico` não deve virar ferramenta de avaliação individual de técnicos.
- **Operacionais:** uso em campo, no celular, durante o atendimento (C1-03); equipe fixa de 14 técnicos (`d3_ordens.id_tecnico`); análise de garantia com prazo de 30 dias (C1-01).

**[MUDOU]** "Proporção de corretivas" saiu daqui, porque é causa e não restrição. A restrição ética foi ampliada.

## 5. Oportunidades candidatas de IA (sem juízo)
- Detecção de anomalia na telemetria para antecipar falhas
- Recuperação (RAG) sobre o manual e o histórico de ordens
- Consulta estruturada do histórico do equipamento (não é IA, mas é candidata a solução)
- Apoio ao diagnóstico de causa
- Assistente conversacional agêntico que abre OS e pede peça (pedido original, C0-05)

**Critério de pronto:** ☑ raiz, não sintoma · ☑ sintomas × causas · ☑ dados e qualidade · ☑ restrições em 3 dimensões · ☑ oportunidades sem escolha
