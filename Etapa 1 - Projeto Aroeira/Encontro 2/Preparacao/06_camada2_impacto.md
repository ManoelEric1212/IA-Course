# Camada 2 (KIT-027): o que ela muda e quais células caem

> A camada 2 traz duas informações (C2-01 e C2-02). Este arquivo explica **o que cada uma significa**, **quais células do Encontro 1 caem** e **o que muda na solução**. As contas foram refeitas por nós sobre `d3_ordens.csv` e `d2_telemetria.csv`, porque o anexo do Wagner veio sem totais, de propósito: totalizar é trabalho do squad.

---

## C2-01 — Revisão do Wagner: a causa registrada pelo técnico está errada com frequência

**O que ele fez:** pegou as corretivas com causa genérica (`causa_nao_identificada`, `corretiva_geral` e `desgaste_natural`, 205 ordens no total), sorteou 60 e comparou a causa registrada com a peça trocada. A regra que ele usou:
- trocou **VS-212** (conjunto de vedação) → era `falha_vedacao`
- trocou **VA-118** (válvula de admissão) → era `falha_valvula_admissao`
- outras peças → `inconclusiva`

**Totalizando o anexo (60 ordens):**

| Revisão | Ordens | % |
|---|---|---|
| reclassificada para `falha_vedacao` | 17 | 28% |
| reclassificada para `falha_valvula_admissao` | 6 | 10% |
| inconclusiva | 37 | 62% |

> **38% das ordens "genéricas" do lote eram, na verdade, vedação ou válvula.** A seleção é reproduzível: `random.seed(20260917)` + `random.sample` sobre as 205 ordens ordenadas por `id_ordem` gera exatamente o lote do anexo.

**Extrapolando para as 205 ordens genéricas** (aplicando a mesma regra peça → causa às 145 que o Wagner não revisou; isso é **cálculo nosso**, não do Wagner):

| Causa | Registrada pelo técnico | Escondida nas genéricas | Total estimado |
|---|---|---|---|
| `falha_vedacao` | 16 | +49 | **65** |
| `falha_valvula_admissao` | 7 | +20 | **27** |
| **Soma** | **23** (2% das corretivas) | **+69** | **92** (8,5% das corretivas) |

**E a telemetria confirma.** A temperatura máxima de descarga sobe nos 7 dias antes da falha, em comparação com a média de 30 a 60 dias antes:

| Grupo | Eventos com telemetria válida | Alta média | Eventos com alta > 3°C |
|---|---|---|---|
| vedação registrada | 11 | +7,3°C | 11 de 11 |
| válvula registrada | 5 | +7,8°C | 5 de 5 |
| **vedação escondida (reclassificada)** | **32** | **+6,7°C** | **31 de 32** |
| **válvula escondida (reclassificada)** | **11** | **+6,5°C** | **10 de 11** |
| inconclusivas | 84 | +0,1°C | 7 de 84 |
| `falha_eletrica` (comparação) | 177 | +0,1°C | 11 de 177 |

Conclusão: as falhas reclassificadas **têm a mesma assinatura** de temperatura das registradas corretamente. O sinal é real e os eventos são **~4× mais numerosos** do que pensávamos (de 16 para ~59 com telemetria).

**Achado extra (incerteza, fora do recorte do Wagner):** 16 ordens registradas como `contaminacao_particulado` trocaram VS-212. Pela mesma regra, seriam vedação. A revisão não cobriu causas específicas, então isso fica como pergunta.

---

## C2-02 — Comunicado da diretoria: verba e prazo
- A verba está aprovada **para o assistente conversacional do pedido original** (C0-05).
- O **piloto deve ser entregue em 90 dias**, e esse prazo é compromisso com a direção geral.
- O plano precisa dizer **o que estará em operação no dia 90 e o que fica para depois**.

O que isso significa:
- Rejeitar o assistente conversacional por completo deixa o projeto **sem verba**. A saída é mostrar que **"assistente conversacional" é a interface**, e que por trás dela o motor continua sendo um workflow (T2.1). As ações de escrita (abrir OS, pedir peça) ficam para depois dos 90 dias.
- O prazo vira **restrição operacional**: 90 dias corta qualquer alternativa que exija treinar modelo com dado que ainda não existe ou integrar com sistemas de escrita.

---

## Quais células do Encontro 1 caem (registrar na Decisão Justificada, campo 4)

> Usem a versão **entregue** no E1 (pasta `Encontro 1/entregaveis1`). É ela que o mentor tem.

| # | Instrumento → célula | O que estava escrito | Caiu com | Por quê |
|---|---|---|---|---|
| **1** ⭐ | **Hipótese, §3, H1** ("problema de X e não de Y") | "temos poucos casos positivos (5 e 11 casos). Por isso… fica mais próximo de uma detecção de anomalia" | **C2-01** | Os positivos estavam **sub-registrados**: há ~92 eventos (~59 com telemetria), não 16. O argumento "poucos casos → anomalia, e não classificação" perde a base. **É a célula principal a registrar.** |
| 2 | **Mapa, §3, Ordens de serviço** | Qualidade **"Alta"** | **C2-01** | 38% das causas genéricas revisadas estavam erradas. `causa_registrada` não é confiável como rótulo. |
| 3 | **Mapa, §2, Reincidência → causa** | Reincidência medida pela repetição de `causa_registrada` | **C2-01** | Se a causa está errada, a contagem de reincidência por causa está **subestimada** (vedação e válvula escondidas sob rótulos genéricos). |
| 4 | **Mapa, §4, Restrições operacionais** | Equipe de 14 técnicos; proporção corretiva × preventiva (sem prazo e sem verba) | **C2-02** | O campo pede "prazo, infraestrutura, orçamento". Agora existe **prazo de 90 dias** e **verba atrelada ao assistente conversacional**. |
| 5 | **Hipótese, §1, H1, critério de teste** | Recall > 80% | **C2-01** (efeito colateral) | Com rótulos errados, o recall medido sobre `causa_registrada` seria falso. O teste precisa usar a causa **corrigida pela peça**. |

Texto pronto para o campo de incerteza (1 frase por célula):
> **Célula que caiu (C2-01):** Hipótese §3/H1. Justificamos detecção de anomalia por haver "5 e 11 casos positivos", mas a revisão do Wagner mostrou que 23 de 60 ordens genéricas eram vedação/válvula. Aplicando a mesma regra peça→causa, os eventos sobem de 23 para ~92, e a telemetria das reclassificadas tem o mesmo sinal (+6,6°C, 41 de 43 > 3°C). O argumento da raridade caiu.

---

## O que muda na solução

| Antes da camada 2 | Depois da camada 2 |
|---|---|
| A2 (telemetria) cobria ~2% das corretivas e ficava para "futuro" | A2 cobre **~8,5%**, com sinal forte e confirmado. Sobe de prioridade. |
| `causa_registrada` usada como verdade | **Pré-processamento obrigatório:** corrigir a causa pela peça trocada (regra do Wagner). Isso é **regra determinística, não modelo**. |
| A3 (assistente agêntico) rejeitada | Reenquadrada: **interface conversacional somente leitura** em 90 dias; abrir OS e pedir peça **depois** (C2-02) |
| Histórico mostrava a causa registrada | Histórico mostra **peças trocadas + causa corrigida**, porque a causa registrada engana (C2-01) |
| 1 tarefa de ML incerta | Para vedação/válvula, um **limiar simples de temperatura** já separa bem (41 de 43 > 3°C, contra 7 de 84 nas inconclusivas). Talvez não precise de ML, e isso vira um bom "X e não Y". |
