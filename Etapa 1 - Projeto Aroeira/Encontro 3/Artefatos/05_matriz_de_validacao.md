# Template: Matriz de Validação (KIT-012)

> Kit de formação | Testar a hipótese e refinar. Preenchida depois da Matriz de Teste. Consolida o que o teste produziu, não o status desejado. IA responsável entra como critério.

## Identificação
| Campo | Preenchimento |
|---|---|
| Squad / Polo | Squad 5 - UFC |
| Data | 15/10/2026 |
| Caso / Desafio | Aroeira Equipamentos Industriais |
| Integrantes e papéis do dia | Registra: ______ · Apresenta: ______ |

## 1. Matriz de validação
Cada critério herda de um eixo da Matriz de Alternativas do E2 ou da Decisão. Risco classificado como técnico, ético ou operacional.

| Critério de validação | Métrica ou evidência | Resultado ou status | Risco associado |
|---|---|---|---|
| **Aderência técnica, Alt. 1** (Matriz E2: aderência "média") | Precisão dos alertas ≥ 0,50 contra a prevalência, com sensibilidade ≥ 0,30 (caminho B) | **Atende:** sensibilidade de 0,603 com precisão de 0,50; prevalência de 0,088; precisão média de 0,477 [nº da saída] | **Técnico:** o sinal pode ser do lote novo da VS-212, e não de operação (C3-02) |
| **Aderência técnica, Alt. 2** (Matriz E2: aderência "alta") | Taxa de acerto e precisão da recuperação (OS e seção certas) | **Não testado:** manual não disponibilizado | **Técnico:** alucinação da LLM e busca errônea (Matriz e Canvas) |
| **Qualidade dos dados, Alt. 2** (Matriz E2: "necessita da causa corrigida pela peça") | Taxa de discordância causa × peça (caminho C) | **Atende ao critério de intervenção:** 0,639 (69 de 108 ordens), 100% causa genérica; a regra peça → causa cobre todos os casos discordantes [nº da saída] | **Técnico:** verificado só em duas peças; D3 sem campo de lote ou fornecedor |
| **Explicabilidade** (Matriz E2: explicabilidade "alta" nas duas alternativas; C3-01) | Cada alerta mostra a temperatura sobre a base do próprio equipamento; cada resposta cita OS e seção do manual; registro recuperável de saída, causa original e corrigida | **Parcial:** explicável caso a caso por desenho; o registro recuperável foi acrescentado ao Canvas hoje e ainda não existe | **Ético/operacional:** saída usada como base para negar garantia (fora de escopo) |
| **Vieses e privacidade** | Cobertura: equipamentos sem telemetria (`d1_frota.tem_telemetria`); `id_tecnico` só como contato, nunca para ranquear (C0-09) | **Atende com ressalva:** o assistente cobre toda a frota; o alerta só os equipamentos com telemetria | **Ético:** cobertura desigual do alerta; `id_tecnico` é dado pessoal (LGPD) |
| **Viabilidade** (Matriz E2: Alt. 1 "média/alta", depende da rede do cliente; Alt. 2 "alta") | Prazo e verba de 90 dias (C2-02); manual digital disponível; rede do cliente (C0-03) | **Atende para o histórico; pendente para o manual** (resposta da empresa: ______) | **Operacional:** manual não verificado; alerta depende da rede |

## 2. Riscos residuais (técnicos, éticos e operacionais)
Quem aceita cada risco e sob qual condição. Nomes propostos pelo squad, a confirmar com o mentor.

| Risco residual | Tipo | Quem aceita (C0-12) | Sob qual condição |
|---|---|---|---|
| Falha de lote misturada com falha de operação no sinal do alerta | Técnico | Nelson, com suprimentos | Enquanto o alerta for só em paralelo; reabre se as trocas de VS-212 seguirem acima da base ou se surgir campo de lote |
| Manual indisponível | Operacional | Nelson | O dia 90 entrega só o histórico; o manual entra quando houver arquivo (plano B: link para a seção do PDF) |
| Falso alarme em operação real (o teste usou histórico) | Técnico | Wagner | Alerta em paralelo até N trocas observadas com precisão ≥ 0,50 e sensibilidade ≥ 0,30 |
| Regra peça → causa verificada só em VS-212/VA-118 | Técnico | Wagner | Revisar as 69 ordens e uma amostra de outras peças antes do piloto |
| Alucinação da LLM na resposta | Técnico | Nelson | Resposta sem fonte citada não é exibida |
| Frota sem telemetria fora do alerta | Ético | Nelson | O assistente de histórico cobre 100% da frota; o alerta não |
| Saída usada como base de negativa de garantia | Ético | Tereza / Cristiane | Uso fora de escopo declarado na Proposta; registro recuperável de cada saída |

## Critério de pronto
- [x] Validação consolida critérios, riscos e métricas
- [x] Riscos residuais explícitos
- [x] IA responsável tratada como critério (explicabilidade, vieses e privacidade)

## Devolutiva do mentor (evidência → interpretação → próximo passo → prazo)
_______________________________________________
