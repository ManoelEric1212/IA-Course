###### MODELO DISCRIMINATIVO X MODELO GENERATIVO



Há uma diferença de natureza no ato de produzir que convém explicitar. Quando um

modelo discriminativo recebe uma entrada, sua resposta é, em geral, determinística: a

mesma entrada leva ao mesmo rótulo. Quando um modelo generativo produz, ele amostra de uma distribuição que aprendeu, e por isso o mesmo pedido pode levar a artefatos

diferentes a cada vez, todos plausíveis.

Essa variabilidade não é defeito, é consequência de o modelo ter aprendido um espaço de possibilidades, e não uma única resposta certa. Ela explica por que duas

execuções de um gerador de texto sobre o mesmo tema rendem parágrafos distintos,

e porque controlar essa variação, decidir quanta liberdade dar à geração, é uma preocupação prática da lente generativa, retomada quando se discute o uso responsável

dessas ferramentas.







Essa propriedade sustenta a detecção de anomalias: um modelo que aprendeu a estrutura do funcionamento normal de

um equipamento atribui baixa plausibilidade a leituras atípicas, e isso sinaliza um possível defeito antes mesmo que alguém o rotule. O ponto conceitual é que produzir exemplos e avaliar plausibilidade são duas faces da mesma capacidade, a de ter modelado a

estrutura dos dados, e não apenas a fronteira entre rótulos.





Exemplo aplicado

Numa linha de inspeção visual, um classificador que decide se uma peça tem

ou não defeito é discriminativo: recebe a imagem e devolve um rótulo. Quando

defeitos reais são raros e faltam exemplos para treinar esse classificador,

um modelo generativo de imagem pode sintetizar fotos plausíveis de peças

defeituosas, ampliando o conjunto de treino. Os dois modelos atuam no mesmo

problema, mas com objetivos opostos: um decide, o outro produz.







AVALIAÇÃO DOS MODELOS



DISCRIMINADTIVO: DIRETO;



GENERATIVO: MULTIPLO







&#x20;Essa dificuldade de avaliação é uma das marcas da

lente generativa e uma das principais fontes de risco em projetos que a adotam, porque

uma saída convincente pode esconder um erro que nenhuma métrica simples detecta. 





###### FAMILIAS DE MODELOS GENERATIVOS



\-decoder-only(autorregressiva):



Ela gera a saída um elemento por vez, da esquerda para

a direita, e cada novo elemento é produzido condicionado a tudo o que já foi gerado e

ao pedido inicial



\-encoder-decoder():



traduzir um documento, resumir um texto

longo, converter uma instrução em uma consulta estruturada. Modelos como T5 e BART

popularizaram a família.



A diferença prática em relação à decoder-only é de ênfase: a

encoder-decoder foi desenhada em torno da ideia de ler tudo antes de escrever, o que

a torna natural para transformação condicionada, enquanto a decoder-only trata a entrada como o começo de um texto a continuar.







\-difusão():



Em vez de produzir a saída de uma vez

ou elemento a elemento, ela parte de ruído puro e o remove em passos sucessivos, refinando o artefato até que uma imagem coerente emerja. A intuição é a de uma fotografia

revelada aos poucos a partir de um chuvisco. 





\-modelos multimodais():





não se define por um mecanismo único, e

sim pela capacidade de combinar mais de uma modalidade, como texto e imagem,

numa representação comum.











Dois detalhes de vocabulário acompanham a família autorregressiva e reaparecem na

camada aplicada. O primeiro é a noção de janela de contexto, a quantidade de texto que

o modelo consegue levar em conta de uma vez ao gerar o próximo elemento; ela limita

quanto de um documento cabe num único pedido. O segundo é que o pedido inicial, o

prompt, é parte do mesmo texto que o modelo continua, e não um canal separado de

instrução: o modelo não distingue, por construção, ordem e conteúdo, apenas continua

o texto que recebeu. Essas duas ideias explicam por que formular bem o pedido e respeitar o limite de contexto são preocupações centrais ao usar modelos decoder-only,

assunto que a camada aplicada desenvolve.









&#x20;Modelos como CLIP estabeleceram a ponte

entre texto e imagem, e os modelos de linguagem multimodais recentes incorporam

essa ponte ao próprio fluxo de geração, recebendo imagens junto com o texto do pedido. Em PD\&I industrial, a multimodalidade é o que permite tratar, num só sistema, um

laudo escrito e a imagem que o acompanha, ou uma instrução em texto e a fotografia

da peça a que ela se refere.











Duas observações fecham o panorama. A primeira é que, em alto nível, todas as quatro

famílias geram artefatos; o que as distingue é o tipo de saída e o modo como a entrada

condiciona a geração, e não uma hierarquia de qualidade entre elas. A segunda é que as

fronteiras entre famílias borram na prática: modelos decoder-only recentes incorporam

entradas de imagem e se tornam multimodais, e técnicas de difusão e de autorregressão convivem em sistemas híbridos. Por isso o nome da família é menos importante do

que a pergunta que ele ajuda a responder: que tipo de artefato a solução precisa produzir, e a partir de que entrada. Reconhecer a família certa é um atalho para antecipar

custo, formato de saída e adequação, não um fim em si mesmo.



###### **FOUNDATION MODELS e CAPACIDADE EMERGENTE**



* **escala: parâmetros e volumes de dados**
* **generalização: capacidade de produzir n tarefas sem rotulos**
* **adaptação: fine-tuninge reaproveiotamento de prompt**



**Três traços convivem num Foundation Model. O primeiro é a escala: da ordem de centenas de milhões a centenas de bilhões de parâmetros, treinados sobre volumes enormes**

**de dados. O segundo é a generalidade do dado de treino: o modelo não é treinado para**

**uma tarefa específica, e sim sobre um corpus amplo que cobre muitos domínios, o que**

**lhe dá um repertório geral em vez de uma especialidade estreita. O terceiro, e o mais**

**importante para a prática, é a possibilidade de adaptação leve: em vez de treinar um**

**modelo do zero para cada tarefa, parte-se de um modelo já treinado e o ajusta com pouco esforço**







**capacidade emergente:**



**Habilidade que aparece em modelos de grande escala e não está presente em modelos**

**menores, sem ter sido programada de forma explícita. O termo descreve a observação**

**de que certas habilidades surgem com o aumento de escala; parte da aparência de salto**

**abrupto, porém, depende da métrica usada para medir a habilidade.**







**palavras chaves em foundation models:

prompting estruturado,**

**recuperação de contexto e fine-tuning**













##### 

##### **Prompting estruturado**



**A ideia é obter o comportamento desejado apenas pela composição da entrada que se apresenta ao modelo, sem**

**alterar seus pesos e sem acrescentar conhecimento externo em tempo de execução.**

**Tudo o que o modelo sabe vem do seu conhecimento paramétrico, fixado no pré-treino;**

**tudo o que ele faz com a tarefa vem da forma como o pedido foi escrito.**





**ntes de promover uma alteração, compara-se a saída nova contra um conjunto de casos de referência, do mesmo modo que se roda uma suíte de testes de regressão; sem essa disciplina, uma melhora local pode degradar casos que já funcionavam**

**sem que ninguém perceba até a produção.**





**Sua maior virtude é o custo de montagem quase nulo; sua principal limitação é**

**a reprodutibilidade, porque a saída pode variar com a redação do prompt e com a versão**

**do modelo, o que exige fixar a versão e manter um conjunto de exemplos de regressão.**













**É importante delimitar o que RAG não faz. Ele acrescenta conhecimento ao contexto, mas**

**não altera o comportamento do modelo: não muda seu estilo, seu tom nem o formato**

**com que ele escreve. Um sistema que responde no registro errado, ou que precisa de**

**um formato muito específico de saída, não melhora por recuperar mais trechos, porque**

**o problema não é de conhecimento. Esse é o limite que separa RAG do terceiro padrão,**

**o fine-tuning leve, tratado na próxima seção.**

**A ancoragem é o que dá ao RAG sua propriedade mais valiosa em PD\&I: a rastreabilidade. Como cada trecho do contexto vem de um documento identificável, a resposta pode**

**apontar de onde veio cada afirmação, e um revisor pode conferir. Isso muda a natureza**

**do erro tolerável. Um sistema que alucina sem fonte é difícil de auditar; um sistema**

**que cita a passagem permite que o usuário valide a citação, mesmo quando o modelo**

**interpreta mal o trecho recuperado. Em setores regulados, é essa rastreabilidade, e não**

**a redução de custo, que costuma justificar a adoção do padrão.**











**LoRA**

**LoRA (low-rank adaptation) é a técnica de ajuste eficiente em parâmetros mais**

**usada: em vez de alterar os pesos originais do modelo, treina-se um pequeno**

**conjunto de matrizes adicionais de baixo posto, que são somadas ao modelo na**

**inferência. O modelo-base permanece intacto, e o adaptador resultante ocupa**

**uma fração mínima do espaço**







**O fine-tuning leve é indicado quando o que falta não é conhecimento, mas comportamento estável. Três sinais o recomendam. Primeiro, quando há um estilo, tom ou formato de saída muito específico que nenhum prompt consegue fixar de forma consistente.**

**Segundo, quando uma tarefa especializada se repete em alto volume e vale internalizar**

**as instruções nos pesos, encurtando o prompt e reduzindo o custo por chamada.**



**A chave para**

**essa leitura é separar duas perguntas que costumam vir embaralhadas. A primeira é sobre conhecimento: o que o sistema precisa saber está no modelo, ou precisa vir de fora?**

**A segunda é sobre comportamento: o jeito como o sistema deve responder, em formato,**

**estilo e consistência, é alcançável por instrução, ou precisa ser aprendido? Conhecimento e comportamento são eixos independentes, e cada padrão atua sobre um deles.**























