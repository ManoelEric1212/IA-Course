# Registro na Decisão Justificada do E2 (KIT-007), campo "Pontos de incerteza"

> A camada 3 (KIT-028) pede que o registro de qual célula caiu com qual informação vá neste campo. Acrescentar ao texto já entregue em 08/10, **sem apagar** o que estava lá.

## Camada 3

**C3-01 (jurídico, contestação do PG-0518):**
> Com a C3-01, nenhuma célula da Decisão caiu, porque a solução não decide cobertura de garantia e as duas saídas são explicáveis caso a caso: a resposta cita a OS e o manual; o alerta compara com a base do próprio equipamento. A exigência vira requisito: registrar de forma recuperável cada resposta, alerta e causa original e corrigida, o que o Canvas ainda não prevê.

**C3-02 (suprimentos, fornecedor novo da VS-212):**
> Com a C3-02, caiu na Matriz a aderência do alerta por telemetria. A estimativa de vedação/válvula da C2-01 foi tratada como taxa estável, mas 35 das 77 corretivas com VS-212 estão no trimestre do lote novo (`d3_ordens.pecas_trocadas`, `data_abertura`). Parte das falhas pode ser de fornecedor, o que a solução não resolve, e a base não tem campo de lote para separar as duas.

## Uso de IA (sugestão rejeitada)
> A ferramenta de IA sugeriu que "a proporção de preventivas vem caindo". Rejeitada: as preventivas são estáveis em número (316 → 340) e quem cresce são as corretivas (411 → 673) (`d3_ordens.tipo_ordem` por semestre).

Observação: o Mapa do E1 registrou como causa provável "a preventiva reduziu". Pela mesma contagem, essa célula do E1 **cai**: o que muda é o crescimento das corretivas, não a queda das preventivas.

## Revisão do critério do alerta (registrar ANTES de rodar o notebook)
> 15/10/2026: por orientação do articulador, o critério "Recall > 80% (C2-01)" foi substituído antes do teste pela precisão. Recall alto em falha rara se obtém alertando quase tudo, que é o risco "alarmes falsos que geram visitas desnecessárias" registrado na Matriz de Alternativas. Critério novo: precisão ≥ 0,50 com sensibilidade ≥ 0,30.

## Após o teste (opcional, como registro pós-teste)
> O teste confirmou a decisão. A premissa 3 (regra do Wagner) saiu fortalecida: as 69 ordens discordantes de VS-212/VA-118 são todas de causa genérica, e nenhuma tem causa específica errada. A incerteza "revalidação das bases de OS por um engenheiro" ficou dimensionada em 69 ordens nessas duas peças.
