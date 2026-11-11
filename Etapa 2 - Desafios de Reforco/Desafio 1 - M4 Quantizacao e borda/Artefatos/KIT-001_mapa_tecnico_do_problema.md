# Mapa Técnico do Problema (KIT-001): Desafio 1 · M4 Quantização e borda

> Preenchido pela squad **no Encontro 1**. **Não escolher tecnologia ainda**: o objetivo é entender o problema.
> As seções 1 a 5 são uma **proposta inicial** com base em `../Preparacao/01_leitura_dos_dados.md` e `../Preparacao/02_embasamento_pre_E1.md`. Levem para a discussão, contestem e reescrevam com as palavras de vocês (o apresentador é sorteado). Cada célula traz a **proveniência** entre parênteses.
> Siglas de proveniência: **SIT** = situação (`M4-C-situacao-v1.pdf` / README do desafio); **DADO** = `relatos_de_campo.csv`; **EMB-n** = achado n do embasamento pré-E1.

## Identificação

| Campo | Preenchimento |
|---|---|
| Squad / Polo | Squad 05 · UFC |
| Data | *(preencher: data do Encontro 1)* |
| Caso / Desafio | Desafio de reforço 1 · M4 Quantização e borda |
| Integrantes e papéis do dia (quem registra / quem apresenta) | *(preencher)* |

## 1. Problema técnico delimitado (raiz, não sintoma)

> Teste: se a frase começa com "comprar GPU" ou "usar IA para…", ainda é solução, e não problema.

**Enunciado (proposta):**

> O relato de campo precisa ser classificado em uma de 5 classes **no ponto de operação, sem conexão e em menos de 1 s**, para acionar a especialidade certa. O modelo atual, porém, só foi posto em operação em servidor com GPU, e não se sabe se ele, ou um substituto, atende a esse limite **no coletor que já existe** (8 GB, CPU, sem GPU) sem perder qualidade na classificação.

*(Passa no teste: não cita "comprar coletor com GPU", "quantizar" nem "TF-IDF". O pedido da TI é **uma** das soluções possíveis e vai para a seção 5.)*

## 2. Sintomas × Causas

| Sintomas observáveis | Causas prováveis |
|---|---|
| Plantas sem nuvem não recebem a classificação na hora (SIT) | O modelo atual (BERTimbau ajustado) depende de servidor com GPU. Com a conectividade não assumível, o edge vira o gatilho (M4, Aula 2) |
| TI pede coletores com GPU (SIT) | Pressupõe que o modelo **não roda** em CPU. **Não verificado:** a memória cabe com folga (pesos float32 = 415,5 MiB, ~5,4% dos 8 GB; EMB-1). O que falta saber é o **tempo** em CPU com 2 threads |
| Risco de acionar a especialidade errada (SIT: "a classe define a especialidade e as peças") | (1) Erro do modelo; (2) **rótulo ambíguo** em relatos com dois problemas: na base, 56 mistos segurança+elétrica estão divididos 29 `eletrica` × 27 `seguranca` (DADO, EMB-6); (3) **truncamento**: 73 relatos em caixa alta passam de 64 tokens, e 4 perdem a pista de segurança no corte (EMB-3, EMB-4) |
| Texto ruidoso no coletor (SIT) | Digitação no campo: abreviações (`mot.`, `bba`, `c/`), erros (`dsijuntor`, `bloqeuio`) e 19,5% dos relatos em CAIXA ALTA (DADO, EMB-3, EMB-5) |

## 3. Dados disponíveis e qualidade

| Dado | Disponível? | Qualidade | Observação |
|---|---|---|---|
| `relatos_de_campo.csv`: 3.000 relatos de jun/2026 (`id`, `data`, `equipamento`, `texto`, `classe`) | sim | **média** | Sintético. Textos curtos (13,4 palavras em média). Classes desbalanceadas, com `seguranca` = 10,6% (a menor e a mais cara de errar). 8 duplicados com o mesmo rótulo (DADO) |
| Rótulo (`classe`) | sim | **média** | Sem regra visível para relatos com dois problemas: os mistos segurança+elétrica dividem-se ~50/50 (EMB-6). Isso impõe um **teto de acurácia** abaixo de 100% para qualquer modelo |
| Texto (`texto`) | sim | **média** | 19,5% em caixa alta, com ~2× mais tokens no BERTimbau *cased* (47,5 × 24,8). 73 relatos (2,4%) passam de 64 tokens (EMB-3). Erros de digitação: 45 de 300 relatos da amostra têm palavra fora do vocabulário do treino (EMB-5) |
| Amostra de medição (300 do teste, semente 42) | sim | alta (reprodutível) | 89 / 69 / 56 / 47 / 39 por classe. 1 relato = 0,33 p.p. Só 1 texto idêntico ao treino, sem vazamento relevante (EMB, seção 5) |
| Especificação do coletor | sim | alta | 8 GB de RAM, sem GPU, < 1 s por relato, um relato por vez. O notebook simula com CPU e 2 threads (SIT) |
| Custo do coletor com GPU × tamanho da frota | **não** | n/a | Sem ele, não dá para calcular o custo total da alternativa da TI. É uma pergunta para o instrutor |
| Regra de prioridade em relato com dois problemas | **não** | n/a | Pergunta para o instrutor |

## 4. Restrições

| Dimensão | Conteúdo (proposta) |
|---|---|
| **Técnicas** | 8 GB de RAM (compartilhados com sistema e app de coleta); **sem GPU**; **sem conexão**; **< 1 s por relato**; classificação **um relato por vez** (não em lote); CPU com 2 threads (SIT). O notebook oficial fixa `max_length=64` e ONNX Runtime em CPU |
| **Éticas / segurança operacional** | A classe `seguranca` aciona a equipe de segurança. Classificar risco de segurança como `eletrica` é o **erro mais caro**, porque o eletricista vai sem a proteção adequada (SIT, DADO). Por isso a qualidade precisa ser vista em **F1 macro**, e não só em acurácia |
| **Operacionais (prazo, infraestrutura, orçamento)** | Desafio de 2 semanas com 2 encontros. Treino do BERTimbau exige GPU T4 do Colab (cota variável). A troca de hardware exige capex × frota, instalação, gestão e substituição de unidades. Caminhos de software reaproveitam o coletor atual (M4 Aula 2, seção 3: custo total, e não preço de compra) |

## 5. Oportunidades candidatas (sem juízo ainda)

> Listar ao menos duas, sem escolher. A escolha vem da medição na semana 2.

1. **Trocar o hardware:** comprar coletores com GPU (pedido da TI) e manter o modelo atual.
2. **Comprimir o modelo atual:** quantização dinâmica int8 do BERTimbau em ONNX Runtime, no coletor atual.
3. **Trocar por um modelo menor:** TF-IDF + regressão logística, no coletor atual.
4. *(Registrada para descarte com motivo)* **Manter o servidor e classificar quando houver conexão.** Fere o requisito "sem conexão, na hora".

## Critério de pronto (autoverificação da squad)

- [ ] Problema enunciado como raiz, não sintoma (o pedido de GPU ficou na seção 5)
- [ ] Sintomas e causas diferenciados
- [ ] Dados e qualidade registrados, com as lacunas (custo da frota, regra de prioridade)
- [ ] Restrições em pelo menos três dimensões
- [ ] Oportunidades como candidatas, sem escolha

## Devolutiva do instrutor (evidência → interpretação → próximo passo → prazo)

| Campo | Registro |
|---|---|
| Evidência observada | *(preenchido em sala)* |
| Interpretação técnica | *(preenchido em sala)* |
| Próximo passo | *(preenchido em sala)* |
| Prazo / momento de revisão | *(preenchido em sala)* |
