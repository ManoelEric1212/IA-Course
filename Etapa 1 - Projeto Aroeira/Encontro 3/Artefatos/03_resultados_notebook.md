# Resultados do notebook KIT-023 (teste de decisão)

> Rodado em sala em 15/10/2026, no Colab da turma, com `SEED = 42`. Dados D1–D4 do caso. Peças sob suspeita: `VS-212` (vedação) e `VA-118` (válvula de admissão).
> Trocar `[nº da saída]` pelo número da saída no notebook.

## Seção 3: recorte comum
- Período das ordens: 2025-09-01 a 2026-08-31.
- Ordens que trocaram peça sob suspeita: **108**, todas corretivas.
- Dessas, **43 em jun–ago/26**, o trimestre do lote novo da VS-212 (C3-02).

## Seção 4: escolha do caminho e critério (escrito ANTES de rodar)
> **Caminho escolhido:** B, e C em seguida.
> **Por que este:** B testa a Alt. 1 da Matriz do E2 (alerta por telemetria para vedação e válvula) pelo risco que registramos, o falso alarme. C testa o dado que a Alt. 2 (assistente) exige, a causa corrigida pela peça. Abrimos mão do A, que mede ciclo × ambiente e responde à pergunta da garantia, não à nossa.
> **Critério declarado:** B: precisão ≥ 0,50 com sensibilidade ≥ 0,30. Por orientação do articulador, substituímos o "Recall > 80%" do E2 pela precisão, porque recall alto em falha rara se consegue alertando quase tudo. C: taxa de discordância limite de 0,30.

---

## Caminho B, preditivo → Alt. 1 (alerta por telemetria)

### O que executou
1. **Janelas:** para cada equipamento com telemetria, recortes de **30 dias** que andam de **7 em 7 dias**. Cada janela resume o que se sabia no fim dela (temperatura máxima média, pico de temperatura, ciclo médio, pressão média). Recebe rótulo **1** se VS-212 ou VA-118 foi trocada nos **30 dias seguintes**, e **0** se não.
2. **Divisão temporal:** primeiros 70% das janelas no tempo para treino, últimos 30% para teste. O modelo aprende com o passado e é avaliado num período que nunca viu.
3. **Modelo:** Random Forest de referência, com 200 árvores de decisão votando. `class_weight="balanced"` dá peso extra às janelas com troca, porque elas são raras. A saída é um escore de 0 a 1 por janela.
4. **Ponto de corte:** `sensibilidade_na_precisao` testou todos os cortes e achou o que captura mais janelas com troca mantendo **pelo menos metade dos alertas corretos**.
5. **Teste de sanidade:** recusa campos que só existem depois do evento (`..._no_horizonte`), para evitar vazamento.

Atributos escolhidos: `["temp_maxima_media", "temp_maxima_pico", "ciclo_medio", "pressao_media"]`. A temperatura é o sinal apontado pela C2-01.

### Critério (passo A)
`precisao_fixada = 0.50`, `sensibilidade_minima_declarada = 0.30`

### Saídas obtidas [nº da saída]
| Medida | Valor |
|---|---|
| Prevalência no teste (janelas com troca) | **0,088** |
| Janelas positivas no teste | **126** |
| Sensibilidade com precisão ≥ 0,50 | **0,603** (76 de 126 janelas positivas) |
| Precisão média (área da curva precisão × sensibilidade) | **0,477** |
| Decisão do notebook | **sustenta** |

Atenção: **janelas não são trocas.** Como as janelas andam de 7 em 7 dias e o horizonte é de 30 dias, a mesma troca aparece como positiva em várias janelas seguidas. Nunca escrever "76 trocas".

### Leitura
- A precisão de 0,50 é cerca de **5,7 vezes a prevalência**: um alerta por sorteio acertaria 1 em 11; este acerta 1 em 2.
- A precisão média de 0,477 é cerca de **5,4 vezes a prevalência**: o sinal existe em toda a curva, não só num corte favorável.
- O B prova que **a telemetria tem informação** para antecipar a troca. Não é o alerta de produção: é o teste de que o sinal existe.

### Resposta da célula (seção 8)
> **O que o teste mostrou:** com precisão ≥ 0,50, o alerta capturou 60,3% das janelas positivas do período de teste (76 de 126), com prevalência de 0,088. A precisão média foi 0,477, cerca de 5,4 vezes a prevalência. Pelo critério declarado antes (precisão ≥ 0,50, sensibilidade ≥ 0,30), a Alt. 1 se sustenta.
> **O que isso muda:** a telemetria tem sinal para antecipar a troca de VS-212/VA-118. Na Matriz de Validação entra a precisão, não a acurácia, porque a falha é rara. O alerta continua em paralelo, só registrando (Canvas), até cumprir o critério de entrada; ganha força como próximo passo depois do dia 90.
> **Limite do resultado:** as janelas se sobrepõem, então 126 positivos não são 126 trocas; o período de teste cai em boa parte no trimestre do lote novo da VS-212 (C3-02), e o sinal pode refletir falha de lote; o ponto de corte foi escolhido no próprio teste, o que é otimista; só equipamentos com telemetria; o rótulo é "trocou a peça", não "falhou por vedação"; a versão por limiar ("iniciar sem ML", Matriz) não foi medida.

---

## Caminho C, sobre dados → Alt. 2a (dados do assistente)

### O que executou
**Sem modelo.** É uma auditoria de rótulo (dimensão "acurácia" do framework de data quality, M3). A mesma OS descreve a falha duas vezes: na `causa_registrada` (lista fechada preenchida pelo técnico) e em `pecas_trocadas` (apontamento de material).
1. Selecionou as 108 ordens de VS-212/VA-118.
2. Definiu as causas compatíveis com cada peça:
   - VS-212 → `falha_vedacao` ou `contaminacao_particulado`;
   - VA-118 → `falha_valvula_admissao` ou `contaminacao_particulado`.
3. Contou as ordens cuja causa registrada não está na lista da peça trocada.
4. Mostrou uma amostra de 20 ordens com o relato do técnico, para leitura humana.

### Critério (passo A)
`taxa_discordancia_limite = 0.30`

### Saídas obtidas [nº da saída]
| Medida | Valor |
|---|---|
| Ordens de VS-212/VA-118 | 108 |
| Taxa de discordância | **0,639** (69 ordens) |
| Decisão do notebook | **intervir nos dados** |
| Discordantes com causa genérica | **69** |
| Discordantes com causa específica incompatível | **0** |
| VS-212 | 77 ordens, discordância 0,636 |
| VA-118 | 31 ordens, discordância 0,645 |
| Antes de jun/26 | 65 ordens, discordância 0,631 |
| Jun–ago/26 (lote novo) | 43 ordens, discordância 0,651 |
| Causa genérica nas peças suspeitas | **0,639** |
| Causa genérica nas demais corretivas | **0,139** |

O recorte por peça e por período foi leitura complementar, feito depois do critério. Não foi critério de decisão.

### Leitura
- **Intervir nos dados**, com folga: 0,639 é mais que o dobro do limite.
- **Toda a discordância é causa genérica.** O técnico não registra a falha errada; registra uma causa vaga, e a peça preenche. É exatamente o que a regra do Wagner corrige: **a premissa 3 da Decisão sai fortalecida**.
- **Estável** entre as peças e antes/depois do lote novo: o problema é do registro, não do lote.
- **Concentrado nas falhas que importam:** causa genérica cerca de **4,6 vezes** mais frequente nessas peças que nas demais corretivas. É o argumento do M3: corrigir o dado antes do modelo.
- Não confundir com a C2-01: os 38% do Wagner são das ordens **genéricas** que eram vedação/válvula pela peça; os 64% de hoje são das ordens **dessas peças** que têm causa genérica.

### Resposta da célula (seção 10)
> **O que o teste mostrou:** 63,9% das 108 ordens de VS-212/VA-118 (69 ordens) têm causa registrada incompatível com a peça, todas por causa genérica. A taxa é estável entre as peças e antes/depois de jun/26, e a causa genérica é 4,6 vezes mais comum nessas peças que nas demais corretivas (0,639 contra 0,139). Pelo critério declarado (> 0,30), a decisão é intervir nos dados.
> **O que isso muda:** a correção pela peça é pré-requisito do assistente (Alt. 2) e entra no cronograma antes da consulta ao histórico. A revalidação pelo engenheiro, incerteza da Matriz e da Decisão, fica dimensionada em 69 ordens nessas duas peças.
> **Limite do resultado:** só duas peças; o cálculo não diz se a peça trocada era a causa real da falha; o relato do técnico foi lido em apenas 20 ordens.

---

## Caminho A, analítico (não rodado)
Compararia a taxa de falha por equipamento-ano entre grupos de ciclo de trabalho × classe de ambiente, com intervalo por reamostragem dos equipamentos. Responde "ambiente com muito particulado falha mais?", que é a pergunta da negativa por uso fora de especificação (C3-01), não a nossa. Fica como próximo passo para a garantia.

## Resumo

| | Caminho B | Caminho C |
|---|---|---|
| Alternativa (Matriz E2) | Alt. 1, alerta por telemetria | Alt. 2, assistente (dado que ele usa) |
| Modelo | Random Forest | Nenhum (contagem e comparação) |
| Forma de teste (KIT-011) | Prática | Analítica |
| Pergunta | O sinal para prever existe? | O rótulo que vamos consultar é confiável? |
| Critério a priori | precisão ≥ 0,50 e sensibilidade ≥ 0,30 | discordância > 0,30 |
| Resultado | sensibilidade 0,603; precisão média 0,477 (prevalência 0,088) | discordância 0,639, 100% genérica |
| Decisão | sustenta | intervir nos dados |
