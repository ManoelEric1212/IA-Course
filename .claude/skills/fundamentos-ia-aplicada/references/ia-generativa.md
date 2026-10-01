# Base de Conhecimento — Módulo IA Generativa (Fundamentos de IA Aplicada, M1)

> Fonte: AULA 1.pdf, Aula 2.pdf, Aula 3.pdf, guia.pdf (checklist T1.3), MAtriz de decisao genAi x ML.pdf (T1.1), MAtriz de riscos.pdf (T1.2), exemplo colab.pdf, IA_010.ipynb, anotações.md.
> Professor: Arthur Nascimento. Curso base de IA, Unidade M1 (competências M1.C1/C2/C3).
> Este documento é fonte de verdade terminológica: os termos e definições abaixo reproduzem a redação exata do material original sempre que possível (glossários, quadros, armadilhas).

---

## 0. Resumo executivo do módulo (progressão lógica das aulas)

O módulo M1 trata a IA Generativa como **uma lente** aplicável a qualquer problema que admita síntese de um artefato — não como tecnologia paralela ou "versão mais moderna" do ML clássico. A progressão é estritamente em três camadas, cada uma condicionando a seguinte:

1. **Camada conceitual (AULA 1 — texto-base da competência M1.C1/C2 inicial).** Estabelece o vocabulário: a diferença de *objetivo de modelagem* entre modelo **discriminativo** (aprende a fronteira entre respostas) e modelo **generativo** (aprende a estrutura dos dados e pode amostrar exemplos novos); as **quatro famílias arquiteturais** que realizam geração em alto nível (decoder-only, encoder-decoder, difusão, multimodais); e o que torna um modelo um **Foundation Model** (escala, generalidade do dado, adaptação leve), incluindo a leitura crítica de **capacidade emergente**. Fecha nomeando — sem detalhar — os três modos de adaptação: prompting, recuperação de contexto (RAG) e fine-tuning leve.

2. **Camada aplicada (Aula 2 — M1.C2).** Detalha os três padrões nomeados ao final da camada conceitual como **padrões de engenharia reconhecíveis numa especificação de solução**: prompting estruturado (ajusta a entrada), RAG mínimo (ajusta o contexto/conhecimento) e fine-tuning leve (ajusta os pesos/comportamento). Introduz a heurística central: os três **não competem, se compõem**, e a ordem de adoção é sempre por **custo crescente** (prompting → RAG → fine-tuning), nunca o inverso. O notebook IA_010 instrumenta exatamente o padrão RAG.

3. **Camada decisória (Aula 3 — M1.C3).** Desloca a pergunta de "qual arquitetura/padrão" para "qual decisão de projeto, defensável perante stakeholders não técnicos". Organiza **cinco decisões encadeadas**: (1) GenAI vs ML clássico — a decisão-mãe, ancorada em cinco eixos (custo, latência, reprodutibilidade, precisão, disponibilidade de dados); (2) modelo aberto vs API gerenciada — onde o modelo roda; (3) in-context learning vs fine-tuning — como adaptar; (4) RAG vs contexto fechado — de onde vem o conhecimento; (5) alocação de custo e fechamento decisório — tradução para cronograma/custo/validação. Essas decisões se registram em três instrumentos: **matriz de decisão T1.1**, **matriz de riscos T1.2** e **checklist T1.3**.

O fio condutor que atravessa as três camadas é a separação de **duas perguntas independentes**: (a) *conhecimento* — o que o sistema precisa saber está no modelo ou precisa vir de fora? → resolvida por prompting (nada externo) ou RAG (conhecimento externo); (b) *comportamento* — o jeito de responder é alcançável por instrução ou precisa ser aprendido? → resolvida por prompting/RAG (instrução) ou fine-tuning (aprendido, gravado nos pesos). Confundir essas duas perguntas é a origem da maior parte das "armadilhas comuns" listadas pelo material.

O notebook prático (IA_010) e o exemplo Colab operacionalizam a camada aplicada (RAG), e os templates T1.1/T1.2/T1.3 operacionalizam a camada decisória.

---

## 1. AULA 1.pdf — "IA Generativa: Foundation Models e panorâmica arquitetural" (camada conceitual, Unidade M1)

Sumário original: 1. Modelos discriminativos e modelos generativos — 2. Panorâmica arquitetural em alto nível — 3. Foundation Models e capacidade emergente — Conclusão.

### 1.1 Modelos discriminativos e modelos generativos

**Conceito-base (M0, recuperado):** um modelo é uma função com valores ajustáveis que recebe uma entrada e devolve uma saída.

**Definições formais:**
- **Modelo discriminativo**: aquele que aprende a fronteira entre as respostas possíveis e, dada uma entrada, devolve um rótulo ou um valor. Aprende a relação entre entrada e resposta — não lhe interessa como os dados de entrada se distribuem no mundo, apenas onde fica a linha que separa uma resposta de outra. Metáfora do curso: é a reta que separa pontos azuis de pontos vermelhos num plano.
- **Modelo generativo**: aquele que aprende a estrutura dos próprios dados e, por isso, pode produzir exemplos novos plausíveis. Aprende como as nuvens de pontos se distribuem (a forma de cada conjunto) e pode sortear um ponto novo plausível que não estava nos dados.
- A diferença está **no objetivo de modelagem, não no tamanho do modelo**. Existem modelos generativos pequenos (treináveis num laptop) e modelos discriminativos enormes.

**Natureza da produção — determinismo vs amostragem:**
- Discriminativo: resposta em geral **determinística** — mesma entrada leva ao mesmo rótulo.
- Generativo: **amostra de uma distribuição aprendida** — o mesmo pedido pode levar a artefatos diferentes a cada vez, todos plausíveis. Essa variabilidade **não é defeito**; é consequência de ter aprendido um espaço de possibilidades. Controlar essa variação (decidir quanta liberdade dar à geração) é preocupação prática central (ligada a *temperatura*, tratado na Aula 2).

**Quadro 1 — Modelo discriminativo versus modelo generativo** (reproduzido):

| Aspecto | Discriminativo | Generativo |
|---|---|---|
| O que aprende | a fronteira entre as respostas | a estrutura dos dados |
| A pergunta que responde | a que classe ou valor corresponde a entrada | como se parece um exemplo plausível |
| O que produz | um rótulo ou um número | um artefato novo (texto, imagem, dado) |
| Custo típico | menor, inferência rápida | maior, inferência mais cara |
| Exemplos | floresta aleatória, regressão, SVM | modelos de linguagem, modelos de difusão |

**Uso menos óbvio — detecção de anomalias:** como o modelo generativo modela quão plausível é um exemplo, pode medir o quanto um caso novo se afasta do normal. Um modelo que aprendeu a estrutura do funcionamento normal de um equipamento atribui baixa plausibilidade a leituras atípicas, sinalizando defeito antes da rotulagem humana. **Ponto conceitual:** produzir exemplos e avaliar plausibilidade são duas faces da mesma capacidade — ter modelado a estrutura dos dados, não apenas a fronteira entre rótulos.

**Tipo de dado necessário para aprender:**
- Discriminativo costuma exigir **pares rotulados** (caro e lento de produzir).
- Muitos generativos aprendem via **aprendizado auto-supervisionado**, a partir de dados não rotulados (o próprio dado fornece o sinal de treino, ex.: prever a próxima palavra). Isso libera o treino da dependência de rotulagem manual — explica por que generativos de grande escala puderam treinar em volumes inalcançáveis por rotulagem manual.

**Fronteira não é rígida:** um modelo generativo de linguagem pode ser usado em tarefa discriminativa (basta pedir que classifique). No sentido inverso, pré-treinamento generativo (prever partes de um texto a partir do resto) costuma ser ponto de partida de modelos depois ajustados a tarefas discriminativas (ex.: família BERT). O que muda é *para que foi treinado e o que consegue produzir*, não uma proibição de uso.

**Exemplo aplicado (inspeção visual):** um classificador que decide se uma peça tem defeito é discriminativo (recebe imagem, devolve rótulo). Quando defeitos reais são raros e faltam exemplos de treino, um modelo generativo de imagem pode sintetizar fotos plausíveis de peças defeituosas, ampliando o conjunto de treino. Os dois atuam no mesmo problema com objetivos opostos: um decide, o outro produz.

**Assimetria de custo/garantia:** generativos de uso geral tendem a ser maiores, exigir mais computação, e entregar saídas que precisam de verificação (plausível ≠ correto: um resumo bem escrito pode ter um número errado; código sintaticamente perfeito pode não fazer o pedido). Discriminativos enxutos respondem em microssegundos, pouca memória, saída verificável entre poucas opções.

**Avaliação dos modelos:**
- Discriminativo: **direto** — compara-se a resposta prevista com a resposta correta e mede-se o acerto.
- Generativo: **múltiplo/difícil** — não há, em geral, uma única resposta certa; um bom resumo, imagem ou trecho de código admitem muitas formas válidas; julgar qualidade exige critérios mais elaborados, muitas vezes humanos. **Essa dificuldade de avaliação é uma das marcas da lente generativa e uma das principais fontes de risco em projetos que a adotam**, porque uma saída convincente pode esconder um erro que nenhuma métrica simples detecta.

**Desfazendo confusão de vocabulário:** "generativo", no sentido técnico, designa uma **propriedade estatística** do modelo (aprender estrutura dos dados e poder amostrar exemplos novos) — não é sinônimo de produto comercial nem de escala particular. Quando o mercado fala em "IA Generativa" normalmente se refere a uma família específica de modelos generativos de grande escala — os **Foundation Models**. O conceito é anterior e mais amplo que qualquer produto.

> **GLOSSÁRIO (do material):** *Modelo discriminativo e modelo generativo* — Modelo discriminativo é aquele que aprende a fronteira entre as respostas possíveis e, dada uma entrada, devolve um rótulo ou um valor. Modelo generativo é aquele que aprende a estrutura dos próprios dados e, por isso, pode produzir exemplos novos plausíveis. A diferença está no objetivo de modelagem, não no tamanho do modelo.

> **ARMADILHA COMUM:** A confusão decisória mais cara desta lente é supor que generativo é sempre superior e tratar todo problema como problema de IA Generativa. Decidir se uma peça tem defeito, prever demanda ou ordenar candidatos são perguntas discriminativas, em que um modelo de ML clássico costuma ser mais barato, mais rápido e mais fácil de verificar. Escolher um modelo generativo nesses casos troca uma solução adequada por uma cara e de saída incerta.

### 1.2 Panorâmica arquitetural em alto nível

Objetivo: situar uma solução, em alto nível, na família arquitetural correta, **sem** entrar em detalhe matemático ou de regime de treinamento (mecanismo de *attention* e pré-treinamento em escala são escopo do curso de LLMs da Fase 2). **Arquitetura = a forma da função que o modelo realiza.**

Quatro famílias cobrem a maior parte do que se observa em PD&I industrial:

**1) Decoder-only (autorregressiva)** — família hoje dominante em texto e código. Gera a saída **um elemento por vez, da esquerda para a direita**, cada novo elemento condicionado a tudo o que já foi gerado + o pedido inicial ("bola de neve"). Quase qualquer tarefa de texto vira "continuação" (responder, traduzir, resumir, classificar). Exemplos: GPT, Llama, Phi.
 - **Vocabulário associado:** *janela de contexto* — quantidade de texto que o modelo consegue levar em conta de uma vez ao gerar o próximo elemento; limita quanto de um documento cabe num único pedido. *Prompt* — é parte do mesmo texto que o modelo continua, **não é um canal separado de instrução**: o modelo não distingue, por construção, ordem e conteúdo, apenas continua o texto recebido.
 - > **GLOSSÁRIO:** *Modelo Autorregressivo* — Modelo que gera a saída um elemento por vez, em que cada novo elemento é produzido condicionado a tudo o que já foi gerado. É a base das arquiteturas decoder-only: o texto cresce passo a passo, e cada passo usa os anteriores como contexto.

**2) Encoder-decoder (sequência a sequência)** — separa explicitamente duas etapas: o *encoder* lê a entrada inteira e a codifica numa representação interna; o *decoder* produz a saída condicionada a essa representação ("ler tudo antes de escrever"). Vantajosa para transformar uma sequência inteira em outra: traduzir, resumir texto longo, converter instrução em consulta estruturada. Exemplos: T5, BART. Diferença prática frente à decoder-only é de **ênfase**, não de capacidade — na prática moderna, muitas tarefas de transformação também são resolvidas por decoder-only.
 - **Nota lateral — encoder-only (não é generativa):** modelos como BERT em uso típico leem a entrada e produzem uma representação numérica (útil para classificar, buscar, agrupar), sem gerar artefato novo. O que coloca um modelo nesta panorâmica não é a tecnologia transformer, e sim o objetivo de produzir uma saída nova.

**3) Difusão** — domina a geração de sinais contínuos (imagens, áudio). Em vez de produzir de uma vez ou elemento a elemento, **parte de ruído puro e o remove em passos sucessivos**, refinando o artefato até emergir algo coerente ("fotografia revelada aos poucos a partir de um chuvisco"). Pode ser condicionada por texto. Exemplo: Stable Diffusion. Em PD&I industrial importa mais pela **síntese de dados** (gerar imagens plausíveis de condição rara para aumentar conjunto de treino escasso) do que pela geração artística.
 - **Nota histórica:** antes da difusão dominar, a abordagem mais conhecida eram as **GANs** (redes generativas adversariais) — duas redes competem, uma gera candidatos e outra tenta distingui-los de exemplos reais, o gerador melhora tentando enganar o avaliador. GANs produziram resultados marcantes mas são **notoriamente instáveis de treinar**; em boa parte das aplicações recentes foram substituídas por difusão, mais estável e mais fácil de condicionar por texto.

**4) Modelos multimodais** — não se definem por um mecanismo único, mas pela **capacidade de combinar mais de uma modalidade** (texto e imagem, p.ex.) numa representação comum. A partir dessa representação compartilhada, o modelo pode descrever uma imagem em texto, buscar imagens por consulta textual, ou gerar imagem a partir de descrição. Exemplo fundador da ponte texto-imagem: CLIP. Em PD&I industrial, permite tratar num só sistema um laudo escrito e a imagem que o acompanha, ou instrução em texto e fotografia da peça referida.

**Eixo conceitual transversal — o que condiciona a geração:** mais esclarecedor na hora de escolher do que o nome da arquitetura é perguntar **o que condiciona a saída**: decoder-only e encoder-decoder diferem em como tratam a entrada condicionante; difusão a recebe como orientação do processo de remoção de ruído; multimodais permitem condicionamento de mais de uma modalidade simultaneamente.

**Duas observações que fecham o panorama:**
1. Em alto nível, todas as quatro famílias geram artefatos; o que as distingue é o **tipo de saída** e **como a entrada condiciona a geração** — não uma hierarquia de qualidade.
2. As fronteiras entre famílias **borram na prática** (decoder-only recentes incorporam entrada de imagem e viram multimodais; difusão e autorregressão convivem em sistemas híbridos). O nome da família é menos importante do que a pergunta que ajuda a responder: *que tipo de artefato a solução precisa produzir, e a partir de que entrada*.

**Uso prático do panorama (heurística de mapeamento):** texto ou código → decoder-only; transformação de um texto inteiro em outro → encoder-decoder (embora decoder-only também resolva); imagem ou áudio → difusão; mais de uma modalidade no problema → multimodal. Não esgota a decisão (envolve custo, disponibilidade, qualidade exigida), mas evita perguntas mal colocadas (ex.: buscar modelo de texto para saída que é imagem).

**Exemplo aplicado (inspeção visual industrial, difusão):** imagens de um defeito raro podem ser escassas para treinar detector confiável. Um modelo de difusão, condicionado por descrição, sintetiza imagens plausíveis daquele defeito e equilibra o conjunto de treino. A escolha da família decorre do tipo de saída desejado (imagem → difusão, não modelo de texto).

**Referência fundadora citada:** VASWANI, A. et al. *Attention Is All You Need*. NeurIPS, 2017 (arxiv.org/abs/1706.03762).

### 1.3 Foundation Models e capacidade emergente

**Três traços de um Foundation Model (já citados em M0, aprofundados aqui):**
1. **Escala** — da ordem de centenas de milhões a centenas de bilhões de parâmetros, treinados sobre volumes enormes de dados.
2. **Generalidade do dado de treino** — não treinado para tarefa específica; corpus amplo cobrindo muitos domínios → repertório geral, não especialidade estreita.
3. **Adaptação leve** (o mais importante na prática) — em vez de treinar do zero para cada tarefa, parte-se de um modelo já treinado e ajusta-se com pouco esforço. É este traço que **desloca o grosso do custo** do treinamento (caro, único) para a adaptação (barata, repetível) — "sem ele, a escala seria apenas uma despesa; com ele, a escala vira um ativo reaproveitável".

**Sobre a escala:** crescer um modelo = aumentar conjuntamente três grandezas — nº de parâmetros, volume de dados de treino, quantidade de computação. A observação de que desempenho melhora de forma relativamente previsível à medida que essas grandezas crescem juntas é chamada **leis de escala** — transformou escala de aposta em estratégia.

**Sobre a generalidade:** viável porque o aprendizado é majoritariamente **auto-supervisionado** (prevê partes do dado a partir de outras partes, sem rótulos humanos) — libera o treino de dados rotulados escassos/caros.

**Três formas de adaptação leve (apenas nomeadas aqui, detalhadas na camada aplicada):**
- **Prompting / aprendizado em contexto** — instrução em linguagem natural, possivelmente com exemplos, sem treinamento adicional.
- **Fine-tuning leve** — continua-se o treinamento sobre dados específicos, ajustando apenas fração pequena dos parâmetros.
- **Recuperação de contexto (RAG)** — não altera o modelo; injeta no próprio pedido o conteúdo externo de que a resposta depende.
- O que todas compartilham: **não repetir o pré-treinamento** — aproveitam o repertório geral existente e o especializam.

**Quadro 2 — Formas de adaptar um Foundation Model** (reproduzido):

| Forma | O que ajusta | Quando tende a caber |
|---|---|---|
| Prompting (em contexto) | nada; usa instrução e exemplos no próprio pedido | tarefas cobertas pelo repertório geral; prototipagem rápida |
| Fine-tuning leve | uma fração pequena dos parâmetros | tarefa recorrente, com dados próprios e formato específico |
| Recuperação de contexto | nada no modelo; injeta documentos no pedido | quando a resposta depende de conteúdo externo e atualizável |

**Etapa de adaptação adicional — alinhamento/instruction-following:** um Foundation Model treinado apenas para prever continuação de texto **não segue instruções naturalmente** — continua o texto, mas não necessariamente faz o que se pede. Para virar assistente útil, aplica-se etapa adicional em que o modelo é ajustado para **seguir instruções** e **alinhar respostas a preferências humanas** (métodos pertencem ao curso de LLMs Fase 2). Importante: o modelo usado na prática raramente é a base crua, é uma versão já adaptada a seguir instruções.

**Capacidade emergente:**
> **GLOSSÁRIO:** *Capacidade emergente* — Habilidade que aparece em modelos de grande escala e não está presente em modelos menores, sem ter sido programada de forma explícita. O termo descreve a observação de que certas habilidades surgem com o aumento de escala; parte da aparência de salto abrupto, porém, depende da métrica usada para medir a habilidade.

Exemplo citado mais discutido: o próprio **in-context learning** (resolver tarefa nova a partir de poucos exemplos no pedido, sem treino adicional) — fraco/ausente em modelos pequenos, utilizável em modelos grandes.

**Cautela interpretativa (leitura técnica vs marketing):** trabalhos recentes mostraram que parte da "emergência abrupta" pode ser, em boa medida, **efeito da métrica escolhida**: métricas que só pontuam acertos perfeitos criam impressão de salto; métricas graduais revelam melhora contínua. Não nega que modelos maiores fazem mais; nega que haja necessariamente um limiar mágico. **Lição dupla:** escala traz ganhos reais, mas "emergência" não deve ser tomada como promessa de que basta crescer o modelo para obter, de forma confiável, qualquer habilidade desejada. Decisões fundadas em emergência *prometida*, e não em avaliação *medida*, são frágeis.

**Migração do risco (consequência mais ampla):** com Foundation Models, a prática se desloca de "treinar modelo específico por tarefa" para "adaptar base compartilhada"; o esforço migra da coleta massiva de dados rotulados para **a engenharia da adaptação e, sobretudo, para a avaliação das saídas**. O risco de projeto está menos na obtenção de dados de treino e mais na verificação de que o modelo adaptado faz o que se espera, com confiabilidade e custo aceitável. Isso leva à ideia de **tratar a avaliação como entregável**, com critérios explícitos do que conta como resposta aceitável — não um detalhe final.

**Exemplo aplicado:** equipe precisa responder perguntas sobre documentação técnica interna de equipamento. Em vez de treinar do zero (exigiria muitos exemplos rotulados), adapta-se um Foundation Model por *prompting*, fornecendo instrução e trechos da documentação no próprio pedido. O esforço migra da coleta de dados de treino para a engenharia do pedido e a verificação das respostas.

> **ARMADILHA COMUM:** Supor que adotar um Foundation Model dispensa a decisão entre IA Generativa e ML clássico, ou que a escala do modelo garante correção. Um modelo grande produz saídas plausíveis, não necessariamente corretas, e continua exigindo verificação. A adoção de uma base ampla é uma escolha com custo de inferência e de avaliação, não um atalho que encerra as decisões do projeto.

**Bibliografia mínima citada (Aula 1):** VASWANI et al. *Attention Is All You Need* (NeurIPS 2017); BOMMASANI, R. et al. *On the Opportunities and Risks of Foundation Models* (Stanford CRFM, 2021); HO, J.; JAIN, A.; ABBEEL, P. *Denoising Diffusion Probabilistic Models* (NeurIPS 2020).
**Bibliografia complementar:** DEVLIN et al. *BERT* (NAACL 2019); WEI, J. et al. *Emergent Abilities of Large Language Models* (TMLR 2022); SCHAEFFER, MIRANDA, KOYEJO. *Are Emergent Abilities of Large Language Models a Mirage?* (NeurIPS 2023); GOODFELLOW, BENGIO, COURVILLE. *Deep Learning* (MIT Press, 2016, cap. 20).

---

## 2. Aula 2.pdf — "IA Generativa: prompting, RAG e fine-tuning como padrões aplicados" (camada aplicada, Unidade M1)

Sumário original: 1. Prompting estruturado — 2. RAG Mínimo — 3. Fine-tuning leve — 4. Reconhecimento de padrões em uma especificação (4.1 Sinais na especificação e o padrão que cada um indica) — Conclusão.

### 2.1 Prompting estruturado

**Definição:** padrão de **menor custo de montagem** entre os três — ponto de partida natural de quase todo projeto generativo. Ideia: obter o comportamento desejado **apenas pela composição da entrada** apresentada ao modelo, **sem alterar pesos** e **sem acrescentar conhecimento externo em tempo de execução**. Tudo que o modelo sabe vem do conhecimento paramétrico (pré-treino); tudo que faz com a tarefa vem de como o pedido foi escrito.

O adjetivo "estruturado" distingue do uso improvisado de um chatbot: o prompt é montado com **partes nomeadas e estáveis**, versionáveis, testáveis e auditáveis como qualquer artefato de software.

**Quatro componentes (Quadro 1 — Anatomia de um prompt estruturado, reproduzido):**

| Componente | Função | Exemplo de Conteúdo |
|---|---|---|
| Instrução de sistema | Fixa papel, restrições e política para toda a sessão | "Você é um triador de chamados; nunca invente campos ausentes" |
| Instrução de tarefa | Descreve o que fazer com a entrada atual | "Classifique a severidade e extraia o equipamento citado" |
| Exemplos (few-shot) | Calibram formato e fronteira de decisão | Dois chamados resolvidos, com a saída no formato alvo |
| Contrato de saída | Especifica o formato verificável da resposta | JSON com campos severidade (enum) e equipamento (string) |

**Conceitos associados:**
- **In-context learning / few-shot / zero-shot** (recuperado do M0): exemplos mostram pares entrada-saída no formato esperado — regime **few-shot** quando há vários exemplos, **zero-shot** quando não há nenhum.
- > **GLOSSÁRIO:** *Saída estruturada (structured output)* — a resposta que o modelo produz em formato verificável por máquina, como um objeto JSON com campos obrigatórios e valores restritos a um conjunto fechado, em vez de texto em prosa. O **function calling** é o mecanismo que impõe esse contrato.
- **Contrato de saída** é o que separa uma demonstração de uma solução: a resposta do modelo raramente é o produto final, alimenta um pipeline a jusante. Prática mínima quando o formato é crítico: **pedir o formato no prompt E validar a saída fora do modelo** (o modelo respeita o contrato na maioria das vezes, não em todas).
- **Prompt como software:** cada parte nomeada é artefato sob controle de versão, com histórico e responsável. Antes de promover alteração, compara-se a saída nova contra **conjunto de casos de referência** — como suíte de testes de regressão; sem essa disciplina, melhora local pode degradar casos que já funcionavam sem que ninguém perceba até produção.
- **Temperatura:** parâmetro de geração — temperatura alta aumenta variabilidade (útil para exploração, nociva para saída estável); reduz-se a temperatura e fixa-se a versão do modelo quando se exige saída estável.
- **Few-shot** calibra formato e fronteira de decisão em casos ambíguos, costuma render mais que instruções longas em prosa.
- **Decomposição:** quebra tarefa complexa em passos menores; às vezes pede que o modelo exponha raciocínio intermediário (*chain-of-thought* implícito) — melhora desempenho em tarefas multi-etapa, **mas** (ressalva do módulo M5) o texto do raciocínio é uma **verbalização plausível, não um registro fiel da computação interna** — não deve ser tratado como explicação auditável.
- Instrução de sistema concentra a **política de resposta** (recusar fora de escopo, não inventar valores ausentes, não extrapolar). Restrições em linguagem natural são **frágeis** (seguidas por regularidade estatística, não garantia) — precisam ser reforçadas por **validação determinista a jusante**, fora do modelo.

**Condições de uso (as três precisam se sustentar simultaneamente):**
1. O conhecimento necessário já está no pré-treino do modelo.
2. O formato de saída é controlável por contrato.
3. O volume e a latência toleram uma chamada de modelo por item.

**Virtude/limitação:** virtude = custo de montagem quase nulo. Limitação = **reprodutibilidade** (saída pode variar com redação do prompt e versão do modelo) → exige fixar versão e manter conjunto de exemplos de regressão.

**Pontos de ruptura (cada um aponta para outro padrão):**
- Conhecimento não cabe na janela de contexto, ou é privado/recente demais, ou resposta precisa citar fonte → caminha para **RAG**.
- Falta não é conhecimento, mas comportamento/formato consistente que nenhum prompt estabiliza → caminho é **fine-tuning leve**.

**Exemplo aplicado (triagem de chamados de manutenção):** planta recebe milhares de chamados em texto livre; classificar por severidade e extrair equipamento, devolvendo JSON (severidade: baixa/média/alta; equipamento). Conhecimento já está no modelo, volume tolera uma chamada por chamado, formato controlável por contrato → caso típico resolvido por prompting estruturado, sem RAG nem fine-tuning.

> **ARMADILHA COMUM — "engenharia de prompt sem teto":** ao primeiro resultado insatisfatório, reação frequente é reescrever o prompt indefinidamente. Quando o problema real é ausência de conhecimento ou ausência de comportamento estável, nenhuma reescrita resolve, e o custo de iteração cresce sem convergir. A decisão correta não é melhorar o prompt, e sim **trocar de padrão**; confundir os dois é o erro decisório mais comum desta camada.

**Para aprofundar citado:** WENG, L. *Prompt Engineering* (lilianweng.github.io, 2023).

### 2.2 RAG Mínimo

**Definição:** RAG (retrieval-augmented generation) é o padrão que resolve a primeira grande ruptura do prompting — **a ausência de conhecimento**. O sistema recupera, a cada pergunta, os trechos mais relevantes de um corpus próprio e os entrega ao modelo como contexto adicional. A geração passa a ser **ancorada** nesses trechos → reduz alucinação e permite citar a fonte. Conhecimento deixa de estar congelado nos pesos e passa a viver num **índice** atualizável sem retreinar nada.

**Pipeline mínimo — duas raias (Figura 1):**
- **Raia de indexação (offline, roda uma vez por versão do corpus):** documento → **chunking** (divisão em trechos) → **embedding** (vetor por modelo de embedding) → armazenado em **índice vetorial**.
- **Raia de consulta (online, a cada pergunta):** pergunta → mesmo modelo de embedding → índice devolve os **k trechos de maior similaridade** → trechos + pergunta montados em contexto → modelo gera resposta.
- "Mínimo" = ausência de refinamentos como **reordenação (reranking)** e **reescrita da consulta** (escopo do curso de eixo Fase 2).

> **GLOSSÁRIO:** *Chunking* — divisão de cada documento do corpus em trechos menores antes da indexação, de modo que a recuperação devolva passagens específicas, e não documentos inteiros. O tamanho do trecho e a sobreposição entre trechos vizinhos são decisões de projeto que afetam diretamente a qualidade da recuperação.

**Mecanismo de recuperação (coração do padrão, também seu ponto mais frágil):** busca por **similaridade no espaço de embeddings** — trechos cujo vetor está próximo do vetor da pergunta são considerados relevantes. Captura **proximidade de sentido**, não coincidência de palavras (ex.: "falha de rolamento" recupera trecho sobre "mancal desgastado" mesmo sem palavras coincidentes). Mas é **cego ao que não recuperou**: se o trecho certo não entra entre os k recuperados, o modelo gera com base em material irrelevante e a resposta fica errada **com aparência de segurança**.

**Regra prática central:** *a qualidade da resposta nunca supera a qualidade da recuperação.*

**Duas alavancas de projeto:**
1. **k** (nº de trechos recuperados) — k baixo arrisca deixar de fora a passagem certa; k alto enche o contexto de ruído, dilui o sinal e encarece a geração. Não há valor universal — calibra-se contra exemplos reais do domínio.
2. **Chunking** (tamanho do trecho e sobreposição) — talvez a alavanca mais subestimada. Trechos longos demais misturam assuntos e degradam precisão; trechos curtos demais fragmentam informação e perdem contexto. Pequena sobreposição entre trechos vizinhos evita cortar frase/procedimento ao meio.

**Avaliação do RAG:** começa **antes da resposta** — mede-se se o trecho que contém a informação correta foi de fato recuperado, porque uma geração impecável sobre contexto errado continua sendo resposta errada.

**O que RAG não faz:** acrescenta conhecimento ao contexto, mas **não altera o comportamento do modelo** — não muda estilo, tom, nem formato de escrita. Um sistema que responde no registro errado não melhora recuperando mais trechos (problema não é de conhecimento). Esse é o limite que separa RAG de fine-tuning leve.

**Valor em PD&I — rastreabilidade:** como cada trecho vem de documento identificável, a resposta pode apontar de onde veio cada afirmação, e um revisor pode conferir. Sistema que alucina sem fonte é difícil de auditar; sistema que cita a passagem permite validar a citação mesmo quando o modelo interpreta mal o trecho. **Em setores regulados, é essa rastreabilidade — não a redução de custo — que costuma justificar a adoção do padrão.**

**Exemplo aplicado (assistente sobre documentação técnica):** fabricante mantém milhares de páginas de manuais que mudam a cada revisão; objetivo é responder perguntas de operadores e indicar a página de origem. Treinar conhecimento nos pesos seria caro e ficaria desatualizado; RAG indexa manuais, recupera trechos por pergunta e ancora a resposta neles, com rastreabilidade. Quando o manual muda, basta reindexar.

**Indicação de uso:** conhecimento privado, volumoso, ou muda mais rápido que ciclo de retreino; solução precisa apontar origem da informação. Custo estrutural: infraestrutura do índice, latência adicional da busca, sensibilidade a chunking e k.

> **ARMADILHA COMUM:** Confundir falta de conhecimento com falta de comportamento. Equipes adotam RAG esperando que corrija estilo/formato das respostas, e se frustram quando recuperar mais contexto não muda o registro do texto. RAG resolve o que o modelo não sabe, não o jeito como ele escreve. Tratar os dois problemas como um só leva a investir no padrão errado e a concluir, equivocadamente, que a abordagem generativa não serve para o caso.

**Para aprofundar citado:** LEWIS, P. et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (NeurIPS 2020, arXiv:2005.11401); GAO, Y. et al. (arXiv:2312.10997, 2023).

### 2.3 Fine-tuning leve

**Definição:** fine-tuning é o **ajuste dos pesos** de um modelo pré-treinado a partir de exemplos próprios, para que ele passe a se comportar de forma específica. O qualificador **"leve"** é o que torna o padrão viável em PD&I: ajusta-se apenas **pequena fração** dos parâmetros (técnicas de ajuste eficiente em parâmetros), cabendo em hardware modesto. Diferente dos outros dois padrões, aqui **o conhecimento muda de lugar**: parte do comportamento desejado passa a residir nos pesos — não no prompt, nem em índice externo.

**PEFT** = família de técnicas de ajuste fino eficiente em parâmetros. Regime de treino mais comum em projetos aplicados: **ajuste supervisionado** (pares de entrada/saída exemplares preparados pela equipe). Regimes de alinhamento por preferência humana existem mas são escopo da Fase 2.

> **GLOSSÁRIO:** *LoRA* (low-rank adaptation) — a técnica de ajuste eficiente em parâmetros mais usada: em vez de alterar os pesos originais do modelo, treina-se um pequeno conjunto de matrizes adicionais de baixo posto, que são somadas ao modelo na inferência. O modelo-base permanece intacto, e o adaptador resultante ocupa uma fração mínima do espaço.

**Três sinais que recomendam fine-tuning leve (todos sobre *como* o modelo responde, não sobre *o que* ele sabe):**
1. Estilo, tom ou formato de saída muito específico que nenhum prompt consegue fixar de forma consistente.
2. Tarefa especializada se repete em alto volume e vale internalizar as instruções nos pesos, encurtando o prompt e reduzindo custo por chamada.
3. Latência/custo de prompts longos repetidos milhões de vezes supera o custo de treinar uma vez.

**Fine-tuning completo vs leve (PEFT):** completo reescreve todos os pesos, exige infraestrutura/dados/orçamento raramente justificáveis em PD&I aplicada, produz modelo inteiro novo para servir/versionar. PEFT inverte a economia: modelo-base único e compartilhado, cada tarefa especializada vira **adaptador pequeno** acoplado na inferência — permite manter vários comportamentos especializados sobre o mesmo modelo, trocando só o adaptador.

**Quadro 2 — Os três padrões aplicados lado a lado** (reproduzido integralmente):

| Eixo | Prompting estruturado | RAG mínimo | Fine-tuning leve |
|---|---|---|---|
| O que altera | A entrada do modelo | O contexto recuperado | Os pesos do modelo |
| Resolve falta de | Nada externo; usa o que o modelo já sabe | Conhecimento | Comportamento ou formato |
| Dados necessários | Poucos exemplos no prompt | Corpus indexável | Pares rotulados de qualidade |
| Atualização | Reescrever o prompt | Reindexar o corpus | Retreinar o adaptador |
| Rastreabilidade da fonte | Não | Sim, pela recuperação | Não |
| Custo de montagem | Quase nulo | Médio (índice e latência) | Alto (dados e treino) |

**Exemplo aplicado (laudos em formato fixo):** laboratório precisa que cada laudo siga estrutura rígida de seções/terminologia/ordem, tom uniforme entre analistas. Tentativas de fixar por prompt produziram variação inaceitável. Fine-tuning leve sobre algumas centenas de laudos bem redigidos internaliza o formato nos pesos, estabiliza a saída e encurta o prompt. Conhecimento clínico vem dos dados de entrada; o que se ensinou foi **a forma de escrever**.

**Aritmética de custo:** prompting e RAG não têm custo de treino, mas pagam a cada chamada por tokens de instrução/contexto — em altíssimo volume, custo recorrente domina. Fine-tuning leve concentra gasto em treino único e, ao internalizar instruções nos pesos, encurta o prompt de cada chamada subsequente, reduzindo custo marginal.

**Avaliação com cuidado extra — esquecimento catastrófico:** mede-se ganho na tarefa-alvo, mas verifica-se também se o ajuste **não degradou capacidades gerais** que o projeto ainda usa (esquecimento catastrófico). Conjunto de avaliação que cubra tarefa especializada + casos gerais de controle é a salvaguarda mínima; sem ele, modelo pode parecer melhor no treinado e pior em tudo o mais, regressão só aparece em produção.

**Pontos de ruptura (mais severos que os outros padrões — raramente é ponto de partida):**
- Exige dados rotulados de qualidade (curadoria é o maior custo escondido — tratado em profundidade no módulo M3).
- Não incorpora bem conhecimento que muda (cada atualização pede novo treino, ao contrário da reindexação barata do RAG).
- Risco de overfitting e de esquecer capacidades gerais se treino for desequilibrado.
- Não oferece rastreabilidade da fonte (o que aprendeu se dissolveu nos pesos).

> **ARMADILHA COMUM — "fazer fine-tuning para ensinar fatos":** tentação de treinar o modelo com documentos internos para que ele os memorize confunde os papéis dos padrões. Conhecimento que muda pertence a um índice de RAG (reindexa-se em minutos); gravá-lo nos pesos resulta em respostas desatualizadas, caras de corrigir e sem citação de fonte. **Fine-tuning ensina comportamento, RAG fornece conhecimento**; inverter os dois é a confusão decisória central desta seção.

### 2.4 Reconhecimento de padrões em uma especificação

**Duas perguntas independentes que organizam a leitura de qualquer especificação:**
1. **Conhecimento:** o que o sistema precisa saber está no modelo, ou precisa vir de fora?
2. **Comportamento:** o jeito como o sistema deve responder (formato, estilo, consistência) é alcançável por instrução, ou precisa ser aprendido?

**Heurística de sequenciamento (ordem de custo crescente, não arbitrária):**
1. Comece sempre por **prompting estruturado** (menor custo, muitas vezes suficiente).
2. Suba para **RAG** quando a especificação revelar necessidade de conhecimento privado, volumoso, recente ou rastreável.
3. Considere **fine-tuning leve** quando falta comportamento estável que nem prompting nem RAG entregam.
> Ecoa, na lente criativa, a mesma disciplina que o módulo M2 aplica à lente da autonomia: **não suba de patamar de custo antes que o patamar atual se mostre insuficiente.**

**Sequência de perguntas diagnósticas:**
1. O conhecimento necessário é geral e estável, ou privado/volumoso/mutável?
2. A saída precisa ser verificável por máquina a jusante, ou citar fonte?
3. Estilo/tom/formato são alcançáveis por instrução, ou já se mostraram instáveis sob prompting?
4. Qual o volume esperado de chamadas e o horizonte do projeto?

**Quadro 3 — Sinais na especificação e o padrão que cada um indica** (reproduzido integralmente):

| Sinal no texto da especificação | Padrão indicado |
|---|---|
| O conhecimento necessário é geral e já consolidado | Prompting estruturado |
| A saída precisa de formato verificável para um pipeline | Prompting estruturado (contrato de saída) |
| Há base de conhecimento privada, extensa ou mutável | RAG mínimo |
| A resposta precisa citar a fonte de origem | RAG mínimo |
| O estilo ou formato precisa ser uniforme e nenhum prompt fixa | Fine-tuning leve |
| Tarefa especializada repetida em altíssimo volume | Fine-tuning leve (custo por chamada) |

**Ponto conceitual mais importante:** abandonar a ideia de que os padrões são alternativas mutuamente exclusivas — **eles se compõem**. Prompting estruturado está presente em **todas** as soluções (mesmo RAG ou modelo ajustado ainda recebem instruções e contrato de saída). RAG e fine-tuning combinam-se com naturalidade: comportamento ajustado por fine-tuning + conhecimento atualizado por RAG.

**Ordem em que se empilham (quando ambos RAG+fine-tuning necessários):** ajustar o comportamento **uma vez** (fine-tuning) e recuperar o conhecimento **a cada chamada** (RAG) — índice é a peça que se atualiza com frequência, adaptador é a peça estável.

**Exemplo aplicado (assistente regulado de seguradora):** respostas precisam citar cláusula exata → RAG sobre acervo de apólices. Precisam seguir tom padronizado e formato fixo exigido por compliance, que nenhuma instrução estabilizou → fine-tuning leve. Toda chamada parte de prompt estruturado com contrato de saída. A especificação pede os **três padrões compostos**, não um só.

> **ARMADILHA COMUM — "o reflexo do mais novo":** diante de um problema, equipes tendem a alcançar primeiro o padrão mais sofisticado que conhecem (RAG ou fine-tuning) sem testar se um prompt estruturado já resolveria. Consequência: custo e complexidade injustificados, mais superfícies de falha para manter. **A decisão defensável parte sempre do padrão mais simples e só sobe quando há evidência de que ele não basta; o ônus da prova é de quem quer subir, não de quem fica.**

**Ponte para a camada decisória:** reconhecer o padrão correto é antecipar o custo que ele impõe ao projeto — cada padrão carrega perfil distinto de custo, latência, dados e rastreabilidade; a escolha (ou a ordem de empilhamento) precisa ser registrada e defendida. Nem todo problema que admite geração pede modelo generativo: classificação de alto volume com rótulos disponíveis costuma ser melhor servida por classificador clássico.

**Bibliografia citada:** LEWIS et al. 2020; OUYANG, L. et al. *Training Language Models to Follow Instructions with Human Feedback (InstructGPT)*, NeurIPS 2022; GAO et al. 2023; VASWANI et al. 2017. **Regulação citada:** UE, Regulamento 2024/1689 (EU AI Act, artigos GPAI 51–55); Brasil, PL 2338/2023 (marco regulatório da IA).

---

## 3. Aula 3.pdf — "IA Generativa: Camada Decisória (decisões correlatas)" (M1.C3)

Sumário original: 1. GenAI versus ML clássico — 2. Modelo aberto versus API gerenciada — 3. In-context learning versus fine-tuning — 4. RAG versus contexto fechado — 5. Alocação de custo e fechamento decisório — 6. Conclusão.

> Nota estrutural: as **cinco decisões formam uma cadeia**, não caixas isoladas — cada escolha fixa um termo do custo total e condiciona a próxima decisão.

### 3.1 GenAI versus ML clássico (a decisão-mãe)

**Reformulação do problema:** a primeira decisão da lente criativa **não** pergunta qual tecnologia é mais avançada — pergunta **qual classe de solução resolve a tarefa ao menor custo de risco**. Tratar IA Generativa como "o passo seguinte e mais sofisticado" em relação ao ML clássico **inverte a ordem correta do raciocínio: a tarefa decide, não a moda.**

**Componentes do "custo de risco":**
- **Risco de erro** — saída incorreta gera retrabalho/prejuízo.
- **Risco de custo** — operação em escala consome orçamento desproporcional ao valor entregue.
- **Risco de manutenção** — solução exige cuidado contínuo que a equipe não sustenta.
- **Risco de conformidade** — saída precisa ser auditável e o modelo escolhido não permite.

**Pergunta âncora (separa dois regimes):**
- Tarefa exige **sintetizar um artefato aberto** (texto livre, código, imagem, resumo) — sem rótulo fixo a prever, a síntese é a própria tarefa → pende fortemente para **GenAI**.
- Tarefa exige **produzir rótulo/valor/estrutura** a partir de entrada bem definida (classificar defeito, prever demanda, agrupar registros) — alvo discreto e mensurável → **ML clássico** é o ponto de partida natural.

**Exemplo aplicado:** classificar chamados de manutenção em categorias já conhecidas, com milhares de exemplos rotulados no histórico — um classificador de gradient boosting resolve com acurácia equivalente a LLM, responde em milissegundos, custa fração por inferência. LLM só se justificaria se a tarefa passasse a exigir **redigir** a resposta ao técnico, não apenas etiquetar.

**Os cinco eixos (estrutura da matriz T1.1):**
1. **Custo** — classificador clássico treinado custa quase nada por chamada; LLM consome tokens/GPU a cada execução.
2. **Latência** — milissegundos (modelo pequeno) vs centenas de ms a segundos (geração).
3. **Reprodutibilidade** — favorece ML clássico: determinístico, auditável; geração varia com temperatura/versão/contexto, dificulta auditoria e regressão.
4. **Precisão** — eixo que mais surpreende: em tarefas tabulares estreitas, discriminativo bem ajustado frequentemente **iguala ou supera** um LLM; vantagem da GenAI aparece sobretudo em linguagem aberta.
5. **Disponibilidade de dados** — inverte o jogo no início: ML clássico exige conjunto rotulado representativo; GenAI opera com poucos exemplos ou nenhum (vantagem de "partida a frio").

> Os cinco eixos **raramente pesam igual** — a tarefa concreta define quais dominam. Ex.: apoio à decisão clínica → precisão e reprodutibilidade acima de custo; assistente interno de baixo risco → tolera variabilidade por rapidez de entrega; serviço de alto volume → custo por inferência domina. **Ordenar os eixos por importância antes de comparar é o que transforma a matriz T1.1 de checklist genérico em argumento específico.**

> **ARMADILHA COMUM:** tratar GenAI como *default* moderno, supondo que um LLM é sempre a versão superior de qualquer solução. Ignora que, sob paridade de precisão, o modelo clássico costuma vencer em custo, latência e auditabilidade. Consequência: sistema mais caro, mais lento e menos reprodutível do que o necessário, defendido pela novidade e não pela adequação à tarefa.

> **ATENÇÃO (sobre o eixo de precisão — onde a intuição mais erra):** em muitas tarefas tabulares, discriminativo bem ajustado e LLM chegam a acurácias próximas; quando isso acontece, **precisão deixa de ser critério de desempate**, e a decisão se resolve nos outros quatro eixos, em geral a favor do modelo clássico (mais barato, mais rápido, mais auditável). **A lição não é que o ML clássico domina sempre, e sim que, sob paridade de precisão, os custos assimétricos decidem.**

**Árvore de decisão GenAI vs ML clássico (Figura 1 / "Figura 4" — três perguntas encadeadas, percorrer de cima para baixo, parar no primeiro desfecho aplicável):**

```
P1: A saída esperada é um artefato aberto (texto, código, imagem, resumo sob demanda)?
 ├── SIM → usar IA Generativa (síntese do conteúdo é a própria tarefa)
 └── NÃO → segue para P2

P2: Existe conjunto de dados rotulado, suficiente, estável e representativo
    para classificação/previsão?
 ├── SIM → usar ML clássico (menor custo, menor latência, maior auditabilidade)
 └── NÃO → segue para P3

P3: Baixa latência, alto volume de processamento ou reprodutibilidade rigorosa
    são requisitos essenciais?
 ├── SIM → usar ML clássico ou um modelo pequeno dedicado
 └── NÃO → usar GenAI como ponte (few-shot ou RAG), reavaliar quando houver mais dados
```
> Critério de base para as três perguntas: os cinco eixos — custo, latência, reprodutibilidade, precisão, disponibilidade de dados.

**Caminho híbrido (desfecho mais útil na prática industrial):** usar GenAI como **ponte** para vencer a partida a frio (sem dados rotulados), prevendo **migração para modelo discriminativo** à medida que o volume rotulado cresce e os eixos de custo/reprodutibilidade passam a pesar mais. **Registrar essa intenção de migração no momento da decisão evita que a solução de partida se cristalize por inércia.**

### 3.2 Modelo aberto versus API gerenciada

**Definição das alternativas:** API gerenciada entrega o modelo como serviço (envia prompt, recebe resposta, sem infraestrutura própria). Modelo de pesos abertos roda no perímetro da própria organização (servidores/nuvem privada controlados pela equipe).

> **GLOSSÁRIO:** *Modelo de pesos abertos (open-weights)* — Modelo cujos parâmetros treinados são distribuídos publicamente, permitindo que a organização o execute, ajuste e audite no próprio ambiente, sem depender do provedor original a cada inferência. Distingue-se de modelo de código aberto, que também libera o código de treino e, por vezes, os dados.

**API gerenciada — vantagens/contrapartidas:** vence em velocidade de partida (não exige GPU/MLOps/provisionamento; custo por token previsível em baixo volume; provedor cuida de disponibilidade/atualização). Contrapartidas: dados saem do perímetro a cada chamada (pode ser inaceitável sob privacidade/residência de dados — módulo M3); custo por token cresce linear com volume; **versão do modelo muda sob a aplicação sem aviso**, afetando reprodutibilidade (saída que passava nos testes ontem pode mudar hoje, quebrando suítes de regressão).

**Pesos abertos — vantagens/contrapartidas:** mantém dados no perímetro (conformidade/privacidade); amortiza custo fixo de infraestrutura, vantajoso em alto volume; **fixa a versão do modelo** (controle de reprodutibilidade). Preço: esforço de provisionar GPU, operar, monitorar, manter — competências que nem todo squad domina.

**Esforço de operação subestimado (ao hospedar pesos abertos):** servir com baixa latência sob carga variável; dimensionar GPU para o pico sem desperdiçar no vale; aplicar **quantização** para caber no hardware disponível (módulo M4); montar monitoramento que detecte degradação antes do usuário.

> **GLOSSÁRIO:** *Dependência de fornecedor (vendor lock-in)* — Situação em que uma solução fica atrelada a um provedor específico, de modo que trocar de fornecedor exige reescrever integrações, revalidar saídas e, por vezes, renegociar custo. Em GenAI, manifesta-se quando prompts, formatos e pós-processamento são calibrados para um modelo proprietário cuja API e versão a organização não controla.

**Heurística de decisão:** baixo volume/prototipagem/PoC → API gerenciada quase sempre vence (tempo de partida). Alto volume sustentado, dados sensíveis, ou exigência regulatória de residência de dados → pesos abertos auto-hospedados tendem a vencer (custo amortizado, controle, conformidade). Existe um **ponto de cruzamento de custo** que depende do volume projetado — estimá-lo honestamente é parte do dever decisório. Estratégia comum: começar com API gerenciada no protótipo, migrar para pesos abertos quando o volume de produção justificar o investimento.

**Exemplo aplicado:** instituição financeira extrai cláusulas de contratos com dados pessoais de clientes — enviar a API externa esbarra em proteção de dados/política interna. Opta por modelo de pesos abertos de porte médio em nuvem privada, aceitando custo de operação por manter processamento no perímetro auditável.

**Ligação com a próxima decisão:** API gerenciada fixa custo por inferência e devolve reprodutibilidade ao provedor; pesos abertos transferem custo de inferência para custo de infraestrutura e **habilitam ajuste fino local**.

### 3.3 In-context learning versus fine-tuning

**Definições:** in-context learning adapta comportamento pela instrução/exemplos no próprio prompt, **sem alterar parâmetros**. Fine-tuning ajusta os pesos a partir de exemplos rotulados, modificando o modelo de forma persistente.

> **GLOSSÁRIO:** *In-context learning (aprendizado em contexto)* — Capacidade de um modelo generativo de ajustar sua resposta a partir de instruções e de exemplos fornecidos no próprio prompt, sem atualização de pesos. Inclui o regime zero-shot, sem exemplos, e o few-shot, com poucos exemplos demonstrativos. **O efeito dura apenas o tempo daquela chamada.**

**In-context learning:** custa pouco para iterar (muda instrução, testa de novo, sem treino). Limitado pela janela de contexto, sensível à redação, cada token adicional de prompt aumenta custo por inferência. Mais expressivo do que parece: permite demonstrar formato esperado, restringir vocabulário, induzir raciocínio em etapas — mas tudo vive dentro da janela de contexto e desaparece ao fim da chamada.

**Fine-tuning (leve):** indicado para fixar estilo/formato/consistência em domínio estreito; reduz tamanho do prompt e latência em produção. Preço: custo inicial de dados rotulados de qualidade + risco de overfit + conhecimento congelado nos pesos.

> **ATENÇÃO — confusão decisória crítica:** usar fine-tuning para injetar conhecimento factual ou volátil no modelo. O ajuste de pesos ensina **forma e comportamento**, não é instrumento adequado para manter fatos atualizados (cabe à recuperação de contexto). Tentar ensinar fatos por fine-tuning resulta em informação que envelhece, custo de retreino a cada mudança, e um modelo que **ainda assim alucina** sobre o que mudou após o treino.

**Exigência sobre dados não diminui com "leve":** fine-tuning leve reduz custo computacional do ajuste, **não** reduz exigência sobre os dados — pede exemplos rotulados representativos em quantidade/qualidade suficientes; curadoria costuma ser o **gargalo real do projeto**, não o treino em si. Conjunto pequeno/enviesado reintroduz overfitting pela porta dos dados.

**Figura 2 — Matriz comparativa entre prompt engineering, RAG e fine-tuning ao longo de sete eixos de decisão** (reproduzida; nota: aqui usa "prompt engineering" como sinônimo de prompting estruturado):

| Eixo de comparação | Prompt engineering | RAG | Fine-tuning |
|---|---|---|---|
| O que ajusta | Instruções e exemplos no prompt | Contexto recuperado de base externa | Pesos do modelo, com dados rotulados |
| Conhecimento volátil | Limitado ao contexto da conversa | Atualiza respostas via recuperação, sem novo treino | Fixa o conhecimento nos parâmetros (não acompanha mudanças) |
| Custo inicial | Baixo | Médio | Alto |
| Custo por inferência | Baixo | Baixo (mencionado como baixo no texto descritivo da figura) | Baixo |
| Esforço de manutenção | Baixo | Médio | Alto (maior) |
| Rastreabilidade da fonte | — (não mencionada/baixa) | Sim, cita diretamente os trechos recuperados | Limitada |
| Risco principal | Fragilidade das instruções e limitação do contexto | Recuperação de informações pouco relevantes | Sobreespecialização do modelo e custo de novos treinamentos |

**Heurística de sequenciamento (decorre da matriz):** comece por **prompt engineering** (mais barato de testar, revela rapidamente viabilidade) → acrescente **RAG** quando precisar de conhecimento externo/extenso/mutável → recorra a **fine-tuning** apenas quando prompt+RAG não garantirem formato/consistência/latência exigidos, e houver dados rotulados estáveis. **Subir de degrau antes da hora gasta esforço que o degrar anterior resolveria.**

**Exemplo concreto do sequenciamento:** padronizar extração de campos de laudos técnicos em formato estruturado. 1º recurso: prompt com poucos exemplos do formato (resolve a maioria a custo quase nulo). Se laudos referenciam normas que mudam: acrescenta-se RAG para trazer a norma vigente. Só quando o formato precisa ser rigorosamente consistente em altíssimo volume e o prompt longo encarece cada chamada: fine-tuning de modelo menor passa a compensar.

### 3.4 RAG versus contexto fechado

**Definições:** contexto fechado = resposta vem apenas do que o modelo aprendeu no treino (pesos). RAG = sistema busca trechos relevantes em base externa e injeta no contexto antes de gerar, fundamentando a saída em fontes consultáveis.

**Contexto fechado:** dispensa infraestrutura de recuperação, responde bem sobre conhecimento estável/geral. Contrapartidas: conhecimento envelhece na data de corte do treino; não oferece atribuição de fonte; tende a alucinar mais sobre fatos de nicho/proprietários nunca vistos.

**RAG corrige os três pontos:** atualiza-se trocando a base (sem retreinar); cita o trecho que fundamentou a resposta (sustenta auditoria, conecta à lente de transparência do módulo M5); reduz alucinação sobre fatos do domínio ao ancorá-los em documentos reais.

**Partes do pipeline (cada uma é ponto de falha e eixo de custo):** documentos → fragmentados em trechos → embeddings → índice; consulta → pergunta vira embedding → recupera trechos próximos → opcionalmente **reordenamento (reranking)** → contexto do modelo. Fragmentar mal, escolher embeddings inadequados ao domínio, ou recuperar trechos demais degrada a resposta tanto quanto modelo fraco. "RAG não é um interruptor que se liga, é um pipeline que se calibra e se mantém."

**Quando NÃO justifica o pipeline:** conhecimento estável, cabe no prompt, não exige atribuição de fonte → contexto fechado entrega resposta com menos partes móveis, menor latência, nenhum custo de índice. Montar RAG nesse caso adiciona complexidade que não se paga.

**Exemplo aplicado:** área de conformidade responde dúvidas sobre normas técnicas revisadas a cada poucos meses. Contexto fechado responderia com base na versão vigente na data de treino, sem saber de revisões recentes e sem indicar fonte. Com RAG sobre repositório atualizado, cada resposta cita o artigo consultado e reflete a versão corrente; atualizar = reindexar.

> **ARMADILHA RECORRENTE:** supor que RAG elimina a alucinação. A recuperação **reduz** a alucinação sobre fatos do domínio, mas **não a anula**: quando o passo de recuperação falha (trecho errado ou nenhum trecho útil), o modelo ainda pode gerar resposta confiante e incorreta a partir do contexto pobre. Confiar cegamente no RAG sem avaliar a qualidade da recuperação apenas **desloca** o ponto de falha, em vez de removê-lo.

**Relação explícita com fine-tuning (confusão decisória mais cara da lente criativa):** problema é manter fatos atualizados → resposta é **RAG**, não fine-tuning. Problema é ajustar forma/estilo/formato de saída → resposta é **fine-tuning**, não RAG. "**Fatos pedem recuperação; comportamento pede ajuste de pesos.**"

**Heurística de escolha:** prefira RAG quando conhecimento é volátil, extenso ou proprietário, e quando atribuição de fonte importa; fique no contexto fechado quando conhecimento é estável, pequeno e cabe no prompt.

**Valor da atribuição de fonte:** em domínios regulados, citar o documento que fundamentou cada afirmação é parte da exigência de transparência (módulo M5) e facilita validação (revisor confere resposta contra fonte sem reexecutar o modelo). Contexto fechado não oferece esse rastro → mais barato de operar, mais difícil de auditar. Essa troca (custo de operação × auditabilidade) **reaparece em quase todas as decisões do módulo**.

### 3.5 Alocação de custo e fechamento decisório

**Quatro fontes de custo de uma solução generativa:**
- **Custo por inferência** — depende de tokens, volume de chamadas, preço.
- **Custo inicial** — setup, eventual fine-tuning, construção de índice.
- **Custo de manutenção** — deriva temporal, reindexação, reavaliação contínua.
- **Custo de risco** (muitas vezes esquecido) — alucinação, propriedade intelectual, conformidade.

> **GLOSSÁRIO:** *Custo de inferência* — Custo incorrido a cada execução do modelo em produção, medido em tokens processados, tempo de computação ou chamadas a uma API. Diferencia-se do custo de treino ou de setup, que ocorre uma vez, e cresce com o volume de uso, o que o torna o componente dominante do custo total em aplicações de alto tráfego.

**Estimar o termo dominante (não exige número exato):** alto tráfego → custo por inferência tende a dominar tudo (reduzir prompt médio ou trocar modelo menor pesa mais que otimizar setup). Baixo tráfego com base de conhecimento grande → custo de manter índice atualizado pode superar custo das chamadas. Identificar qual termo domina **antes de otimizar** evita poupar onde não importa.

**Validação de saídas generativas (cuidado que classificador clássico não exige):** avalia-se com conjuntos de exemplos representativos, critérios explícitos de qualidade e, quando cabe, **modelo juiz (LLM-as-judge)** que pontua respostas — lembrando que **esse juiz também erra** e precisa ser calibrado contra julgamento humano. Suítes de regressão guardam casos que já funcionaram e alertam quando mudança de prompt/modelo/base os quebra. Sem esse aparato, "a qualidade vira impressão, e impressão não sustenta compromisso perante stakeholders."

**Cadeia das cinco decisões (cada escolha fixa um termo do custo total):** GenAI vs ML clássico define o regime inteiro de gasto recorrente → API gerenciada converte custo em preço por token (previsível, linear no volume) / pesos abertos convertem em custo de infraestrutura (fixo, depende de operação) → RAG acrescenta custo de manter índice / fine-tuning antecipa custo de setup e retreino.

> **ARMADILHA/ATENÇÃO — mais cara desta seção:** estimar custo de produção a partir do custo de protótipo. Piloto com baixo volume e prompts curtos sugere gasto modesto que se multiplica quando tráfego real chega, prompts crescem e janela de contexto se enche. Apresentar ao stakeholder o custo do protótipo como se fosse custo de operação gera compromissos que o orçamento não sustenta, e mina a confiança na decisão técnica quando a conta real aparece.

**Três compromissos para traduzir a decisão GenAI vs ML clássico a um stakeholder não técnico:**
1. **Cronograma** — GenAI com partida a frio prototipa rápido, mas construção da avaliação adiciona tempo que precisa ser previsto; ML clássico exige tempo de rotulagem antes de qualquer resultado.
2. **Custo** — apresentar **faixas** de custo total de propriedade (não números pontuais), separando regime de protótipo do regime de produção.
3. **Validação** — reconhecer que saídas não determinísticas exigem instrumentos diferentes de um classificador: conjuntos de avaliação, uso cuidadoso de LLM-as-judge, suítes de regressão (organizados pelo checklist T1.3).

**Traduzir para cada interlocutor (mesma decisão, "moeda" diferente):** quem cuida do orçamento quer previsibilidade de custo e ponto de escala; quem responde pelo produto quer latência aceitável e qualidade percebida; quem responde por risco quer auditabilidade e conformidade.

**Os três instrumentos do módulo (onde os compromissos se registram):**
- **Matriz de decisão T1.1** — documenta GenAI vs ML clássico ao longo dos cinco eixos, com justificativa por eixo.
- **Matriz de riscos T1.2** — mapeia alucinação, viés, propriedade intelectual, custo, deriva temporal, com probabilidade/severidade/mitigação.
- **Checklist T1.3** — verifica se a avaliação das saídas foi montada antes do deploy.

**Tratar a decisão como revisitável:** o ponto de cruzamento entre alternativas se move quando volume cresce, dados rotulados se acumulam, ou regulação muda. **Registrar as premissas que sustentaram a decisão é o que torna a reabertura barata.**

**Síntese da Conclusão (Aula 3):** a decisão GenAI vs ML clássico não mede sofisticação, mede adequação da classe de solução à tarefa ao menor custo de risco. As cinco decisões formam uma cadeia, não caixas isoladas. O que se espera não é dominar cada técnica, mas **justificar uma decisão defensável** — que vira compromisso de cronograma, custo e validação, registrável nos três instrumentos (T1.1, T1.2, T1.3).

---

## 4. Templates e ferramentas de decisão (reprodução integral)

### 4.1 Matriz de decisão GenAI versus ML clássico — Template T1.1 (MAtriz de decisao genAi x ML.pdf)

> Material é um **guia preenchido**, não um exercício de avaliação. Face 1: matriz preenchida para cenário de exemplo. Face 2: instrução de uso (o que cada eixo mede) + segundo exemplo com desfecho oposto.

**Face 1 — Cenário avaliado:** assistente que responde dúvidas técnicas de clientes sobre normas regulatórias de equipamentos médicos. Base documental reúne as normas aplicáveis, revistas a cada poucos meses. Volume estimado: 2.000 consultas/dia. Exigência de rastreabilidade da fonte e de não exposição de dados sensíveis.

**Escala de peso:** 1 = baixo, 2 = médio, 3 = alto. Justificativa deve se ancorar em evidência do cenário, não em preferência geral.

| Eixo de decisão | Peso (1–3) | Alternativa favorecida | Justificativa no caso |
|---|---|---|---|
| Custo (gasto por inferência e operação) | 2 | GenAI | A 2.000 consultas/dia o volume é moderado; custo por inferência da GenAI é aceitável e não inverte a decisão, mas deve ficar sob monitoramento. |
| Latência (tempo de resposta exigido) | 1 | Empate | A tarefa não é de tempo real; resposta na casa de segundos é tolerada, então a latência não decide o caso. |
| Reprodutibilidade (mesma entrada, mesma saída; auditabilidade) | 3 | ML clássico | O eixo puro favorece modelo determinístico; como a tarefa não é classificável, a exigência de auditoria é atendida por RAG com citação da fonte, e não por ML clássico. |
| Precisão (qualidade da saída na tarefa) | 3 | GenAI | A tarefa é gerar resposta em linguagem aberta com citação; classificador não produz esse tipo de saída, então a GenAI é a única que atende. |
| Disponibilidade de dados (volume e estabilidade de dados rotulados) | 3 | GenAI | Não há dataset rotulado de perguntas e respostas; conhecimento está nos documentos de norma, o que favorece GenAI com RAG na partida a frio. |

**Síntese decisória:**

| Campo | Preenchimento |
|---|---|
| Decisão recomendada | GenAI com RAG (contexto recuperado e citação obrigatória da fonte) |
| Eixos que mais pesaram | Precisão e disponibilidade de dados (natureza da saída e ausência de rótulos), com reprodutibilidade atendida pela citação |
| Justificativa integrada | A tarefa é síntese de linguagem aberta sobre conhecimento documental volátil, sem rótulos disponíveis, e o ML clássico não gera a resposta. A GenAI com RAG atende precisão e dados, e a auditoria é coberta pela citação da fonte. O custo é aceitável no volume atual e fica sob monitoramento. |
| Premissas a revisitar | Se o volume crescer a ponto de o custo por inferência dominar, reabrir a alocação de custo (modelo menor, cache). Se a tarefa migrar para classificação de chamados, reabrir a favor de ML clássico. |

**Face 2 — O que cada eixo mede e o que puxa para cada lado:**
- **Custo** — gasto recorrente por inferência + custo de operação. Puxa para ML clássico quando volume alto e tarefa estreita (modelo treinado custa quase nada por chamada). Puxa para GenAI quando volume baixo ou tarefa exige síntese aberta que o clássico não entrega.
- **Latência** — tempo de resposta tolerado pela aplicação. Puxa para ML clássico em tempo real/alto volume (milissegundos importam). Puxa para GenAI quando tolera centenas de ms a segundos.
- **Reprodutibilidade** — mesma entrada → mesma saída; auditabilidade. Puxa para ML clássico quando há exigência de auditoria, testes de regressão estáveis, rastreabilidade. Puxa para GenAI apenas quando variabilidade de saída é aceitável.
- **Precisão** — qualidade da saída na tarefa concreta. Em tarefas tabulares estreitas, GenAI e ML clássico costumam **empatar** (eixo não decide, migra para os outros quatro). Puxa para GenAI sobretudo em linguagem aberta.
- **Disponibilidade de dados** — volume/estabilidade de dados rotulados representativos. Puxa para ML clássico quando há dataset rotulado abundante/estável. Puxa para GenAI na partida a frio (via few-shot ou RAG).

**O que conta como justificativa adequada:** específica do cenário, aponta a evidência que sustenta a tendência. Frases como "GenAI é mais moderna" ou "ML clássico é mais simples" **não servem** — não se ligam ao caso. Justificativa adequada diz, por exemplo, volume estimado, se há dados rotulados, latência exigida, obrigação de auditoria. Quando dois eixos apontam para lados opostos, **o peso decide**, e o conflito deve aparecer na síntese, não ser escondido.

**Segundo exemplo, desfecho oposto:** cenário: classificar 50 mil chamados de manutenção/dia em categorias conhecidas, com histórico rotulado abundante. Desfecho se inverte, ML clássico vence (dados rotulados + saída é rótulo discreto + custo por inferência domina no alto volume).

| Eixo de decisão | Peso | Alternativa favorecida | Justificativa no caso |
|---|---|---|---|
| Custo | 3 | ML clássico | A 50 mil chamadas diárias, o custo por inferência domina; um classificador treinado custa uma fração de uma chamada a LLM por item. |
| Disponibilidade de dados | 3 | ML clássico | Há histórico rotulado abundante e estável, condição ideal para um modelo discriminativo. |

**Observações de uso da T1.1:**
- Ordene mentalmente os eixos por peso antes de decidir — é o peso que transforma a matriz de checklist genérico em argumento específico.
- A árvore de decisão (Figura "M1.fig-4", texto-base IA-011/Aula 3) complementa esta matriz: use-a para chegar a uma **hipótese** de decisão e use a matriz para **justificá-la** eixo a eixo.
- Trate a decisão como revisitável. Registre, na síntese, a premissa que, se mudar, reabriria a escolha.
- A decisão registrada aqui se conecta às demais decisões correlatas do módulo (modelo aberto vs API, in-context vs fine-tuning, RAG vs contexto fechado, alocação de custo) e deve ser lida em conjunto com elas.

### 4.2 Matriz de riscos de soluções generativas — Template T1.2 (MAtriz de riscos.pdf)

> Material é um **guia preenchido**. Face 1: matriz de riscos preenchida para o **mesmo cenário** usado em T1.1. Face 2: como avaliar probabilidade/severidade e o que conta como mitigação adequada. **As categorias de risco e as mitigações típicas são fixas**; a coluna "mitigação adotada" é a escolha feita para o caso.

**Cenário avaliado (igual ao T1.1):** assistente de dúvidas técnicas sobre normas regulatórias de equipamentos médicos, base documental volátil, volume 2.000 consultas/dia, exigência de rastreabilidade e não exposição de dados sensíveis. Solução escolhida em T1.1: **GenAI com RAG**.

**Face 1 — Matriz de riscos preenchida (as 5 categorias de risco são FIXAS — ponto crítico para qualquer desafio):**

| Risco | Probabilidade (B/M/A) | Severidade (B/M/A) | Mitigações típicas (referência) | Mitigação adotada no caso |
|---|---|---|---|---|
| **Alucinação** (saída plausível, mas factualmente incorreta) | Alta | Alta | RAG com atribuição de fonte; verificação humana em casos críticos; restringir o escopo da resposta | RAG sobre o repositório oficial de normas, com citação obrigatória do artigo, e revisão humana quando a confiança da recuperação for baixa. |
| **Viés** (saída que reproduz ou amplifica preconceitos dos dados) | Média | Média | avaliação por slices; conjunto de teste balanceado; revisão de prompts; articulação com o módulo M3 | Avaliação por slices (tipo de norma e categoria de produto), revisão dos prompts e conjunto de teste balanceado entre as normas mais consultadas. |
| **Propriedade intelectual** (uso indevido de conteúdo protegido na entrada ou na saída) | Baixa | Média | política de uso de dados; filtros de saída; rastreabilidade da fonte; cláusulas com o provedor | A base usa normas oficiais de uso permitido; a citação da fonte garante rastreabilidade e há cláusula de uso de dados com o provedor do modelo. |
| **Custo** (gasto em produção acima do previsto) | Média | Média | teto de tokens; cache de respostas; modelo menor; monitoramento de custo por chamada | Teto de tokens por resposta, cache das perguntas mais frequentes, modelo menor na maioria dos casos e monitoramento de custo por chamada no volume de 2.000/dia. |
| **Deriva temporal** (queda de qualidade conforme dados e mundo mudam) | Alta | Alta | reavaliação periódica; reindexação do RAG; suite de regressão; alarme de degradação | Reindexação do RAG a cada atualização de norma, suite de regressão sobre perguntas conhecidas e alarme de degradação de qualidade em produção. |

**Síntese de riscos:**

| Campo | Preenchimento |
|---|---|
| Riscos prioritários (alta probabilidade e alta severidade) | Alucinação e deriva temporal; ambos exigem mitigação ativa antes do deploy. |
| Riscos residuais aceitos (e por quê) | Propriedade intelectual, dada a baixa probabilidade (base de normas oficiais) e a rastreabilidade já garantida pela citação. |
| Responsável pelo monitoramento contínuo | Time de produto para qualidade e custo; jurídico e conformidade para citação e propriedade intelectual. |
| Gatilho de reavaliação (o que dispara revisão do risco) | Publicação de nova versão de norma, ou queda de qualidade detectada pela suite de regressão. |

**Face 2 — Como avaliar probabilidade e severidade:**
- **Probabilidade** — quão provável o risco se materializar neste cenário, dado o modelo, os dados e o uso. Três níveis: baixa/média/alta. Ex.: alucinação tende a ter probabilidade alta em perguntas sobre fatos de nicho e baixa em tarefas de reescrita de texto fornecido.
- **Severidade** — tamanho do dano se o risco ocorrer. Depende do **uso**, não apenas do modelo (ex.: alucinação em rascunho interno = severidade baixa; mesma alucinação em resposta a cliente em setor regulado = severidade alta).
- O **produto informal** de probabilidade × severidade ordena a atenção. Alta probabilidade + alta severidade → "riscos prioritários", exigem mitigação antes do deploy. Baixo impacto → podem ser aceitos como residuais, desde que registrados.

**O que conta como mitigação adequada:** concreta, verificável e proporcional ao risco. "Tomar cuidado com alucinação" **não é mitigação**; "ancorar respostas em RAG com citação da fonte e exigir revisão humana antes do envio ao cliente" **é**. Mitigação adequada nomeia **quem** executa e **quando**. Mitigações que reduzem um risco às custas de agravar outro (ex.: encurtar prompts para cortar custo ao preço de mais alucinação) **devem tornar essa troca explícita**.

**Observações de uso da T1.2:**
- Complemento da T1.1: a T1.1 escolhe a abordagem, a T1.2 mapeia os riscos dessa escolha. Ler as duas em conjunto.
- O eixo de custo dialoga com a alocação de custo (seção 5 da Aula 3): subestimar o custo de produção é, ele próprio, um risco.
- Viés e propriedade intelectual conectam-se à IA responsável do módulo M3; registrar a dependência com aquele módulo quando existir.
- Tratar a matriz como **viva** — o "gatilho de reavaliação" existe porque os riscos mudam com volume, dados e regulação.

### 4.3 Checklist de avaliação — Template T1.3 (guia.pdf)

> Guia preenchido para o mesmo cenário (assistente de dúvidas sobre normas regulatórias, GenAI com RAG), mostrando o estado de uma avaliação **pronta para produção**. Cada item marcado indica verificação satisfeita; em caso real, item não satisfeito vira **lacuna a resolver** ou **risco a registrar explicitamente na matriz T1.2**.

**1. Conjunto de avaliação (eval set):**
- [x] Existe um conjunto de avaliação separado, que não foi usado para ajustar prompts nem para fine-tuning.
- [x] O conjunto cobre os casos típicos e também os casos difíceis e de borda esperados em produção.
- [x] O conjunto inclui exemplos por *slice* relevante (tipo de norma e categoria de produto), e não apenas o caso médio.
- [x] O tamanho do conjunto é suficiente para que uma diferença de qualidade não seja apenas ruído.

**2. Métricas e critérios de qualidade:**
- [x] A métrica escolhida é adequada à tarefa, e não uma métrica genérica aplicada por hábito.
- [x] Os critérios de qualidade estão escritos de forma que duas pessoas avaliem a mesma saída de modo semelhante.
- [x] Há um limiar mínimo de aprovação definido **antes** de olhar os resultados, e não ajustado depois para passar.
- [x] Como a tarefa usa RAG, a qualidade da **recuperação** é avaliada separadamente da qualidade da **geração**.

**3. Avaliação por modelo juiz (LLM-as-judge), quando aplicável:**
- [x] O uso de um modelo juiz é justificado pela inviabilidade de avaliação só por métrica direta ou só por humano.
- [x] O modelo juiz foi calibrado contra julgamento humano em uma amostra, e a concordância é aceitável.
- [x] O prompt do juiz tem critérios explícitos e é versionado junto com o resto da avaliação.
- [x] Há consciência de que o juiz também erra, e casos sensíveis ainda passam por revisão humana.

**4. Suite de regressão:**
- [x] Existe um conjunto de casos que já funcionaram, guardado para detectar regressões.
- [x] A suite roda quando muda o prompt, o modelo, a versão do provedor ou a base de conhecimento.
- [x] Uma falha na regressão **bloqueia o deploy** até ser investigada, em vez de ser ignorada.

**5. Riscos, custo e conformidade:**
- [x] Os riscos estruturais foram mapeados na matriz T1.2 (alucinação, viés, propriedade intelectual, custo, deriva temporal).
- [x] O custo por inferência foi medido com prompts de **tamanho realista**, e não com o protótipo de baixo volume.
- [x] Como há exigência regulatória e de privacidade, a avaliação cobre também conformidade, e não apenas qualidade.
- [x] A rastreabilidade necessária (citação de fonte, log de entrada e saída) está disponível para auditoria.

**6. Prontidão para deploy:**
- [x] Existe um plano de reavaliação periódica para detectar deriva temporal após o deploy.
- [x] Há um responsável nomeado pelo monitoramento contínuo da qualidade em produção.
- [x] Existe um caminho de **rollback** ou de intervenção humana caso a qualidade caia.
- [x] A decisão de avançar para produção foi registrada, com as lacunas remanescentes assumidas de forma explícita.

---

## 5. exemplo colab.pdf

Página de redirecionamento apenas, com link para o Google Colab do notebook prático da Unidade M1 (IA Generativa): `https://colab.research.google.com/drive/1gimCSEf8s-zy31eUAWc--YZp6cnt0TCQO?usp=sharing`. Não contém conteúdo textual adicional — corresponde ao mesmo material instrumentado no arquivo IA_010.ipynb (seção 6).

---

## 6. Notebook IA_010.ipynb — RAG mínimo instrumentado

**Competência:** M1.C2 — reconhecer em uma especificação os três padrões aplicados centrais (prompting estruturado, RAG, fine-tuning leve); **este notebook instrumenta especificamente o padrão de RAG**.

**Pergunta central do notebook:** dada uma pergunta, como o sistema recupera os trechos mais relevantes de um corpus e os usa para ancorar a resposta? E, mais importante: **o que muda na resposta do mesmo modelo quando o contexto recuperado está presente, e quando está ausente?**

**Escolhas de projeto do notebook (relevantes para entender o desenho pedagógico):**
- Roda 100% em CPU, sem GPU, sem chave de API, sem serviços pagos.
- Modelo de embedding: **`all-MiniLM-L6-v2`** (sentence-transformers), ~90 MB.
- Modelo gerador: **`Qwen/Qwen2.5-0.5B-Instruct`** (transformers/PyTorch), ~1 GB — modelo pequeno/aberto deliberadamente; "em produção dariam lugar a modelos maiores". Foco é o **pipeline**, não a capacidade do modelo gerador.
- Índice vetorial: **FAISS** (`faiss-cpu`), `IndexFlatIP` (produto interno). Como os vetores são **normalizados**, produto interno = **similaridade do cosseno**.
- Corpus carregado diretamente no código (`CORPUS_LOCAL`, 12 frases) para garantir reprodutibilidade total e evitar falhas de conexão — fatos técnicos de uma "planta fictícia" (intervalos de lubrificação, pressões nominais, limiares de alarme) que nenhum LLM teria visto no pré-treino: **condição exata em que RAG se justifica** (conhecimento privado, fora dos pesos).

**Pipeline implementado passo a passo:**
1. **Indexação (offline):** `embedder.encode(corpus, normalize_embeddings=True)` → vetores float32 → `faiss.IndexFlatIP(dim)` → `index.add(doc_vectors)`. Dimensão do embedding: 384. Cada documento do corpus já é curto o bastante para servir como um trecho — **sem necessidade de chunking adicional** neste exemplo (com documentos longos, seria necessário).
2. **Consulta (online):** função `recuperar(pergunta, k=TOP_K)` — embute a pergunta no **mesmo espaço vetorial** (ponto crítico: pergunta e corpus precisam usar o mesmo embedder), `index.search(query_vec, k)` devolve `(scores, indices)` já ordenados do mais ao menos similar. `TOP_K = 3`.
3. **Geração com e sem contexto:** duas políticas de sistema distintas:
   - `SISTEMA_SEM`: "Você é um assistente técnico de manutenção industrial. Responda em uma única frase curta e objetiva." (resposta **paramétrica**, só o que o modelo memorizou).
   - `SISTEMA_COM`: "...Use SOMENTE o contexto fornecido para responder. Se a resposta não estiver no contexto, diga que a informação não consta. Responda em uma única frase curta e objetiva." (resposta **ancorada** — política típica de RAG em produção).
   - `prompt_com_contexto` concatena os trechos recuperados (um por linha, prefixados com "- ") antes da pergunta, sob o cabeçalho "Contexto:".

**Resultado empírico da comparação (três perguntas sobre fatos do corpus fictício):**

| Pergunta | Resposta sem contexto (paramétrica) | Resposta com contexto (ancorada) | Score top-1 |
|---|---|---|---|
| De quanto em quanto tempo o mancal do compressor C-12 deve ser lubrificado? | "30 minutos." (inventado/errado) | "O mancal do compressor C-12 deve ser lubrificado a cada 500 horas." (correto) | 0,801 |
| Qual a vazão de projeto da bomba P-5? | "aproximadamente 100 metros cúbicos por segundo." (inventado/errado) | "A vazão de projeto da bomba P-5 é de 30 metros cúbicos por hora." (correto) | 0,761 |
| Qual o torque de aperto dos parafusos do flange F-15? | "aproximadamente 2000 Newton-metros." (inventado/errado) | "O torque de aperto dos parafusos do flange F-15 é de 85 newton-metros." (correto) | 0,923 |

**Leitura pedagógica desse resultado:** sem contexto, o modelo pequeno **inventa um valor plausível mas errado** porque o fato é privado e não está nos seus pesos — é **alucinação com aparência de segurança**. Com contexto recuperado, a resposta reflete o trecho correto e poderia citar a fonte. A diferença entre as colunas **é exatamente o valor que a etapa de recuperação acrescenta**. A qualidade da resposta com contexto depende inteiramente de a recuperação ter trazido o trecho certo — reafirma a regra prática: *a qualidade da resposta nunca supera a qualidade da recuperação*.

**Perguntas para reflexão propostas pelo notebook (sem gabarito, para discussão):**
1. Em quais perguntas a resposta com contexto diferiu substancialmente da resposta sem contexto? O que isso sugere sobre quando RAG agrega valor (e quando não agrega — ex.: pergunta sobre fato geral/público)?
2. A recuperação acrescenta busca vetorial + leitura de k trechos a cada chamada, antes da geração. Em termos de custo/latência por consulta, o que essa etapa adiciona frente a um prompt direto? Em que cenário industrial o custo extra se justifica, e em qual não se justifica?
3. Ao aumentar mentalmente o corpus de 12 para 10 mil trechos: o que muda nas duas alavancas de projeto (chunking e k)? Que novo modo de falha aparece quando há muitos trechos parecidos competindo na recuperação?

**Sugestões de exploração (opcionais, não obrigatórias para rodar o notebook):**
- Variar `TOP_K` (1 e depois 6) e observar efeito nas respostas com contexto.
- Acrescentar ao corpus um trecho que **contradiga** outro (ex.: dois intervalos diferentes para o mesmo mancal) e observar como recuperação/geração lidam com a contradição.
- Fazer pergunta cuja resposta **não** esteja no corpus e verificar se o modelo (com `SISTEMA_COM`) admite que a informação não consta, em vez de inventar.
- Trocar o modelo gerador por um maior (`Qwen/Qwen2.5-1.5B-Instruct`) e comparar qualidade/tempo.
- Trocar o modelo de embedding e ver se a ordem dos trechos recuperados muda.

**Exercício opcional hands-on:** reimplementar a função de recuperação (`minha_recuperacao`) completando dois `# TODO:` — (1) gerar embedding normalizado da pergunta no mesmo espaço do corpus; (2) buscar os k trechos mais similares no índice FAISS (`index.search`). Autoverificação por propriedade (sem revelar a resposta): confere que a função devolve `k` trechos válidos, em ordem de similaridade decrescente (`scores[0] >= scores[-1]`, dentro de tolerância numérica). Gabarito nas duas últimas células, com comentário reforçando: pergunta e trechos precisam usar o **mesmo embedder**; vetores normalizados e em float32 porque o índice é de produto interno (cosseno); `index.search` devolve `(scores, indices)` já ordenados do mais ao menos similar.

**Vocabulário listado explicitamente pelo notebook (seção "Vocabulário utilizado"):** prompting; RAG (retrieval-augmented generation); embedding; similaridade vetorial (cosseno); chunking; índice vetorial (FAISS); recuperação (retrieval) top-k; contexto; **geração ancorada (grounding)**; alucinação.

---

## 7. Anotações pessoais do aluno (anotações.md) — integração e cruzamento

O arquivo de anotações do aluno é majoritariamente um **resumo/transcrição parcial da AULA 1 e parte da Aula 2** (discriminativo x generativo, famílias de modelos generativos, Foundation Models/capacidade emergente, prompting estruturado, RAG, LoRA/fine-tuning). Todo o conteúdo já está incorporado e expandido nas seções 1 e 2 acima, com a redação completa do e-book (as anotações eram trechos truncados/resumidos do mesmo texto). Pontos que vale destacar como **grifos de ênfase do próprio aluno** (sinalizam onde ele considerou mais importante fixar, mesmo com formatação truncada no arquivo original):
- Destacou separadamente "AVALIAÇÃO DOS MODELOS: DISCRIMINATIVO: DIRETO; GENERATIVO: MÚLTIPLO" como contraste central.
- Destacou as quatro famílias generativas com marcadores próprios (decoder-only/autorregressiva; encoder-decoder; difusão; multimodais) — confirma que essa taxonomia é o núcleo factual mais "decorável" da Aula 1.
- Destacou os três traços de Foundation Model em formato de bullet (escala; generalização; adaptação) — a mesma estrutura do e-book.
- Capturou a definição de LoRA quase literalmente igual ao glossário oficial.
- Capturou a frase-chave sobre RAG: "RAG não muda o comportamento do modelo: não muda seu estilo, seu tom nem o formato" e a frase sobre rastreabilidade como o que "justifica a adoção do padrão" em setores regulados — ambas reproduzidas integralmente na seção 2.2 acima.
- Capturou a separação dos "dois eixos independentes" (conhecimento vs comportamento) que é a heurística-chave da seção 2.4.

**Conclusão da integração:** não há conceito nas anotações que contradiga ou adicione algo ausente do material oficial — elas são subconjunto fiel da Aula 1/2. A base de conhecimento abaixo (seções 8–10) já incorpora tudo.

---

## 8. Glossário técnico consolidado (termo: definição)

- **Modelo discriminativo**: aprende a fronteira entre as respostas possíveis; dada uma entrada, devolve um rótulo ou um valor. Resposta determinística (mesma entrada → mesmo rótulo). Avaliação direta (compara-se com resposta correta).
- **Modelo generativo**: aprende a estrutura dos próprios dados; pode produzir exemplos novos plausíveis, amostrando de uma distribuição aprendida. Resposta não determinística (mesmo pedido pode gerar artefatos diferentes, todos plausíveis). Avaliação múltipla/difícil (sem resposta única correta).
- **Aprendizado auto-supervisionado**: regime em que o próprio dado fornece o sinal de treino (ex.: prever a próxima palavra a partir das anteriores), sem depender de rótulos humanos — permite treinar sobre dados não rotulados, abundantes.
- **Decoder-only (autorregressiva)**: família que gera a saída um elemento por vez, da esquerda para a direita, cada elemento condicionado a tudo que já foi gerado + pedido inicial. Base da maioria dos LLMs atuais (GPT, Llama, Phi).
- **Modelo autorregressivo**: modelo que gera a saída um elemento por vez, cada novo elemento condicionado a tudo o que já foi gerado — base das arquiteturas decoder-only.
- **Janela de contexto**: quantidade de texto que o modelo consegue levar em conta de uma vez ao gerar o próximo elemento; limita quanto de um documento cabe num único pedido.
- **Prompt (em decoder-only)**: parte do mesmo texto que o modelo continua — não é canal separado de instrução; o modelo não distingue, por construção, ordem e conteúdo.
- **Encoder-decoder (sequência a sequência)**: família que lê a entrada inteira (encoder) antes de produzir a saída condicionada (decoder) — natural para tradução, sumarização, transformação condicionada. Ex.: T5, BART.
- **Encoder-only**: lê a entrada e produz representação numérica útil para classificar/buscar/agrupar, sem gerar artefato novo — **não é generativo** (ex.: BERT em uso típico).
- **Difusão**: parte de ruído puro e o remove em passos sucessivos até emergir um artefato coerente (imagem/áudio); pode ser condicionada por texto. Ex.: Stable Diffusion.
- **GAN (rede generativa adversarial)**: duas redes competem (gerador vs discriminador/avaliador); gerador melhora tentando enganar o avaliador. Notoriamente instáveis de treinar; em grande parte substituídas por difusão.
- **Modelos multimodais**: combinam mais de uma modalidade (texto, imagem) numa representação comum, permitindo descrever, buscar ou gerar entre modalidades. Ex.: CLIP.
- **Foundation Model**: modelo de grande escala (centenas de milhões a centenas de bilhões de parâmetros), treinado sobre corpus geral e amplo, que serve de base reaproveitável para muitas tarefas via adaptação leve. Três traços: escala, generalidade do dado, adaptação leve.
- **Leis de escala**: regularidade observada de que o desempenho melhora de forma relativamente previsível à medida que parâmetros, dados e computação crescem juntos.
- **Capacidade emergente**: habilidade que aparece em modelos de grande escala e não está presente em modelos menores, sem ter sido programada explicitamente; parte da aparência de salto abrupto depende da métrica usada para medir a habilidade.
- **In-context learning (aprendizado em contexto)**: capacidade de um modelo generativo ajustar sua resposta a partir de instruções/exemplos no próprio prompt, sem atualização de pesos. Inclui zero-shot (sem exemplos) e few-shot (poucos exemplos). Efeito dura apenas o tempo daquela chamada.
- **Prompting estruturado**: padrão de obter comportamento desejado apenas pela composição da entrada, sem alterar pesos nem acrescentar conhecimento externo; prompt montado com partes nomeadas, versionáveis, testáveis, auditáveis.
- **Instrução de sistema**: componente do prompt que fixa papel, restrições e política de resposta para toda a sessão.
- **Instrução de tarefa**: componente do prompt que descreve o que fazer com a entrada específica.
- **Exemplos (few-shot)**: pares entrada/saída no formato esperado, incluídos no prompt para calibrar formato e fronteira de decisão.
- **Contrato de saída**: especificação explícita do formato que a resposta deve ter para ser consumida pelo sistema a jusante.
- **Saída estruturada (structured output)**: resposta em formato verificável por máquina (ex.: JSON com campos obrigatórios e valores restritos), em vez de texto em prosa.
- **Function calling**: mecanismo que impõe o contrato de saída estruturada.
- **Temperatura**: parâmetro de geração que controla a variabilidade da saída; alta = mais exploração/variação, baixa = mais estabilidade.
- **RAG (retrieval-augmented generation)**: padrão que recupera, a cada pergunta, trechos relevantes de um corpus próprio e os entrega ao modelo como contexto adicional, ancorando a geração e permitindo citar a fonte.
- **Chunking**: divisão de cada documento do corpus em trechos menores antes da indexação, para que a recuperação devolva passagens específicas, não documentos inteiros.
- **Embedding**: representação vetorial de um texto num espaço de muitas dimensões, em que proximidade mede proximidade de sentido (não de grafia).
- **Índice vetorial**: estrutura (ex.: FAISS) que armazena embeddings para busca eficiente por similaridade.
- **Top-k (recuperação)**: os k trechos de maior similaridade devolvidos pelo índice para uma dada pergunta.
- **Reranking (reordenação)**: refinamento (fora do escopo "mínimo") que reordena os trechos recuperados antes de entrarem no contexto.
- **Geração ancorada (grounding)**: geração fundamentada em contexto recuperado/fornecido, em oposição a uma resposta puramente paramétrica.
- **Alucinação**: saída plausível, porém factualmente incorreta.
- **Fine-tuning**: ajuste dos pesos de um modelo pré-treinado a partir de exemplos próprios, para que passe a se comportar de forma específica — altera o modelo de forma persistente.
- **Fine-tuning leve / PEFT (ajuste fino eficiente em parâmetros)**: ajusta-se apenas uma pequena fração dos parâmetros, cabendo em hardware modesto.
- **LoRA (low-rank adaptation)**: técnica PEFT mais usada — treina pequeno conjunto de matrizes adicionais de baixo posto, somadas ao modelo na inferência; modelo-base permanece intacto.
- **Esquecimento catastrófico**: degradação de capacidades gerais do modelo como efeito colateral do fine-tuning em uma tarefa específica.
- **Modelo de pesos abertos (open-weights)**: modelo cujos parâmetros são distribuídos publicamente, permitindo execução/ajuste/auditoria no próprio ambiente da organização — distinto de modelo de código aberto (que também libera código de treino/dados).
- **Dependência de fornecedor (vendor lock-in)**: situação em que uma solução fica atrelada a um provedor específico, tornando a troca custosa (reescrever integrações, revalidar saídas, renegociar custo).
- **Custo de inferência**: custo incorrido a cada execução do modelo em produção (tokens, tempo de computação, chamadas de API); cresce com o volume de uso.
- **Contexto fechado**: geração que se apoia apenas no conhecimento aprendido no treino (pesos), sem recuperação externa.
- **LLM-as-judge (avaliação por modelo juiz)**: uso de um modelo para pontuar/avaliar respostas de outro modelo, calibrado contra julgamento humano.
- **Suíte de regressão**: conjunto de casos já funcionais, usado para detectar se uma mudança (prompt, modelo, versão, base) quebrou algo que funcionava.
- **Quantização**: técnica para reduzir o tamanho/exigência de hardware de um modelo, permitindo caber em hardware disponível (tratada em detalhe no módulo M4).
- **Deriva temporal**: queda de qualidade da solução conforme os dados e o mundo mudam ao longo do tempo.
- **Matriz de decisão T1.1**: instrumento que documenta a escolha GenAI vs ML clássico ao longo dos cinco eixos (custo, latência, reprodutibilidade, precisão, disponibilidade de dados), com peso e justificativa por eixo.
- **Matriz de riscos T1.2**: instrumento que mapeia os riscos estruturais de uma solução generativa (alucinação, viés, propriedade intelectual, custo, deriva temporal) por probabilidade, severidade e mitigação.
- **Checklist T1.3**: instrumento que verifica se a avaliação das saídas foi montada antes do deploy (eval set, métricas, LLM-as-judge, suíte de regressão, riscos/custo/conformidade, prontidão para deploy).

---

## 9. Armadilhas comuns (consolidado, por origem)

1. **(Aula 1 — discriminativo/generativo)** Supor que generativo é sempre superior e tratar todo problema como problema de IA Generativa — quando a pergunta é discriminativa (classificar, prever, ordenar), ML clássico costuma ser mais barato, rápido e fácil de verificar.
2. **(Aula 1 — Foundation Models)** Supor que adotar um Foundation Model dispensa a decisão GenAI vs ML clássico, ou que escala garante correção — modelo grande produz saídas plausíveis, não necessariamente corretas; continua exigindo verificação.
3. **(Aula 2 — prompting)** "Engenharia de prompt sem teto": reescrever o prompt indefinidamente quando o problema real é falta de conhecimento ou de comportamento estável — a decisão correta é trocar de padrão, não insistir.
4. **(Aula 2 — RAG)** Confundir falta de conhecimento com falta de comportamento: esperar que RAG corrija estilo/tom/formato — RAG resolve o que o modelo não sabe, não o jeito como ele escreve.
5. **(Aula 2 — fine-tuning)** Fazer fine-tuning para ensinar fatos (em vez de comportamento) — gera respostas desatualizadas, caras de corrigir, sem citação de fonte. Fine-tuning ensina comportamento; RAG fornece conhecimento.
6. **(Aula 2 — composição de padrões)** "O reflexo do mais novo": montar RAG ou fine-tuning sem testar primeiro se um prompt estruturado já resolveria — custo e complexidade injustificados; o ônus da prova é de quem quer subir de patamar.
7. **(Aula 3 — GenAI vs ML)** Tratar GenAI como *default* moderno, supondo que LLM é sempre superior — sob paridade de precisão, o modelo clássico costuma vencer em custo, latência e auditabilidade.
8. **(Aula 3 — precisão)** Não reconhecer paridade de precisão entre GenAI e ML clássico em tarefas tabulares — quando há paridade, os outros quatro eixos decidem (geralmente a favor do clássico).
9. **(Aula 3 — in-context vs fine-tuning)** Usar fine-tuning para injetar conhecimento factual ou volátil — ajuste de pesos ensina forma/comportamento, não é instrumento para manter fatos atualizados.
10. **(Aula 3 — RAG vs contexto fechado)** Supor que RAG elimina a alucinação — reduz, mas não anula; falha de recuperação ainda gera resposta confiante e errada, apenas deslocando o ponto de falha.
11. **(Aula 3 — custo)** Estimar custo de produção a partir do custo de protótipo — volume real, prompts maiores e janela de contexto cheia multiplicam o gasto; gera compromissos que o orçamento não sustenta.

---

## 10. Tipos de desafio que um instrutor poderia propor com base neste conteúdo

1. **Classificação de cenário (discriminativo vs generativo):** dado um caso de PD&I industrial, pedir para classificar se a tarefa é discriminativa ou generativa e justificar com a pergunta âncora ("que pergunta o modelo responde?").
2. **Identificação de família arquitetural:** dado um tipo de artefato de saída e entrada (ex.: "gerar imagem de defeito raro a partir de descrição textual"), pedir para apontar a família (decoder-only/encoder-decoder/difusão/multimodal) e justificar pelo tipo de condicionamento.
3. **Diagnóstico de Foundation Model vs capacidade emergente:** pedir para distinguir um ganho real de escala de uma "promessa de emergência" mal fundamentada, usando o argumento da métrica (Schaeffer et al.).
4. **Reconhecimento de padrão numa especificação:** dar uma especificação de solução em prosa (com pistas misturadas sobre conhecimento/comportamento/volume) e pedir que o aluno identifique qual(is) padrão(ões) — prompting, RAG, fine-tuning — se aplicam, e em que ordem devem ser empilhados.
5. **Diagnóstico de armadilha:** apresentar um diálogo ou decisão de projeto com um erro típico embutido (ex.: equipe fazendo fine-tuning para "ensinar" uma tabela de preços que muda todo mês) e pedir para identificar a armadilha e a correção.
6. **Preenchimento da matriz de decisão T1.1:** dado um cenário novo (com volume, dados disponíveis, exigências de latência/auditoria), pedir para preencher os cinco eixos com peso, alternativa favorecida e justificativa específica do cenário (não genérica), e produzir a síntese decisória.
7. **Preenchimento da matriz de riscos T1.2:** dado o mesmo cenário (ou outro), pedir para avaliar probabilidade/severidade das cinco categorias fixas (alucinação, viés, propriedade intelectual, custo, deriva temporal) e propor mitigação adotada concreta (com responsável e gatilho).
8. **Auditoria via checklist T1.3:** apresentar uma solução "quase pronta para produção" com uma ou mais lacunas deliberadas (ex.: sem suíte de regressão, sem eval set separado) e pedir para apontar os itens não satisfeitos do checklist e as consequências.
9. **Percurso pela árvore de decisão GenAI vs ML clássico:** dar um cenário e pedir que o aluno percorra as três perguntas encadeadas da árvore e chegue ao desfecho correto, citando os cinco eixos.
10. **Decisão correlata — modelo aberto vs API gerenciada:** cenário com dados sensíveis + alto volume projetado; pedir justificativa da escolha e estimativa do raciocínio sobre o "ponto de cruzamento de custo".
11. **Decisão correlata — RAG vs contexto fechado:** cenário em que o conhecimento é estável e pequeno (deveria usar contexto fechado) vs cenário em que é volátil/volumoso (deveria usar RAG); testar se o aluno reconhece quando RAG é *over-engineering*.
12. **Exercício prático de RAG (baseado no notebook IA_010):** pedir para implementar/explicar a função de recuperação (embedding da pergunta no mesmo espaço do corpus, busca top-k em índice FAISS por similaridade de cosseno via produto interno em vetores normalizados), ou interpretar uma tabela de resultados "com e sem contexto" e explicar a diferença em termos de alucinação/ancoragem.
13. **Calibração de alavancas de RAG:** cenário com corpus crescendo de 12 para 10 mil trechos; pedir para discutir o que muda em chunking, k, e nos modos de falha (ruído, trechos concorrentes/contraditórios).
14. **Tradução para stakeholder:** pedir para traduzir uma decisão GenAI vs ML clássico em três compromissos (cronograma, custo em faixas, validação) para três públicos diferentes (orçamento, produto, risco/conformidade).
15. **Identificação de glossário/vocabulário técnico:** questões de "termo: definição" cobrando a redação exata dos glossários oficiais (ex.: definir LoRA, capacidade emergente, chunking, custo de inferência, vendor lock-in).
16. **Cadeia de decisões:** pedir para explicar por que as cinco decisões (GenAI vs ML; modelo aberto vs API; in-context vs fine-tuning; RAG vs contexto fechado; alocação de custo) formam uma cadeia e não escolhas independentes, com exemplo de como uma decisão anterior condiciona a seguinte.
17. **Questão de armadilha composta:** cenário onde múltiplas armadilhas se sobrepõem (ex.: equipe usa fine-tuning para fatos voláteis E estima custo a partir do protótipo) — pedir para separar os dois erros e propor a correção para cada um.

---

*Fim do documento. Este material cobre a totalidade textual dos sete PDFs do módulo IA GENERATIVA, o notebook IA_010.ipynb (27 células) e o arquivo anotações.md, com reprodução literal de quadros, glossários, armadilhas e exemplos aplicados sempre que extraídos do texto original.*
