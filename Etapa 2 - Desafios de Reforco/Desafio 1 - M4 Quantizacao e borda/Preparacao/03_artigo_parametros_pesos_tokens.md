# O que acontece dentro do modelo quando o técnico digita um relato

### Parâmetros, pesos e tokens explicados com o nosso próprio dado, e por que essas contas decidem se precisamos ou não comprar GPU

*Leitura: ~15 minutos · Squad 05 UFC · Desafio 1 (M4) · Leia antes do glossário (`04_glossario_notebook_01.md`)*

---

Um técnico está ao lado de uma bomba numa planta sem internet. Ele pega o coletor e digita:

> **MOTOR ELETRICO COM CORRENTE ALTA**

Em menos de um segundo, o coletor precisa responder `eletrica` e acionar o eletricista. Parece mágica, mas por baixo é só aritmética: **muitas multiplicações e somas com números que o modelo aprendeu**. Esses números são os **parâmetros**, e é sobre eles (e sobre os **tokens**, a forma como o texto entra no modelo) que gira o nosso desafio.

Este texto começa com um modelo tão pequeno que dá para fazer à mão e termina no BERTimbau, com 109 milhões de números. No caminho fica claro por que a squad passa tanto tempo calculando bytes e contando tokens.

---

## 1. Um modelo que cabe num guardanapo

Esqueça redes neurais por um minuto. Imagine que a squad quer classificar relatos à mão, com uma regra de pontuação: cada palavra dá pontos para cada classe.

| Palavra | eletrica | mecanica | seguranca |
|---|---:|---:|---:|
| `corrente` | **+2,0** | 0,0 | 0,0 |
| `disjuntor` | **+2,5** | 0,0 | 0,0 |
| `rolamento` | 0,0 | **+2,5** | 0,0 |
| `guarda-corpo` | 0,0 | 0,0 | **+3,0** |
| `motor` | +0,5 | +0,5 | 0,0 |
| *ponto de partida* | +0,2 | +0,3 | −0,5 |

Chega o relato **"motor com corrente alta"**. Somamos os pontos das palavras que aparecem:

```
eletrica  = 0,2 + 0,5 (motor) + 2,0 (corrente) = 2,7   ← vence
mecanica  = 0,3 + 0,5 (motor)                  = 0,8
seguranca = −0,5                               = −0,5
```

Pronto: você acabou de rodar um **modelo de classificação**. Agora os nomes:

- Cada número da tabela que multiplica uma palavra (2,0, 2,5, 0,5...) é um **peso**. Ele diz **o quanto** aquela palavra puxa o relato para aquela classe.
- A linha "ponto de partida" é o **viés** (*bias*): um valor somado sempre, qualquer que seja o relato. O −0,5 da segurança diz algo como "na dúvida, não chute segurança".
- **Pesos + vieses = parâmetros.** São todos os números que definem o comportamento do modelo.
- Rodar o modelo num relato novo se chama **inferência**.

E o que é **treinar**? É deixar o computador **descobrir esses números sozinho**, olhando milhares de relatos já classificados. Ele começa com números aleatórios, erra, ajusta um pouquinho cada peso para errar menos e repete até a tabela ficar boa.

> **Detalhe que vai importar mais tarde:** quem escolhe *quantas* palavras entram na tabela, *quantas* vezes o treino passa pelos dados ou *quanto* cada ajuste mexe nos números somos nós. Esses são os **hiperparâmetros**. O modelo aprende **parâmetros**; nós escolhemos **hiperparâmetros**.

### Quantos parâmetros tem esse modelo?

Basta contar as células: **palavras × classes + um viés por classe**. Com 5 palavras e 3 classes, são 5 × 3 + 3 = **18 parâmetros**.

---

## 2. Do guardanapo ao caminho C (TF-IDF + regressão logística)

O caminho C do desafio é, na essência, **a mesma tabela**, só que maior e preenchida pelo treino:

- **TF-IDF** decide **quanto vale cada palavra** num relato. Palavra rara e específica (`disjuntor`) vale mais; palavra que aparece em todo relato (`com`, `do`) vale quase nada.
- **Regressão logística** é a tabela de pesos: uma linha por palavra, uma coluna por classe, mais os vieses.

No nosso dado, o vocabulário do treino tem **705 palavras** (contagem do embasamento) e há **5 classes**:

```
705 palavras × 5 classes + 5 vieses = 3.530 parâmetros
```

Três mil e quinhentos números. Cabe numa planilha.

**Uma consequência direta:** a tabela só tem linha para palavras que **apareceram no treino**. Se o técnico digitar `dsijuntor` (erro de digitação), não existe linha para essa palavra, e ela simplesmente **não conta**. No embasamento, 45 dos 300 relatos da amostra têm pelo menos uma palavra assim. Isso é o "risco do caminho C" no KIT-004.

---

## 3. E o BERTimbau? Onde estão os 109 milhões?

O BERTimbau não pontua palavra por palavra. Ele transforma cada pedaço do texto num **vetor de 768 números** e passa esses vetores por 12 camadas, cada uma "conversando" com as outras palavras da frase. É isso que permite entender que *"corrente"* em *"corrente alta"* é elétrica e, em *"corrente da esteira"*, é mecânica.

Cada uma dessas transformações é uma **matriz de pesos**. Somando todas, com os números exatos da configuração do modelo:

| Parte do modelo | Como se calcula | Parâmetros |
|---|---|---:|
| **Embeddings** (o "dicionário" de vetores) | 29.794 tokens × 768 + posições (512 × 768) + extras | 23.278.080 |
| **12 camadas** de atenção + rede interna | 7.087.872 por camada × 12 | 85.054.464 |
| *Pooler* (resumo final da frase) | 768 × 768 + 768 | 590.592 |
| **Total** | | **108.923.136** |

> No ajuste fino, o notebook 02 acrescenta só a "cabeça" de classificação: 768 × 5 + 5 = **3.845 parâmetros**. É praticamente a nossa tabela do guardanapo, colocada em cima de 109 milhões de números pré-treinados.

Para ter a escala:

| Modelo | Parâmetros | Comparação |
|---|---:|---|
| Guardanapo | 18 | |
| Caminho C (TF-IDF + RL) | ~3.530 | |
| BERTimbau (caminhos A e B) | ~108,9 milhões | **~31 mil vezes** o caminho C |
| Qwen2.5-1.5B (notebook 01, contraste) | ~1,5 bilhão | ~14 vezes o BERTimbau |

---

## 4. Por que gastar tempo calculando isso?

Porque **cada parâmetro é um número guardado em memória e usado numa conta**. Saber quantos são responde às duas perguntas do coletor: **cabe?** e **responde a tempo?**

### 4.1 Cabe? (memória)

Cada número ocupa um espaço que depende da **precisão** em que é guardado:

| Precisão | Bytes por número | BERTimbau inteiro |
|---|---:|---:|
| float32 | 4 | 108,9 M × 4 ≈ **436 MB** |
| float16 | 2 | ≈ 218 MB |
| int8 | 1 | ≈ **109 MB** |

O coletor tem 8 GB, e 436 MB são ~5%. **Cabe com folga, mesmo sem quantizar.** Esse cálculo de uma linha já enfraquece o argumento de "precisamos de GPU porque o modelo não cabe".

> É exatamente o que o `accelerate estimate-memory` faz no notebook 01: lê a configuração, conta os parâmetros e multiplica pelos bytes. Ele mostra 415,52 "MB" porque usa unidades binárias (MiB): 108.923.136 × 4 ÷ 1.048.576 ≈ 415,5. É a mesma conta (a diferença na segunda casa decimal vem de alguns poucos valores auxiliares que o modelo também guarda).

### 4.2 Responde a tempo? (contas)

Aqui está o ponto que muita gente perde: **caber não é responder rápido**. Cada token que entra no BERT passa por todas as matrizes das 12 camadas. Uma estimativa clássica é de **~2 operações por parâmetro, por token**:

```
BERTimbau, relato típico (26 tokens):
  2 × 85 milhões (parâmetros das camadas) × 26 tokens ≈ 4,4 bilhões de operações

Caminho C, relato típico (13 palavras):
  13 palavras × 5 classes ≈ 65 multiplicações
```

> ⚠️ **Isso é uma estimativa de ordem de grandeza, não uma medição.** O tempo real depende da CPU, do runtime (ONNX Runtime), das 2 threads e de vários outros fatores. **Quem mede é o notebook 02, depois do KIT-003.** A estimativa serve para entender *por que* a pergunta do desafio é sobre tempo, e não sobre memória.

Repare que a conta do BERT tem um fator **× tokens**. Então, quanto mais tokens o relato tem, mais caro ele fica. Isso nos leva à segunda metade da história.

---

## 5. Tokens: como o texto entra no modelo

O modelo não lê letras nem palavras. Ele lê **tokens**: pedaços de texto que estão no seu vocabulário fixo. O BERTimbau tem **29.794** tokens no vocabulário. O **tokenizador** corta o relato nesses pedaços e troca cada um pelo seu número de identificação (*id*).

Todos os exemplos abaixo são **reais**, rodados com o tokenizador do BERTimbau:

### 5.1 Uma frase comum

```
"Motor elétrico com corrente alta"
→ [CLS] Motor elétrico com corrente alta [SEP]           7 tokens
→ ids: 101 13485 11633 170 5820 2729 102
```

- `[CLS]` e `[SEP]` são **tokens especiais** que marcam o início e o fim. Todo relato ganha esses dois.
- Palavras comuns viram **um token só**.
- Os *ids* são só endereços: o id 5820 aponta para a linha da tabela de **embeddings** onde está o vetor de 768 números de "corrente". **É por isso que a tabela de embeddings tem 29.794 × 768 parâmetros**: uma linha por token do vocabulário.

### 5.2 A mesma frase, sem acento (como no nosso dado)

```
"motor eletrico com corrente alta"
→ [CLS] motor eletr ##ico com corrente alta [SEP]         8 tokens
```

O `##` quer dizer "continuação da palavra anterior". Como `eletrico` sem acento não está no vocabulário, o tokenizador o monta com dois pedaços conhecidos: `eletr` + `##ico`. **Mais um token**, só pela falta do acento.

### 5.3 A mesma frase, em CAIXA ALTA

```
"MOTOR ELETRICO COM CORRENTE ALTA"
→ [CLS] M ##O ##TO ##R E ##L ##ET ##RI ##CO CO ##M CO ##R ##RE ##NT ##E AL ##TA [SEP]
                                                          20 tokens
```

Por que isso acontece? O modelo é **cased**: aprendeu com maiúsculas e minúsculas diferentes, e textos inteiros em maiúsculas eram raros no material de pré-treino. "MOTOR" não está no vocabulário, então o tokenizador **quebra quase letra por letra**.

Resultado: **a mesma informação custa quase 3× mais tokens**. E, pela conta da seção 4.2, quase 3× mais operações. Além disso, os pedaços `M`, `##O`, `##TO` carregam muito menos significado que `motor`.

No nosso dado, **19,5% dos relatos estão em caixa alta**, com **47,5 tokens em média, contra 24,8** dos demais.

### 5.4 Erros de digitação e abreviações

```
"disjuntor desarmando na partida"   → dis ##junto ##r desar ##mando na partida        9 tokens
"dsijuntor desarmando na partida"   → d ##si ##junto ##r desar ##mando na partida    10 tokens
"bba c/ vazamento"                  → b ##ba c / vaz ##amento                          8 tokens
"guarda-corpo solto"                → guarda - corpo sol ##to                          7 tokens
```

Compare com o caminho C: para o TF-IDF, `dsijuntor` é uma palavra **desconhecida** e é ignorada. O BERT **não ignora**: monta a palavra com pedaços (`d ##si ##junto ##r`) e ainda consegue aproveitar o `##junto`. Essa é uma vantagem real do BERT sobre o TF-IDF com texto ruidoso, que será posta à prova na medição.

### 5.5 O limite de 64 tokens (truncamento)

O notebook 02 usa `max_length=64`: **o que passar de 64 tokens é cortado**. Num relato normal (~26 tokens), isso nunca acontece. Mas um relato longo em caixa alta pode chegar a **93 tokens**. No nosso dado:

- **73 relatos** passam de 64 tokens, todos em caixa alta;
- em **4** deles, o corte cai justamente em cima da pista de segurança. Um exemplo real da amostra:

> CABO DE ALIMENTACAO DO TALHA DA PONTE ROLANTE COM ISOLAMENTO DANIFICADO, ~~GUARDA-CORPO PERTO DO TALHA DA PONTE ROLANTE SOLTO~~

O BERT "lê" o isolamento danificado (elétrico) e **nunca vê o guarda-corpo** (segurança). Não é a quantização nem o modelo que erram aqui: é o **dado que entra cortado**.

### 5.6 Por que contar tokens, então?

| Porque... | Consequência no desafio |
|---|---|
| O custo do BERT cresce com o número de tokens | Relatos em caixa alta são mais lentos. A **média** de tempo esconde essa cauda |
| Existe um limite (64) | O que passa dele é cortado, e pode ser a parte importante |
| O vocabulário define a tabela de embeddings | 29.794 × 768 = a maior parte do modelo (~21%) |
| O TF-IDF conta **palavras**, não tokens | Ele não sofre com caixa alta (põe tudo em minúsculas), mas ignora palavras que nunca viu |

---

## 6. A ponte para a quantização

Agora o desafio fica simples de enunciar:

> O BERTimbau tem 108,9 milhões de parâmetros. Guardados em float32, ocupam 4 bytes cada. **Quantizar** é guardar cada um em **1 byte** (int8), com uma régua (a *escala*) para voltar ao valor aproximado.

O ganho é óbvio: ~4× menos espaço e contas mais baratas. A perda é sutil: cada peso é **arredondado** para uma das 255 marcas da régua. Se um único peso for muito grande, a régua fica esticada e os outros, pequenos, caem todos nas mesmas poucas marcas. No notebook 01, com um peso extremo plantado, a matriz passa a usar **14 marcas em vez de 238**, e **31% dos pesos viram zero**.

Os detalhes (escala, dequantização, quantização dinâmica) estão no **glossário** (`04_glossario_notebook_01.md`), que é a próxima leitura.

---

## 7. Para levar para o Encontro 1

1. **Parâmetros são os números que o modelo aprendeu.** Pesos multiplicam, vieses somam. Hiperparâmetros são escolhas nossas.
2. **Contar parâmetros responde "cabe?":** 108,9 M × 4 bytes ≈ 436 MB, ou ~5% do coletor. Memória não é o problema.
3. **Caber não é responder a tempo:** o custo do BERT é de bilhões de operações por relato e cresce com o número de tokens. Só a medição do notebook 02 diz se fica abaixo de 1 s.
4. **Tokens são o "pedágio" do texto:** caixa alta, falta de acento e erros de digitação aumentam o número de tokens; acima de 64, o relato é cortado.
5. **Os dois caminhos de software erram de jeitos diferentes:** o BERT sofre com caixa alta e truncamento, e o TF-IDF sofre com palavras que nunca viu. Por isso, na defesa, vale olhar os erros **por recorte**, e não só a média.

---

*Números deste texto: configuração oficial do `neuralmind/bert-base-portuguese-cased` (vocabulário 29.794, 768 dimensões, 12 camadas, rede interna 3.072), tokenizador rodado em 10/11/2026 e contagens do embasamento (`02_embasamento_pre_E1.md`). A estimativa de operações (2 × parâmetros × tokens) é uma aproximação, não uma medição de tempo.*
