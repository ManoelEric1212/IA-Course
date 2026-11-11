# Matriz de Alternativas (KIT-004): Desafio 1 · M4 Quantização e borda

> Preenchido pela squad **no Encontro 1**. Cada célula traz: **avaliação + justificativa curta + proveniência + [referência do curso]**.
> Nenhuma célula traz número **medido de modelo**: tempo e qualidade de B e C só existem depois do notebook 02. Onde a célula diz "medir", é de propósito.
> Proveniência: **SIT** = situação; **EMB-n** = `../Preparacao/02_embasamento_pre_E1.md`; **M4-An** = aula do M4 (`Edge_AI/`).

## Identificação

| Campo | Preenchimento |
|---|---|
| Squad / Polo | Squad 05 · UFC |
| Data | *(preencher: data do Encontro 1)* |
| Caso / Desafio | Desafio de reforço 1 · M4 Quantização e borda |
| Integrantes e papéis do dia (quem registra / quem apresenta) | *(preencher)* |

## 1. Comparação de alternativas

### A. Comprar coletores com GPU (pedido da TI) e manter o modelo atual

| Critério | Avaliação |
|---|---|
| **Aderência ao problema** | **Alta tecnicamente, baixa como decisão.** Resolve o tempo de resposta por força bruta, mas parte de uma premissa não verificada: a de que o modelo não roda em CPU. A memória não é o problema (415,5 MiB de 8 GB; EMB-1) |
| **Dados necessários** | Os de hoje. Falta o **custo por coletor × tamanho da frota** para comparar o custo total (pergunta ao instrutor) |
| **Viabilidade** | **Baixa no prazo:** depende de compra, logística e substituição em campo. [M4-A2 seção 3: custo total de propriedade, e não preço de compra] |
| **Riscos** | Capex sem necessidade, se B ou C atenderem. A GPU embarcada traz consumo, calor e gestão de frota. A qualidade continua com os mesmos problemas de dado (mistos e truncamento; EMB-3, EMB-6) |
| **Explicab. / TRL** | Igual à de hoje. TRL alto para o modelo, mas o hardware novo em campo não foi validado |

### B. Quantizar o BERTimbau (ONNX Runtime, int8 dinâmica)

| Critério | Avaliação |
|---|---|
| **Aderência ao problema** | **Alta.** Mantém o modelo e o pipeline de treino, roda no coletor atual e reduz os pesos ~4× (103,9 MiB; EMB-1). [M4-A1: compressão e runtimes] |
| **Dados necessários** | Os de hoje e nenhum novo treino. A quantização dinâmica não precisa de dado de calibração |
| **Viabilidade** | **Alta:** uma chamada (`quantize_dynamic`) depois da exportação ONNX. **Tempo em CPU: medir** (etapa 8) |
| **Riscos** | **Perda de qualidade concentrada** nos relatos de fronteira (mistos) e nas classes pequenas, porque um peso extremo reduz os níveis úteis (238 → 14 no estudo; EMB-2). Herdam-se os problemas do BERT *cased*: caixa alta com 2× mais tokens e 7 relatos da amostra truncados, 1 deles perdendo a pista de segurança (EMB-3, EMB-4) |
| **Explicab. / TRL** | Igual à do modelo atual (BERT, caixa-preta). TRL 4–5: técnica madura, falta medir neste dado |

### C. Trocar por TF-IDF + regressão logística

| Critério | Avaliação |
|---|---|
| **Aderência ao problema** | **Alta, se a qualidade aguentar.** Modelo muito pequeno e rápido, imune à caixa alta (põe tudo em minúsculas; EMB-3). Já usado no M0 |
| **Dados necessários** | Os de hoje. Retreino barato, que pode até acontecer no próprio coletor |
| **Viabilidade** | **Muito alta:** treina em segundos, sem GPU. **Tempo e qualidade: medir** (etapa 6) |
| **Riscos** | **Não reconhece palavra que não viu:** 45 de 300 relatos da amostra têm palavra fora do vocabulário, quase sempre erro de digitação da palavra-chave (`bloqeuio`, `dsijuntor`; EMB-5). Não entende ordem nem contexto: em relato misto, o peso das palavras decide sozinho. Abreviações novas do campo exigem retreino |
| **Explicab. / TRL** | **Mais alta das três:** os pesos por palavra mostram por que a classe foi escolhida (útil para contestar um acionamento). TRL alto |

### D. Manter o servidor e classificar quando houver conexão

| Critério | Avaliação |
|---|---|
| **Aderência ao problema** | **Descartada.** Fere o requisito "sem conexão, na hora" (SIT): o técnico precisa da classe para acionar a especialidade naquele momento |

## 2. Abordagem recomendada + pontos de incerteza

**Recomendação (antes da medição):** **não decidir pela compra (A) antes de medir B e C**, porque a premissa da compra (o modelo não roda em CPU) não se sustenta na memória e não foi testada no tempo. A ordem de preferência, **se ambos atenderem ao critério do KIT-003**, é:
1. **C**, se atender: menor custo, menor tempo, mais explicável e imune à caixa alta;
2. **B**, se C falhar na qualidade: preserva o modelo atual;
3. **A** só se B **e** C falharem, e com o custo total na mesa.

> A squad pode discordar dessa ordem (por exemplo, preferir B por manter a qualidade do modelo atual). Se discordar, registrar aqui o motivo, e não apagar a ordem acima.

**Pontos de incerteza:**
1. Tempo em CPU de H0/B/C: não medido (notebook 02, etapas 6 a 8).
2. Regra de prioridade em relatos com dois problemas: pergunta ao instrutor (EMB-6).
3. Truncamento em 64 tokens: afeta B, mas não C (EMB-3).
4. Custo do coletor com GPU × frota: sem dado.
5. Média × p95 da latência, e arquivo × RAM em execução.

## Critério de pronto (autoverificação da squad)

- [ ] ≥ 2 alternativas avaliadas em todas as dimensões
- [ ] Cada célula com justificativa e proveniência
- [ ] Recomendação + incertezas
- [ ] Nenhum número de modelo "chutado" no lugar do que será medido

## Devolutiva do instrutor (evidência → interpretação → próximo passo → prazo)

| Campo | Registro |
|---|---|
| Evidência observada | *(preenchido em sala)* |
| Interpretação técnica | *(preenchido em sala)* |
| Próximo passo | *(preenchido em sala)* |
| Prazo / momento de revisão | *(preenchido em sala)* |
