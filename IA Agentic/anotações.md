Um agente, neste curso, é um sistema de software que recebe um objetivo, decide por

conta própria quais ações tomar para alcançá-lo, executa essas ações sobre um ambiente por meio de ferramentas, observa o resultado e repete o processo até concluir a

tarefa ou atingir uma condição de parada.



###### Reasoning engine

Componente de um agente que decide, a cada passo do laço, qual será a próxima

ação. Lê o estado da tarefa e produz uma decisão (chamar uma ferramenta,

registrar um resultado ou parar). Em geral é desempenhado por um modelo de

linguagem, mas a função de decisão é distinta do modelo que a executa.





\-Tools:as funções e APIs que o agente pode

invocar para agir sobre o mundo, como consultar um banco de dados, chamar um serviço externo, executar um cálculo determinístico ou escrever um arquivo. 



\- memória:A memória de curto prazo

é o contexto imediato da tarefa em andamento, o histórico de ações e observações

que cabe na janela do modelo e que é reapresentado a cada decisão.





A memória de

longo prazo, quando o sistema a exige, é um armazenamento mais duradouro, externo

à janela, que sobrevive a uma execução e de onde o agente recupera informação sob

demanda.





\- planning:a capacidade de decompor um

objetivo amplo em uma sequência de subtarefas.



Os três componentes,

tools, memória e planning, não operam isoladamente: é o reasoning engine que os mobiliza, decidindo a cada passo qual tool chamar, o que consultar na memória e quando

o plano precisa de ajuste.



trace:o registro dessas decisões







Assistente x Agente





Um assistente que consulta o tempo e responde fez

uma chamada de ferramenta, mas não iterou; um agente que consulta, avalia o retorno,

decide consultar outra coisa e só então responde, esse iterou.







Cada degrau do continuum pode ser ilustrado com um caso de PD\&I industrial. No degrau do chatbot está um assistente que responde dúvidas sobre uma norma técnica

a partir do texto que lhe foi dado, sem consultar nada externo. No degrau seguinte, do

assistente com uma chamada de ferramenta, está um sistema que, ao receber a pergunta sobre um equipamento, consulta uma vez a ficha desse equipamento e responde,

num único passo.



&#x20;No degrau do agente single-loop está um sistema que, diante de um

diagnóstico ambíguo, decide consultar o histórico, avalia o retorno, decide consultar o

manual da peça suspeita e só então conclui. No degrau de maior autonomia está um

sistema que planeja uma investigação completa, distribui subtarefas e consolida os

achados. O mesmo domínio comporta os quatro degraus; o que muda é a abertura do

problema que se quer resolver.



##### tool calling:mecanismo que permite a um modelo de linguagem agir, e não apenas escrever



Em vez de texto livre, o modelo emite uma chamada estruturada,

com o nome da ferramenta e os argumentos, segundo um esquema declarado. O

sistema executa e devolve o resultado como nova observação. É o contrato que

liga decisão a ação.





Uma armadilha frequente é supor que a arquitetura agentic é o default moderno, a ser adotado por ser o mais avançado. A consequência é o over-engineering: equipes envolvem em um laço autônomo tarefas cujo caminho é conhecido de antemão, pagando custo, latência e imprevisibilidade sem ganho

correspondente. Autonomia é uma escolha condicionada ao problema, não

um patamar a ser alcançado.













##### Panorama de paradigmas em alto nível



* ###### &#x20;ReAct:reasoning and acting:

Nele, o agente intercala passos de raciocínio explícito e passos de ação num mesmo laço: registra

um raciocínio sobre o que precisa, escolhe uma ação, observa o resultado, raciocina

de novo à luz da observação e prossegue.



Em prosa, um trace de ReAct se lê como

uma alternância de pensamento, ação e observação: o agente pensa que precisa de

um dado, age consultando uma fonte, observa o valor retornado, pensa que ainda falta

outro dado, age de novo, e assim por diante até concluir.



Exemplo:

O agente raciocina que

precisa primeiro da medição do lote, age consultando a tool de medições, observa o

valor retornado; raciocina que precisa agora da especificação de tolerância, age consultando a tool de especificações, observa o intervalo permitido; raciocina que pode

comparar os dois, age chamando a tool de cálculo, observa que o valor está dentro do

intervalo; e, julgando o objetivo atingido, encerra com a resposta.



* ###### plan-and-execute: 

Em vez de aceitar a primeira saída, o agente avalia

criticamente o próprio resultado e tenta melhorá-lo numa nova passagem, usando a autocrítica como insumo

A separação favorece tarefas longas e estruturadas, em que pensar o todo antes de começar evita desvios e retrabalho, e em que um

plano explícito também facilita a supervisão humana, pois pode ser revisado antes da

execução.



* ###### reflexão:



Em vez de aceitar a primeira saída, o agente avalia

criticamente o próprio resultado e tenta melhorá-lo numa nova passagem, usando a autocrítica como insumo.



Exemplo:

A reflexão eleva a qualidade sobretudo em tarefas com critério

de sucesso verificável, como gerar código que precisa passar em testes ou produzir

um texto que deve satisfazer uma lista de requisitos: nesses casos, a verificação fornece um sinal objetivo que orienta a próxima tentativa. Onde não há critério verificável,

a reflexão corre o risco de apenas reescrever a saída de forma mais convincente, sem

necessariamente torná-la mais correta, e a cada ciclo adicional acrescenta chamadas

ao modelo.



* ###### &#x20;multi-agente:



em que vários agentes especializados colaboram,

cada um com um papel, uma instrução e um conjunto de tools próprios, coordenados

por um agente orquestrador ou por um protocolo de troca de mensagens. 





Em PD\&I industrial, começar

com um único agente bem instruído e só decompor em papéis quando a sobrecarga de

um deles ficar evidente costuma ser o caminho mais seguro







O ReAct, por intercalar uma

chamada de modelo a cada passo, fica caro e lento quando a tarefa tem muitos passos

triviais que não precisariam de raciocínio; nesses casos, um workflow resolve melhor.

O plan-and-execute sofre quando o ambiente é imprevisível e o plano inicial envelhece

rápido, situação em que a adaptação contínua do ReAct é preferível. A reflexão desperdiça chamadas quando não há um critério objetivo que diga se a nova tentativa é de fato

melhor. O multi-agente penaliza tarefas simples, em que a coordenação entre agentes

custa mais do que o ganho de especialização. A pergunta correta nunca é qual o paradigma mais avançado, mas qual a dificuldade específica do problema e qual estratégia

a enfrenta com o menor custo.





##### Model Context Protocol



O Model Context Protocol, ou MCP, é uma proposta de protocolo aberto para reduzir

esse acoplamento. Ele define uma interface uniforme, no estilo cliente e servidor, pela

qual um agente descobre e invoca ferramentas e acessa fontes de dados expostas por

servidores que falam o mesmo protocolo. O efeito prático é transformar um problema

de muitas integrações ponto a ponto num problema em que cada lado fala o protocolo

uma única vez: quem constrói uma ferramenta a expõe como servidor compatível, e

qualquer agente que seja cliente do protocolo passa a poder usá-la sem integração

específica. 







Consumir um servidor já homologado economiza esforço e tende a ser preferível quando a

ferramenta é genérica e bem mantida. Construir a própria integração se justifica quando

a ferramenta é específica do domínio, quando há requisitos de segurança que um servidor genérico não atende, ou quando o controle sobre o comportamento da integração é

parte do valor da solução. 







##### Dois padrões aplicados em PD\&I industrial



* &#x20;single-loop com tools controladas. 

Há um único reasoning

engine que repete o ciclo perceber-decidir-agir sobre um conjunto pequeno e curado de

ferramentas, com uma condição de parada explícita. O termo single-loop indica o que

esse padrão não tem: não há hierarquia de planos elaborados de antemão, não há múltiplos agentes coordenados, não há orquestração complexa. Há um laço, poucas tools

bem definidas e limites claros, como um número máximo de iterações.





Convém detalhar o que mantém o agente single-loop sob controle. Três limites costumam acompanhá-lo. O primeiro é a lista restrita de tools, escolhida de modo que cada

ação possível seja conhecida e auditável. O segundo é o teto de iterações, que impede

o laço de prosseguir indefinidamente e funciona como salvaguarda de custo. O terceiro

é a condição de parada bem definida, que diz ao agente quando o objetivo foi atingido. 





* &#x20;workflow determinista com chamadas pontuais de modelo:





&#x20;Aqui

a estrutura de controle é fixa: um grafo de passos definido por quem projetou o sistema,

em que o modelo é chamado em pontos específicos para executar uma subtarefa bem

delimitada, como classificar um documento, extrair campos de um texto ou gerar um

resumo.





&#x20;A diferença essencial em relação ao agente é que, no workflow, o modelo não decide o fluxo; ele preenche lacunas dentro de um fluxo que já está decidido.



A consequência de custo merece um contraste numérico em ordem de grandeza. Um

workflow que chama o modelo duas vezes por requisição tem custo e latência essencialmente constantes, fáceis de multiplicar pelo volume esperado. Um agente que, conforme o caso, faz de três a quinze iterações tem custo que varia na mesma proporção,

e o planejamento de capacidade precisa considerar não a média, mas também o pior

caso, sob pena de subdimensionar a infraestrutura e estourar o orçamento em picos.

Essa assimetria de previsibilidade, e não apenas o custo médio, é parte do que se pondera ao escolher entre os padrões.







###### Reconhecimento do padrão em uma especificação:





* A primeira é se o conjunto de passos necessários é conhecido de antemão
* A segunda pergunta é como se decide a ramificação do fluxo.



* terceira pergunta é quantas chamadas ao modelo a tarefa exige por requisição e se esse número é fixo ou variável.
* A quarta pergunta é qual o orçamento de custo e latência e qual o nível de auditabilidade exigido.



Um terceiro exemplo, propositalmente intermediário, mostra como a sequência lida com

casos que não são puros. Uma especificação pede um sistema que processe pedidos

de compra: na maior parte do tempo, os passos são fixos, validar o pedido, conferir o orçamento, registrar e notificar, o que aponta claramente para workflow. Mas há uma etapa em que, diante de uma exceção de orçamento, o sistema deve investigar alternativas

consultando fornecedores e histórico em ordem que depende do que encontra. As três

primeiras perguntas apontam para workflow no fluxo principal, e a etapa de exceção

aponta para agente. O reconhecimento correto não é escolher um dos dois para tudo,

mas identificar que o fluxo principal é um workflow que, num nó específico, aciona um

pequeno agente para a subtarefa aberta. Localizar a autonomia onde ela é necessária,

em vez de espalhá-la, é o ganho da leitura cuidadosa.









###### 

###### 

###### DECISÃO WORKFLOW X AGENT







o workflow determinista, quem desenha a solução fixa de antemão a sequência de passos e as ramificações possíveis. No agente, o sistema decide, a cada

passo, o que fazer em seguida, em função do que acabou de observar. Vale insistir num

ponto que costuma gerar confusão: a diferença não está na presença de um modelo.

Um workflow pode chamar um modelo dentro de um passo, para classificar um texto ou

extrair campos, sem deixar de ser um workflow. O que muda é o controle do caminho,

fixo no workflow e decidido em execução no agente. Essa é a decisão de arquitetura

mais consequente do módulo, porque dela dependem o custo, a previsibilidade e a auditabilidade de tudo o que vem depois.





###### branching dinâmico: Há branching dinâmico quando o próximo passo depende de resultados intermediários que não se consegue enumerar de antemão.





Branching dinâmico

Situação em que o próximo passo de uma solução depende de resultados que

só surgem durante a execução, de modo que a sequência de ações não pode ser

fixada de antemão. É o sinal central que distingue um problema de agente de um

problema de workflow.





Sobe-se para o agente quando duas condições se encontram, e não apenas uma. A primeira é que o branching dinâmico seja irrelutável, o que significa que você tentou fixar

o fluxo e não conseguiu sem enumerar um número impraticável de casos. A segunda é

que a autonomia agregue valor real, o que significa que a flexibilidade resolve um problema concreto da tarefa, e não que ela soa mais avançada numa apresentação. 





A decisão se organiza em três eixos, que o template T2.1 vai formalizar e que vale antecipar aqui. O primeiro é o branching dinâmico: o caminho é fixável ou não? O segundo é

o custo: quantas chamadas a mais o agente introduz em relação a um workflow equivalente, e esse acréscimo é sustentável no volume previsto? O terceiro é a transparência:

você consegue auditar e explicar a sequência de decisões a um stakeholder ou a um

regulador? Os três eixos são lidos em conjunto, e não isoladamente.





##### modos de falha 





Um sistema que decide a cada passo tem uma superfície de falha maior que um workflow de caminho fixo, por duas razões cumulativas. A primeira é que cada decisão de runtime pode errar, e há muitas decisões. A segunda é que os erros se encadeiam, por que a saída de um passo é a entrada do seguinte. Quatro modos de falha aparecem com frequência em PD\&I industrial e merecem nome próprio, aqui apresentados na forma

em que se manifestam no laço de um agente. 







prompt injection

Ataque ou falha em que conteúdo lido pelo agente a partir do ambiente, como

um documento ou uma observação de tool, contém instruções que o desviam do

objetivo original. É um risco próprio de sistemas que combinam leitura de texto

não confiável com a capacidade de executar ações.











isso conduz à segunda decisão da seção, a centralidade do raciocínio. A pergunta é

onde colocar a decisão aberta, aquela que de fato exige interpretar uma situação nova,

e onde manter o controle determinista. A boa prática é restringir o modelo de linguagem

aos pontos em que esse tipo de decisão é realmente necessário, e cercá-lo de controle

determinista: validação das saídas, limites de iteração, roteamento fixo entre etapas.

Quanto mais do caminho puder ser determinista, menor a superfície de falha, mais barato o sistema e mais simples a auditoria.









A terceira decisão é a tolerância a falhas em loop, que se traduz em três custos a serem

aceitos de forma consciente. Há o custo financeiro, porque cada nova tentativa de recuperação é uma chamada paga ao modelo. Há o custo de transparência, porque sem

um trace registrado a falha é invisível e não há o que depurar quando o resultado vem

errado. E há o custo de auditoria, porque em setor regulado é preciso reconstruir, depois

do fato, porque o agente agiu como agiu. Decidir a tolerância a falhas é, na prática, decidir quanto investir em validação e em observabilidade antes de colocar o agente em

produção, e esse investimento entra no orçamento do projeto desde o início, não como

ajuste posterior.







Fechamento decisório: a autonomia no ciclo do projeto



* O primeiro compromisso é o custo de inferência, que é multiplicativo. Um agente com k passos faz ao menos k chamadas ao modelo, e mais ainda quando há tentativas repetidas de recuperação.
* O segundo compromisso é a latência, que é sequencial. O tempo total de resposta soma cada chamada ao modelo e cada execução de tool, na ordem em que acontecem, porque um passo depende do resultado do anterior e não pode ser antecipado.
* O terceiro compromisso é a observabilidade, que precisa ser instrumentada desde o

&#x20;início, e não acrescentada depois que um problema aparece. Sem o registro do raciocínio, da ação e da observação a cada passo, não há como       auditar nem depurar o agente quando o resultado vem errado, porque o que se vê de fora é apenas a saída final, sem o histórico que a produziu.







Para a estimativa de ordem de grandeza, vale fixar uma regra prática que pode ser aplicada já na fase de proposta. O custo de um agente é da ordem do número de passos vezes o custo por chamada ao modelo, somado ao custo de execução das tools. Compare

esse número com o custo de uma chamada direta, que é uma unidade de referência. Se

o agente típico usa quatro passos e o pior caso usa oito, dimensione pelo pior caso, ou

imponha um teto de iterações que torne o custo máximo previsível e financiável.





RESUMO









A camada decisória do módulo M2 organizou a lente da autonomia em torno de três

decisões encadeadas. A primeira é a heurística workflow versus agente, que coloca o

workflow como default e reserva o agente para o branching dinâmico irrelutável que

agrega valor real. A segunda é o tratamento dos modos de falha recorrentes, loops,

seleção de tool errada, prompt injection e cascading errors, com mitigações que agem  entre a observação e a próxima decisão. A terceira é a tradução da escolha em compromissos de projeto: custo de inferência, latência e observabilidade, dimensionados pelo

pior caso





Os instrumentos que sustentam essas decisões são os templates T2.1, matriz de decisão workflow versus agente, e T2.2, matriz de modos de falha e mitigações. Eles conectam o módulo ao encontro 6 da Formação 1, Desenhar a solução, em que a opção por

um agente precisa ser registrada com seus compromissos explícitos antes de a arquitetura ser fechada. O preenchimento desses instrumentos é a evidência de aprendizagem

da camada decisória.







