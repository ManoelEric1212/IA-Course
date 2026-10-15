# Unidade 2 — Escopo e Fundamentos de Gestão de Projetos (CP.B2)

Fonte: `COnducao de projetos/ESCOPO E FUNDAMENTOS DE GESTAO DE PROJETOS/ANOTAÇÕES.md` (anotações do aluno, cobrindo as aulas 1–4) + templates `FICHA DE ESCOPO DE PROJETO.pdf`, `MATRIZ DE STAKEHOLDERS.pdf`, `CRONOGRAMA COM GATES.pdf`, `MATRIZ DE RISCO.pdf`, `GLSSÁRIO.pdf`.

Esta unidade abre o método de Condução de Projetos (PD&I industrial). Competência de referência: CP.B2.C1 — traduzir um problema de negócio apresentado pela empresa parceira em problema técnico delimitado, identificando stakeholders, critérios de sucesso, restrições e premissas.

## 1. Tradução de problema de negócio em problema técnico

Framework de leitura em três movimentos:

1. **Separar sintoma de causa.** O que a empresa observa (descarte alto, atraso na decisão de compra, reclamação de cliente) é o **sintoma**; a pergunta que abre a conversa é o que o gera.
2. **Localizar o problema raiz e enunciá-lo em uma ou duas frases, sem mencionar tecnologia.**
3. **Verificar o lastro de dados**: que dados existem hoje, com que qualidade e com que acesso. Um problema tecnicamente bem enunciado sem dados que o sustentem ainda não é um projeto viável — é uma **hipótese de aquisição de dados**.

### Exemplo (ebook)
Uma agroindústria pede um dashboard com IA para a manutenção. O sintoma (descoberto na segunda conversa): paradas não programadas de secadores consumiram doze dias de operação no último ano. A causa provável: a manutenção é puramente corretiva, sem uso sistemático dos dados de sensores já gerados. O problema raiz, sem tecnologia: **antecipar falhas dos secadores com antecedência suficiente para programar a intervenção fora da janela de operação**. Note o movimento: o "dashboard" desaparece do enunciado (pode reaparecer na solução, ou não — decisão de fases seguintes); o lastro de dados vira pergunta objetiva (que sensores existem, com que histórico, falhas passadas registradas com data e tipo?).

### Glossário — restrições e premissas
- **Restrição**: limite duro que a solução precisa respeitar sob pena de ser inviável (o dado não pode sair do ambiente da empresa; o orçamento de nuvem tem teto; a resposta precisa caber na janela do processo; a regulação exige explicação da decisão).
- **Premissa**: suposição assumida como verdadeira para o planejamento seguir, sem verificação completa agora (os sensores cobrem os equipamentos críticos; o histórico de falhas está registrado com qualidade; a parceira liberará acesso ao banco em duas semanas). Toda premissa carrega uma **data de reavaliação**, que normalmente vira um marco do cronograma.

### Escopo e fora de escopo
A saída do curso é tratar o **fora de escopo como backlog priorizável com responsável**: cada item registrado ganha um dono e uma posição de prioridade; a decisão de incorporá-lo é tomada nos pontos de revisão do projeto (gates), por um fluxo declarado de controle de mudanças, com efeito registrado sobre prazo, custo e qualidade. Registrado assim, o escopo vira instrumento de negociação contínua — não uma linha fixa que se defende por teimosia.

### Artefato: Ficha de Escopo de Projeto
Consolida: o enunciado do problema técnico delimitado; os critérios de sucesso técnicos e de negócio **com a ponte entre eles**; as restrições; as premissas com data de reavaliação; e a fronteira de escopo com o fora de escopo tratado como backlog priorizável com responsável.

### Artefato: Matriz de Stakeholders
Registra cada stakeholder com: seu **interesse**, seu **poder**, o **quadrante** resultante (cruzamento interesse × poder) e a **estratégia de engajamento** correspondente a esse quadrante.

**Conexão com o laboratório**: esta delimitação é exatamente o trabalho do **Encontro 1** da Formação 1 ("Compreender o caso e delimitar o problema"): separação de sintomas e causas, enunciado da raiz, levantamento de dados e restrições, tudo antes de qualquer escolha de tecnologia. No laboratório, isso se consolida no **Mapa Técnico do Problema** (instrumento de squad, em sala); a Ficha de Escopo e a Matriz de Stakeholders deste curso são o treino individual dessa consolidação coletiva.

## 2. Decomposição em milestones e cronograma com gates

Um projeto de meses não se conduz como bloco único: decompõe-se em **entregáveis**, que se organizam em **milestones**.

- **Milestone (marco)**: um estado consolidado do projeto, **demonstrável por evidência** — não apenas uma data no calendário. Diferença central: "marcamos janeiro para a modelagem" (calendário decorativo) vs. "em janeiro demonstramos o modelo atingindo o critério X no dado Y" (instrumento de condução).
- Exemplos de marcos num arco típico: problema delimitado com dados confirmados; hipótese testada em prova de conceito; solução decidida com arquitetura desenhada; validação concluída com entrega defensável.

Componentes do milestone neste curso: **definição de pronto**, **mapeamento de dependências críticas** (ferramentas, usuários, terceiros, aprovações, layout etc.) e **gate review**.

### Regra prática de dependências
- Dependências críticas entram no cronograma **com nome, responsável e data**, nunca como suposição difusa — muitas nascem das premissas da ficha de escopo, e a data de reavaliação da premissa vira um marco do cronograma.
- O caminho que passa por dependências críticas recebe **folga explícita**, porque é nele que o atraso não se recupera.
- Padrão do curso: identificar **ao menos três dependências críticas** no cenário — projetos reais raramente têm menos.

### Gate
O **gate** é o momento em que o projeto para de produzir e decide o próprio rumo. Dupla função:
1. **Decisão de continuidade**: diante da evidência acumulada desde o último gate, o projeto **continua**, **pivota** (muda de abordagem preservando o objetivo) ou **para**.
2. **Revisão de processo**: independentemente da decisão, o time pergunta o que no modo de trabalhar deve mudar no próximo ciclo (do acesso a dados que emperrou à comunicação que falhou).

A primeira função protege o investimento; a segunda melhora o modo de trabalhar sem esperar o fim do projeto. *Gate review* ≠ *status report* (o status report é fluxo contínuo; o gate consome os reports acumulados e produz decisão — ver também B6).

| Decisão | Quando é a leitura adequada | O que precisa ficar registrado |
|---|---|---|
| **Continuar** | A evidência do período sustenta os critérios de pronto e nenhum risco crítico se concretizou. | Evidência apresentada, próximos milestones confirmados, riscos reavaliados. |
| **Pivotar** | O objetivo permanece válido, mas a abordagem atual não atinge o critério declarado dentro do prazo. | Critério de pivô acionado, abordagem nova, efeito sobre cronograma e custo, o que se preserva do trabalho feito. |
| **Parar** | Nenhuma abordagem viável atinge o critério com os dados e o prazo disponíveis, ou o problema perdeu valor para o negócio. | Critério de descontinuação acionado, diagnóstico do que se aprendeu, recomendação devolvida ao cliente. |

**Postura de PD&I vs. pesquisa**: na régua da pesquisa, "parar" soa a fracasso, e a tentação de estender mais um ciclo é permanente. Na régua de PD&I industrial, **parar bem é um resultado**: um projeto que consome dois meses, conclui que o problema não é tratável com os dados existentes e devolve um diagnóstico acionável custou uma fração do projeto que se arrasta um ano para chegar à mesma conclusão.

### Armadilha comum
Tratar o gate como **reunião de progresso**: o time relata avanços, todos concordam que está indo bem, e nenhuma decisão contra critério acontece. O cronograma vira peça decorativa, os critérios de pivô nunca são acionados porque nunca são consultados, e o projeto descobre no penúltimo mês aquilo que um gate honesto teria revelado no primeiro terço. Sintoma de alerta: se os últimos três gates terminaram sem nenhuma decisão registrada além de "seguir em frente", ou os critérios estão frouxos, ou o gate não está acontecendo de verdade.

## 3. Risco operacional

Em projetos industriais reais, a incerteza **técnica** é apenas uma das fontes de fracasso, e raramente a mais frequente. Projetos morrem por atraso de dados que nunca chegaram, por escopo que cresceu sem renegociação, por uma cláusula de propriedade intelectual descoberta tarde, por uma exigência regulatória que ninguém mapeou.

### Cinco categorias de risco operacional
1. **Risco técnico** — a abordagem escolhida não atinge o desempenho mínimo; os dados têm menos sinal do que se supunha; a integração com o sistema legado se revela mais dura que o previsto.
2. **Risco de cronograma** — subestimação sistemática; em projetos de IA, as etapas de aquisição/preparação de dados e as de integração consomem, com regularidade, mais tempo do que a modelagem (que costuma concentrar a atenção).
3. **Risco de dependência (externa)** — atraso ou falha daquilo que não está sob controle do time: o dado que a parceira ia liberar, o acesso que a TI ia conceder, a decisão que o comitê ia tomar.
4. **Risco de mudança de escopo** — erosão do acordo original por acréscimos não renegociados.
5. **Risco de conformidade** (governança, regulatório e PI) — descumprimento de cláusulas contratuais, termos de licença de uso de software/dados ou marcos regulatórios vigentes (LGPD, diretrizes de governança e ética em IA). Ver B4 para o detalhamento regulatório (LGPD/GDPR/EU AI Act) e B3 para PI de modelo/fornecedores.

### Quatro estratégias de tratamento
- **Evitar**: alterar o plano para que o risco não exista (ex.: trocar um dado pessoal por um agregado).
- **Mitigar**: reduzir probabilidade ou severidade (ex.: fechar um acordo de dados com data e responsável — ver B4).
- **Transferir**: deslocar o efeito para quem pode absorvê-lo (ex.: cláusula contratual).
- **Aceitar**: conviver com o risco de forma registrada — decisão legítima para riscos de baixa prioridade.

Regra de ouro: **mitigação sem responsável nomeado é intenção, não mitigação.**

### Artefato: Matriz de Risco
Registra, por risco: categoria (das cinco acima), probabilidade/severidade, estratégia de tratamento e responsável. Fornecedores (B3) e obrigações regulatórias (B4) alimentam, respectivamente, as categorias de Dependência Externa e Conformidade/PI desta matriz — cada linha deve apontar para um nome, um contrato e um responsável, não ficar genérica.

## Encadeamento com as unidades seguintes
- **B3** (Decisão de solução e arquitetura) lê a Ficha de Escopo (delimitação do problema, lastro de dados) para preencher a Matriz de Alternativas e a Ficha de Decisão build/buy/integrate.
- **B4** (Dados em PD&I industrial) lê o lastro de dados da Ficha de Escopo como ponto de partida da classificação de prontidão de fonte.
- Fornecedores e cláusulas identificados no B3 e as obrigações regulatórias do B4 **retroalimentam** a Matriz de Risco deste bloco (categorias Dependência Externa e Conformidade).

## Correspondência com o kit de laboratório (Formação 1 / Projeto Aroeira)
| Instrumento deste curso (CDP) | Instrumento do kit de formação (KIT) | Encontro |
|---|---|---|
| Ficha de Escopo de Projeto | Mapa Técnico do Problema (KIT-001) | Encontro 1 |
| (restrições/premissas) | Hipótese Técnica (KIT-003) — campo de condição | Encontro 1 |
| Matriz de Stakeholders | — (não há KIT equivalente direto no arco de 3 encontros) | — |
| Cronograma com Gates | Acordo de Squad (KIT-020) — rodízio/decisão; gates do curso ≈ fim de cada Encontro | Encontro 1 |
| Matriz de Risco | Pontos de incerteza da Decisão Justificada; Matriz de Riscos do M1 (`fundamentos-ia-aplicada`) | Encontro 2/3 |
