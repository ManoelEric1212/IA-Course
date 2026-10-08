# Dossiê do caso — Camada 2 (KIT-027)

> Fonte: `Projeto/Encontro 2/Documentos/KIT-027_camada_02.pdf`. Liberada na **abertura do Encontro 2**. Códigos `C2-01` e `C2-02`. As camadas 0 e 1 continuam valendo. O registro de qual célula do E1 caiu vai no campo de pontos de incerteza da Decisão Justificada (KIT-007).

## C2-01. Revisão manual de ordens pelo engenheiro de campo (Wagner)
- **Recorte:** corretivas com causa genérica (`causa_nao_identificada`, `corretiva_geral`, `desgaste_natural`), 205 ordens em d3.
- **Lote:** 60 ordens sorteadas. É reproduzível com `random.seed(20260917); random.sample(sorted_por_id_ordem, 60)` (conferido: bate com o anexo).
- **Regra usada:** peça trocada VS-212 → `falha_vedacao`; VA-118 → `falha_valvula_admissao`; outras peças → `inconclusiva` (sem causa nova).
- **Totais (o anexo vem sem totais, de propósito):** 17 vedação, 6 válvula, 37 inconclusivas. **38% das genéricas eram vedação/válvula.**
- **Extrapolação pela mesma regra às 205** (cálculo do squad, não do Wagner): +49 vedação, +20 válvula. Vedação + válvula passam de 23 para **~92** corretivas (~8,5%).
- **Telemetria confirma:** as reclassificadas têm a mesma assinatura das registradas, com alta média de `temp_descarga_maxima` de +6,5 a 6,7°C nos 7 dias antes, contra a média de 30 a 60 dias antes. 41 de 43 ficam acima de 3°C. Nas inconclusivas, +0,1°C (7 de 84 acima de 3°C).
- **Fora do recorte:** 16 corretivas `contaminacao_particulado` trocaram VS-212 (possível rótulo errado, não revisado).

## C2-02. Comunicado da diretoria: prazo e verba
Verba aprovada **para o assistente conversacional do pedido original** (C0-05). Piloto em **90 dias** a partir da aprovação do plano, como compromisso com a direção geral. O plano deve dizer **o que estará em operação no dia 90 e o que fica para depois**.

## Células do E1 que caem (Squad 5)
- **Hipótese §3/H1:** "poucos casos positivos (5 e 11) → detecção de anomalia". Os positivos estavam sub-registrados (C2-01). **É a principal.**
- **Mapa §3:** qualidade de Ordens "Alta" (C2-01).
- **Mapa §2:** reincidência medida por `causa_registrada` (C2-01).
- **Mapa §4:** restrições operacionais sem prazo e sem verba (C2-02).

Análise completa e esboços: `Projeto/Encontro 2/Preparacao/` (arquivo `06_camada2_impacto.md`).
