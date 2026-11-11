# Embasamento antes do E1 (medido em 10/11/2026)

> **O que foi rodado:** as células do notebook de estudo (`01_estudo_memoria_e_precisao.ipynb`), o `accelerate estimate-memory` (que lê só a configuração, sem baixar pesos), o tokenizador do BERTimbau sobre os 3.000 relatos e a divisão treino/teste/amostra **idêntica** à do notebook 02 (80/20 estratificada, semente 42, amostra de 300).
> **O que NÃO foi rodado, de propósito:** nenhum modelo foi treinado, exportado, quantizado ou cronometrado. A comparação BERT float32 × int8 × TF-IDF responde à pergunta do desafio e só acontece **depois** de o KIT-003 ser entregue.
> **Como reproduzir:** os scripts e a saída completa estão em `analise/` (`embasamento.py`, `caixa_alta.py`, `saida_embasamento.txt`).

## Resumo em 6 achados

| # | Achado | Número | Muda o quê |
|---|---|---|---|
| 1 | Memória **não** é o gargalo | BERTimbau float32: **415,5 MiB** (~5,4% dos 8 GB); int8: **103,9 MiB** | Reforça que a decisão se dá no **tempo em CPU** e na **perda de qualidade**, e enfraquece o pedido de GPU (KIT-001) |
| 2 | Um peso extremo destrói a quantização de uma matriz | Escala sobe ~21×, erro médio sobe ~21×, **31% dos pesos viram zero**, de 238 para **14 níveis** usados | Explica *por que* a perda da int8 pode existir mesmo com o arquivo 4× menor (KIT-003, justificativa) |
| 3 | **73 relatos (2,4%) passam de 64 tokens e são truncados**, e **todos são de CAIXA ALTA** | Caixa alta = 19,5% dos relatos, com **47,5 tokens em média, contra 24,8** dos outros; maior relato = 93 tokens | **Corrige** a leitura anterior ("praticamente nada truncado"). Novo risco para os caminhos 1 e 2 (BERT), mas não para o TF-IDF |
| 4 | O truncamento pode **cortar a pista de segurança** | 4 relatos na base perdem "guarda-corpo" no corte, e **1 deles está na amostra de 300** | Incerteza registrada no KIT-003 e no KIT-004 |
| 5 | O TF-IDF vai encontrar palavras que nunca viu | **45 dos 300** relatos da amostra têm ≥1 palavra fora do vocabulário do treino (erros de digitação: `dsijuntor`, `bloqeuio`, `caldira`...), mas são só **1,3% das palavras** | Hipótese (c) é plausível, mas tem risco concreto e mensurável (KIT-004, risco do caminho C) |
| 6 | O rótulo de relatos mistos é ambíguo também na amostra | **5 mistos** segurança+elétrica na amostra (3 `eletrica`, 2 `seguranca`) e mais **6 com pista de segurança rotulados `eletrica`** | Até ~5 relatos (≈1,7 p.p.) da amostra têm rótulo "cara ou coroa": isso sustenta a tolerância de 2 p.p. no critério |

## 1. Memória (`accelerate estimate-memory`, etapa 4 do notebook 02)

| Modelo | float32 | float16 | int8 | int4 | Maior camada (float32) |
|---|---:|---:|---:|---:|---:|
| BERTimbau base | 415,52 MiB | 207,76 MiB | 103,88 MiB | 51,94 MiB | 88,81 MiB |
| Qwen2.5-1.5B-Instruct | 5,75 GiB | 2,88 GiB | 1,44 GiB | 736,1 MiB | 890,25 MiB |

- Em MB decimais (unidade do resto do notebook): BERTimbau float32 ≈ **436 MB**, int8 ≈ **109 MB**. A conta de padaria do passo a passo (0,44 GB / 0,11 GB) estava certa.
- A maior camada do BERTimbau é a **tabela de embeddings** (vocabulário de ~29,8 mil × 768). Sozinha, ela é ~21% do modelo.
- **Ressalva:** é o tamanho dos **pesos**. A RAM em execução inclui tokenizador, ONNX Runtime e ativações, e o notebook 02 mede o **arquivo** `.onnx`, não a RAM. Por isso o critério usa folga de 1/8 da memória.
- **Pergunta 4 do estudo:** o Qwen 1,5B em int4 (~736 MiB) **caberia** nos 8 GB. A memória, porém, não é a única medida: a situação exige **< 1 s por relato em CPU com 2 threads**, e um modelo generativo de 1,5 bi de pesos gera token a token. Caber não é responder a tempo.

## 2. Quantização linear de uma matriz 768×768 (células 5 e 7 do estudo)

| | Sem peso extremo | Com 1 peso = 5,0 |
|---|---:|---:|
| Bytes float32 → int8 | 2.359.296 → 589.824 (4×) | igual |
| Escala | 0,00183 | 0,03937 (**21×**) |
| Erro médio absoluto | 0,00046 | 0,00984 (**21×**) |
| Maior erro | 0,000917 (= escala/2) | ~escala/2 |
| Níveis int8 distintos usados | 238 | **14** |
| Pesos que viram 0 | n/d | **31%** |

**Respostas às perguntas do estudo (para a squad conferir e reescrever):**
1. *Quanto ocupa e quanto representa dos 8 GB?* ~436 MB em float32 (5,4%) e ~109 MB em int8 (1,4%).
2. *Por que a perda depende dos extremos?* A escala é `max|w|/127`. Um único peso grande estica a escala, e os demais, pequenos, caem em poucos níveis (14 em vez de 238), muitos deles em zero. O erro de **todos** cresce na mesma proporção da escala.
3. *O que não muda / o que pode mudar?* Não mudam a arquitetura, o número de pesos, o tokenizador nem as classes. Podem mudar a saída (logits) e, portanto, a classe prevista nos relatos que estão perto da fronteira, como os mistos (achado 6).
4. *Qwen 1,5B em int4?* Ver seção 1: cabe, mas a latência em CPU é a medida que decide.

## 3. Tokenização e truncamento (o achado novo)

O BERTimbau é **cased**: o vocabulário foi aprendido com maiúsculas e minúsculas. Texto em CAIXA ALTA quase não aparece no pré-treino, e o tokenizador o quebra em pedaços de 1 a 3 letras:

```
"TECNICO RELATA LINHA DE AR COMPRIMIDO..." →
['T','##EC','##N','##IC','##O','R','##EL','##AT','##A','L','##IN','##HA','DE','AR','CO','##MP',...]
```

| | Base (3.000) | Amostra (300) |
|---|---:|---:|
| Relatos em caixa alta | 584 (19,5%) | 58 (19,3%) |
| Tokens médios: caixa alta × normal | 47,5 × 24,8 | 47,9 × 26,0 |
| Relatos com > 64 tokens (truncados) | **73**, todos em caixa alta | **7**, todos em caixa alta |
| Truncados que perdem a pista de segurança no corte | 4 (3 `eletrica`, 1 `seguranca`) | **1** (`eletrica`) |

Exemplo que perde a pista na amostra: *"CABO DE ALIMENTACAO DO TALHA DA PONTE ROLANTE COM ISOLAMENTO DANIFICADO, GUARDA-CORPO PERTO DO TALHA DA PONTE ROLANTE SOLTO"*. O modelo BERT nunca "vê" o guarda-corpo.

Também se observam: tokens por relato com média 29,2, mediana 26, p95 55 e máximo 93; **fertilidade de 2,02 subtokens por palavra**. Erros de digitação viram subtokens (`cntator` → `c ##nta ##tor`), então o BERT não "desconhece" a palavra, mas a representação fica distante da palavra certa.

**O que isso muda (hipóteses, não conclusões):**
- **Para o BERT (caminhos 1 e 2):** a caixa alta é um **recorte provável de erro** (M3, error analysis por slices). A caixa alta está espalhada por todas as classes (13–23%), então não deve enviesar uma classe específica.
- **Para o TF-IDF (caminho C):** o `TfidfVectorizer` padrão põe tudo em minúsculas, então a caixa alta **não** o afeta.
- **Para a latência:** o tempo do BERT cresce com o número de tokens, e um relato em caixa alta tem ~2× mais tokens. A **média** de tempo esconde essa cauda. O truncamento em 64 tokens, porém, **limita o pior caso**: nenhum relato custa mais de 64 tokens.
- **O notebook é oficial e fixa `max_length=64`.** Não vamos alterá-lo. Isso vira **limitação registrada** e pergunta ao instrutor.

## 4. Vocabulário do TF-IDF (risco do caminho C)

- Vocabulário do treino (padrão do `TfidfVectorizer`, palavras ≥ 2 letras, minúsculas): **705 palavras**.
- Na amostra: **45 de 300 relatos** com ≥ 1 palavra desconhecida; **52 de 3.885 palavras (1,3%)**.
- Quase todas são **erros de digitação de palavras conhecidas**: `acoplaento`, `bloqeuio`, `dsijuntor`, `disuntor`, `caldira`, `compresosr`, `hdiraulica`, `isloamento`, `proteao`...
- Leitura: o TF-IDF ignora essas palavras, mas o resto do relato (média de 13 palavras) costuma bastar. O risco é quando a palavra-chave da classe é justamente a que está errada (`bloqeuio` → segurança). **Hipótese (c) segue em aberto**, mas agora com o recorte de risco nomeado.

## 5. Amostra de medição: os números exatos

A amostra de 300 tem distribuição um pouco diferente da estimada no passo a passo:

| Classe | Estimado (proporcional) | **Real na amostra** |
|---|---:|---:|
| eletrica | ~90 | **89** |
| mecanica | ~84 | **69** |
| hidraulica | ~50 | **56** |
| instrumentacao | ~44 | **47** |
| seguranca | ~32 | **39** |

- Cada relato vale **0,33 p.p.** de acurácia. Em `seguranca`, cada erro vale **~2,6 p.p. de recall**, o que é ruidoso demais para virar critério isolado, mas é bom de **olhar** na defesa.
- **Vazamento:** só 1 texto da amostra aparece idêntico no treino. É desprezível.
- **Relatos mistos na amostra:** 5 segurança+elétrica (3 `eletrica`, 2 `seguranca`) + 6 com pista de segurança rotulados `eletrica`. Lista completa em `analise/saida_embasamento.txt`.

## 6. Duas coisas do notebook 02 que o critério precisa considerar

1. **A tabela da etapa 9 calcula só `perda_de_acuracia`.** A perda de **F1 macro** está no critério, mas não vira coluna. Ela precisa ser calculada à mão (`f1_macro` da referência float32 menos o da linha) e citada na conclusão.
2. **A coluna `cabe_no_coletor` usa `tamanho_mb < 8000` e `ms < 1000`.** O nosso critério é mais exigente (≤ 1.000 MB). `cabe_no_coletor = True` **não** significa "atendeu ao critério da squad". Isso deve ficar claro na KIT-011 (E2).

## Situação das hipóteses do rascunho

| Hipótese | Antes | Depois do embasamento |
|---|---|---|
| Memória não é o gargalo | conta de padaria | **confirmada** (415,5 MiB / 103,9 MiB) |
| (a) BERT float32 não cabe no tempo em CPU | hipótese | **em aberto**: só a etapa 7 do notebook mede |
| (b) int8 perde pouca acurácia | hipótese | **em aberto**, com mecanismo de perda entendido (seção 2) e recorte de risco nomeado (caixa alta) |
| (c) TF-IDF chega perto do BERT | hipótese | **em aberto**, com risco nomeado (45/300 relatos com palavra desconhecida) e vantagem nomeada (imune à caixa alta) |
| (d) rótulo inconsistente em mistos | achado | **confirmado na amostra** (5 + 6 relatos), além do novo efeito do truncamento |

## Perguntas novas para o instrutor (além das do passo a passo)

1. Existe regra de prioridade quando o relato tem dois problemas (por exemplo, segurança sempre prevalece)?
2. O truncamento em 64 tokens (73 relatos, todos em caixa alta) é intencional? Podemos registrar como limitação sem mexer no notebook?
3. O critério pode incluir a perda de F1 macro calculada à mão, se a etapa 9 só calcula a perda de acurácia?
4. Vale medir o p95 da latência, além da média? Se não, registramos a média como limitação.
