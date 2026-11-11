# Guia de termos do notebook 01 (memória e precisão)

> **Para quem:** toda a squad, antes de abrir o `01_estudo_memoria_e_precisao.ipynb` e antes do E1.
> **Por que importa:** no E2 o apresentador é **sorteado**. Qualquer pessoa pode ter de explicar o que é um peso, por que o int8 ocupa 4× menos ou de onde vem a perda da quantização.
> **Leia antes:** `03_artigo_parametros_pesos_tokens.md`, que explica com exemplos o que são parâmetros, pesos e tokens. Este glossário é a consulta rápida.
> **Como usar:** leia as seções 1 a 4 (cerca de 20 min), confira a seção 6 com o notebook aberto e faça o quiz da seção 8 em dupla.
> **Fontes:** o próprio notebook 01, o glossário oficial do M4 (`Edge_AI/GLOSSÁRIO.pdf`, citado como **[Gloss. M4]**) e os números que rodamos em 10/11 (`02_embasamento_pre_E1.md`).

---

## 1. A ideia em uma imagem

Um modelo treinado é **uma receita + uma tabela de números**:

```
              MODELO
   ┌─────────────────────────────┐
   │  Arquitetura (a receita)     │  quais contas fazer e em que ordem
   │  = grafo de operações        │  ex.: "multiplique por esta matriz, some, aplique ativação..."
   ├─────────────────────────────┤
   │  Pesos (a tabela de números) │  ~109 milhões de números no BERTimbau,
   │  = parâmetros aprendidos     │  aprendidos no treino
   └─────────────────────────────┘
```

- **Treinar** é ajustar os números da tabela.
- **Quantizar** é guardar esses mesmos números com **menos casas de precisão**. A receita continua igual e a quantidade de números também.
- O notebook 01 inteiro responde a duas perguntas: **quanto espaço essa tabela ocupa** e **o que se perde quando a guardamos com menos precisão**.

---

## 2. O que tem dentro de um modelo

| Termo | O que é | Analogia / exemplo no nosso caso |
|---|---|---|
| **Parâmetro** | Qualquer número que o modelo **aprende** no treino. Na prática, "parâmetro" e "peso" são usados como sinônimos | O BERTimbau base tem **~109 milhões** de parâmetros; o Qwen2.5-1.5B tem **~1,5 bilhão** (o "1.5B" do nome) |
| **Peso** (*weight*) | Parâmetro que multiplica uma entrada. Diz **o quanto** um sinal influencia o próximo | É como o "volume" de cada fio que liga um neurônio ao outro |
| **Viés** (*bias*) | Parâmetro que é **somado** (não multiplicado). Também é aprendido | O "ajuste de zero" de cada neurônio. São poucos perto dos pesos |
| **Hiperparâmetro** | Número que **a gente escolhe** antes do treino; o modelo não aprende | Taxa de aprendizado `lr=5e-5`, 2 épocas, lote de 32 e `max_length=64` (todos no notebook 02). **Não confundir com parâmetro** |
| **Camada** (*layer*) | Um bloco da receita, com a sua própria matriz de pesos | O BERT base tem 12 camadas *transformer* empilhadas |
| **Matriz de pesos 768 × 768** | A forma típica de uma camada do BERT: 768 entradas × 768 saídas = **589.824 pesos** | É a matriz que o notebook 01 cria para brincar de quantizar |
| **768** | A "largura" do BERT base: cada token vira um vetor de 768 números | É o tamanho do vetor interno (*hidden size*) |
| **Embeddings** | A primeira tabela do modelo: um vetor de 768 números para cada token do vocabulário | No BERTimbau é a **maior camada** (88,8 MiB em float32, ~21% do modelo), porque o vocabulário tem ~29,8 mil tokens |
| **Ativações** | Os valores **intermediários** calculados durante a execução, que dependem do relato que entrou. Não são guardados no arquivo [Gloss. M4] | Pesos = fixos, vêm do arquivo. Ativações = mudam a cada relato |
| **Tensor** | O nome que o PyTorch dá a uma "matriz de qualquer dimensão" | `pesos` no notebook é um tensor 768 × 768 |

> **Para fixar:** parâmetros/pesos ficam no **arquivo** e ocupam **disco e memória**. Ativações existem só **durante a execução** e ocupam memória extra. Por isso o tamanho do arquivo ≠ RAM usada (e daí a folga de 1/8 no nosso critério).

---

## 3. Bits, bytes e precisão

### 3.1 Tipos de dado (*dtype*)

| Tipo | Bits | Bytes por peso | O que guarda | Quantos valores diferentes |
|---|---:|---:|---|---|
| **float32** (FP32) | 32 | 4 | número com vírgula, alta precisão | ~4 bilhões |
| **float16** (FP16) | 16 | 2 | número com vírgula, meia precisão | ~65 mil |
| **int8** (INT8) | 8 | 1 | inteiro de −128 a 127 | 256 |
| **int4** (INT4) | 4 | 0,5 | inteiro de −8 a 7 | 16 |

- **Precisão numérica** = quantos bits cada número usa. Menos bits = arquivo menor e contas mais baratas, **mas** com mais erro de arredondamento [Gloss. M4].
- **Regra do curso:** FP16 costuma ser "quase indolor"; INT8 costuma perder pouco; INT4 já exige verificação cuidadosa no dado real [Gloss. M4].

### 3.2 A conta do tamanho

```
tamanho ≈ número de parâmetros × bytes por parâmetro
BERTimbau: 109 milhões × 4 bytes ≈ 436 MB (float32)   → × 1 byte ≈ 109 MB (int8)
```

### 3.3 MB × MiB (confunde todo mundo)

| Unidade | Vale | Quem usa |
|---|---|---|
| **MB** (megabyte, decimal) | 1.000.000 bytes | O resto do notebook 02 (`tamanho_mb`) |
| **MiB** (mebibyte, binário) | 1.048.576 bytes | O `accelerate` (ele escreve "MB", mas é MiB) |

Por isso o `accelerate` mostra **415,52 MB** e a conta dá **~436 MB**: é o mesmo tamanho em unidades diferentes. 1 GB binário (GiB) = 1.073,7 MB decimais, como avisa o notebook.

---

## 4. Quantização, peça por peça

**Quantização** = trocar cada peso float32 por um inteiro pequeno e guardar **um número de escala** para conseguir voltar ao valor aproximado [Gloss. M4].

### 4.1 Os três passos do notebook (quantização linear simétrica)

```
1. escala   = maior |peso| da matriz / 127
2. inteiro  = arredonda(peso / escala)       → fica entre −127 e 127
3. de volta = inteiro × escala               → valor aproximado (dequantização)
```

**Exemplo com números redondos:** se o maior peso é 0,254, a escala é 0,254 / 127 = **0,002**.

| Peso original | peso / escala | Inteiro guardado | De volta | Erro |
|---:|---:|---:|---:|---:|
| 0,0100 | 5,0 | 5 | 0,0100 | 0 |
| 0,0113 | 5,65 | 6 | 0,0120 | 0,0007 |
| −0,0031 | −1,55 | −2 | −0,0040 | 0,0009 |
| 0,0009 | 0,45 | 0 | 0,0000 | 0,0009 |

O erro nunca passa de **metade da escala** (0,001 aqui), porque o arredondamento desloca no máximo meio "degrau".

### 4.2 Termos da quantização

| Termo | O que é |
|---|---|
| **Fator de escala** (*scale*) | O tamanho de um "degrau" entre dois inteiros vizinhos. Liga o mundo float ao mundo inteiro [Gloss. M4] |
| **Níveis** | Os valores inteiros possíveis. Em int8 simétrico, de −127 a 127 = **255 níveis** |
| **Arredondamento** | A origem de **todo** o erro da quantização |
| **Dequantização** | O passo 3: inteiro × escala → valor aproximado [Gloss. M4] |
| **Erro de quantização** | Diferença entre o peso original e o "de volta". O notebook mostra o **erro médio** e o **maior erro** |
| **Outlier / peso extremo** | Um peso muito maior que os outros. Ele **estica a escala** e piora todos os demais (seção 5) |
| **Zero-point** | Deslocamento usado quando a faixa não é simétrica em torno de zero [Gloss. M4]. **O notebook 01 não usa**, porque faz a versão simétrica, a mais simples |
| **Quantização dinâmica** | Pesos quantizados de antemão; as **ativações** são quantizadas durante a execução, sem dado de calibração [Gloss. M4]. É a que o notebook 02 usa (`quantize_dynamic`) |
| **Calibração** | Passar alguns dados reais pelo modelo para escolher as escalas das ativações. Necessária na quantização **estática**, mas não na dinâmica [Gloss. M4] |
| **Quantização pós-treino** (PTQ) | Quantizar um modelo já treinado, sem treinar de novo. É o nosso caso [Gloss. M4] |
| **Treino consciente de quantização** (QAT) | Treinar já "sabendo" que vai quantizar. Recupera acurácia, mas custa um novo treino. Só entra se a PTQ falhar [Gloss. M4] |
| **Degradação de acurácia** | A perda de qualidade causada pela compressão. Pode se concentrar em **recortes** do dado (*slices*) [Gloss. M4]. Para nós, os recortes suspeitos são relatos mistos e caixa alta |
| **Kernels inteiros** | Código que faz as contas **direto em inteiros**. Sem eles, guardar menos bits não acelera nada [Gloss. M4]. O ONNX Runtime tem esses kernels para CPU |

---

## 5. Os números que o notebook 01 mostra (já rodamos)

| | Matriz normal | Com **um** peso = 5,0 |
|---|---:|---:|
| Bytes float32 → int8 | 2.359.296 → 589.824 (4× menor) | igual |
| Escala | 0,00183 | 0,03937 (**21× maior**) |
| Erro médio | 0,00046 | 0,00984 (**21× maior**) |
| Maior erro | 0,000917 (= escala / 2 ✔) | ≈ escala / 2 |
| Níveis realmente usados | 238 de 255 | **14** de 255 |
| Pesos que viram 0 | n/d | **31%** |

**Como contar essa história em 30 segundos:** "Com um único peso gigante, a régua passa a ir até 5. Os outros pesos, que são pequenininhos, ficam todos espremidos em 14 marcas da régua, e um terço deles vira zero. O arquivo continua 4× menor, mas a informação se perdeu."

---

## 6. O código do notebook, linha a linha

| Linha | O que faz |
|---|---|
| `!accelerate estimate-memory <modelo> ...` | Lê só a **configuração** do modelo no Hugging Face Hub (sem baixar pesos) e calcula o tamanho em cada dtype. O `!` roda um comando de terminal dentro do notebook |
| `--library_name transformers` | Diz ao `accelerate` que o modelo é da biblioteca Transformers |
| `--dtypes float32 float16 int8 int4` | Os tipos de dado da tabela |
| `torch.manual_seed(0)` | Fixa a **semente** do sorteio: todo mundo obtém os mesmos números |
| `torch.randn(768, 768) * 0.05` | Sorteia 589.824 números de uma distribuição normal (média 0) e os encolhe para ficarem parecidos com pesos reais (pequenos, em torno de zero) |
| `pesos.abs().max()` | Maior valor absoluto da matriz |
| `/ 127` | Divide pelo maior inteiro positivo usado, e o resultado é a **escala** |
| `torch.round(...)` | Arredonda para o inteiro mais próximo |
| `.to(torch.int8)` | Guarda como inteiro de 8 bits (1 byte) |
| `inteiros.float() * escala` | Dequantização: volta para float aproximado |
| `element_size()` | Bytes por elemento (4 em float32, 1 em int8) |
| `numel()` | Número de elementos (589.824) |
| `.item()` | Converte um tensor de 1 número num número Python comum, para imprimir |
| `com_extremo[0, 0] = 5.0` | Planta um peso extremo na posição (linha 0, coluna 0) |

### Colunas da tabela do `accelerate`

| Coluna | Significado |
|---|---|
| **dtype** | O tipo de dado da linha |
| **Largest Layer** | Tamanho da maior camada. Importa porque é o maior bloco que precisa caber de uma vez na memória |
| **Total Size** | Tamanho de todos os pesos = o necessário para **carregar e rodar** (inferência), sem contar as ativações |
| **Training using Adam** | Memória para **treinar**: ~4× o modelo, porque o treino guarda pesos + **gradientes** + 2 estados do otimizador Adam. "N/A" em int8/int4 porque não se treina nessas precisões |

### Nomes dos modelos

| Nome | Como ler |
|---|---|
| `neuralmind/bert-base-portuguese-cased` | Organização `neuralmind` / modelo **BERT**, tamanho **base** (~110 M), treinado em **português**, **cased** = diferencia maiúsculas de minúsculas. É por causa do *cased* que o texto em CAIXA ALTA vira muitos pedaços (ver `02_embasamento_pre_E1.md`) |
| `Qwen/Qwen2.5-1.5B-Instruct` | Família Qwen 2.5, **1,5 bilhão** de parâmetros, versão **Instruct** (ajustada para seguir instruções). É um modelo **generativo**, que escreve texto token a token. Serve no notebook como contraste de escala |

---

## 7. Confusões comuns (e a frase certa)

| ❌ Frase errada | ✅ Frase certa |
|---|---|
| "Quantizar reduz o número de parâmetros" | Reduz os **bytes por parâmetro**. O número de parâmetros é o mesmo (quem remove pesos é o *pruning*) |
| "Se ficou 4× menor, ficou 4× mais rápido" | O tamanho cai ~4×. O tempo **só** cai se o runtime tiver **kernels inteiros**, e é preciso **medir** |
| "Se cabe na memória, roda no coletor" | Precisa caber **e** responder em < 1 s. O Qwen em int4 cabe (736 MiB), mas gera token a token em CPU |
| "O arquivo tem 109 MB, então usa 109 MB de RAM" | A RAM inclui ainda as ativações, o tokenizador e o runtime |
| "Parâmetro e hiperparâmetro são a mesma coisa" | Parâmetro o modelo **aprende**; hiperparâmetro **nós escolhemos** |
| "415 MB e 436 MB são valores diferentes" | São o mesmo tamanho em MiB e em MB |
| "A perda da quantização é igual em todo o dado" | Pode se **concentrar** em recortes. Olhar classe pequena (`seguranca`) e relatos difíceis |

---

## 8. Quiz para fazer em dupla (10 min)

Uma pessoa pergunta e a outra responde **sem olhar**. Depois troquem. Abram o gabarito só no fim.

1. Qual é a diferença entre peso e ativação?
2. O BERTimbau tem ~109 M de parâmetros. Quanto ele ocupa em float16?
3. Por que o `accelerate` diz 415 MB se a conta dá 436?
4. Qual é a fórmula da escala no notebook?
5. Qual é o maior erro possível de um peso quantizado?
6. O que acontece com a escala quando aparece um peso extremo? E com os outros pesos?
7. A quantização muda o tokenizador ou as 5 classes?
8. Por que a coluna "Training using Adam" é ~4× o modelo?
9. O que significa *cased* no nome do BERTimbau, e por que isso importa no nosso dado?
10. O Qwen 1,5B em int4 caberia no coletor? Ele serviria?

<details>
<summary><b>Gabarito</b></summary>

1. O peso é aprendido no treino e fica no arquivo. A ativação é calculada a cada relato, durante a execução.
2. 109 M × 2 bytes ≈ 218 MB (o `accelerate` mostra 207,76 MiB).
3. O `accelerate` usa MiB (1.048.576 bytes) e o notebook 02 usa MB (1.000.000 bytes).
4. `escala = max(|peso|) / 127`.
5. Metade da escala (o arredondamento desloca no máximo meio degrau).
6. A escala cresce (21× no exemplo). Os outros pesos caem em poucos níveis (14 em vez de 238), muitos viram zero, e o erro médio de todos sobe na mesma proporção.
7. Não. Mudam só os valores guardados dos pesos (e, na dinâmica, as ativações durante a execução). Arquitetura, número de pesos, tokenizador e classes ficam iguais.
8. O treino guarda pesos + gradientes + 2 estados do Adam (momento e variância) = 4 cópias.
9. *Cased* = diferencia maiúsculas de minúsculas. O vocabulário quase não tem palavras em CAIXA ALTA, então esses relatos viram ~2× mais tokens, e 73 deles passam do limite de 64 e são cortados.
10. Caber, cabe (~736 MiB). Mas é generativo, gera token a token em CPU, e para escolher 1 de 5 classes não precisa disso. O limite de < 1 s é o que decide.

</details>

---

## 9. Termos que já aparecem no notebook 02 (para chegar preparado)

| Termo | O que é |
|---|---|
| **Token / tokenizador** | O tokenizador corta o texto em pedaços (tokens) que o modelo conhece. `cntator` → `c`, `##nta`, `##tor` (o `##` indica "continuação de palavra") |
| **`max_length=64`** | Limite de tokens por relato. O que passar disso é **cortado** (truncado) |
| **Inferência** | Usar o modelo treinado para classificar, sem aprender nada. É o que o coletor faz |
| **Latência** | Tempo para classificar **um** relato. No nosso critério: < 1.000 ms |
| **Lote** (*batch*) | Vários relatos de uma vez. O coletor classifica **um por vez**, e por isso o `medir_latencia` não pode passar a lista inteira |
| **Threads** | Quantos "trabalhadores" da CPU fazem as contas em paralelo. O coletor é simulado com 2 |
| **ONNX** | **Formato** de arquivo portável, com o grafo e os pesos. Não roda nada sozinho [Gloss. M4] |
| **ONNX Runtime** | O **runtime** que lê o `.onnx` e executa em CPU. É *neutro*: não depende do framework de treino [Gloss. M4] |
| **Exportação** | Converter o modelo do PyTorch para o formato ONNX [Gloss. M4] |
| **Benchmark on-device** | Medir no dispositivo alvo com o dado real. O Colab com 2 threads é uma **aproximação** do coletor, não o coletor [Gloss. M4] |
| **Ajuste fino** (*fine-tuning*) | Pegar o BERTimbau pré-treinado e treinar um pouco mais nos nossos relatos (2 épocas) |
| **Época** | Uma passada completa por todos os relatos de treino |
| **Acurácia / F1 macro** | Acurácia = fração de acertos. F1 macro = média do F1 de cada classe, com o mesmo peso para todas, o que protege `seguranca` |
| **MLflow** | Ferramenta que registra cada execução (modelo, métricas e critério) no arquivo `mlflow.db` |
| **TCO** (custo total de propriedade) | Tudo o que uma alternativa custa no ciclo de vida, e não só o preço de compra. É a base para comparar "comprar GPU" × "software" [Gloss. M4] |
