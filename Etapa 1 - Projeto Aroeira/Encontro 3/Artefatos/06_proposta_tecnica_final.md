# Proposta Técnica Final (KIT-015)

> O template KIT-015 não está na pasta; a estrutura segue a apresentação do E3. Integração dos artefatos do arco, **sem redação nova**: cada parte cita de onde veio.

## Identificação
| Campo | Preenchimento |
|---|---|
| Squad / Polo | Squad 5 - UFC |
| Data | 15/10/2026 |
| Caso / Desafio | Aroeira Equipamentos Industriais |
| Integrantes e papéis do dia | Registra: ______ · Apresenta: ______ |

## 1. Problema (1 frase, do Mapa Técnico do E1)
> O tempo médio de atendimento sobe e os chamados reincidem porque o técnico não tem acesso ao histórico do equipamento atendido por outro colega, e a causa registrada nas ordens não diz qual foi a falha (C0-05, C1-02, C1-03, C1-04; `d3_ordens`).

## 2. Abordagem escolhida e justificada (Decisão do E2, confirmada pelo teste)
> Workflow determinístico com **assistente conversacional somente leitura** que consulta o histórico das ordens de serviço, **com a causa corrigida pela peça**, e o manual da série CP (Alt. 2 da Matriz). Em paralelo, **alerta por telemetria para vedação e válvula** (Alt. 1), só registrando. Workflow, não agente: o caminho é fixo e a auditoria exige fonte citável.
>
> Justificativa: viabilidade no prazo e no orçamento de 90 dias (C2-02); aderência à reincidência ligada à troca de técnico (C1-03); auditoria e rastreabilidade por fontes citáveis (C0-04, C1-01), agora exigidas caso a caso pelo jurídico (C3-01). A Alt. 3 (workflow que cria OS) fica para depois do piloto.

## 3. Arquitetura (Canvas do E2, revisado no E3)
- **Entrada:** pergunta do técnico em texto livre; histórico de OS (`d3_ordens`); manual técnico digitalizado; telemetria diária (`d2_telemetria`).
- **Pré-processamento:** corrigir a causa registrada pela peça trocada, **sem sobrescrever a causa original**; segmentar o manual; limpar a telemetria.
- **Componentes:** consulta ao histórico; RAG no manual; chamada pontual de LLM; orquestração do workflow; alerta por telemetria em paralelo.
- **Saída:** resposta com referência ao equipamento, à OS e ao trecho do manual; alerta registrado.
- **Novo no E3, registro recuperável (C3-01):** para cada resposta e alerta, guardar a versão da regra ou modelo e do limiar, a janela de telemetria usada, a OS e o trecho citados, e a causa original e a corrigida.
- **O que tem prazo e o que é investigação:**
  - o dia 90 garante o assistente sobre o **histórico com causa corrigida** (D3 testado);
  - o **manual** entra como verificação com data e plano B (link para a seção do PDF), porque o squad não teve acesso ao arquivo (premissa 2).

## 4. Validação (Matriz de Teste e Matriz de Validação)
| Alternativa | Hipótese | Critério a priori | Método | Resultado |
|---|---|---|---|---|
| Alt. 1, alerta | A telemetria sinaliza a troca de VS-212/VA-118 sem gerar visita à toa | precisão ≥ 0,50 e sensibilidade ≥ 0,30 | Prático, caminho B (Random Forest, divisão temporal) | Sensibilidade de 0,603 com precisão de 0,50; prevalência de 0,088. **Sustenta**, mas continua em paralelo (lote novo no período de teste) |
| Alt. 2a, dados | A causa registrada esconde a falha e a peça corrige | discordância > 0,30 | Analítico, caminho C | 0,639, toda por causa genérica. **Correção pela peça é pré-requisito** |
| Alt. 2b, recuperação | O assistente responde com OS e seção certas, mais rápido | resposta rastreável, 90 dias sem treino | Conceitual | Atende por desenho; **taxa de acerto não medida** (manual indisponível) |

## 5. Uso pretendido e fora de escopo
> **Uso pretendido:** o técnico consultar histórico e manual durante o atendimento e ver alertas de vedação e válvula.
> **Fora de escopo:** servir de base para negar garantia; avaliar ou ranquear técnicos (`id_tecnico`); abrir OS ou pedir peça automaticamente no piloto.

## 6. Riscos e próximos passos
**Riscos** (Matriz de Validação):
- sinal do alerta misturado com falha do lote novo (C3-02);
- manual indisponível;
- falso alarme em operação real;
- regra peça → causa verificada só em duas peças;
- alucinação;
- frota sem telemetria fora do alerta.

**Próximos passos (residência):**
- revisar as 69 ordens com o engenheiro e estender a regra a outras peças;
- pedir campo de lote ou fornecedor em D3;
- obter o manual digital e medir a taxa de acerto e o tempo de busca (linha de base);
- rodar o alerta em paralelo até N trocas observadas, com a precisão e a sensibilidade declaradas;
- produzir plano de validação, matriz de avaliação contínua, runbook, model card e datasheet;
- caminho A (ciclo × ambiente) como pergunta aberta para a garantia.

## 7. Fechamento: volta ao problema do E1
> Com o histórico corrigido pela peça na mão, o técnico que chega a um equipamento atendido por outro colega sabe o que já foi feito e qual foi a falha real. É isso que ataca a reincidência e, com ela, o tempo médio do painel.

## Critério de pronto
- [x] Integra problema até validação de forma coerente
- [x] Arquitetura com referência ao Canvas
- [x] Validação com hipótese, critério, método e resultado
- [x] Riscos e próximos passos explícitos
- [x] Fecha com o problema do E1
