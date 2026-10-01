# Base de Conhecimento — Módulo "Introdução a IA"
### Curso: Fundamentos de IA Aplicada | Unidade M0 | Prof. Arthur Nascimento | Programa Industr.IA

> Documento de extração densa e estruturada, fiel ao conteúdo original dos 5 PDFs da unidade M0 ("Panorama de IA Aplicada"). Destina-se a servir de base de referência (skill de conhecimento) para resolver desafios futuros sobre este módulo. Terminologia em português preservada conforme o material original.

---

## AULA 1 — E-book: "Panorama de IA Aplicada: vocabulário, arco histórico e taxonomia de paradigmas e tarefas" (Unidade M0)

### 1. Tema central
Texto-base fundacional do curso, dividido em três seções: (0.1) vocabulário fundacional de ML, (0.2) arco histórico e arquitetural das famílias técnicas de IA, (0.3) taxonomia de paradigmas de aprendizagem e tarefas. Camada **conceitual**. Fecha a competência **M0.C1**.

### 2. Conceitos e definições formais

**Modelo**: função com valores ajustáveis (parâmetros) que recebe uma entrada e produz uma saída. O que torna um modelo útil é que seus valores internos são **aprendidos a partir de exemplos**, não escritos à mão por um programador.

**Parâmetro**: valor interno do modelo, ajustado automaticamente pelo treinamento. Varia de poucas dezenas (regressão linear) a centenas de bilhões (modelo de linguagem grande).

**Hiperparâmetro** (glossário formal): "Valor de configuração definido antes do treinamento e não ajustado por ele. Exemplos: a taxa de aprendizado, a profundidade máxima de uma árvore, o número de camadas de uma rede. Diferem dos parâmetros, que o treinamento ajusta. A escolha de hiperparâmetros é decidida por experimentação, normalmente sobre o conjunto de validação."

**Treinamento**: processo de ajustar os parâmetros para que as saídas do modelo se aproximem das saídas desejadas nos exemplos disponíveis. Mede o erro, calcula a direção de ajuste de cada parâmetro e aplica o ajuste, repetindo o laço muitas vezes.

**Gradiente**: direção de descida do erro, calculada para todos os parâmetros ao mesmo tempo ("se eu aumentasse um pouquinho este valor, o erro subiria ou desceria?").

**Descida do gradiente (gradient descent)**: algoritmo padrão de ajuste que move cada parâmetro na direção do gradiente.

**Taxa de aprendizado (learning rate)**: hiperparâmetro que determina o tamanho do passo em cada ajuste. Passo grande demais → oscila sem convergir; passo pequeno demais → convergência lenta, pode parar num ponto subótimo.

**Época**: uma passagem completa pelo conjunto de treino inteiro.

**Lote (batch)**: subconjunto menor do conjunto de treino, usado por vez quando mostrar todos os exemplos de uma vez é caro/não cabe na memória.

**Iteração**: um único ajuste de parâmetros sobre um lote.

**Inferência**: uso do modelo já treinado — apresenta-se entrada nova, lê-se a saída, sem alterar parâmetros. É o que ocorre em produção, repetidamente; concentra decisões de custo e latência (em oposição ao treinamento, caro/raro).

**Generalização**: capacidade de o modelo ir bem em dados novos (não vistos no treino). "É o único desempenho que interessa na prática."

**Overfitting** (glossário formal): "Situação em que o modelo vai muito bem nos dados de treinamento e mal em dados novos, porque ajustou-se a ruído e a particularidades irrelevantes. O extremo oposto é o underfitting, quando o modelo é simples demais para capturar o padrão. Técnicas de regularização, que penalizam complexidade, ajudam a conter o overfitting."

**Underfitting**: modelo simples demais para capturar o padrão; vai mal tanto em treino quanto em dados novos.

**Parada antecipada (early stopping)**: técnica que interrompe o treinamento no ponto em que a curva de erro de validação para de cair e começa a subir (ponto de separação entre as curvas de treino e validação = sinal de overfitting).

**Regularização**: técnicas que penalizam complexidade para conter overfitting (inclui dropout, parada antecipada, restrições sobre parâmetros).

**Conjunto de treino**: parte dos dados (~60%) sobre a qual os parâmetros são ajustados.

**Conjunto de validação**: parte dos dados (~20%) usada para comparar modelos e escolher hiperparâmetros. Não entra no ajuste de parâmetros. É iterado junto com o treino.

**Conjunto de teste**: parte dos dados (~20%) reservada para estimativa final e honesta da generalização. **Usado uma única vez**, ao final.

**Regra de ouro** (box do e-book): "O conjunto de teste estima a generalização e é tocado uma só vez. Se ele orientar o ajuste, a estimativa fica otimista (vazamento de dados) e deixa de representar adequadamente o desempenho em novos dados."

**Validação cruzada**: quando os dados são poucos para sustentar divisão fixa em três conjuntos, reaproveita os dados em múltiplas partições rotativas.

**Vazamento de dados (data leakage)**: erro em que informação do teste influencia (ainda que indiretamente) o treinamento ou a escolha de hiperparâmetros — ex.: normalizar todos os dados juntos antes de separá-los. Resultado: estimativa de desempenho inflada que não se confirma em produção.

**Métricas de classificação**: acurácia, precisão, recall, F1, matriz de confusão (ver Quadro 2 abaixo).

**Métricas de regressão**: MAE, RMSE, R² (ver Quadro 3 abaixo).

**Balanceamento de classes**: quando uma classe é muito mais frequente que outra (ex.: 95%/5%), a acurácia perde sentido isolada; estratégias: reportar precisão/recall/F1, sobreamostrar a classe rara, subamostrar a classe abundante, atribuir pesos diferentes por classe na função de perda.

**Perceptron (1958)**: modelo capaz de separar duas classes ajustando pesos sobre entradas numéricas; uma única camada de decisão; limitado a problemas linearmente separáveis — esfriou o interesse por ~2 décadas.

**Retropropagação (backpropagation, 1986)**: tornou prático treinar redes com várias camadas.

**ML clássico**: árvores de decisão, florestas aleatórias, máquinas de vetores de suporte (SVM), métodos de regressão. Funcionam bem com dados tabulares e quantidades moderadas de exemplos; pouca computação; continua sendo a escolha certa para muitos problemas industriais.

**Três insumos que faltavam entre o perceptron (1958) e o Deep Learning (2012)**: (1) dados em volume — escala só disponível com a internet e bases como ImageNet (anotada manualmente 2009-2010); (2) computação — GPUs, acessíveis a labs acadêmicos por volta de 2010; (3) truques de engenharia — ReLU, dropout, normalização de batch.

**AlexNet (2012)**: rede convolucional grande treinada em GPU sobre ImageNet; vitória em torneio de visão computacional = marco visível do início do Deep Learning.

**Três condições que favorecem o ML clássico sobre Deep Learning** (texto corrido, não em quadro):
1. Dados tabulares em volume moderado (milhares a centenas de milhares de linhas) → floresta aleatória/gradient boosting batem rede profunda em precisão, fração do custo.
2. Orçamento de inferência apertado (hardware restrito, latência baixa) → modelos clássicos respondem em microssegundos sem hardware especializado.
3. Auditabilidade importa (crédito, saúde, conformidade regulatória) → métodos clássicos são mais fáceis de explicar/justificar.
"Em todos esses casos, partir direto para a rede mais nova é trocar uma solução adequada por uma cara, lenta e opaca."

**Três famílias de arquitetura do Deep Learning (~2012)**:
- **Perceptron multicamadas (MLP)**: rede totalmente conectada; mais geral; cada neurônio conecta-se a todos da camada seguinte; não assume estrutura na entrada; serve a dados tabulares/tarefas simples; perde para arquiteturas especializadas quando há estrutura espacial/sequencial.
- **Rede convolucional (CNN)**: explora estrutura espacial de imagens, aplicando o mesmo filtro a regiões locais, compondo em camadas; captura bordas/texturas/formas sem nomeação manual.
- **Rede recorrente (RNN)**, destaque para **LSTM (1997)**: processa dados em sequência mantendo estado interno que carrega informação entre passos; adequada a texto, áudio, séries temporais.

Traço comum das três: **aprendizado de representações em camadas** — a rede descobre atributos cada vez mais abstratos a partir dos dados brutos, em vez de o engenheiro defini-los manualmente.

**Attention / Transformer (2017)**: mecanismo que processa uma sequência inteira em paralelo e modela relações de longa distância melhor que RNNs — cada palavra "olha" diretamente para qualquer outra, sem depender de intermediárias (ao contrário da RNN, que entrega informação em cadeia).

**Foundation Model** (glossário formal): "Modelo de grande escala, treinado em volume amplo de dados gerais, que serve de base para muitas tarefas diferentes mediante adaptação leve, em vez de ser treinado do zero para cada tarefa. Modelos de linguagem grandes são o exemplo mais conhecido. O termo foi popularizado por um relatório de Stanford em 2021."

**Três traços que tornam um modelo "fundacional"**: (1) escala (centenas de milhões a centenas de bilhões de parâmetros, dezenas de bilhões de exemplos de treino); (2) generalidade do dado de treino (corpus amplo cobrindo muitos domínios, não uma tarefa específica); (3) possibilidade de adaptação leve para tarefas específicas sem repetir o pré-treino.

**Fine-tuning**: continua o treinamento do modelo pré-treinado sobre dados específicos da tarefa-alvo, ajustando todos os parâmetros ou subconjunto. **LoRA**: variante econômica que ajusta matrizes pequenas somadas aos pesos originais.

**Prompting**: dispensa treinamento extra; o modelo recebe instrução em linguagem natural (possivelmente com exemplos) e produz saída com base apenas no contexto.

**Três caminhos de uso de um Foundation Model** (Figura 4): (1) Pré-treino — dados gerais (trilhões de tokens sem rotulação) → treinamento auto-supervisionado em larga escala → modelo base. Custo muito alto, duração em meses. (2) Fine-tuning — modelo base + dados específicos (milhares de exemplos rotulados) → treinamento adicional → modelo adaptado. Custo médio, horas/dias. (3) Prompting — modelo base + instrução em linguagem natural → saída desejada. Custo por chamada, segundos.

**Sistemas agênticos (a partir de 2023)**: envolvem um modelo de linguagem em um laço de decisão com ferramentas e memória. Motivação: um Foundation Model isolado responde bem a perguntas em passagem única, mas não age no mundo, não verifica fatos externos, não persegue objetivos multi-etapa. Três componentes adicionados: (1) **ferramentas** acionáveis (busca web, execução de código, consulta a banco de dados, envio de e-mail); (2) **memória** que persiste entre passos; (3) **laço de decisão** que escolhe a próxima ação a partir do estado atual e do objetivo.

**Paradigma de aprendizagem**: descreve *a partir de que tipo de sinal* o modelo aprende. Quatro paradigmas tratados no M0: supervisionado, não supervisionado, auto-supervisionado, por reforço.

**Aprendizado supervisionado**: cada exemplo vem com a resposta correta (rótulo); o modelo aprende a reproduzir essa associação.

**Aprendizado não supervisionado**: não há rótulos; o modelo busca estrutura nos próprios dados (ex.: clustering).

**Aprendizado por reforço**: um agente aprende por tentativa e erro a partir de recompensas, ajustando uma política para maximizar o retorno ao longo do tempo. Típico de problemas de controle.

**Vocabulário do aprendizado por reforço**:
- **Agente**: observa estado, escolhe ação via política, recebe recompensa e novo estado.
- **Ambiente**: sistema externo sobre o qual o agente atua.
- **Estado**: descrição da situação do ambiente observada pelo agente.
- **Ação**: escolha do agente em cada passo.
- **Política**: regra que o agente usa para escolher ação a partir do estado; é o que se aprende.
- **Recompensa**: sinal (positivo/negativo) devolvido pelo ambiente após cada ação. Objetivo: maximizar a *soma* das recompensas ao longo do tempo, não a recompensa isolada de cada passo.
- **Exploração versus explotação**: dilema central — explorar ações pouco testadas (podem render mais no longo prazo) vs. explotar ações já comprovadamente boas.

**Aprendizado auto-supervisionado** (glossário formal, 0.3): "Paradigma em que os rótulos são gerados a partir dos próprios dados, sem anotação humana. Um modelo de linguagem aprende prevendo a próxima palavra de textos existentes: o texto é, ao mesmo tempo, entrada e resposta. É o que viabiliza treinar Foundation Models em grande escala, já que dispensa rotulagem manual de cada exemplo." Motivo de virar motor dos LLMs: rotular dados custa caro; texto traz sinal de treino gratuito (prever a próxima palavra é checável automaticamente). O mesmo princípio se estende a outras modalidades (prever pedaço escondido de imagem, próximo quadro de vídeo, áudio mascarado). O subproduto é a **representação aprendida**, base para adaptações posteriores (fine-tuning/prompting).

**Tarefa**: descreve *o que o modelo produz*, independentemente de como aprendeu. Seis tarefas tratadas: classificação, regressão, clustering, geração, recuperação, controle.
- **Classificação**: atribui entrada a categoria discreta.
- **Regressão**: produz número contínuo.
- **Clustering**: agrupa exemplos por semelhança sem categorias predefinidas.
- **Geração**: produz artefato novo (texto, imagem, áudio, código, dado sintético).
- **Recuperação**: encontra, num acervo, itens mais relevantes para uma consulta.
- **Controle**: escolhe ações que afetam um ambiente ao longo do tempo.

**Ideia central da seção 0.3 (ortogonalidade)**: paradigma e tarefa são **eixos independentes**; a mesma tarefa admite paradigmas diferentes, e o mesmo paradigma serve a tarefas diferentes. Não devem ser confundidos.

**RAG (retrieval-augmented generation)**: pipeline que combina recuperação (busca trechos relevantes num acervo de documentos) e geração (LLM produz resposta com base nesses trechos) — exemplo canônico de **composição de tarefas**.

**Ranking sobre classificação**: outra composição frequente — um modelo classifica candidatos por categoria e outro ordena por relevância.

### 3. Frameworks / processos / heurísticas

**Pseudocódigo do laço de treinamento**:
```
# durante o treinamento
for exemplo, resposta in treino:
    previsao = modelo(exemplo)
    erro = comparar(previsao, resposta)
    ajustar(modelo, erro)
```
**Pseudocódigo da inferência** (laço desaparece, cada chamada independente):
```
# em produção, com o modelo já treinado
previsao = modelo(entrada_nova)
```

**Ciclo treino/validação/teste** (Figura 2): (1) Partição do conjunto de dados rotulados em Treino (~60%), Validação (~20%), Teste (~20%). (2) Laço de ajuste e avaliação final: Treinar (ajusta parâmetros no treino) ↔ Validar (compara modelos/escolhe hiperparâmetros) — iterar: repetir até o desempenho de validação estabilizar → modelo final → Testar (uma vez).

**Sequência de perguntas para classificar um problema novo** (heurística de diagnóstico, seção 0.3):
1. Há rótulos disponíveis (ou orçamento/capacidade de produzi-los)? Se sim e o objetivo é prever o rótulo → **supervisionado**. Se não → **não supervisionado** ou **auto-supervisionado**, conforme o sinal de treino extraível dos próprios dados.
2. O sistema age sobre um ambiente e recebe consequências entre passos, ou só responde a entradas isoladas? Se age → **por reforço**.
3. O que o sistema produz em cada chamada? Categoria (classificação) / número (regressão) / agrupamento sem rótulos prévios (clustering) / artefato novo (geração) / itens recuperados (recuperação) / decisão de ação (controle)?
A combinação das respostas posiciona o problema na matriz paradigma×tarefa e antecipa técnicas, métricas e riscos de execução.

**Heurística de escolha de métrica por custo do erro**: a escolha entre métricas depende do **custo dos erros**, não do nome da tarefa.
- Filtro de spam: falso positivo (perder e-mail legítimo) é mais doloroso que falso negativo (deixar passar spam) → **precisão** importa mais.
- Triagem de doença grave: falso negativo (deixar passar caso positivo) é muito pior → **recall** importa mais.
- F1 ajuda quando os dois lados doem de forma parecida.
- Regra prática: olhar sempre mais de uma métrica em conjunto — "uma única métrica é fácil de otimizar e fácil de enganar."

**Princípio arquitetural de PD&I**: as quatro famílias (ML clássico, Deep Learning, Foundation Models, sistemas agênticos) **coexistem** em vez de se substituírem num mesmo projeto. A pergunta operacional não é "qual família é a melhor" e sim "qual família é mais adequada a esta parte específica do problema, dadas as restrições de dado, custo, latência e auditabilidade".

### 4. Exemplos aplicados (industriais/PD&I)

- **Manutenção preditiva**: fábrica registra vibração, temperatura, corrente de motores para prever falhas. Dados tabulares, classificação. Métrica não pode ser só acurácia (falhas são raras) — recall e precisão importam mais: deixar passar falha custa parada não planejada; alarme falso custa inspeção.
- **Inspeção visual de defeitos** (Deep Learning/CNN) vs. **previsão de inadimplência por histórico de pagamentos** (ML clássico/floresta aleatória) — mesma empresa, famílias diferentes, porque dados e tarefa diferem.
- **Paradigmas na fábrica de motores**: supervisionado (prever rótulo falha/normal a partir de sensores), não supervisionado (clustering de motores por comportamento, sem grupos definidos a priori), por reforço (agente decide "esperar" vs. "manutenção preventiva" a cada turno para minimizar paradas).
- **Indústria têxtil**: classificação supervisionada (peça com/sem defeito, fotos rotuladas) + clustering não supervisionado (agrupar tipos de defeito não definidos a priori) sobre o **mesmo acervo de imagens** — mesma tarefa de dados, duas combinações paradigma/tarefa distintas.
- **Quadro 4** (exemplos industriais por paradigma×tarefa): ver tabela abaixo.

### 5. Armadilhas / erros comuns

1. **Medir desempenho no próprio conjunto de treino** e comemorar acurácia alta (quase sempre otimista — o modelo já viu as respostas).
2. **Vazamento de dados** (deixar informação do teste vazar para o ajuste, ex.: normalizar todos os dados juntos antes de separá-los) → estimativa de desempenho inflada, modelo decepciona em produção.
3. **Supor que a família mais recente é sempre a melhor** — tentar resolver com Foundation Model um problema que uma árvore de decisão resolveria com mais precisão, menor custo e mais auditabilidade → "sistema caro, lento e difícil de explicar, escolhido por moda e não por adequação." Situar a técnica começa pela natureza dos dados/tarefa, não pela data de publicação do método.
4. **Confundir paradigma com tarefa** — dizer que um projeto "é de classificação" para descrever como o modelo aprende, ou chamar supervisionado de "tarefa". Consequência: subestimar requisitos (esquecer de perguntar se existem rótulos, quem vai produzi-los, a que custo). "Muitos projetos travam não por falta de modelo, mas por falta de dados rotulados que ninguém previu."

### 6. Tabelas / quadros estruturados

**Quadro 1 — Parâmetro versus Hiperparâmetro**

| Aspecto | Parâmetro | Hiperparâmetro |
|---|---|---|
| Quem ajusta | O treinamento, automaticamente | A pessoa que conduz o experimento |
| Quando | Durante o treino | Antes do treino, mantido fixo durante ele |
| Exemplos | Pesos de uma rede, coeficientes de uma regressão | Taxa de aprendizado, profundidade máxima de árvore, número de camadas |

**Quadro 2 — Métricas de classificação**

| Métrica | Para que serve | Fórmula verbal |
|---|---|---|
| Acurácia | Fração de acertos no total | Acertos sobre total |
| Precisão | Quanto das previsões positivas estava correto | Acertos positivos sobre previsões positivas |
| Recall | Quanto dos positivos reais foi capturado | Acertos positivos sobre positivos reais |
| F1 | Síntese de precisão e recall | Média harmônica de precisão e recall |
| Matriz de confusão | Mapa de acertos e erros por categoria | Tabela de combinações real por previsto |

**Quadro 3 — Métricas de regressão**

| Métrica | Para que serve | Fórmula verbal |
|---|---|---|
| Erro absoluto médio (MAE) | Tamanho médio do erro, peso linear | Média da diferença absoluta entre previsto e real |
| Raiz do erro quadrático médio (RMSE) | Tamanho médio do erro, penaliza erros grandes | Raiz quadrada da média do quadrado da diferença |
| Coeficiente de determinação (R²) | Fração da variação explicada | 1 = explicação perfeita; 0 = não explica nada; pode ser negativo |

**Quadro 4 — Exemplo industrial típico por combinação paradigma×tarefa**

| Paradigma | Tarefa | Exemplo industrial |
|---|---|---|
| Supervisionado | Classificação | Detecção de defeitos em peças por imagem rotulada |
| Supervisionado | Regressão | Previsão de demanda de energia a partir de variáveis climáticas |
| Não supervisionado | Clustering | Segmentação de motores por padrão de operação |
| Auto-supervisionado | Geração | Modelo de linguagem aprendendo a prever o próximo token |
| Auto-supervisionado | Recuperação | Busca semântica em base de manuais técnicos |
| Por reforço | Controle | Otimização de scheduling em linha de produção |

**Figura 6 — Matriz Paradigma × Tarefa (típico / possível / incomum)**

| Paradigma ↓ / Tarefa → | Classificação | Regressão | Clustering | Geração | Recuperação | Controle |
|---|---|---|---|---|---|---|
| Supervisionado | típico | típico | incomum | possível | possível | possível |
| Não supervisionado | incomum | incomum | típico | possível | possível | incomum |
| Auto-supervisionado | possível | possível | possível | típico | típico | possível |
| Por reforço | incomum | incomum | incomum | possível | incomum | típico |

Leitura por colunas: ex. geração é típica do auto-supervisionado, mas também possível em não supervisionado (modelos que aprendem a distribuição) e em RL (refino por recompensa de um gerador) — nomear a tarefa não basta para fixar a técnica. Leitura por linhas: RL concentra-se em controle, raramente é escolha para classificação tabular.

**Figura 5 — Arco histórico-arquitetural (linha do tempo por família)**: 1958 Perceptron → 1986 Retropropagação → anos 1990 Árvores/SVM (ML clássico) → 1997 LSTM (RNN) → 2012 AlexNet (CNN, marco do Deep Learning) → 2017 Transformers → 2018-2020 BERT/GPT (Foundation Models) → 2023+ Sistemas Agênticos. Famílias: Precursores, ML Clássico, Deep Learning, Foundation Models, Sistemas Agênticos. Nota: linha do tempo esquemática, posições aproximadas, sem escala.

### 7. Vocabulário/glossário da aula
Modelo, parâmetro, hiperparâmetro, treinamento, inferência, gradiente, descida do gradiente, taxa de aprendizado, época, lote/batch, iteração, generalização, overfitting, underfitting, parada antecipada, regularização, conjunto de treino/validação/teste, validação cruzada, vazamento de dados, acurácia, precisão, recall, F1, matriz de confusão, MAE, RMSE, R², balanceamento de classes, sobreamostragem, subamostragem, perceptron, retropropagação, ML clássico, árvore de decisão, floresta aleatória, SVM, gradient boosting, GPU, ImageNet, AlexNet, ReLU, dropout, normalização de batch, MLP, CNN, RNN, LSTM, attention, transformer, Foundation Model, pré-treino, fine-tuning, LoRA, prompting, sistemas agênticos, ferramenta, memória, laço de decisão, paradigma de aprendizagem, supervisionado, não supervisionado, auto-supervisionado, por reforço, agente, ambiente, estado, ação, política, recompensa, exploração vs. explotação, representação aprendida, tarefa, classificação, regressão, clustering, geração, recuperação, controle, RAG, ranking.

---

## AULA 2 — Google Colab: "Panorama de IA Aplicada" (Guia de Acesso ao Notebook, Unidade M0)

### 1. Tema central
Notebook prático que compara duas abordagens para uma tarefa de **classificação** sobre o dataset Titanic: (a) **paradigma clássico supervisionado** com Random Forest (treinamento tradicional) vs. (b) **Foundation Model via prompting** (in-context learning, zero-shot/few-shot) usando um LLM pequeno (Qwen2.5-0.5B) local via Hugging Face Transformers, sem treinamento adicional.

### 2. Conceitos e definições (reforçados/aplicados no notebook)
- **In-context learning**: comportamento do Foundation Model ajustado apenas pelos exemplos/instruções do próprio prompt, sem atualização de pesos.
- **Few-shot**: uso do LLM com alguns exemplos resolvidos dentro do prompt.
- **Zero-shot**: uso do LLM sem nenhum exemplo no prompt, apoiado só na instrução.
- **Feature importances**: interpretação de quais atributos mais pesam nas decisões da Random Forest.
- **Codificação one-hot**: transforma coluna categórica em várias colunas binárias (uma por categoria); descartar uma delas evita redundância.
- **Custo por previsão**: tempo de inferência como dimensão de avaliação, ao lado da acurácia.

### 3. Framework / processo (estrutura do notebook — tabela "Palavra → Tradução")

| Etapa | Conteúdo |
|---|---|
| Preparação de dados | Carregamento do dataset Titanic, tratamento de valores ausentes, codificação one-hot de variáveis categóricas |
| Classificador Clássico | Treinamento/avaliação de RandomForest, separação treino/teste, feature importances, matriz de confusão |
| Foundation Model + Prompting | LLM pequeno (Qwen2.5-0.5B) local via Hugging Face Transformers, sem treinamento adicional |
| In-Context Learning | Comparação few-shot vs. zero-shot: como o prompt afeta o comportamento do modelo |
| Comparação de Soluções | Avaliação conjunta de acurácia e custo por previsão (tempo de inferência); trade-offs entre abordagens |

**Conceitos-chave declarados**: paradigma, tarefa, treinamento vs. inferência, generalização, prompting, few-shot, zero-shot.

**Objetivo declarado**: "Fixar a diferença entre treinamento e inferência, compreender o poder e as limitações do in-context learning e aprender a avaliar soluções não apenas pela acurácia, mas também pelo custo computacional."

### 4. Exemplo aplicado
Dataset Titanic (clássico de ML) usado como veículo prático para contrastar ML clássico supervisionado com uso de Foundation Model via prompting na mesma tarefa de classificação.

### 5. Armadilhas
Implícita: avaliar uma solução **só** pela acurácia, ignorando custo computacional/latência por previsão — risco já sinalizado na Aula 1 (regra de olhar mais de uma métrica/dimensão em conjunto).

### 6. Tabelas
Ver tabela "Palavra → Tradução" acima (única tabela do documento).

### 7. Vocabulário da aula
Random Forest, in-context learning, few-shot, zero-shot, feature importances, matriz de confusão, codificação one-hot, custo por previsão, Qwen2.5-0.5B, Hugging Face Transformers.

---

## AULA 3 — E-book: "Panorama de IA Aplicada: as cinco lentes transversais" (Unidade M0.C2)

### 1. Tema central
Segundo recurso de organização do módulo, complementar à taxonomia da Aula 1: as **cinco lentes transversais** (Generativa, Agentic, Data-Centric, Edge, Explainable), entendidas como ângulos de leitura aplicáveis a qualquer problema de IA — não tecnologias nem etapas de projeto. Fecha o módulo de nivelamento (M0).

### 2. Conceitos e definições formais

**Lente (conceito)**: "Uma lente não muda o objeto que se observa; muda o que se torna visível nele." Lentes se acumulam — nada impede olhar um problema por duas ou três lentes ao mesmo tempo (e em geral deve-se fazer isso). Diferença-chave vs. taxonomia (Aula 1): a taxonomia **classifica** o que um sistema é (paradigma+tarefa, rótulo único); a lente **não rotula**, apenas escolhe o que perguntar — e não é exclusiva.

**Lente transversal** (glossário formal): "Ângulo de leitura que se aplica a qualquer problema de IA, qualquer que seja o eixo técnico envolvido. Diferente de um eixo técnico, que reúne métodos de uma área, a lente transversal não nomeia uma tecnologia, e sim uma pergunta recorrente (sobre geração, autonomia, dados, execução ou transparência) que atravessa todos os eixos."

**Eixo técnico** (distinção IMPORTANTE!): "Um eixo técnico responde à pergunta com que tecnologia se resolve, e cada eixo reúne métodos, ferramentas e competências de uma área." Os **sete eixos técnicos** do programa: LLMs, Visão Computacional, Machine Learning, Real Time Processing, Deep Learning, NLP, Engenharia de Dados.

**Propriedade central — transversalidade**: qualquer um dos 7 eixos técnicos pode ser lido por qualquer uma das 5 lentes (e vice-versa: uma lente, como a Edge, atravessa LLMs, Visão Computacional, Real Time Processing, Engenharia de Dados etc.). "Toda lente atravessa todo eixo; por isso as lentes são ângulos de leitura, não tecnologias paralelas."

**As cinco lentes** (cada uma = pergunta característica + módulo que a desenvolve):

1. **Generativa** (M1): "Ele produz um artefato novo?" — texto, imagem, áudio, código, dados sintéticos. Traz consigo: avaliação de qualidade sem resposta única correta, contenção de alucinação/cópia indevida, controle sobre o gerado. Sinal no enunciado: verbos como *criar, redigir, desenhar, sintetizar*.
2. **Agentic** (M2): "O sistema decide e age em um laço, ou só responde a uma solicitação isolada?" — consulta ferramentas, mantém memória, persegue objetivo em vários passos. Pergunta: quanto de iniciativa o sistema tem, quais ferramentas aciona, que salvaguardas garantem previsibilidade/reversibilidade. Sinal: enunciado descreve sequência de passos com decisão entre eles.
3. **Data-Centric** (M3): "O ganho vem de trocar/ajustar o modelo, ou de melhorar o dado que o alimenta?" — qualidade, cobertura, balanceamento, rotulagem do dataset, governança de dados. "Em muitos problemas industriais, investir em dados rende mais que investir em arquitetura." Sinal: desempenho estagna mesmo trocando de modelo.
4. **Edge** (M4): "Onde e sob que restrições o sistema executa?" — servidor com folga vs. dispositivo com pouca memória/energia/conectividade intermitente e exigência de resposta imediata. Trata compressão, latência, custo de inferência, compromisso precisão×hardware. Sinal: menção a dispositivo, sensor, latência, operação sem rede.
5. **Explainable** (M5): "Por que o sistema produziu esta saída, e quem responde por ela?" — justificabilidade a quem é afetado, auditoria, regulação, confiança para agir com base na indicação do sistema. Sinal: decisão envolve pessoas, dinheiro ou segurança.

**As cinco perguntas em sequência prática** (checklist de diagnóstico): há criação de artefato novo (generativa)? o sistema decide e age em laço, ou só responde (agentic)? o gargalo está no modelo ou no dado (data-centric)? onde e sob que restrições isso vai executar (edge)? é preciso justificar a saída e dizer quem responde por ela (explainable)?

### 3. Frameworks / processos / heurísticas
- Checklist das 5 perguntas (acima) — aplicar a qualquer problema antes de escolher a ferramenta.
- Regra prática: um sistema real "costuma exigir mais de uma [lente] simultaneamente" — nunca tratar como mutuamente exclusivas.
- Matriz lente × eixo técnico (Figura 1, ver tabela abaixo) como mapa de centralidade relativa (não presença/ausência).

### 4. Exemplos aplicados

- **Visão Computacional por 5 lentes**: generativa → imagens sintéticas para ampliar treino escasso; agentic → inspetor automático que decide e aciona descarte; data-centric → qualidade das imagens rotuladas; edge → inferência na própria câmera da linha; explainable → por que a peça foi classificada defeituosa.
- **Lente Edge atravessando eixos**: LLM pequeno embarcado, inferência na câmera (Visão Computacional), orçamento de latência (Real Time Processing), o que processar localmente vs. enviar (Engenharia de Dados).
- **Linha de envase de bebidas**: sistema rejeita garrafas com rótulo torto/vedação falha a partir de imagens — problema de Visão Computacional pedindo **três lentes simultâneas**: data-centric (defeitos raros, ganho maior vem de rotular/balancear bem, não trocar modelo), generativa (gerar imagens sintéticas de defeito para suprir escassez), explainable (operador precisa saber por que a garrafa foi rejeitada para confiar no corte/ajustar limiar).

### 5. Armadilhas / erros comuns
1. **Pensar nas lentes como uma 6ª/7ª/8ª categoria de tecnologia** — "o engano mais comum."
2. **Tratar as lentes como mutuamente exclusivas** (classificar um projeto como "generativo OU agêntico"), quando um sistema real costuma estar sob várias lentes ao mesmo tempo.
3. **Confundir lente com eixo técnico ou com uma equipe** — ex. achar que "lente Edge" = "squad de Real Time Processing", ou que explicabilidade é assunto de um time só. Consequência: requisitos de execução/dados/transparência ficam sem dono, fora do escopo.

### 6. Tabelas / matrizes

**Figura 1 (Aula 3) / Matriz completa (Aula 4) — Cinco lentes × sete eixos técnicos** (escala: Central / Recorrente / Pontual — indica centralidade relativa, **não** presença/ausência; todas as lentes atravessam todos os eixos):

| Lente ↓ / Eixo → | LLMs | Visão Computacional | Machine Learning | Real Time Processing | Deep Learning | NLP | Engenharia de Dados |
|---|---|---|---|---|---|---|---|
| **Generativa** (M1) | Central | Recorrente | Recorrente | Pontual | Central | Central | Recorrente |
| **Agentic** (M2) | Central | Pontual | Pontual | Recorrente | Pontual | Recorrente | Recorrente |
| **Data Centric** (M3) | Recorrente | Central | Central | Recorrente | Central | Recorrente | Central |
| **Edge** (M4) | Recorrente | Central | Recorrente | Central | Central | Pontual | Pontual |
| **Explainable** (M5) | Recorrente | Recorrente | Central | Pontual | Recorrente | Recorrente | Pontual |

### 7. Vocabulário/glossário da aula
Lente transversal, eixo técnico, lente generativa, lente agentic, lente data-centric, lente edge, lente explainable, central/recorrente/pontual (escala de centralidade).

---

## AULA 4 — Slide/Figura: "Cinco lentes transversais × sete eixos técnicos" (Unidade M0.C2)

### 1. Tema central
Peça visual (infográfico de uma figura) que reproduz e detalha, em formato de matriz de centralidade, a mesma relação lentes×eixos apresentada ao final da Aula 3 — com texto alternativo de acessibilidade completo e legenda formal da escala.

### 2. Conceitos e definições
Reitera literalmente: "**Central**: ângulo de decisão dominante nesse eixo. **Recorrente**: ângulo secundário, aparece com frequência. **Pontual**: ângulo situacional, menos central." E a ressalva central: "Todas as lentes atravessam todos os eixos; a escala indica centralidade relativa, não presença ou ausência. Nenhuma célula significa que a lente não se aplica àquele eixo."

### 3. Framework
A matriz em si é a ferramenta/heurística: permite, para qualquer eixo técnico, identificar rapidamente qual lente tende a ser o ângulo de decisão dominante.

### 4. Exemplos aplicados
Não traz exemplo narrativo novo; é a materialização tabular do conteúdo da Aula 3.

### 5. Armadilhas
Implícita (reforça a da Aula 3): não interpretar célula vazia/de menor intensidade como "a lente não se aplica".

### 6. Tabela completa (idêntica à da Aula 3, reproduzida com os mesmos valores)

| Lente ↓ / Eixo → | LLMs | Visão Computacional | Machine Learning | Real Time Processing | Deep Learning | NLP | Engenharia de Dados |
|---|---|---|---|---|---|---|---|
| **Generativa** (lente criativa · M1) | Central | Recorrente | Recorrente | Pontual | Central | Central | Recorrente |
| **Agentic** (lente da autonomia · M2) | Central | Pontual | Pontual | Recorrente | Pontual | Recorrente | Recorrente |
| **Data Centric** (lente dos dados · M3) | Recorrente | Central | Central | Recorrente | Central | Recorrente | Central |
| **Edge** (lente do deployment · M4) | Recorrente | Central | Recorrente | Central | Central | Pontual | Pontual |
| **Explainable** (lente da transparência · M5) | Recorrente | Recorrente | Central | Pontual | Recorrente | Recorrente | Pontual |

### 7. Vocabulário
Mesmo da Aula 3, com os apelidos explícitos de cada lente: "lente criativa" (Generativa), "lente da autonomia" (Agentic), "lente dos dados" (Data Centric), "lente do deployment" (Edge), "lente da transparência" (Explainable).

---

## AULA 5 — Glossário completo da Unidade M0 ("Panorama de IA Aplicada")

### 1. Tema central
Glossário oficial e consolidado de toda a Unidade M0, em ordem alfabética, com tags de origem `[M0: seção]` indicando de qual parte do texto-base (ou notebook) cada termo vem, e remissões cruzadas ("veja X"). É o documento normativo de definições — fonte de verdade terminológica do módulo.

### 2–7. Conteúdo
Este documento **é**, em si, o glossário — reproduzido de forma consolidada e completa na seção "Lista consolidada de termos técnicos" ao final deste arquivo (ver abaixo), para evitar duplicação. Nenhum conceito novo além dos já capturados nas Aulas 1–4 é introduzido aqui; o valor da Aula 5 está na **formalização exata das definições** (muitas delas usadas aqui como texto oficial de referência para correção de respostas de alunos).

Observações estruturais do próprio glossário (metadados importantes para avaliação):
- Convenção de tags: `[M0: seção]` e, quando o texto-base trazia box-glossário formal, a marca `box` é adicionada (ex.: `[M0: 0.1, box]`). Termos introduzidos apenas no notebook (Aula 2) trazem a marca do notebook (ex.: `[M0: 0.2, IA-003]`).
- Termos com entrada "veja X" são só remissões (sinônimo/sigla), sem definição própria: Backpropagation→Retropropagação; CNN→Rede convolucional; Data leakage→Vazamento de dados; Feature→Atributo; Gradient descent→Descida do gradiente; MAE→Erro absoluto médio; MLP→Perceptron multicamadas; R²→Coeficiente de determinação; RandomForest→Floresta aleatória; RMSE→Raiz do erro quadrático médio; RNN→Rede recorrente; SVM→Máquina de vetores de suporte; Target→Alvo.

---

## RESUMO EXECUTIVO DO MÓDULO (Unidade M0 — "Introdução a IA" / Panorama de IA Aplicada)

O módulo M0 é o **nivelamento conceitual** que sustenta todo o curso "Fundamentos de IA Aplicada". Ele não ensina a implementar nada em profundidade (nenhuma matemática avançada, pouco código) — seu objetivo é dar **vocabulário preciso** e **dois recursos de organização mental** (taxonomia e lentes) para que qualquer problema técnico encontrado nos módulos seguintes (M1–M5) possa ser situado com critério.

**Progressão lógica entre as aulas:**

1. **Aula 1 (e-book, seções 0.1–0.3)** constrói a base em três camadas sucessivas:
   - **0.1 Vocabulário fundacional**: fixa o significado operacional de modelo, parâmetro/hiperparâmetro, treinamento/inferência, overfitting/generalização, conjuntos treino-validação-teste e métricas de avaliação (classificação e regressão). Esse vocabulário é pré-requisito para tudo que vem depois.
   - **0.2 Arco histórico e arquitetural**: usa esse vocabulário para mapear a evolução técnica em quatro grandes famílias — ML clássico, Deep Learning, Foundation Models, Sistemas Agênticos — do perceptron (1958) aos agentes (2023+). A lição central é que a família mais recente **não é automaticamente a melhor**; a escolha depende da natureza dos dados/tarefa e de restrições de custo, latência e auditabilidade.
   - **0.3 Taxonomia de paradigmas e tarefas**: acrescenta um segundo eixo de classificação, ortogonal ao primeiro — **paradigma** (como o modelo aprende: supervisionado, não supervisionado, auto-supervisionado, por reforço) × **tarefa** (o que o modelo produz: classificação, regressão, clustering, geração, recuperação, controle). Fecha a competência M0.C1: saber classificar um problema dado nesses dois eixos.

2. **Aula 2 (notebook Colab)** é a aplicação prática imediata da seção 0.2/0.3: compara, no mesmo problema de classificação (Titanic), um modelo de ML clássico supervisionado (Random Forest, treinado) contra um Foundation Model usado via prompting (zero-shot/few-shot, sem treinamento) — tornando tangíveis treinamento×inferência, paradigma×tarefa e o trade-off acurácia×custo computacional.

3. **Aula 3 (e-book, "cinco lentes transversais")** introduz o **segundo recurso de organização do módulo**, de natureza distinta e complementar à taxonomia: em vez de classificar *o que um sistema é*, as lentes (Generativa, Agentic, Data-Centric, Edge, Explainable) perguntam *por quais ângulos ele deve ser lido* — e são explicitamente distintas dos sete **eixos técnicos** do programa (LLMs, Visão Computacional, Machine Learning, Real Time Processing, Deep Learning, NLP, Engenharia de Dados). A propriedade central é a **transversalidade**: toda lente atravessa todo eixo, e lentes se acumulam (um problema real pede várias ao mesmo tempo).

4. **Aula 4 (matriz visual)** consolida visualmente a relação lentes×eixos em uma matriz de centralidade (Central/Recorrente/Pontual), reforçando que a escala indica *prevalência relativa*, nunca presença/ausência.

5. **Aula 5 (glossário)** fecha o módulo formalizando, em ordem alfabética e com rastreabilidade de origem, todas as definições construídas nas aulas anteriores — funcionando como a fonte normativa de verificação terminológica.

**Conclusão pedagógica do módulo** (conforme o próprio texto-base): o par **taxonomia (paradigma+tarefa)** + **lentes transversais (5 ângulos)** é a base assumida em todos os módulos seguintes (M1 lente generativa, M2 agentic, M3 data-centric, M4 edge, M5 explainable) e em todos os momentos presenciais do programa. O quiz do módulo é o objeto IA-006.

---

## LISTA CONSOLIDADA DE TERMOS TÉCNICOS (glossário unificado "termo: definição")

> Baseado no glossário oficial da Aula 5, complementado com termos das demais aulas. Ordem alfabética (ignorando acentos/maiúsculas), conforme convenção do material.

- **Ação**: no aprendizado por reforço, a escolha que o agente faz em cada passo e que afeta o ambiente; a sequência de ações é guiada pela política e avaliada pelas recompensas que produz.
- **Acurácia**: fração de acertos sobre o total de exemplos; em conjuntos desequilibrados pode parecer alta sem que o modelo seja útil.
- **Agente**: no RL, entidade que observa o estado do ambiente, escolhe ações via política e aprende com as recompensas; no contexto agêntico (M2), sistema que envolve um LLM em laço de decisão com ferramentas e memória.
- **Agentic (lente)**: lente transversal sobre comportamento agêntico e autonomia operacional; pergunta se o sistema decide e age em laço (ferramentas, memória, objetivo multi-passo) ou só responde a uma solicitação isolada (M2).
- **AlexNet**: rede convolucional grande, treinada em GPU sobre ImageNet, cuja vitória em torneio de visão computacional (2012) marca o início visível do Deep Learning.
- **Alvo (target)**: saída que o modelo deve prever, conhecida nos exemplos de treino (categoria em classificação, número em regressão).
- **Ambiente**: no RL, sistema externo sobre o qual o agente atua, devolvendo novo estado e recompensa a cada ação.
- **Aprendizado auto-supervisionado**: paradigma em que os rótulos são gerados a partir dos próprios dados, sem anotação humana (ex.: prever a próxima palavra); viabiliza treinar Foundation Models em escala.
- **Aprendizado não supervisionado**: paradigma em que os dados não trazem rótulos e o modelo busca estrutura por conta própria.
- **Aprendizado por reforço**: paradigma em que um agente aprende por tentativa e erro a partir de recompensas, ajustando uma política para maximizar o retorno ao longo do tempo; típico de controle.
- **Aprendizado supervisionado**: paradigma em que cada exemplo de treino vem com a resposta correta (rótulo).
- **Árvore de decisão**: modelo de ML clássico que organiza decisões em sequência de testes sobre atributos; base para florestas aleatórias.
- **Atributo (feature)**: coluna de entrada de um modelo, a partir da qual ele faz a previsão.
- **Attention**: mecanismo que pondera relações entre elementos de uma sequência; núcleo da arquitetura transformer.
- **Balanceamento de classes**: grau em que as categorias de um problema de classificação aparecem em proporções parecidas; desequilíbrio exige precisão/recall/F1 em vez de acurácia, e estratégias como sobre/subamostragem ou pesos por classe.
- **Batch (lote)**: subconjunto do conjunto de treino usado em um único ajuste de parâmetros; cada lote processado = uma iteração.
- **BERT**: modelo de linguagem baseado em transformer (2018), representação bidirecional de contexto; impulsionou a evolução dos Foundation Models.
- **Classificação**: tarefa em que o modelo atribui uma entrada a uma categoria discreta.
- **Clustering**: tarefa em que o modelo agrupa exemplos por semelhança sem categorias predefinidas; típica do não supervisionado.
- **Codificação one-hot**: representação que transforma coluna categórica em várias colunas binárias.
- **Coeficiente de determinação (R²)**: métrica de regressão; fração da variação dos dados explicada pelo modelo (0 a 1, pode ser negativo).
- **Conjunto de teste**: parte dos dados reservada para estimativa final e honesta da generalização; usado uma única vez.
- **Conjunto de treino**: parte dos dados usada para ajustar os parâmetros do modelo.
- **Conjunto de validação**: parte dos dados usada para comparar modelos e escolher hiperparâmetros; não entra no ajuste de parâmetros.
- **Controle**: tarefa em que o modelo escolhe ações que afetam um ambiente ao longo do tempo; típica do RL.
- **Curva de aprendizado**: gráfico do erro em treino/validação ao longo das épocas; a separação entre as curvas sinaliza início do overfitting.
- **Data-centric (lente)**: lente transversal sobre os dados; pergunta se o ganho vem do modelo ou da melhoria do dataset (M3).
- **Deep Learning**: família arquitetural de redes neurais profundas que aprendem representações em camadas; dominante em visão/linguagem a partir de 2012; também um dos 7 eixos técnicos.
- **Descida do gradiente (gradient descent)**: algoritmo padrão de ajuste de parâmetros, move cada parâmetro na direção do gradiente, passo dado pela taxa de aprendizado.
- **Dropout**: regularização que desliga aleatoriamente neurônios durante o treino.
- **Edge (lente)**: lente transversal sobre o local de execução; pergunta se o sistema roda perto do equipamento (restrições de memória/energia/conectividade/latência) ou em servidor com folga (M4).
- **Eixo técnico**: recorte por tecnologia/competência do programa (7 ao todo: LLMs, Visão Computacional, Machine Learning, Real Time Processing, Deep Learning, NLP, Engenharia de Dados); responde "com que tecnologia se resolve", em contraste com a lente.
- **Engenharia de Dados**: eixo técnico dedicado a pipelines que ingerem, transformam e disponibilizam dados.
- **Época**: passagem completa pelo conjunto de treino inteiro.
- **Erro absoluto médio (MAE)**: métrica de regressão; média do valor absoluto dos erros, peso linear.
- **Estado**: no RL, descrição da situação do ambiente observada pelo agente antes de escolher ação.
- **Explainable (lente)**: lente transversal sobre transparência; pergunta se é possível justificar a decisão e quem responde por ela (M5).
- **Exploração versus explotação**: dilema central do RL entre testar ações pouco conhecidas e repetir ações já boas.
- **F1**: métrica de classificação, média harmônica de precisão e recall.
- **Falso negativo**: caso positivo real classificado como negativo; custa caro em falhas/doenças (pesa o recall).
- **Falso positivo**: caso negativo real classificado como positivo; custa caro em spam (pesa a precisão).
- **Ferramenta**: no contexto agêntico, recurso externo acionável pelo modelo (busca web, execução de código, consulta a BD, envio de mensagens) (M2).
- **Few-shot**: uso de Foundation Model com alguns exemplos no prompt (in-context learning); oposto de zero-shot.
- **Fine-tuning**: adaptação de Foundation Model pré-treinado via treinamento adicional sobre dados da tarefa-alvo.
- **Floresta aleatória**: ML clássico; combina muitas árvores de decisão com variações aleatórias.
- **Foundation Model**: modelo de grande escala treinado em dados gerais amplos, base para muitas tarefas via adaptação leve; termo popularizado por relatório de Stanford (2021).
- **Generalização**: capacidade do modelo de ir bem em exemplos novos — único desempenho que interessa na prática.
- **Generativa (lente)**: lente transversal sobre criação; pergunta se o sistema produz artefato novo (M1).
- **Geração**: tarefa em que o modelo produz artefato novo; típica do auto-supervisionado em escala.
- **GPT**: família de modelos de linguagem baseados em transformer, treinados de forma generativa em larga escala.
- **GPU**: placa gráfica; paralelismo que viabilizou o Deep Learning por volta de 2010.
- **Gradient boosting**: ML clássico que combina árvores em sequência, cada uma corrigindo erros da anterior; competitivo com redes profundas em dados tabulares a custo menor.
- **Gradiente**: direção, para todos os parâmetros simultaneamente, em que o erro diminui mais rápido.
- **Hiperparâmetro**: valor de configuração definido antes do treino e não ajustado por ele (ex.: taxa de aprendizado, profundidade de árvore, nº de camadas).
- **ImageNet**: grande base de imagens anotadas (2009-2010) que forneceu escala de dados para treinar redes profundas de visão.
- **In-context learning**: ajuste do comportamento de um Foundation Model só pelos exemplos/instruções do prompt, sem atualização de pesos.
- **Inferência**: uso do modelo já treinado — entrada nova, saída lida, sem alterar parâmetros; ocorre em produção.
- **Iteração**: um único ajuste de parâmetros baseado em um lote.
- **Lente transversal**: ângulo de leitura aplicável a qualquer problema de IA, independente do eixo técnico; 5 no programa: Generativa, Agentic, Data Centric, Edge, Explainable.
- **LLMs (eixo)**: eixo técnico dedicado a Large Language Models; apoia-se em transformer e pré-treino auto-supervisionado.
- **LoRA**: fine-tuning econômico (low-rank adaptation) que ajusta matrizes pequenas somadas aos pesos originais.
- **LSTM**: arquitetura de RNN (1997) para dependências de longo prazo em sequências.
- **Machine Learning (eixo)**: eixo técnico; métodos clássicos e profundos aplicados a problemas tabulares/estruturados.
- **Matriz de confusão**: tabela que organiza acertos/erros de classificação por categoria.
- **Memória**: no contexto agêntico, componente que persiste entre passos do laço de decisão (M2).
- **ML clássico**: família arquitetural anterior ao Deep Learning (árvores, florestas, SVM, regressão); segue sendo a escolha certa para muitos problemas tabulares industriais.
- **Modelo**: função com parâmetros ajustáveis que recebe entrada e produz saída, aprendida a partir de exemplos.
- **NLP (eixo)**: eixo técnico de processamento de linguagem natural.
- **Normalização de batch**: técnica que estabiliza o treino de redes profundas reescalando ativações por lote.
- **Overfitting**: modelo vai bem no treino e mal em dados novos, por ajuste a ruído/particularidades; oposto: underfitting.
- **Parada antecipada (early stopping)**: interrompe o treino quando o erro de validação para de cair e começa a subir.
- **Paradigma de aprendizagem**: a partir de que sinal o modelo aprende (supervisionado, não supervisionado, auto-supervisionado, por reforço); eixo independente da tarefa.
- **Parâmetro**: valor interno do modelo, ajustado pelo treinamento.
- **Perceptron**: modelo de 1958, separa duas classes ajustando pesos; limitado a problemas linearmente separáveis.
- **Perceptron multicamadas (MLP)**: rede totalmente conectada, a mais geral do Deep Learning; perde para CNN/RNN quando há estrutura espacial/sequencial.
- **Política**: no RL, regra que o agente usa para escolher ação a partir do estado; o que se aprende.
- **Pré-treino**: etapa mais cara de construção de um Foundation Model, treino em larga escala sobre dados gerais, geralmente auto-supervisionado.
- **Precisão**: fração das previsões positivas que estava correta.
- **Prompting**: uso de Foundation Model via instrução em linguagem natural, sem treinamento adicional.
- **RAG (retrieval-augmented generation)**: pipeline que compõe recuperação + geração.
- **Raiz do erro quadrático médio (RMSE)**: métrica de regressão; penaliza erros grandes mais que o MAE.
- **Ranking**: tarefa de ordenar candidatos por relevância, frequentemente composta sobre classificação prévia.
- **Real Time Processing (eixo)**: eixo técnico de sistemas com restrições de latência/processamento em fluxo.
- **Recall**: fração dos casos positivos reais capturados pelo modelo.
- **Recompensa**: no RL, sinal (positivo/negativo) devolvido pelo ambiente após cada ação.
- **Recuperação**: tarefa de encontrar, num acervo, os itens mais relevantes para uma consulta.
- **Rede convolucional (CNN)**: arquitetura que explora estrutura espacial de imagens.
- **Rede neural profunda**: rede com várias camadas, aprende representações em camadas a partir de dados brutos.
- **Rede recorrente (RNN)**: arquitetura para dados em sequência com estado interno entre passos.
- **Regressão**: tarefa que produz número contínuo.
- **Regularização**: técnicas que penalizam complexidade para conter overfitting.
- **ReLU**: função de ativação que zera negativos e deixa passar positivos.
- **Representação aprendida**: forma interna de codificação dos dados, subproduto do treino (especialmente auto-supervisionado).
- **Retropropagação**: algoritmo (1986) que tornou prático treinar redes com várias camadas.
- **Sistemas agênticos**: sistemas que envolvem um modelo em laço de decisão com ferramentas e memória, perseguindo objetivo multi-passo (desde 2023).
- **Sobreamostragem (oversampling)**: aumenta presença da classe rara no treino.
- **Subamostragem (undersampling)**: reduz presença da classe abundante no treino.
- **Tarefa**: o que o modelo produz, independente de como aprendeu; 6 no M0: classificação, regressão, clustering, geração, recuperação, controle; eixo independente do paradigma.
- **Taxa de aprendizado (learning rate)**: hiperparâmetro que define o tamanho do passo na descida do gradiente.
- **Token**: unidade de fragmentação de texto para um modelo de linguagem.
- **Transformer**: arquitetura (2017) que processa sequência inteira em paralelo via attention; base dos Foundation Models.
- **Treinamento**: processo de ajuste dos parâmetros para aproximar saídas das desejadas.
- **Underfitting**: modelo simples demais para capturar o padrão; vai mal em treino e em dados novos.
- **Validação cruzada**: reaproveita os dados em múltiplas partições rotativas quando o conjunto é pequeno.
- **Vazamento de dados (data leakage)**: informação do teste influencia treino/escolha de hiperparâmetros; infla estimativa de desempenho.
- **Visão Computacional (eixo)**: eixo técnico de problemas com entrada imagem/vídeo.
- **Zero-shot**: uso de Foundation Model sem exemplo no prompt.

---

## TIPOS DE DESAFIO POSSÍVEIS (para avaliação/instrução com base neste módulo)

1. **Classificar um cenário em paradigma + tarefa**: dado um enunciado de problema industrial (ex.: "uma fábrica quer agrupar máquinas por padrão de vibração sem categorias prévias"), pedir ao aluno que identifique o paradigma (não supervisionado) e a tarefa (clustering), justificando pelos sinais textuais (há rótulos? o sistema age sobre ambiente? o que ele produz?).

2. **Identificar qual(is) lente(s) transversal(is) se aplica(m) a um sistema descrito**, exigindo reconhecer que mais de uma lente pode ser relevante simultaneamente (ex.: um sistema de inspeção visual que também gera imagens sintéticas e precisa justificar rejeições → Data-Centric + Generativa + Explainable).

3. **Apontar o erro conceitual em uma afirmação**, replicando as armadilhas documentadas: por exemplo, uma frase que confunde paradigma com tarefa ("este projeto é supervisionado, logo a tarefa é supervisionada"), ou que trata lentes como mutuamente exclusivas, ou que supõe que "mais recente = melhor" (Foundation Model para um problema tabular simples que uma árvore resolveria melhor).

4. **Preencher uma matriz/quadro em branco**: dar a matriz paradigma×tarefa ou lente×eixo técnico parcialmente preenchida e pedir para completar com "típico/possível/incomum" ou "Central/Recorrente/Pontual", com justificativa.

5. **Escolher a métrica de avaliação correta dado um cenário de custo assimétrico de erro** (ex.: triagem médica → recall; filtro de spam → precisão; dataset de falhas raras → F1/recall, não acurácia), explicando por que a acurácia isolada falharia.

6. **Diagnosticar overfitting/vazamento de dados a partir de uma descrição de experimento** (ex.: "o cientista normalizou todos os dados antes de separar treino/teste e obteve 99% de acurácia" → identificar vazamento de dados e explicar a consequência).

7. **Posicionar uma técnica na família arquitetural correta** (ML clássico / Deep Learning / Foundation Model / Sistemas Agênticos) a partir da descrição de um caso de uso, e justificar com base em dado/custo/latência/auditabilidade, não em data de publicação.

8. **Distinguir eixo técnico de lente transversal** em um enunciado ambíguo que mistura os dois conceitos (pegadinha clássica do material).

9. **Montar um pipeline composto** (ex.: RAG, ranking sobre classificação) e identificar as tarefas/paradigmas de cada etapa separadamente, reconhecendo que métricas e riscos diferem por etapa.

10. **Reconstituir uma definição de glossário a partir de pistas** (dar exemplos e pedir o termo técnico exato, ou o inverso: dar o termo e pedir a definição "quase-exata" do material, testando precisão terminológica).

11. **Aplicar a sequência de 3 perguntas de diagnóstico de paradigma/tarefa** (ou as 5 perguntas das lentes) a um caso novo nunca visto em aula, simulando a transferência de competência (M0.C1) para um problema real de PD&I.

12. **Comparar trade-offs de abordagens** (ML clássico treinado vs. Foundation Model via prompting) em termos de acurácia × custo computacional × tempo de inferência, no estilo do notebook da Aula 2.

13. **Explicar por que um hiperparâmetro específico foi mal escolhido** dado um sintoma (ex.: curva de erro oscilando → taxa de aprendizado alta demais; convergência lenta → taxa de aprendizado baixa demais).

14. **Identificar, em uma descrição de projeto real de PD&I com múltiplos componentes, qual família tecnológica e qual lente cabe a cada componente** (replicando o exemplo do e-book com floresta aleatória + CNN + Foundation Model + agente orquestrador no mesmo projeto).
