# Encontro 3 — Testar, validar e defender ("A escolha se sustenta?")

> Fonte: `Projeto/Encontro 3/Documentos/2_Encontro3_Apresentacao_Industr.IA_v1.1.pptx.pdf` (APR-IND-PRD-2026-005 v1.1, apoio ao roteiro ROT-IND-PRD-2026-004). Polo UFC Sobral, Squad 05, **15/10/2026, 17:00–21:00**. Os templates KIT-011/012/015/016/021 e o notebook do teste ainda **não** estão na pasta. Estão no tópico "Encontro 3" da turma.

## As 5 entregas
| # | Instrumento | Quem | Conteúdo |
|---|---|---|---|
| 1 | Matriz de Teste | 2 sub-times → versão única | hipótese (a do E1, com o que a camada 3 mudou), evidência que confirma/refuta, forma de teste (conceitual/analítica/prática), **critério de sucesso antes de rodar**, caminho do notebook (A, B ou C, com motivo), resultado e limitações |
| 2 | Matriz de Validação | squad | critérios com métrica/evidência e resultado; riscos residuais; **ética, viés, privacidade e explicabilidade como critérios** |
| 3 | Proposta Técnica Final | squad | problema em 1 frase, abordagem, arquitetura (dados + validação, citando o Canvas), próximos passos/riscos/residência. **Integração, sem redação nova**; fecha com o problema do E1 |
| 4 | Roteiro de Pitch | squad | 30 s problema → 60 s abordagem → 60 s justificativa → 60 s validação, riscos e próximos passos (sem esconder risco). Defesa curta: a bancada pergunta o que a proposta **não** resolve; cada resposta aponta o artefato |
| 5 | Princípios transferíveis | squad | 3 a 5 regras: "Quando ___, decidimos ___, porque ___ (Encontro ___, artefato ___)" + o que fariam diferente |

Prontos: matrizes = critério antes do teste, resultado e limitações, riscos residuais, IA responsável como critério. Proposta = coerente do problema à validação, cita o Canvas, validação com hipótese/critério/método/resultado, riscos e próximos passos, fecha com o problema do E1.

## Regras do dia
- Proveniência inclui agora **qual saída do notebook** gerou cada número.
- 4 sorteios de defesa (Teste, Validação, Proposta, Pitch): sorteado justifica 2 células que não escreveu.
- Critério escrito depois do resultado não conta. Pergunta-guia: "que número, se não aparecer, faria vocês mudarem a decisão?"
- Registro de uso de IA continua nos pontos de incerteza da **Decisão Justificada** (sugestão, rejeição, motivo técnico).
- **3 perguntas**, só da Matriz de Teste até o intervalo. Não acumulam do E2.
- Corte de tempo, se necessário: cede a profundidade da Proposta. Não cedem os 50 min do notebook, os critérios de pronto das matrizes nem os sorteios.

## Agenda (relógio 17:00)
| Rel. | Fase |
|---|---|
| 00:00 | Abertura + camada 3; registrar **na Decisão Justificada do E2** qual célula caiu (C3-01/C3-02) ou "nenhuma, porque…" |
| 00:25 | Matriz de Teste 1ª parte (sub-times; perguntas abertas) |
| 00:50 | Critério a priori, versão única, caminho do notebook + sorteio |
| 01:15 | Intervalo (perguntas fecham) |
| 01:30 | Execução no notebook (Colab, seção 4: caminho e critério), 50 min |
| 02:20 | Resultado + Matriz de Validação |
| 02:50 | Fechamento das matrizes + sorteio |
| 03:00 | Proposta Técnica Final; 03:25 fechamento + sorteio |
| 03:30 | Pitch e defesa curta + sorteio |
| 03:45 | Princípios, devolutiva (evidência → interpretação → próximo passo → prazo), reflexão: "quando o teste mudou o que iam defender? o que ele não mostra?" |

## Camada 3 (C3)
- **C3-01, jurídico (Tereza):** cliente contestou judicialmente a negativa do **PG-0518** (OS-001537, EQ-0129, aberto 2026-06-15, R$ 16.811,33, motivo `uso_fora_de_especificacao`). Exigência que vira **requisito do produto**: toda decisão de cobertura apoiada em modelo precisa de explicação **caso a caso**, auditável, apresentável a terceiros e **registrada para recuperação posterior**. Explicação global (do conjunto) não serve. Tereza participa do E3.
- **C3-02, suprimentos:** a **VS-212** passou a vir de fornecedor novo; o lote entrou no **último trimestre** dos registros (jun–ago/2026). Não informa volume nem data por planta.

### Cruzamento com os dados (feito em 14/10/2026, para preparo)
- **OS-001537** = corretiva `causa_nao_identificada` que trocou **VS-212**. Pela regra do Wagner, seria `falha_vedacao`. EQ-0129: CP-75, PL-07, `metalurgia_leve`, `particulado_alto`, com telemetria, garantia desde 2025-12-13.
- Telemetria do EQ-0129: `temp_descarga_maxima` média de 100,7°C nos 7 dias antes (só 3 dias válidos) contra 96,2°C na base de 30–60 dias, **+4,5°C**, acima do limiar de 3°C: assinatura de vedação.
- Trocas de VS-212 por mês em d3: ~4,7/mês de set/25 a mai/26 (42 em 9 meses) → **15, 9, 11** em jun–ago/26 (35 em 3 meses), ~2,5×.
- Leitura: o histórico pós-lote mistura falha de operação com possível falha de lote. A regra peça → causa continua dizendo "vedação", mas não diz **por quê**, e a negativa por uso fora de especificação pode estar confundindo as duas. A folha de dados com as faixas do CP-75 não está no dossiê, então não dá para afirmar se houve uso fora de especificação.

## Impacto no Squad 5 (entregas do E2 em `entregaveis-e2-squad5.md`), revisado em 14/10/2026

### Dados que embasam (d3 + d2 + d4)
| Corretivas com VS-212 | Antes de jun/26 (9 meses) | Jun–ago/26 (3 meses) |
|---|---|---|
| Ordens | 42 | 35 |
| % das corretivas do período | 6,0% | 9,1% |
| Com telemetria válida, alta > 3°C | 20 de 21 (média +7,0°C) | **28 de 28** (média +6,7°C) |
| Negativas `uso_fora_de_especificacao` | 11 | 9 |

Leitura: o lote novo **aumenta a frequência** da falha de vedação, mas ela continua com a **mesma assinatura de temperatura**. A regra peça → causa e o alerta continuam identificando vedação. O que muda é a **causa raiz** (operação × lote) e a estabilidade da taxa. D3 não tem campo de lote nem fornecedor, e a C3-02 não dá data por planta.

### C3-01: nenhuma célula cai, mas surge um requisito
- A solução não decide cobertura. Workflow com fonte citada e limiar por equipamento são explicáveis caso a caso (ex.: EQ-0129, +4,5°C). A justificativa de auditoria da Decisão (C0-04, C1-01) **sai fortalecida**.
- Ficam **incompletas**: Canvas/saída (sem registro recuperável de resposta, alerta, causa original e corrigida) e Canvas/riscos (resposta ou alerta usado como base de negativa, pois a coordenação usa histórico e medição, C1-01). O pré-processamento não pode **sobrescrever** a causa original.
- Limita a evolução: H1 escrita como "ML supervisionada/classificação" só é aceitável com explicação por instância; o limiar atende direto.
- Contexto: 109 das 155 negativas por uso fora de especificação são em `particulado_alto`. Isso sugere decisão pelo ambiente (explicação de conjunto), que a C3-01 diz não atender. É inferência, não fato do dossiê.

### C3-02: cai parcialmente a leitura da camada 2
- **Cai:** Matriz, alerta por telemetria, aderência. A estimativa de ~92 vedação/válvula (C2-01) foi tratada como taxa estável, mas 35 das 77 corretivas com VS-212 estão no trimestre do lote novo. Parte do aumento de vedação é de fornecedor, que o assistente e o alerta não resolvem, só detectam.
- **Não cai:** premissa 3 da Decisão (regra do Wagner) como **identificação** de vedação; o sinal continua (28/28). Cai apenas se interpretada como "vedação = falha de operação".
- **Afeta o teste:** prevalência maior no fim do período muda precisão e falso alarme; o critério precisa ser estratificado antes e depois de jun/26.
- **Nova incerteza:** sem campo de lote em d3, não dá para separar falha de lote de falha de operação.
