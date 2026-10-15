\- **A tradução** segue um framework de leitura em três movimentos. O primeiro é separar

sintoma de causa: o que a empresa observa (descarte alto, atraso na decisão de compra, reclamação de cliente) é o sintoma, e a pergunta que abre a conversa é o que o gera.



\- O segundo movimento **é localizar** o problema raiz e enunciá-lo em uma ou duas frases,

sem mencionar tecnologia.



\-O terceiro movimento é verificar o **lastro de dados:** que dados existem hoje, com que qualidade e com que

acesso, porque um problema tecnicamente bem enunciado sem dados que o sustentem ainda não é um projeto viável, é uma hipótese de aquisição de dados.





###### Exemplo: 





Uma agroindústria pede um dashboard com IA para a manutenção. O sintoma, descoberto na segunda conversa, é que

paradas não programadas de secadores consumiram doze dias de operação no último

ano. A causa provável é que a manutenção é puramente corretiva: não há uso sistemático dos dados de sensores que os equipamentos já geram. O problema raiz, enunciado

sem tecnologia, fica assim: antecipar falhas dos secadores com antecedência suficiente para programar a intervenção fora da janela de operação. Repare no que a tradução

fez: o dashboard desapareceu do enunciado, e talvez reapareça na solução, talvez não;

a decisão sobre isso pertence às fases seguintes, não a esta. E o lastro de dados virou

uma pergunta objetiva: que sensores existem, com que histórico, e as falhas passadas

foram registradas com data e tipo?















Este tópico abre a primeira fase do método e tem por objetivo que você traduza um problema de negócio apresentado pela empresa parceira em problema técnico delimitado,

identificando stakeholders, critérios de sucesso, restrições e premissas (competência

CP.B2.C1).



###### restrições: restrição é limite duro, que a solução precisa respeitar sob pena de ser inviável: o dado não pode sair do ambiente da empresa, o orçamento de nuvem tem teto,

a resposta precisa caber na janela do processo, a regulação exige explicação da decisão.



###### premissas: Premissa é suposição assumida como verdadeira para o planejamento seguir, sem

verificação completa agora: os sensores cobrem os equipamentos críticos, o histórico

de falhas está registrado com qualidade, a parceira liberará acesso ao banco em duas

semanas.



###### escopo: A saída deste curso é tratar o fora de escopo como

backlog priorizável com responsável. Cada item registrado ganha um dono e uma posição de prioridade. A decisão de incorporá-lo é tomada nos pontos de revisão do projeto,

por um fluxo declarado de controle de mudanças, com efeito registrado sobre prazo,

custo e qualidade. Registrado assim, o escopo vira instrumento de negociação contínua.





##### 

##### **Para traduzir um problema em um projeto:**





A ficha de escopo de projeto consolida o enunciado do problema técnico delimitado, os critérios

de sucesso técnicos e de negócio com a ponte entre eles, as restrições, as premissas

com data de reavaliação e a fronteira de escopo com o fora de escopo tratado como

backlog priorizável com responsável. A matriz de stakeholders registra cada stakeholder com seu interesse, seu poder, o quadrante resultante e a estratégia de engajamento

correspondente. 




**Para o primeiro encontro:**
---



Uma última conexão fecha este tópico, e ela olha para o laboratório presencial. A delimitação que você exercitou aqui é exatamente o trabalho do Encontro 1 da Formação 1, Compreender o caso e delimitar o problema: diante do caso do squad, a primeira

entrega presencial é a separação de sintomas e causas, o enunciado da raiz, o levantamento de dados e restrições, tudo antes de qualquer escolha de tecnologia. No laboratório, você consolidará esta análise no Mapa Técnico do Problema, o instrumento do

kit de formação que o squad preenche em conjunto no Encontro 1. A ficha de escopo

e a matriz de stakeholders que você preencher no curso são o treino individual dessa

consolidação coletiva. Com o problema delimitado, a pergunta seguinte é de tempo:

como transformar essa delimitação em um caminho conduzível, com datas, pontos de

decisão e um ritmo de trabalho?







O primeiro instrumento é a decomposição. Um projeto de meses não se conduz como

um bloco único; ele se decompõe em entregáveis, e os entregáveis se organizam em

milestones. Milestone, ou marco, é um estado consolidado do projeto, demonstrável

por evidência - e não somente uma data no calendário.







Problema delimitado com dados

confirmados é um marco; hipótese testada em prova de conceito é outro; solução decidida com arquitetura desenhada, um terceiro; validação concluída com entrega defensável, o último do arco típico. A diferença entre marcamos janeiro para a modelagem e

em janeiro demonstramos o modelo atingindo o critério X no dado Y é toda a diferença

entre um calendário decorativo e um instrumento de condução.





MILESTONE:

* DEFINIÇÃO DE PRONTO;
* MAPEAMENTO DE DEPENDÊNCIAS CRÍTICAS (FERRAMENTAS, USUÁRIOS,TERCEIROS,APROVAÇÕES, LAYOUT ETC...)
* Gate review





A regra prática tem duas metades. Primeiro, dependências

críticas entram no cronograma com nome, responsável e data, nunca como suposição difusa; repare que muitas delas nascem das premissas registradas na ficha de

escopo, e a data de reavaliação da premissa vira um marco do cronograma.

o caminho que passa por elas recebe folga explícita, porque é nele que o atraso não

se recupera. Identificar pelo menos três dependências críticas no cenário fictício é o

padrão que o cronograma do caderno demonstra, e o número não é arbitrário: projetos

reais raramente têm menos que isso.







O gate é o momento em que o projeto para de produzir e decide o próprio

rumo, e a sua marca neste curso é a dupla função. A primeira função é a decisão de continuidade: diante da evidência acumulada desde o último gate, o projeto continua como

está, pivota (muda de abordagem preservando o objetivo) ou para. A segunda função

é a revisão de processo: independentemente da decisão, o time pergunta o que no seu

modo de trabalhar deve mudar no próximo ciclo, do acesso a dados que emperrou à

comunicação que falhou. A primeira função protege o investimento; a segunda melhora

o modo de trabalhar sem esperar o fim do projeto.





gate reviwe x status report 



* COntinuar: 

Quando é a leitura adequada:



A evidência do período sustenta

os critérios de pronto e nenhum

risco crítico se concretizou.





O que precisa ficar registrado:



Evidência apresentada, próximos

milestones confirmados, riscos reavaliados.



* Pivotar



Quando é a leitura adequada:



O objetivo permanece válido, mas

a abordagem atual não atinge o

critério declarado dentro do prazo



O que precisa ficar registrado:



Critério de pivô acionado, abordagem

nova, efeito sobre cronograma e custo,

o que se preserva do trabalho feito.





* PArar



Quando é a leitura adequada:



Nenhuma abordagem viável

atinge o critério com os dados e o

prazo disponíveis, ou o problema

perdeu valor para o negócio.



O que precisa ficar registrado:



Critério de descontinuação acionado,

diagnóstico do que se aprendeu, recomendação devolvida ao cliente.





Na régua da pesquisa, parar soa como fracasso, e a tentação de estender mais um ciclo é permanente.

Na régua de PD\&I industrial, parar bem é um resultado: um projeto que consome dois

meses, conclui com evidência que o problema não é tratável com os dados existentes

e devolve ao cliente um diagnóstico acionável custou uma fração do projeto que se arrasta um ano para chegar à mesma conclusão









A armadilha central deste tópico é tratar o gate como reunião de progresso:

o time relata avanços, todos concordam que está indo bem, e nenhuma decisão

contra critério acontece. O cronograma vira peça decorativa, os critérios

de pivô nunca são acionados porque nunca são consultados, e o projeto descobre no penúltimo mês aquilo que um gate honesto teria revelado no primeiro

terço. O sintoma é fácil de detectar: se os últimos três gates terminaram

sem nenhuma decisão registrada além de seguir em frente, ou os critérios

estão frouxos, ou o gate não está acontecendo de verdade.







##### 

##### RISCO OPERACIONAL 



* RISCO TÉCNICO
* RISCO DE CRONOGRAMA
* RISCO DE DEPENDÊNCIA
* RISCO DE MUDANÇA DE ESCOPO
* RISCO DE CONFORMIDADE







Em projetos industriais reais, a incerteza técnica é apenas uma

das fontes de fracasso, e raramente a mais frequente. Projetos morrem por atraso de

dados que nunca chegaram, por escopo que cresceu sem renegociação, por uma cláusula de propriedade intelectual descoberta tarde, por uma exigência regulatória que ninguém mapeou. Gerir risco operacional é olhar para todas essas fontes com o mesmo

rigor que se dedica à técnica.







O risco técnico é o

mais familiar: a abordagem escolhida não atinge o desempenho mínimo, os dados têm

menos sinal do que se supunha, a integração com o sistema legado se revela mais dura

que o previsto. O risco de cronograma é a subestimação sistemática, e em projetos de

IA ela tem endereço conhecido: as etapas de aquisição e preparação de dados e as etapas de integração consomem, com regularidade, mais tempo do que a modelagem que

costuma concentrar a atenção. O risco de dependência externa é o atraso ou a falha

daquilo que não está sob controle do time: o dado que a parceira ia liberar, o acesso que

a TI ia conceder, a decisão que o comitê ia tomar. O risco de mudança de escopo é a erosão do acordo original por acréscimos não renegociados. O risco de conformidade (governança, regulatório e PI) abrange o descumprimento de cláusulas contratuais, termos

de licença de uso de software/dados ou marcos regulatórios vigentes, tais como a Lei

Geral de Proteção de Dados (LGPD) e diretrizes de governança e ética em Inteligência

Artificial.









Evitar é alterar o plano para que o risco não exista, como trocar um dado pessoal por

um agregado. Mitigar é reduzir probabilidade ou severidade, como fechar um acordo de

dados com data e responsável. Transferir é deslocar o efeito para quem pode absorvê-

\-lo, como uma cláusula contratual. Aceitar é conviver com o risco de forma registrada,

decisão legítima para riscos de baixa prioridade. Mitigação sem responsável nomeado

é intenção, não mitigação.













