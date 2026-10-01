# Base de Conhecimento — Módulo M2: IA Agêntica
### Curso Base de IA | Fundamentos de IA Aplicada | Prof. Arthur Nascimento (Industr.IA)

> Documento de extração de conhecimento denso, estruturado e fiel aos materiais originais do módulo, destinado a servir de fonte de verdade (skill de referência) para resolver e avaliar desafios sobre IA Agêntica. Terminologia preservada em português exatamente como no curso. Fontes: Aula 1 (e-book "Arquitetura de Agentes e Padrões Aplicados"), Aula 2 (guia do notebook Colab IA_018), Aula 3 (e-book "A decisão Workflow vs Agente e os Modos de falha"), GLOSSÁRIO.pdf, TEMPLATE 1 (Matriz de Decisão), TEMPLATE 2 (Matriz de Modos de Falha), notebook IA_018.ipynb, anotações.md do aluno.

---

## 0. Mapa do módulo e progressão lógica (resumo executivo)

O módulo M2, "lente da autonomia", está organizado em **três camadas** que avançam em sequência lógica:

1. **Camada conceitual** (Aula 1, seções 1–4): define a **arquitetura canônica de um agente** (reasoning engine, tools, memória, planning, laço perceber-decidir-agir), distingue **agente** de **assistente conversacional** via o mecanismo de **tool calling**, apresenta o **panorama de paradigmas de raciocínio** (ReAct, Plan-and-Execute, Reflexão, Multi-agente) e situa o **Model Context Protocol (MCP)** como padrão emergente de integração.
2. **Camada aplicada** (Aula 1, seções 5–6): caracteriza os **dois padrões centrais de PD&I industrial** — **agente single-loop com tools controladas** e **workflow determinista com chamadas pontuais de modelo** — e ensina a **reconhecer** qual padrão uma especificação sugere, por meio de uma sequência de quatro perguntas.
3. **Camada decisória** (Aula 3): transforma reconhecimento em **decisão justificada**, por meio da **heurística do branching dinâmico** (workflow é o default; agente só se justifica quando o branching é irrelutável **e** a autonomia agrega valor real), do mapeamento dos **quatro modos de falha recorrentes** (loop, seleção de tool errada, prompt injection, cascading error) e da tradução da escolha em **três compromissos de projeto**: custo de inferência (multiplicativo), latência (sequencial) e observabilidade (instrumentada desde o início). Essa camada é formalizada nos instrumentos **T2.1** (matriz de decisão) e **T2.2** (matriz de modos de falha), que conectam o módulo ao encontro 6 da Formação 1 ("Desenhar a solução").

Paralelamente, o **notebook IA_018** (Aula 2) torna tudo isso **inspecionável na prática**: um reasoning engine determinista (função Python legível, não um LLM) decide a próxima ação de um agente single-loop com duas tools (`buscar_corpus`, `calcular`) sobre um corpus mock de um mancal industrial, produzindo um **trace** passo a passo que expõe tanto uma sequência de decisão correta (Tarefa A) quanto uma **seleção de ferramenta incorreta seguida de recuperação** (Tarefa B).

**Fio condutor único do módulo inteiro**: a diferença entre **decidir o caminho de antemão** (workflow) e **decidir o caminho em execução** (agente). Essa diferença — e não o framework, nem a presença de um modelo de linguagem — é o que determina custo, latência, previsibilidade e auditabilidade. O **ônus da prova é invertido**: quem precisa se justificar é a autonomia, não o workflow. "Comece pela solução mais simples que resolve o problema e só adote a complexidade que o problema exigir."

---

## 1. Aula 1 — E-book: "IA agêntica: Arquitetura de Agentes e Padrões Aplicados"

### 1.1 Estrutura (sumário oficial)
1. Arquitetura canônica de um agente (p.3)
2. Agente e assistente conversacional (p.7)
3. Panorama de paradigmas em alto nível (p.10)
4. Model Context Protocol como padrão de integração (p.14)
5. Dois padrões aplicados em PD&I industrial (p.17)
6. Reconhecimento do padrão em uma especificação (p.20)
7. Conclusão (p.23)

### 1.2 Arquitetura canônica de um agente (camada conceitual)

**Definição formal (texto-base):**
> "Um agente, neste curso, é um sistema de software que recebe um objetivo, decide por conta própria quais ações tomar para alcançá-lo, executa essas ações sobre um ambiente por meio de ferramentas, observa o resultado e repete o processo até concluir a tarefa ou atingir uma condição de parada."

A palavra que carrega o peso da definição é **decide**: não basta executar uma sequência de chamadas, é preciso escolher a próxima ação em função do que foi observado, sem que a escolha esteja inteiramente fixada de antemão.

**Contraste com chamada isolada de modelo**: numa chamada isolada, entrada → saída → fim, sem ação sobre o mundo nem observação de consequências. No agente, a mesma capacidade do modelo é colocada **dentro de um laço**. A diferença não está no modelo (pode ser o mesmo), está **na estrutura que o envolve**.

#### Os quatro componentes canônicos

1. **Reasoning engine (módulo de raciocínio)** — comanda o laço. A cada passo, lê o estado da tarefa (objetivo + histórico de ações + observações acumuladas) e decide: invocar uma ferramenta com argumentos, registrar um resultado parcial, ou encerrar com resposta final. Em geral desempenhado por um LLM, mas **a função de decisão é conceitualmente independente da tecnologia que a realiza** — separar função de substrato evita que trocar de modelo pareça exigir reescrever o sistema inteiro.

2. **Tools** — funções e APIs que o agente invoca para agir sobre o mundo (consultar banco de dados, chamar serviço externo, executar cálculo determinístico, escrever arquivo). Sem tools, o agente só raciocina em texto. Distinção importante: **tools de leitura** (só trazem informação) vs **tools de escrita** (alteram o estado do mundo) — as de escrita concentram a maior parte do risco. **Número excessivo de tools degrada a decisão**: mais opções → mais frequente o erro de seleção → conjuntos pequenos e bem delimitados são preferíveis.

3. **Memória**:
   - **Memória de curto prazo**: contexto imediato da tarefa em andamento — histórico de ações e observações que cabe na janela do modelo, reapresentado a cada decisão.
   - **Memória de longo prazo**: armazenamento mais duradouro, externo à janela, que sobrevive a uma execução; o agente recupera informação sob demanda.
   - Gerir a memória de curto prazo é gerir **recurso escasso**: o que fica no contexto original, o que é resumido, o que vai para armazenamento externo. Manter histórico demais encarece e gera ruído; descartar demais faz o agente perder o fio. **Mesmo o que cabe na janela não é inofensivo**: informação relevante enterrada em contexto longo tende a ser subutilizada.

4. **Planning (planejamento)** — capacidade de decompor um objetivo amplo em sequência de subtarefas. Pode ser **implícito** (emerge passo a passo do raciocínio) ou **explícito** (plano elaborado antes de executar). Planejamento explícito ajuda em tarefas longas e estruturadas e facilita supervisão humana (plano revisável antes da execução), mas exige revisão quando observações divergem do previsto.

> Os três componentes (tools, memória, planning) **não operam isoladamente**: é o reasoning engine que os mobiliza, decidindo a cada passo qual tool chamar, o que consultar na memória e quando o plano precisa de ajuste.

#### O ciclo: perceber, decidir, agir
Agente percebe o estado a partir de uma observação → reasoning engine decide a próxima ação (considerando objetivo + memória) → agente age via tool → ambiente devolve nova observação → ciclo recomeça.

**Condição de parada**: critério explícito de quando encerrar (objetivo atingido, número máximo de iterações, orçamento de erro esgotado). Sem ele, o laço pode não terminar — problema de custo e confiabilidade.

**Figura 1 (descrição)**: diagrama em blocos — retângulo "Ambiente (dados, sistemas, usuário)" envolve tudo; bloco central azul "Reasoning engine (modelo que decide)"; acima "Planning – decompor o objetivo"; à esquerda "Memória – contexto curto e armazenamento" (setas de mão dupla); à direita "Tools – funções e APIs invocáveis" (setas de mão dupla); abaixo "Observação" (sobe do ambiente, vai ao reasoning engine) e "Ação" (vem do reasoning engine, desce ao ambiente). Repete até objetivo ou condição de parada.

**Observabilidade e trace**: como o agente decide em vários passos, o registro dessas decisões (**trace**) é o principal artefato para entender, auditar e corrigir o sistema. Guarda, por iteração: raciocínio → ação → argumentos → observação. Sem trace, comportamento indesejado vira caixa-preta.

**Exemplo aplicado (suporte técnico industrial)**: agente recebe chamado, consulta base de manuais (tool de busca), verifica histórico do equipamento (outra tool), só então redige resposta com procedimento de manutenção. Número de consultas varia conforme o chamado.

**Observação sobre frameworks**: todos os frameworks de mercado (LangChain, LangGraph, AutoGen, CrewAI etc.) instanciam a mesma arquitetura canônica — reasoning engine, tools, memória, planning. Escolha de framework é decisão de produtividade/integração, não sobre "o que um agente é".

### 1.3 Agente e assistente conversacional

**Assistente conversacional**: responde a uma entrada e termina. Mesmo mantendo histórico multi-turno, cada resposta é **uma única passagem do modelo**, sem agir sobre ambiente externo e observar consequências antes de responder.

**Agente**: possui **agência** — seleciona ações, executa via tools, observa efeitos, itera rumo a objetivo, **sem devolver o controle a cada passo**. A propriedade decisiva **não é** a presença de um LLM (comum aos dois) nem a capacidade de chamar uma ferramenta pontualmente (um assistente também pode). É **o laço**: existência de um ciclo em que o sistema escolhe e encadeia ações autonomamente, decidindo quando continuar e quando parar.

> "Um assistente que consulta o tempo e responde fez uma chamada de ferramenta, mas não iterou; um agente que consulta, avalia o retorno, decide consultar outra coisa e só então responde, esse iterou."

#### Continuum de autonomia (4 degraus, cada um ilustrado em PD&I industrial)
| Degrau | Descrição | Exemplo PD&I industrial |
|---|---|---|
| 1. Chatbot | Apenas conversa, sem ação externa | Responde dúvidas sobre norma técnica a partir do texto dado, sem consultar nada externo |
| 2. Assistente com 1 chamada de ferramenta | Chama ferramenta numa única passagem, sem laço | Ao receber pergunta sobre equipamento, consulta uma vez a ficha do equipamento e responde, em um único passo |
| 3. Agente single-loop | Repete ciclo perceber-decidir-agir, tools controladas, condição de parada clara | Diante de diagnóstico ambíguo, decide consultar histórico, avalia retorno, decide consultar manual da peça suspeita, só então conclui |
| 4. Maior autonomia (planejamento multi-passo, multi-agente) | Planeja investigação completa, distribui subtarefas, consolida achados | Sistema que planeja uma investigação completa |

> "O mesmo domínio comporta os quatro degraus; o que muda é a abertura do problema que se quer resolver." Cada degrau cobra preço em custo de inferência, latência e dificuldade de auditar.

#### Tool calling
**Definição**: mecanismo que permite a um LLM **agir, e não apenas escrever**. Em vez de texto livre, o modelo emite **chamada estruturada** (nome da ferramenta + argumentos, conforme esquema declarado). **O sistema (não o modelo) executa** e devolve o resultado como nova observação. "É o contrato que liga decisão a ação."

Dois pontos sutis:
1. O modelo **propõe**, o código ao redor **executa** — abre espaço para validar argumentos, recusar chamadas malformadas, tratar erros antes que cheguem ao mundo.
2. A **estrutura importa**: chamada com formato declarado (não texto livre) pode ser analisada, validada, registrada de forma confiável.

**Contrato de tool** tem partes: nome, descrição, formato dos argumentos, formato do retorno. Contrato mais claro → menor chance de seleção errada de ferramenta ou argumentos inadequados. **Muitos erros de agentes vêm de contratos ambíguos**, não de o modelo "querer agir mal".

**Tools de escrita devem ser idempotentes** sempre que possível (repetir a mesma chamada não duplica efeito), porque um agente em laço pode reintentar uma ação.

#### Quadro 1 — Assistente conversacional x Agente (lado a lado, reprodução integral)
| Aspecto | Assistente conversacional | Agente |
|---|---|---|
| Unidade de operação | uma passagem do modelo por resposta | laço de vários passos por objetivo |
| Ação sobre o ambiente | nenhuma, ou uma chamada pontual | seleção e encadeamento autônomo de tools |
| Número de passos | fixo (um por resposta) | definido em execução, não de antemão |
| Custo e latência | previsíveis por resposta | variáveis, crescem com o número de passos |
| Auditoria | direta, uma entrada e uma saída | exige inspeção do trace de decisões |

**Custo da confusão terminológica**: tratar como agente o que poderia ser assistente+1 tool = pagar laço sem benefício. Tratar como assistente o que exige agente = forçar numa única passagem tarefa que precisa de iteração → respostas incompletas/frágeis.

**Estado**: assistente sem agência pode ser sem estado entre requisições. Agente é **inerentemente baseado em estado durante a execução** (acumula observações) e pode precisar de **estado persistente entre execuções** (retomar tarefa de onde parou). Isso o torna mais poderoso e mais difícil de testar/reproduzir (mesmo objetivo pode percorrer caminhos diferentes conforme estado encontrado).

**Aplicação aos 7 eixos do programa**: engenharia de dados (agente de inferência adaptativa de esquema), processamento em tempo real (agentes assíncronos), visão computacional (agentes que coordenam ferramentas de percepção). Pergunta universal: a tarefa exige encadear ações em função de observações intermediárias (agente), ou cabe em resposta única (assistente)?

> **ARMADILHA (box ATENÇÃO, Aula 1)**: "Uma armadilha frequente é supor que a arquitetura agentic é o default moderno, a ser adotado por ser o mais avançado. A consequência é o **over-engineering**: equipes envolvem em um laço autônomo tarefas cujo caminho é conhecido de antemão, pagando custo, latência e imprevisibilidade sem ganho correspondente. Autonomia é uma escolha condicionada ao problema, não um patamar a ser alcançado."

### 1.4 Panorama de paradigmas em alto nível

Paradigmas **não são tecnologias rivais que se excluem** — podem se combinar num mesmo sistema. Detalhamento de implementação fica para curso de LLMs da Fase 2.

#### ReAct (reasoning and acting)
Intercala passos de raciocínio explícito e ação no **mesmo laço**: raciocina sobre o que precisa → escolhe ação → observa resultado → raciocina de novo → prossegue. Ganhos: **transparência** (cada ação vem com justificativa textual inspecionável) e **robustez** (reavalia a cada observação, não segue plano cego). Custo: número de chamadas ao modelo cresce com passos do laço.

**Trace-exemplo (tolerância de lote)**: raciocina que precisa da medição → consulta tool de medições → observa valor; raciocina que precisa da especificação de tolerância → consulta tool de especificações → observa intervalo; raciocina que pode comparar → chama tool de cálculo → observa que está dentro do intervalo → encerra com resposta.

#### Plan-and-Execute
Separa em **duas fases** o que o ReAct entrelaça: primeiro elabora um **plano** (sequência de subtarefas), depois **executa** cada passo, revisando se observações divergirem. Favorece tarefas **longas e estruturadas** (evita desvios/retrabalho, facilita supervisão humana via plano revisável). Fragilidade: ambiente imprevisível faz o plano inicial envelhecer rápido.

> Nota: há uma inconsistência textual entre fontes — nas **anotações.md** do aluno, a definição de "plan-and-execute" aparece textualmente idêntica à de "reflexão" (aparente erro de cópia nas anotações pessoais). A definição correta e granular de cada paradigma, validada pelo e-book da Aula 1 e pelo GLOSSÁRIO, é a reproduzida aqui nesta seção e na seção 4 (Glossário).

#### Reflexão (Reflection)
Em vez de aceitar a primeira saída, o agente **avalia criticamente o próprio resultado** e tenta melhorá-lo numa nova passagem, usando autocrítica como insumo. Eleva qualidade **sobretudo em tarefas com critério de sucesso verificável** (código que deve passar em testes, texto que deve satisfazer lista de requisitos) — a verificação dá sinal objetivo. **Onde não há critério verificável**, a reflexão risca apenas reescrever de forma mais convincente, sem necessariamente mais correta, e cada ciclo adiciona chamadas ao modelo.

#### Multi-agente
Vários agentes especializados colaboram, cada um com papel, instrução e tools próprios, coordenados por **agente orquestrador** ou **protocolo de troca de mensagens**. Ajuda quando a tarefa se decompõe naturalmente em papéis distintos (ex.: um pesquisa, outro redige, um terceiro revisa) e quando instruções enxutas por papel melhoram qualidade vs. agente único sobrecarregado.

**Preço alto / modos de falha de coordenação** (contraintuitivos — mais agentes ≠ mais capacidade):
- **Repetir trabalho**: papéis se sobrepõem sem fronteira clara.
- **Divergir sobre o objetivo**: instrução de cada um interpreta de modo distinto.
- **Propagar erro**: saída equivocada de um vira entrada confiável do seguinte, amplificando o engano.

> Recomendação PD&I: "começar com um único agente bem instruído e só decompor em papéis quando a sobrecarga de um deles ficar evidente costuma ser o caminho mais seguro."

#### Quadro 2 — Quatro paradigmas (reprodução integral)
| Paradigma | Ideia central | Quando tende a ajudar |
|---|---|---|
| ReAct | intercala raciocínio e ação no mesmo laço | tarefas exploratórias com correção de curso |
| Plan-and-execute | planeja antes, executa e revisa depois | tarefas longas e estruturadas |
| Reflexão | autocrítica e nova tentativa | tarefas com critério de sucesso verificável |
| Multi-agente | papéis especializados que colaboram | tarefas decomponíveis em papéis distintos |

#### Quando cada paradigma atrapalha (mau encaixe)
- **ReAct**: caro/lento quando a tarefa tem muitos passos triviais que não precisam de raciocínio → workflow resolve melhor.
- **Plan-and-execute**: sofre quando ambiente é imprevisível e plano envelhece rápido → adaptação contínua do ReAct é preferível.
- **Reflexão**: desperdiça chamadas sem critério objetivo de melhoria.
- **Multi-agente**: penaliza tarefas simples, em que coordenação custa mais que o ganho de especialização.

> "A pergunta correta nunca é qual o paradigma mais avançado, mas qual a dificuldade específica do problema e qual estratégia a enfrenta com o menor custo."

Paradigmas se combinam (ex.: sistema multi-agente em que cada agente raciocina em estilo ReAct; plano de alto nível cujos passos são executados com reflexão). Sofisticação ≠ adequação.

**Saiba mais / referências**: YAO et al., *ReAct* (ICLR 2023, arXiv:2210.03629); SCHICK et al., *Toolformer* (NeurIPS 2023, arXiv:2302.04761); ANTHROPIC, *Building Effective Agents* (2024); ANTHROPIC, *Model Context Protocol Specification*; WANG et al., survey de agentes autônomos baseados em LLM (2024); PARK et al., *Generative Agents* (UIST 2023); SHINN et al., *Reflexion* (NeurIPS 2023); LANGCHAIN, *LangGraph Documentation*; WU et al., *AutoGen* (arXiv:2308.08155).

### 1.5 Model Context Protocol (MCP) como padrão de integração

**Problema de combinatória**: sem padrão comum, cada agente precisa de integração sob medida para cada ferramenta — número de integrações cresce com o **produto** entre quantidade de agentes e de ferramentas. Exemplo numérico do e-book: **5 agentes × 8 ferramentas = até 40 integrações possíveis**; cada nova ferramenta acrescenta 5 integrações (uma por agente). Com protocolo comum: **13 adaptações substituem as 40** (cresce com a **soma**, não o produto); nova ferramenta acrescenta apenas 1 adaptação.

**Definição (MCP)**: protocolo aberto, interface uniforme cliente-servidor, pela qual um agente **descobre** e **invoca** ferramentas e acessa fontes de dados expostas por servidores compatíveis, sem integração sob medida para cada par.

**Dois movimentos**:
1. **Descoberta** — agente cliente consulta servidor compatível, recebe lista de recursos oferecidos (descrição + formato de uso).
2. **Invocação padronizada** — uma vez descoberto, o recurso é acionado pelo mesmo mecanismo, qualquer que seja a ferramenta por trás.

**Tipos de recurso sob a interface uniforme**: recursos de **contexto** (dados para fundamentar respostas) e recursos de **ação** (as ferramentas/tools que executam operações). Na especificação técnica do protocolo (fora do escopo deste curso base), essas categorias correspondem às primitivas **Resources, Prompts e Tools**.

**Questão de confiança**: servidor descreve o que oferece; agente que confia cegamente pode ser induzido a ações indevidas por servidor mal-intencionado/comprometido. Recomendação industrial: tratar servidores como **fronteiras de confiança** — usar apenas homologados, validar retornos, limitar o que cada um pode acionar.

**Exemplo aplicado**: equipe de engenharia de dados mantém servidor que expõe consultas a catálogo de dados interno; publicado via protocolo padronizado, diferentes agentes de squads distintos passam a consultá-lo sem integração própria por squad.

**Decisão construir vs. consumir**:
- **Consumir servidor já homologado**: preferível quando ferramenta é **genérica e bem mantida**.
- **Construir integração própria**: justifica-se quando a ferramenta é **específica do domínio**, há **requisitos de segurança** que servidor genérico não atende, ou o **controle sobre o comportamento** é parte do valor da solução.

### 1.6 Dois padrões aplicados em PD&I industrial

#### Padrão 1 — Agente single-loop com tools controladas
Um único reasoning engine repete o ciclo perceber-decidir-agir sobre **conjunto pequeno e curado de ferramentas**, com **condição de parada explícita**. "Single-loop" indica o que **não** tem: hierarquia de planos elaborados de antemão, múltiplos agentes coordenados, orquestração complexa.

**Três limites que mantêm o padrão sob controle** (reaparecem no T2.1 e são centrais para avaliação):
1. **Lista restrita de tools** — cada ação possível conhecida e auditável.
2. **Teto de iterações** — impede laço indefinido; salvaguarda de custo.
3. **Condição de parada bem definida** — diz quando o objetivo foi atingido.

**Bom encaixe**: diagnóstico em que, conforme sintomas, o sistema decide quais verificações rodar e em que ordem, parando quando a causa é identificada (caminho varia por solicitação).
**Mau encaixe**: formulário com campos sempre iguais, validação fixa, destino determinado por campo conhecido (não há decisão de caminho a tomar — agente só adicionaria custo/imprevisibilidade).

#### Padrão 2 — Workflow determinista com chamadas pontuais de modelo
Estrutura de controle **fixa**: grafo de passos definido pelo projetista, modelo chamado em pontos específicos para subtarefa bem delimitada (classificar, extrair campos, gerar resumo). **Diferença essencial**: no workflow, **o modelo não decide o fluxo**; preenche lacunas dentro de um fluxo já decidido. Ramificações são **condicionais programadas** (ex.: "se tipo é A, siga por aqui"), não escolhas livres do modelo.

**Pipeline exemplo (processamento de documentos)**: entrada recebida → nó chama modelo para classificar tipo → ramificação programada encaminha ao extrator adequado → nó chama modelo para extrair campos → nó de validação verifica dados contra regras → saída gravada. Modelo acionado em **2 pontos fixos**, sempre os mesmos; quem decidiu o fluxo foi o projetista.

**Subtarefas comuns para chamadas pontuais de modelo em PD&I industrial**: classificar entrada em categoria conhecida; extrair campos estruturados de texto livre; rotear item para fila correta segundo conteúdo; resumir documento; gerar texto a partir de dados estruturados.

#### Figura 2 (descrição) — Workflow determinista x Agente single-loop lado a lado
- **Workflow determinista** ("caminho conhecido de antemão"): Entrada → Passo fixo → Chamada de modelo (classificar/extrair) → Passo fixo → Saída (sequência linear).
- **Agente single-loop** ("número de passos definido em execução"): Objetivo → Reasoning engine decide a próxima ação ⇄ (invoca/observa) ⇄ Tools controladas → Condição de parada → Saída (ciclo).

#### Quem decide o caminho? (pergunta organizadora)
Workflow: caminho decidido pelo projetista, fixado no código; modelo opera dentro dele. Agente: caminho decidido pelo reasoning engine em tempo de execução, em função das observações.

**Contraste numérico de custo (ordem de grandeza)**: workflow chama o modelo **2 vezes por requisição** → custo/latência essencialmente constantes. Agente faz **de 3 a 15 iterações** conforme o caso → custo varia na mesma proporção; planejamento de capacidade deve considerar **não a média, mas o pior caso**, sob pena de subdimensionar infraestrutura e estourar orçamento em picos.

**Híbridos**: workflow determinista que, em um único nó, aciona um pequeno agente single-loop para subtarefa aberta, depois retoma o fluxo fixo.

**Exemplo aplicado (seguradora)**: triagem de documentos de sinistro = workflow (classificar tipo, extrair campos, encaminhar fila — 2 chamadas de modelo, fluxo fixo). Investigação de sinistro suspeito (consultar bases diferentes em ordem variável) = agente single-loop com tools controladas.

> **ARMADILHA COMUM (box ATENÇÃO)**: "Um erro recorrente é subestimar como custo e latência crescem em arquiteturas agênticas. Como o agente repete o laço e cada iteração é uma nova chamada ao modelo, o custo não cresce de forma linear e previsível como num workflow, mas de forma **multiplicativa** com o número de passos, que varia por execução. Tratar um agente como se tivesse o perfil de custo de uma única chamada produz orçamentos e estimativas de latência irreais."

### 1.7 Reconhecimento do padrão em uma especificação

> Importante: **reconhecer não é ainda decidir**. A decisão justificada (heurística, eixos de comparação) é tratada na camada decisória (Aula 3). Aqui o objetivo é descritivo.

#### Sequência de quatro perguntas
1. **Os passos são conhecidos de antemão?** Teste mental: "você consegue desenhar o fluxograma completo sem saber qual será a entrada específica?" Se sim → workflow. Se o próximo passo depende do que se descobre e não dá para enumerar antecipadamente → indício de agente.
2. **Como se decide a ramificação do fluxo?** Regras/condicionais simples sobre dados estruturados → workflow. Interpretação de conteúdo aberto e variável, não redutível a regras fechadas → reasoning engine de agente se justifica.
3. **Quantas chamadas ao modelo a tarefa exige por requisição, fixo ou variável?** Fixo e pequeno → workflow. Variável, dependente do caso → agente.
4. **Qual o orçamento de custo/latência e o nível de auditabilidade exigido?** Apertado/rigoroso → workflow. Folgado e tolerante à variação → agente viável.

#### Quadro 3 — reprodução integral
| Pergunta sobre a especificação | Indica workflow | Indica agente |
|---|---|---|
| Os passos são conhecidos de antemão? | Sim, grafo fixo | Não, dependem do que se descobre |
| Como se decide a ramificação? | Regras e condicionais simples | Interpretação de conteúdo aberto |
| Quantas chamadas ao modelo por requisição? | Número fixo e pequeno | Número variável por caso |
| Orçamento de custo, latência e auditoria? | Apertado ou rigoroso | Folgado e tolerante a variação |

**Princípio organizador**: "comece pela solução mais simples que resolve o problema e só adote a complexidade que o problema exigir." A sequência não busca razão para usar agente — verifica se o problema **realmente** tem a imprevisibilidade de caminho que só um agente resolve bem.

#### Três exemplos trabalhados
1. **Nota fiscal (puro workflow)**: receber PDF, extrair itens, validar contra cadastro, gerar relatório de divergências. Passos conhecidos, ramificação por regras, chamadas fixas, exigência de auditoria → **workflow determinista**.
2. **Investigação de divergência recorrente (puro agente)**: consultar bases diferentes conforme pistas encontradas → passos não conhecidos, ramificação por interpretação, número variável de consultas → **agente**.
3. **Processamento de pedidos de compra (híbrido/intermediário)**: fluxo principal fixo (validar pedido, conferir orçamento, registrar, notificar) = workflow; mas exceção de orçamento exige investigar alternativas (consultar fornecedores/histórico em ordem que depende do que encontra) = agente **localizado** nessa etapa. "O reconhecimento correto não é escolher um dos dois para tudo, mas identificar que o fluxo principal é um workflow que, num nó específico, aciona um pequeno agente para a subtarefa aberta."

**Risco por família de padrão**: workflow — risco concentrado na **qualidade das chamadas pontuais** (classificação errada segue adiante sem correção) e na **rigidez diante de casos não previstos**. Agente — risco concentrado **no laço** (seleção de tool equivocada, iterações que não convergem, custo que escapa do previsto).

**Uso no trabalho de squad**: alimenta o **Mapa Técnico do Problema** — traduzir intenção vaga em características técnicas comparáveis, linguagem comum entre integrantes de formações distintas.

### 1.8 Conclusão da Aula 1 — três armadilhas a reter
1. Tratar a arquitetura agentic como **default moderno** (autonomia por sofisticação, não por necessidade).
2. Entender tool calling como **habilidade do modelo**, e não como **contrato estruturado** que exige validação e tratamento de erro.
3. Estimar o custo de um agente como se fosse **uma única chamada**, ignorando que o laço multiplica chamadas em número variável.

> "As três têm a mesma raiz: confundir o que o sistema pode fazer com o que o problema exige."

---

## 2. Aula 2 — Notebook IA_018: Agente single-loop com tools e trace anotado

A "Aula 2" em PDF é apenas o **guia de acesso** ao notebook Google Colab (link: colab.research.google.com/drive/11jWKpcwKcdUWJKnmfduI09tf5JFPmGm1). O conteúdo técnico efetivo está no notebook `IA_018.ipynb`, lido e reproduzido integralmente abaixo.

**Competência M2.C1**: "Descrever os componentes canônicos de um agente e diferenciá-lo de um assistente conversacional, reconhecendo os padrões aplicados centrais em PD&I industrial."

**Escolha de projeto declarada**: para rodar em qualquer ambiente, grátis, sem GPU, de modo determinístico, o **reasoning engine é uma função Python transparente** (heurística legível), não um LLM. Em produção esse papel seria de um LLM. Foco: **estrutura do laço**, **contrato de tool calling**, **trace** — não a capacidade do modelo.

**Pergunta central do notebook**: "Dado um objetivo, como um agente decide a próxima ação, executa uma ferramenta e usa o resultado para decidir o passo seguinte? E o que o trace dessa sequência revela sobre o comportamento do agente, inclusive quando ele seleciona a ferramenta errada?"

**Vocabulário do notebook** (remete ao glossário GLO-M2): agente, assistente conversacional, reasoning engine, tool, tool calling, observação, laço (perceber, decidir, agir), condição de parada, trace, workflow determinista.

### 2.1 Corpus mock
Base de 5 documentos técnicos sobre um **mancal** (bearing), com distratores deliberados (para cada pergunta, só 1 documento é relevante; a tool de busca retorna os 2 trechos de maior sobreposição de palavras, podendo trazer um distrator ao lado do relevante):

```python
CORPUS = {
    "doc_torque": "Parafuso de fixacao do mancal: torque nominal de 50 N.m, com tolerancia de mais ou menos 5 por cento.",
    "doc_temperatura": "Faixa de temperatura de operacao do mancal: de 40 a 80 graus C.",
    "doc_manutencao": "Intervalo de manutencao preventiva do mancal: a cada 2000 horas de operacao.",
    "doc_lubrificacao": "Lubrificacao do mancal: graxa de litio, reaplicar a cada 500 horas.",
    "doc_vibracao": "Limite de vibracao aceitavel do mancal: ate 4.5 mm por segundo em RMS.",
}
```

### 2.2 Contrato de tool calling (duas ferramentas)
```python
CONTRATOS_TOOLS = [
    {"nome": "buscar_corpus", "descricao": "Busca trechos na base de documentos tecnicos do equipamento.",
     "parametros": {"consulta": "texto com os termos a procurar"}},
    {"nome": "calcular", "descricao": "Avalia uma expressao aritmetica simples e retorna o resultado numerico.",
     "parametros": {"expressao": "expressao apenas com numeros e operadores + - * / ( )"}},
]
```
- `calcular`: calculadora controlada via `ast` (aceita só aritmética com números; rejeita termos não numéricos com erro explícito, ex.: `"expressao contem termo nao numerico: X"`).
- `buscar_corpus`: busca por **sobreposição de palavras** (interseção de conjuntos de tokens) entre consulta e cada documento; retorna os 2 trechos de maior pontuação.
- `executar_tool(nome, argumentos)`: **despachante que valida o contrato antes de executar** — verifica se a ferramenta existe, se os argumentos esperados estão presentes; só então chama a função registrada. Este é o ponto que concentra validação e tratamento de erro (o "ponto em que decisão vira efeito").

### 2.3 Reasoning engine (heurística determinística — "falha deliberada")
Funções auxiliares de leitura de estado: `_numeros`, `_ja_executou`, `_houve_erro`, `_texto_trecho_principal` (usa **apenas o trecho mais relevante**, o primeiro retornado, ignorando distratores), `_resultados_calculo`.

**Regra deliberadamente imperfeita** (comentário do código): quando o objetivo menciona "margem" ou "diferença", o motor **pula direto para calcular, antes de buscar os dados** — modela uma falha comum de agentes: **agir antes de coletar a informação necessária**. Depois do erro, o motor se corrige.

```python
def decidir_proxima_acao(objetivo, historico):
    ...
    if ("margem" in obj or "diferenca" in obj) and not ja_buscou and not erro_calculo:
        return {"raciocinio": "O objetivo pede uma margem, entao vou calcular a diferenca "
                               "em relacao ao limite. Tentativa direta, ainda sem buscar o limite.",
                "acao": "calcular", "argumentos": {"expressao": f"{leitura_txt} - limite_superior"}}
    if not ja_buscou:
        return {"raciocinio": "Ainda nao tenho a especificacao do equipamento. Vou buscar no corpus.",
                "acao": "buscar_corpus", ...}
    if _pede_conta(objetivo) and not ja_calculou:
        return {"raciocinio": "Ja tenho os valores da especificacao. Vou calcular para comparar.",
                "acao": "calcular", ...}
    return {"raciocinio": "Tenho informacao e calculo suficientes. Vou redigir a resposta final.",
            "acao": "FINAL", "argumentos": {"resposta": _redigir_resposta(objetivo, historico)}}
```

### 2.4 O laço do agente
```python
def executar_agente(objetivo, max_iteracoes=6):
    historico = []
    for i in range(1, max_iteracoes + 1):
        decisao = decidir_proxima_acao(objetivo, historico)
        if decisao["acao"] == "FINAL":
            return {"resposta": ..., "trace": historico, "iteracoes": i - 1, "parou_por": "objetivo atingido"}
        observacao = executar_tool(decisao["acao"], decisao["argumentos"])
        historico.append({"passo": i, "raciocinio": ..., "acao": ..., "argumentos": ..., "observacao": observacao})
    return {"resposta": None, "trace": historico, "iteracoes": max_iteracoes, "parou_por": "limite de iteracoes"}
```
**Duas condições de parada explícitas**: motor declara resposta final (`FINAL`) OU número de iterações atinge o teto (`max_iteracoes=6`).

### 2.5 Trace completo — Tarefa A (sequência de decisões correta)
**Objetivo**: "O torque medido no parafuso do mancal foi de 47 N.m. Pela especificacao, ele esta dentro da tolerancia?"

| Passo | Raciocínio | Ação | Argumentos | Observação |
|---|---|---|---|---|
| 1 | "Ainda nao tenho a especificacao do equipamento. Vou buscar no corpus." | `buscar_corpus` | `{"consulta": "torque parafuso mancal tolerancia"}` | `ok:true`, trechos: doc_torque (relevante) + doc_vibracao (distrator) |
| 2 | "Ja tenho os valores da especificacao. Vou calcular para comparar." | `calcular` | `{"expressao": "50.0 - 50.0 * 5.0 / 100"}` | `ok:true, resultado:47.5` |

**Parou por**: objetivo atingido (2 iterações com tool). **Resposta final**: "O valor medido de 47 N.m esta fora da tolerancia. A faixa permitida vai de 47.5 a 52.5 N.m (nominal 50 N.m, tolerancia de 5 por cento)."

### 2.6 Trace completo — Tarefa B (seleção de ferramenta incorreta + recuperação) — "o trace mais instrutivo do notebook"
**Objetivo**: "Qual a margem em relacao ao limite superior se a temperatura lida no mancal e de 86 graus?"

| Passo | Raciocínio | Ação | Argumentos | Observação |
|---|---|---|---|---|
| 1 | "O objetivo pede uma margem, entao vou calcular a diferenca em relacao ao limite. Tentativa direta, ainda sem buscar o limite." | `calcular` | `{"expressao": "86 - limite_superior"}` | **`ok:false`**, `erro: "expressao contem termo nao numerico: limite_superior"` ← **seleção de ferramenta/ação incorreta** |
| 2 | "Ainda nao tenho a especificacao do equipamento. Vou buscar no corpus." | `buscar_corpus` | `{"consulta": "temperatura operacao mancal faixa"}` | `ok:true`, trechos: doc_temperatura (relevante) + doc_manutencao (distrator) |
| 3 | "Ja tenho os valores da especificacao. Vou calcular para comparar." | `calcular` | `{"expressao": "86 - 80"}` | `ok:true, resultado:6.0` ← **seleção correta / recuperação** |

**Parou por**: objetivo atingido (3 iterações com tool). **Resposta final**: "A faixa de operacao vai de 40 a 80 graus. A leitura de 86 graus esta 6 graus acima do limite superior, portanto fora da faixa."

**Mecanismo de recuperação (explicado na Aula 3)**: o que tornou o sistema recuperável **não foi um modelo melhor** — foi a **observação de erro devolvida pela ferramenta** e a checagem feita antes do passo seguinte, que levou o agente a buscar o dado e só então calcular. É esse desenho (validar/observar erro → corrigir rumo) que transforma uma falha isolada em recuperação, em vez de um **cascading error**.

### 2.7 Como ler o trace (seção 9 do notebook)
"O trace é o principal artefato para entender e auditar um agente... Quando algo dá errado na resposta final, é no trace que se descobre em que passo a decisão se desviou." Em produção, o reasoning engine seria substituído por LLM; a estrutura do laço, o contrato de tool calling e o papel do trace permaneceriam os mesmos.

### 2.8 Perguntas para reflexão (notebook, seção 10 — sem resposta fornecida; conectam ao e-book da Aula 3)
1. No trace da Tarefa B, identifique uma seleção de ferramenta incorreta e uma correta. O que caracteriza cada uma, e o que a observação de erro permitiu ao agente fazer em seguida?
   - *(Resposta-base, conforme Aula 3): passo 1 = incorreta (calcular sem ter buscado o limite); passo 3 = correta (calcular após buscar); a observação de erro do passo 1 foi o sinal que permitiu a correção de rumo no passo 2.)*
2. Cada iteração do laço, num agente real, é uma nova chamada ao modelo. Comparando as tarefas A (2 iterações) e B (3 iterações), como o número de iterações afeta custo e latência? O que isso sugere sobre estimar custo pelo pior caso, e não pela média?
3. As tarefas têm passos que poderiam ser fixados de antemão. Em que ponto a variação de caminho da Tarefa B justificaria um agente, em vez de workflow determinista?
   - *(Resposta-base: só se essa variação — calcular, errar, buscar, recalcular — for recorrente e valiosa; se o caminho real fosse sempre o mesmo, um workflow resolveria com menos custo e mais previsibilidade — "o agente é custo sem retorno" quando a variação é apenas aparente.)*

---

## 3. Aula 3 — E-book: "IA agêntica: A decisão Workflow vs Agente e os Modos de falha"

### 3.1 Estrutura (sumário oficial)
1. A decisão entre workflow e agente (p.3)
2. Modos de falha e a centralidade do raciocínio (p.6)
3. Fechamento decisório: a autonomia no ciclo do projeto (p.10)
4. Conclusão (p.13)

### 3.2 Seção 1 — A decisão entre workflow e agente: a heurística do branching dinâmico

**Pergunta que organiza a seção**: não "qual framework adotar", mas "vale a pena entregar ao próprio sistema a decisão de qual caminho seguir?"

**Reafirmação do critério de arquitetura**: a diferença não está na presença de um modelo (workflow pode chamar modelo num passo, p.ex. classificar texto, sem deixar de ser workflow). O que muda é **o controle do caminho**: fixo no workflow, decidido em execução no agente.

**Branching dinâmico** (definição formal, idêntica à do glossário): "Situação em que o próximo passo de uma solução depende de resultados que só surgem durante a execução, de modo que a sequência de ações não pode ser fixada de antemão. É o sinal central que distingue um problema de agente de um problema de workflow."

**Teste prático**: tentar desenhar o fluxograma completo da solução antes de executá-la, com todas as ramificações nomeadas. Consegue, com número administrável de ramos → caminho fixável → workflow. Ramificações dependem de conteúdo que só aparece em execução, numerosas/imprevisíveis demais para enumerar → caminho dinâmico → agente entra em consideração.

#### A heurística de decisão (default + condições de exceção)
> "Comece pela solução mais simples e aumente a autonomia apenas quando o ganho for claro. **Na dúvida, o default é o workflow.**"

Razões concretas para o workflow como default:
- **Mais previsível** (caminho conhecido, depuração simples — sabe-se em qual passo olhar).
- **Custa menos** (menos chamadas ao modelo; custo de agente cresce com nº de passos).
- **Mais simples de testar** (comportamento determinista; agente pode seguir caminhos diferentes para a mesma entrada).

**Sobe-se para o agente quando DUAS condições se encontram simultaneamente** (não apenas uma):
1. **Branching dinâmico irrelutável** — você tentou fixar o fluxo e não conseguiu sem enumerar número impraticável de casos.
2. **Autonomia agrega valor real** — a flexibilidade resolve problema concreto da tarefa, não "soa mais avançada numa apresentação".

Se só uma condição está presente, a resposta ainda é workflow:
- Muitas ramificações, mas todas conhecidas → **workflow grande**, não agente.
- Autonomia desejável, mas caminho fixável → ainda **workflow**.

#### Caminho do meio: workflow com chamadas pontuais de modelo
Pipeline fixo em que 1-2 passos chamam modelo para tarefa delimitada (classificar documento, extrair informações de texto livre, redigir resumo padronizado). Caminho permanece fixo e auditável; modelo entra só onde interpretação de linguagem é necessária. **Não é agente** porque o sistema não decide a sequência. Desfaz a falsa dicotomia "script rígido vs. agente totalmente autônomo" — "uma das principais fontes de over-engineering na área".

#### Figura 1 (fluxograma de decisão, descrição integral)
"Problema com passos e decisões" → losango "O caminho é conhecido e estável de antemão?"
- **Sim** → "Workflow determinista"
- **Não** → losango "O branching dinâmico é irrelutável e a autonomia agrega valor real?"
  - **Sim** → "Agente single-loop" (observação: "registre desde já: custo de inferência, latência, auditoria")
  - **Não** → "Workflow com chamadas pontuais de modelo"

Legenda-resumo: "Na dúvida, comece pelo workflow. Suba para agente apenas quando o ganho compensar o custo." Subtítulo da figura: **"Workflow por padrão, agente por exceção."**

#### Os três eixos de decisão (antecipação formal do T2.1)
1. **Branching dinâmico**: o caminho é fixável ou não?
2. **Custo**: quantas chamadas a mais o agente introduz em relação a um workflow equivalente, e isso é sustentável no volume previsto?
3. **Transparência**: é possível auditar e explicar a sequência de decisões a um stakeholder/regulador?

> **Ponto crítico**: "cada eixo pode **vetar** a escolha do agente, mesmo quando os outros a favorecem." Ex.: branching alto, mas transparência é requisito regulatório que a autonomia comprometeria → ainda workflow. Os três eixos **são lidos em conjunto, não isoladamente**.

**Exemplo aplicado (triagem de manutenção, equipamentos rotativos)**: workflow inicial (classificar, consultar severidade, encaminhar) funcionava para a maioria; alguns chamados exigiam consultar histórico/manuais/ordens em ordem variável. **Decisão final**: manteve workflow para casos comuns, reservou agente só para fila de exceções (onde branching era de fato imprevisível).

**Conexão com o notebook**: a Tarefa B (calcular → erro → buscar → recalcular) é o tipo de branching dinâmico que justificaria um agente **se for recorrente e valioso**; se o caminho fosse sempre o mesmo, workflow seria melhor.

> **ARMADILHA (box ATENÇÃO)**: "A confusão decisória mais frequente é adotar o agente como default moderno, por ser o que aparece nas demonstrações, e só depois procurar uma justificativa. O efeito é uma solução mais cara, mais lenta e mais difícil de auditar do que o problema exigia. A heurística inverte o ônus da prova: **quem precisa se justificar é a autonomia, não o workflow**."

### 3.3 Seção 2 — Modos de falha e a centralidade do raciocínio

**Premissa**: os modos de falha **não são casos raros de borda** resolvíveis "com um modelo melhor". São **estruturais** a qualquer arquitetura que decide o caminho em tempo de execução.

**Por que a superfície de falha de um agente é maior que a de um workflow (duas razões cumulativas)**:
1. Cada decisão de runtime pode errar, e há muitas decisões.
2. Os erros se encadeiam — a saída de um passo é a entrada do seguinte.

#### Os quatro modos de falha recorrentes

| # | Modo | Como se manifesta | Categoria |
|---|---|---|---|
| 1 | **Loop** | Repete ações sem progredir (ex.: refazer a mesma busca, alternar entre duas ações sem convergir) | decisão |
| 2 | **Seleção de ferramenta errada (tool selection)** | Escolhe tool inadequada, ou tool certa com argumentos errados | decisão |
| 3 | **Prompt injection** | Conteúdo lido do ambiente (documento, observação de tool) contém instruções que desviam o agente do objetivo original | propagação/segurança |
| 4 | **Cascading error** | Erro inicial vira entrada do passo seguinte e se amplifica ao longo do laço; observação ruim contamina decisões posteriores | propagação |

**Nota de categorização do e-book**: os dois primeiros "dizem respeito à decisão em si"; os dois últimos "dizem respeito à propagação". Prompt injection "não tem paralelo direto num workflow fechado" — é falha de segurança específica de sistemas que combinam leitura de texto não confiável com capacidade de executar ações.

**Visibilidade**: loop e seleção errada "só se tornam visíveis quando há um trace para inspecionar" — do lado de fora o sistema só parece lento ou dá resposta estranha sem explicação aparente.

#### Quadro 1 (Aula 3) — Modos de falha recorrentes e mitigações (reprodução integral)
| Modo de falha | Como aparece | Mitigação típica |
|---|---|---|
| Loop | Repete ações sem progredir no objetivo | Limitar iterações e detectar repetição de estado |
| Tool selection errada | Escolhe a ferramenta ou os argumentos errados | Restringir o conjunto de tools e validar argumentos |
| Prompt injection | Conteúdo do ambiente desvia o agente | Isolar e tratar texto não confiável como dado, não instrução |
| Cascading error | Um erro inicial se amplifica no laço | Validar a observação antes da próxima decisão |

#### Figura 2 (descrição) — Propagação de erro no laço e pontos de mitigação
"Como um erro se propaga no laço" / "uma observação ruim contamina as decisões seguintes":
- **Passo 1**: "tool selection incorreta" → mitigação: "Validar a observação antes de seguir"
- **Passo 2**: "decide sobre uma observação errada" → destaque "Onde mitigar" → mitigação: "Limitar iterações e detectar repetição"
- **Passo 3**: "erro amplificado (cascading error)" → mitigação: "Inspecionar o trace de tool selection"
- Rodapé: **"A mitigação age entre a observação e a próxima decisão, não depois do resultado final."**

> **Padrão-chave das mitigações**: quase todas agem **no mesmo lugar — entre a observação e a próxima decisão**: (1) validar a observação com checagens simples antes de prosseguir; (2) limitar número de iterações e detectar repetição de estado; (3) restringir conjunto de tools e argumentos aceitos; (4) tratar todo texto do ambiente como **dado**, nunca como **instrução** a ser obedecida. "Nenhuma dessas medidas torna o agente mais inteligente. Todas tornam o sistema ao redor do agente mais robusto."

#### Centralidade do raciocínio: onde colocar a decisão aberta
Pergunta: onde colocar a decisão que exige interpretar situação nova (modelo) vs. onde manter controle determinista (código/orquestrador)?

**Boa prática**: restringir o LLM aos pontos onde a decisão aberta é **realmente** necessária, cercando-o de controle determinista (validação de saídas, limites de iteração, roteamento fixo entre etapas). **Quanto mais do caminho for determinista → menor superfície de falha, mais barato, mais simples a auditoria.**

- Candidatas legítimas ao modelo: interpretar entrada nova/ambígua (ex.: entender chamado em linguagem livre).
- Devem ficar no **orquestrador determinista** (baratas, testáveis, auditáveis): decisões expressáveis como regra (rotear por campo, validar formato, somar valores).
- **Erro comum**: deixar o modelo decidir também essas últimas por conveniência de implementação, herdando não-determinismo e custo sem benefício.

**Termo do glossário associado**: **Orquestrador baseado em regras** — "Camada de controle de caminho fixo que cerca o modelo num agente, cuidando de roteamento, validação e limites, de modo que o modelo decida apenas onde a interpretação aberta é necessária."

**Exemplo aplicado (inferência de schema)**: 1ª versão deixava modelo decidir tudo → sofria com loops e seleção de tool errada. 2ª versão fixou esqueleto do pipeline determinista (ler, amostrar, validar), reservando modelo só para o passo ambíguo (propor tipo de cada coluna) → número de chamadas caiu, trace ficou auditável, falhas viraram exceções tratáveis.

**Releitura do trace da Tarefa B**: passo 1 = seleção de ferramenta incorreta (calcular antes de buscar); o que tornou o sistema recuperável foi a **observação de erro** + checagem antes do passo seguinte, levando a buscar e só então calcular — transformando falha isolada em recuperação em vez de cascading error.

#### Terceira decisão: tolerância a falhas em loop (três custos conscientes)
1. **Custo financeiro** — cada nova tentativa de recuperação é chamada paga ao modelo.
2. **Custo de transparência** — sem trace registrado, a falha é invisível, nada a depurar.
3. **Custo de auditoria** — em setor regulado, é preciso reconstruir *depois do fato* por que o agente agiu como agiu.

> "Decidir a tolerância a falhas é, na prática, decidir quanto investir em validação e em observabilidade antes de colocar o agente em produção, e esse investimento entra no orçamento do projeto **desde o início**, não como ajuste posterior."

> **ARMADILHA (box ATENÇÃO)**: "A confusão decisória aqui é tratar o trace, ou a cadeia de raciocínio que o modelo verbaliza, **como prova de que o agente agiu corretamente**. O trace mostra o que o agente fez e disse, **não que estava certo**. Confiar no relato do próprio modelo como garantia de correção dispensa a validação externa justamente onde ela é mais necessária."

### 3.4 Seção 3 — Fechamento decisório: a autonomia no ciclo do projeto

**Premissa**: escolher agente é um **compromisso de produto e arquitetura assumido no início**, não otimização deixada para o fim. Tratar custos como "detalhe de implementação" é causa comum de soluções que funcionam em demo e não se sustentam em produção.

#### Os três compromissos de projeto

1. **Custo de inferência (multiplicativo)**: agente com *k* passos faz **ao menos k chamadas** ao modelo (mais ainda com recuperação de erro); chamada direta = 1 inferência. Diferença pode ser de **ordem de grandeza**. Estimar pela média ("caminho feliz") subestima — o teto é dado pelo **pior caso**.

2. **Latência (sequencial)**: tempo total soma cada chamada ao modelo + cada execução de tool, **na ordem em que acontecem** (um passo depende do resultado do anterior, não pode ser antecipado). Agente é, por construção, mais lento que chamada única. Pode **vetar** o agente em aplicações de latência crítica (interface conversacional tempo real, decisão em janela curta), "por melhor que ele resolva a tarefa em termos de qualidade".

3. **Observabilidade**: precisa ser **instrumentada desde o início**, não acrescentada depois. Sem registro de raciocínio/ação/observação por passo, não há como auditar nem depurar. Em setor regulado, vira **requisito**, não conveniência.

#### Figura 3 (descrição) — Da decisão de autonomia aos compromissos de projeto
"Decisão: agente ou workflow?" → 3 setas: "Custo de inferência" (cresce com nº de passos do laço) / "Latência" (soma tempo de cada chamada e tool) / "Observabilidade" (exige registrar e auditar o trace) → "Registrados no encontro 6, Desenhar a solução". Rodapé: "custo aproximado: nº de passos × custo por chamada (ilustrativo)", com 5 barras de alturas crescentes (1 a 5) ilustrando o aumento progressivo do custo.

#### Regra prática de dimensionamento (ordem de grandeza)
> **Custo de um agente ≈ (nº de passos × custo por chamada ao modelo) + custo de execução das tools.** Compare com o custo de uma chamada direta (unidade de referência). "Se o agente típico usa quatro passos e o pior caso usa oito, **dimensione pelo pior caso**, ou imponha um **teto de iterações** que torne o custo máximo previsível e financiável." A latência segue o mesmo raciocínio: estime pelo caminho **mais longo**, não o mais curto.

**Por que pelo pior caso, e não pela média**: como o caminho é decidido em execução, ele **varia** — é justamente essa variação que justificou escolher o agente. "Um sistema cujo caminho varia não tem um custo único, tem **uma distribuição de custos**, e orçar pela média ignora a cauda dessa distribuição, que é onde moram os casos caros." Impor teto de iterações corta essa cauda: troca-se pequena perda de capacidade em casos extremos por **custo máximo conhecido**.

**Exemplo aplicado (triagem de chamados)**: 4 passos típico / 8 pior caso vs. 1 chamada no workflow → agente custaria várias vezes mais no volume diário previsto e responderia mais devagar. Decisão: **teto de 6 iterações** + agente restrito à fila de exceções, workflow no caminho comum.

**Conexão final com o notebook**: Tarefa A = 2 passos, Tarefa B = 3 passos (um de erro+recuperação). Estimar pela Tarefa A subestimaria o consumo real — "é a variação de caminho, e não a média, que define o teto de custo e de latência." A Tarefa B era a **mais informativa para quem precisa orçar a solução**.

**Registro formal**: no ciclo da Formação 1, os três compromissos se registram no **encontro 6, "Desenhar a solução"**. A decisão entre agente e workflow **não pode ficar implícita**: precisa ser declarada, com justificativa e consequências de custo/latência/observabilidade. Os templates **T2.1** (matriz de decisão) e **T2.2** (matriz de modos de falha) são os instrumentos formais para esse registro; **o preenchimento, não a leitura do texto, é a evidência de aprendizagem do módulo.**

> **ARMADILHA de fechamento (box ATENÇÃO)**: "A confusão decisória de fechamento é **orçar o agente pelo caminho feliz e deixar a observabilidade para depois**. O resultado típico aparece em produção: o custo real supera o previsto no pior caso, e, quando uma decisão precisa ser auditada, não há trace para consultar. Custo e observabilidade são **compromissos de início de projeto**, não ajustes finais."

### 3.5 Conclusão da Aula 3

Três decisões encadeadas que organizam a camada decisória de M2:
1. **Heurística workflow vs. agente** — workflow como default, agente reservado ao branching dinâmico irrelutável que agrega valor real.
2. **Tratamento dos modos de falha** — loops, seleção de tool errada, prompt injection, cascading errors — com mitigações entre observação e próxima decisão.
3. **Tradução em compromissos de projeto** — custo de inferência, latência, observabilidade, dimensionados pelo **pior caso**.

> **Fio condutor**: inversão do ônus da prova — em IA Agentic, **quem precisa se justificar é a autonomia, e não o workflow**. Protege contra over-engineering agentic. "A maturidade no uso da lente está menos em saber montar um agente e mais em decidir, com critério e com números, se ele é necessário."

A autonomia atravessa os 7 eixos do programa: LLMs/NLP (eixo natural), Engenharia de Dados (agentes de inferência de schema), Real Time Processing (agentes assíncronos), Visão Computacional (agentes que orquestram tools de percepção). Decisão de fundo sempre a mesma: **quem controla o caminho, e a que custo**.

---

## 4. GLOSSÁRIO oficial do módulo (GLOSSÁRIO.pdf) — reprodução completa e fiel

> Convenção do próprio glossário: cada entrada traz tag de origem `[M2: seção]`; quando há box-glossário formal no texto-base, a definição reproduz o texto do box; termos do notebook trazem marca do notebook (ex.: `[M2: 2.1, IA-018]`); "veja X" = referência cruzada sem definição própria; ordem alfabética ignorando acentos/maiúsculas.

| Termo | Descrição | Origem |
|---|---|---|
| **Agente** | Sistema que percebe, decide e age sobre um ambiente em um laço, escolhendo a próxima ação em função das observações, em vez de seguir um caminho fixado de antemão. Distingue-se do assistente conversacional por agir sobre o mundo e por controlar a própria sequência de passos. | [M2: 2.1, IA-018] |
| **Agente single-loop** | Padrão aplicado em que o agente opera um único laço de decisão e ação, com um conjunto controlado de tools, repetindo perceber, decidir e agir até uma condição de parada. É o padrão central tratado em M2 e o construído no notebook do módulo. | [M2: 2.5, IA-018] |
| **Assistente conversacional** | Sistema que responde a entradas em linguagem natural sem agir sobre o ambiente nem decidir uma sequência de ações próprias. Diferencia-se do agente por não executar tools nem controlar o caminho da solução. | [M2: 2.2] |
| **Branching dinâmico** | Situação em que o próximo passo de uma solução depende de resultados que só surgem durante a execução, de modo que a sequência de ações não pode ser fixada de antemão. É o sinal central que distingue um problema de agente de um problema de workflow. | [M2: 2.7, IA-019] |
| **Cascading error** | Modo de falha em que um erro inicial vira entrada do passo seguinte e se amplifica ao longo do laço, de modo que uma observação ruim contamina as decisões posteriores. Mitiga-se validando a observação antes da próxima decisão. | [M2: 2.8, IA-019] |
| **Condição de parada** | Critério que encerra o laço de um agente, como atingir o objetivo, esgotar um limite de iterações ou detectar repetição de estado. Sua ausência é uma das causas de loop. | [M2: 2.1, IA-018] |
| **Custo de inferência** | Custo incorrido a cada execução do modelo. Num agente é multiplicativo, pois cresce com o número de passos do laço e com as tentativas de recuperação, e por isso deve ser estimado pelo pior caso, e não pela média. | [M2: 2.9] |
| **Laço (observation loop)** | Ciclo em que o agente percebe, decide uma ação, executa-a e incorpora a observação resultante antes da decisão seguinte. É a estrutura que define um agente, e que o notebook do módulo torna inspecionável. | [M2: 2.1, IA-018] |
| **Latência** | Tempo total de resposta de uma solução. Num agente é sequencial, pois soma o tempo de cada chamada ao modelo e de cada execução de tool, o que o torna mais lento que uma chamada única para o mesmo objetivo. | [M2: 2.9] |
| **Loop (modo de falha)** | Falha em que o agente repete ações sem progredir, como refazer a mesma busca ou alternar entre duas ações sem convergir. Mitiga-se limitando o número de iterações e detectando repetição de estado. Veja também condição de parada. | [M2: 2.8, IA-019] |
| **Memória de agente** | Componente que retém contexto entre os passos do laço, como observações anteriores e resultados intermediários, permitindo que o agente decida com base no histórico da tarefa, e não apenas na última entrada. | [M2: 2.1] |
| **Model Context Protocol (MCP)** | Protocolo aberto que padroniza a conexão entre agentes e ferramentas ou fontes de dados, no modelo cliente e servidor. Um agente compatível descobre e invoca recursos expostos por servidores que falam o protocolo, sem integração sob medida para cada par. Reduz o acoplamento entre o desenvolvimento de agentes e o de ferramentas. | [M2: 2.4, IA-017] |
| **Multiagente** | Paradigma em que vários agentes especializados cooperam, cada um com um papel, coordenados por um protocolo de troca. Tratado em alto nível no curso base; o detalhamento fica para os cursos da Fase 2. | [M2: 2.3] |
| **Observabilidade** | Capacidade de inspecionar, registrar e auditar o comportamento interno de um sistema em execução. Para um agente, significa ter o trace de raciocínio, ação e observação de cada passo disponível para depuração e para auditoria, e não apenas o resultado final. | [M2: 2.9, IA-019] |
| **Observação** | Resultado que o ambiente devolve ao agente após a execução de uma tool, e que alimenta a próxima decisão do laço. | [M2: 2.1, IA-018] |
| **Observation loop** | Veja Laço (observation loop). | — |
| **Orquestrador baseado em regras** | Camada de controle de caminho fixo que cerca o modelo num agente, cuidando de roteamento, validação e limites, de modo que o modelo decida apenas onde a interpretação aberta é necessária. Quanto mais do caminho é determinista, menor a superfície de falha. | [M2: 2.8] |
| **Plan-and-Execute** | Paradigma de agente que primeiro elabora um plano de passos e depois os executa, separando o planejamento da execução. Tratado em alto nível no curso base. | [M2: 2.3] |
| **Planning** | Etapa ou componente em que o agente organiza a sequência de ações a seguir, antes ou durante a execução da tarefa. | [M2: 2.1] |
| **Prompt injection** | Ataque ou falha em que conteúdo lido pelo agente a partir do ambiente, como um documento ou uma observação de tool, contém instruções que o desviam do objetivo original. É um risco próprio de sistemas que combinam leitura de texto não confiável com a capacidade de executar ações. | [M2: 2.8, IA-019] |
| **ReAct** | Paradigma de agente que intercala passos de raciocínio e passos de ação num mesmo laço. A cada iteração, o agente registra um raciocínio, escolhe uma ação, executa-a e incorpora a observação resultante antes do raciocínio seguinte. Tende a ser transparente e adaptável, ao custo de mais chamadas ao modelo. | [M2: 2.3, IA-017] |
| **Reasoning engine** | Componente de um agente que decide, a cada passo do laço, qual será a próxima ação. Lê o estado da tarefa e produz uma decisão (chamar uma ferramenta, registrar um resultado ou parar). Em geral é desempenhado por um modelo de linguagem, mas a função de decisão é distinta do modelo que a executa. | [M2: 2.1, IA-017] |
| **Reflection** | Paradigma em que o agente avalia a própria saída e a revisa antes de concluir, usando uma crítica como entrada de uma nova iteração. Tratado em alto nível no curso base. | [M2: 2.3] |
| **Seleção de ferramenta errada** | Modo de falha em que o agente escolhe a tool inadequada para o objetivo, ou a tool certa com argumentos errados. Mitiga-se restringindo o conjunto de tools disponíveis e validando os argumentos antes da execução. | [M2: 2.8, IA-019] |
| **Single-loop** | Veja Agente single-loop. | — |
| **Tolerância a falhas** | Grau de erro em laço que a solução aceita antes de intervir, decidido em função de custo, transparência e auditoria. Definir essa tolerância equivale a decidir quanto investir em validação e em observabilidade. | [M2: 2.9] |
| **Tool** | Função externa que o agente pode invocar para agir sobre o ambiente ou obter informação, como uma busca, um cálculo ou uma chamada de API. O agente a aciona por meio de tool calling. | [M2: 2.1, IA-018] |
| **Tool calling** | Mecanismo pelo qual um modelo de linguagem solicita a execução de uma função externa. Em vez de texto livre, o modelo emite uma chamada estruturada, com o nome da ferramenta e os argumentos, segundo um esquema declarado. O sistema executa e devolve o resultado como nova observação. É o contrato que liga decisão a ação. | [M2: 2.2, IA-017] |
| **Tool selection** | Veja Seleção de ferramenta errada. | — |
| **Trace** | Registro passo a passo do raciocínio, da ação e da observação de um agente ao longo do laço, usado para depurar e auditar. O notebook do módulo torna o trace inspecionável. Veja também observabilidade. | [M2: 2.1, IA-018] |
| **Workflow com chamadas pontuais de modelo** | Pipeline de caminho fixo em que um ou dois passos chamam um modelo para uma tarefa delimitada, como classificar, extrair ou redigir, sem que o sistema decida a sequência. É o meio-termo entre um script rígido e um agente. | [M2: 2.7] |
| **Workflow determinista** | Solução cujo caminho e ramificações são fixados de antemão por quem a desenha, executada de forma previsível e auditável, sem decisão de sequência em tempo de execução. É o default da heurística de M2. | [M2: 2.5, IA-018] |

---

## 5. TEMPLATE T2.1 — Matriz de Decisão Workflow versus Agente (estrutura completa)

**Título oficial**: "IA Agêntica: Matriz de decisão Workflow versus Agente" — Curso base de IA | Unidade M2 | Prof. Arthur Nascimento.

**Propósito declarado**: organiza a decisão da seção 2.7 do texto-base. "Não pergunta qual framework usar, e sim **quem deve controlar o caminho da solução**: o desenho fixo de um workflow ou a decisão em tempo de execução de um agente. Os três eixos são lidos em conjunto, e **qualquer um deles pode, sozinho, recomendar o workflow**."

**Estrutura do documento**: Face 1 (instrumento a preencher) → Face 2 (instrução de uso) → Exemplo preenchido de ponta a ponta.

### Face 1 — Instrumento (tabela a preencher)

| Eixo de decisão | Workflow determinista | Agente single-loop | Justificativa (1 a 3 frases) |
|---|---|---|---|
| **Branching dinâmico.** O caminho da solução pode ser fixado de antemão? | *O caminho do seu caso é fixável? Descreva os passos conhecidos.* | *Que parte do caminho só se decide em execução? Descreva a variação.* | *Qual alternativa o eixo favorece, com a evidência do caso.* |
| **Custo de inferência.** Quantas chamadas a mais o agente introduz? | *Quantas chamadas ao modelo o workflow faria?* | *Quantas chamadas no pior caso do agente, com recuperação?* | *O acréscimo do agente é sustentável no seu volume? Justifique.* |
| **Transparência e auditoria.** A sequência pode ser explicada e auditada? | *A sequência fixa é simples de explicar e registrar?* | *O que precisa ser registrado para auditar o agente?* | *Há requisito de transparência que pese na escolha? Justifique.* |

### Síntese decisória (checklist de opção final + justificativa livre)
```
[ ] Workflow determinista (o caminho é totalmente determinístico)
[ ] Workflow com chamadas pontuais de modelo (pipeline fixo com um passo de modelo)
[ ] Agente single-loop (o branching dinâmico é irrelutável e a autonomia agrega valor)

Justificativa da síntese: ____________________________________________
```
> Nota: há **três opções possíveis na síntese**, embora a tabela de eixos só contraste "Workflow determinista" vs. "Agente single-loop" — a terceira opção (workflow com chamadas pontuais de modelo) é o "caminho do meio" mencionado na Face 2.

### Face 2 — Instrução de uso (critérios de avaliação)
- **Eixo branching dinâmico (critério central)**: teste prático = tentar desenhar o fluxograma completo antes de executar. Consegue, com nº administrável de ramos → fixável → workflow. Ramificações dependem de conteúdo só disponível em execução, numerosas demais para enumerar → favorece agente.
- **Eixo custo de inferência**: workflow = número fixo e pequeno de chamadas. Agente = ao menos uma por passo, mais com recuperação de erro. **Avaliar pelo pior caso, não pela média** — "é a variação de caminho que define o teto de custo."
- **Eixo transparência e auditoria**: em setor regulado, ou quando stakeholder precisa entender a decisão, a previsibilidade do workflow pode pesar mais que a flexibilidade do agente, **mesmo que o branching seja alto**.
- **O que constitui justificativa adequada**: citar **evidência concreta do cenário** (não preferência geral). Em vez de "o agente é mais flexível" → "por que o caminho não pode ser fixado", "quantas chamadas a mais o agente exigiria", "qual requisito regulatório torna a auditoria obrigatória". 1 a 3 frases por eixo são suficientes.
- **Lembrete do caminho do meio**: antes de escolher agente, verificar se o caso não se resolve por workflow com chamadas pontuais de modelo (pipeline fixo, modelo entra só num passo de classificação/extração/redação) — "resolve boa parte dos casos que à primeira vista parecem pedir um agente."

### Exemplo preenchido (reprodução integral — caso de referência)

**Cenário**: indústria de equipamentos rotativos; triagem de chamados de manutenção em texto livre de operadores. Maioria segue fluxo previsível; fila de exceções exige consultar histórico, manuais e ordens abertas em ordem variável caso a caso.

| Eixo de decisão | Workflow determinista | Agente single-loop | Justificativa |
|---|---|---|---|
| Branching dinâmico | Para o chamado comum, o caminho é fixável: classificar, consultar a severidade, encaminhar. | Só a fila de exceções tem caminho variável, pois exige consultar histórico, manuais e ordens em ordem imprevisível. | O branching só é irrelutável nas exceções; no caso comum o caminho é conhecido, o que favorece o workflow. |
| Custo de inferência | Uma chamada de modelo por chamado, apenas na classificação. | De quatro a oito chamadas por chamado no pior caso, somando consulta e recuperação. | No volume diário previsto, o agente custaria várias vezes mais; o workflow mantém o custo previsível. |
| Transparência e auditoria | Sequência fixa, simples de explicar e registrar. | Exige trace completo para auditar cada decisão do laço. | A triagem alimenta indicadores de manutenção; a previsibilidade do workflow facilita a auditoria exigida. |

**Síntese do exemplo**: "Para a triagem de chamados de manutenção, a escolha é um **workflow com uma chamada pontual de modelo** no passo de classificação, reservando o **agente single-loop** apenas à fila de exceções. O caminho comum é fixável e sensível a custo e auditoria, e o branching dinâmico só é irrelutável nas exceções, onde a autonomia compensa o custo adicional e a perda de previsibilidade."

---

## 6. TEMPLATE T2.2 — Matriz de Modos de Falha e Mitigações (estrutura completa)

**Título oficial**: "IA Agêntica: Matriz de Modos de Falha e Mitigações" — Curso base de IA | Unidade M2 | Prof. Arthur Nascimento.

**Propósito declarado**: organiza os modos de falha da seção 2.8 do texto-base. "Parte de **quatro modos recorrentes, já mapeados**, e pede que você avalie, para o seu cenário, **como cada um apareceria, com que risco e com que mitigação**."

### Face 1 — Instrumento (tabela a preencher)
Escala de **Probabilidade** e **Severidade**: baixa, média ou alta.

| Modo de falha | Como apareceria no seu caso | Probabilidade | Severidade | Mitigação adotada |
|---|---|---|---|---|
| **Loop.** O agente repete ações sem progredir no objetivo. | *Como um loop apareceria na sua solução?* | baixa/média/alta | baixa/média/alta | *Ação concreta entre a observação e a próxima decisão.* |
| **Seleção de ferramenta errada.** O agente escolhe a tool inadequada, ou a tool certa com argumentos errados. | *Onde a tool ou os argumentos errados apareceriam?* | baixa/média/alta | baixa/média/alta | *Ação concreta de restrição ou validação.* |
| **Prompt injection.** Conteúdo vindo do ambiente desvia o agente do objetivo. | *Que conteúdo do ambiente poderia desviar o agente?* | baixa/média/alta | baixa/média/alta | *Ação concreta de isolamento ou validação.* |
| **Cascading error.** Um erro inicial vira entrada do passo seguinte e se amplifica. | *Como um erro inicial se propagaria no laço?* | baixa/média/alta | baixa/média/alta | *Ação concreta de validação da observação.* |
| **Outro modo identificado (opcional).** | *Descreva um modo específico do seu caso, se houver.* | baixa/média/alta | baixa/média/alta | *Ação concreta.* |

### Síntese de mitigação
```
Modo de maior risco: _______________  Mitigação prioritária: _______________
```
Critério: "o modo que combina as duas avaliações mais altas" (maior combinação de probabilidade × severidade) — é nele que a mitigação precisa ser mais firme, registrada como compromisso no desenho da solução.

### Face 2 — Instrução de uso

**O que cada modo significa** (reafirmação idêntica ao glossário/e-book):
- **Loop**: repetição de ações sem avanço (mesma busca várias vezes, alternância sem convergência).
- **Seleção de ferramenta errada**: tool inadequada, ou tool certa com argumentos errados.
- **Prompt injection**: texto vindo do ambiente (documento recuperado, saída de tool) contém instruções que desviam o agente.
- **Cascading error**: observação ruim contamina as decisões seguintes (saída de um passo = entrada do próximo).
- Remissão: detalhados na seção 2.8 do texto-base, resumidos no "quadro M2.q-4".

**Como avaliar probabilidade e severidade**:
- **Probabilidade**: quão frequente o modo tende a ser no cenário, dada a natureza das entradas e tools.
- **Severidade**: impacto quando ocorre — "uma resposta levemente pior é baixa, uma ação incorreta sobre um sistema externo é alta."
- **Modo prioritário**: combina as duas avaliações mais altas.

**O que constitui mitigação adequada**: ação concreta, quase sempre agindo **entre a observação e a próxima decisão**.
- Loop → limitar iterações + detectar repetição de estado.
- Seleção errada → restringir conjunto de tools + validar argumentos.
- Prompt injection → tratar todo texto do ambiente como **dado**, nunca instrução.
- Cascading error → validar a observação com checagens simples antes de seguir.
> "Evite registrar apenas a intenção, como **melhorar o prompt**, sem dizer qual verificação concreta será adicionada" — uma mitigação vaga/genérica é insuficiente; precisa ser **operacionalizável e verificável**.

### Exemplo preenchido (reprodução integral — caso de referência)

**Cenário**: agente que responde perguntas técnicas consultando documentos recuperados de base externa (busca trechos, lê, redige resposta). Como lê texto de origem não totalmente confiável e age sobre ele, está exposto aos quatro modos em graus diferentes.

| Modo de falha | Como apareceria | Probabilidade | Severidade | Mitigação adotada |
|---|---|---|---|---|
| Loop | Repete a mesma busca quando não acha o trecho esperado, sem reformular a consulta. | média | baixa | Limitar a seis iterações e detectar repetição da mesma consulta, encerrando com aviso ao usuário. |
| Seleção de ferramenta errada | Chama a busca com termos vagos, ou tenta resumir antes de recuperar o documento. | média | média | Restringir as tools a busca e leitura, e validar que a consulta tem termos mínimos antes de executar. |
| Prompt injection | Um documento recuperado traz uma instrução embutida, como "ignore as regras anteriores", que o agente poderia seguir. | média | **alta** | Tratar o conteúdo recuperado como dado entre delimitadores explícitos, nunca como instrução, e validar a ação antes de executá-la. |
| Cascading error | Um trecho recuperado fora de contexto leva o agente a partir de uma premissa errada e a aprofundá-la. | média | **alta** | Validar a relevância do trecho recuperado antes de usá-lo, conferindo a correspondência com a pergunta. |
| Outro modo identificado: **alucinação por obsolescência de contexto** (resposta desatualizada) | Responde com base em um manual já revisado, sem perceber que há versão mais recente. | média | média | Incluir a data do documento na observação e priorizar a versão mais recente na recuperação. |

**Síntese do exemplo**: "No agente que consulta documentos de uma base externa, o **modo de maior risco é a injeção de prompt (prompt injection)**, pela combinação de probabilidade média e severidade alta. A mitigação prioritária é isolar o conteúdo recuperado como dado, nunca como instrução, e validar a ação antes de executá-la, registrada como requisito de segurança no desenho da solução."

> Nota de calibração útil para avaliar respostas de alunos: no exemplo oficial, **dois modos empatam em severidade alta** (prompt injection e cascading error), ambos com probabilidade média — o critério de desempate para "maior risco" favoreceu prompt injection por ser o risco de **segurança** mais crítico num sistema que lê conteúdo externo e age. Um bom preenchimento de aluno deve justificar explicitamente esse tipo de desempate quando houver.

---

## 7. Anotações pessoais do aluno — pontos de cruzamento e observações

O arquivo `anotações.md` do aluno já continha, de forma condensada, a maior parte do conteúdo conceitual das três aulas (definição de agente, reasoning engine, tools, memória, planning, trace, assistente x agente, tool calling, paradigmas, MCP, os dois padrões aplicados, heurística workflow x agente, branching dinâmico, modos de falha, fechamento decisório). A leitura cruzada com os e-books originais confirma **fidelidade quase literal** às passagens do texto-base (as anotações parecem ser recortes diretos dos PDFs das Aulas 1 e 3).

**Divergência identificada** (já sinalizada na seção 1.4 acima): nas anotações, o parágrafo rotulado "plan-and-execute" reproduz textualmente a definição de **reflexão** ("o agente avalia criticamente o próprio resultado e tenta melhorá-lo numa nova passagem, usando a autocrítica como insumo"), quando a definição correta de plan-and-execute (confirmada pelo e-book da Aula 1 e pelo GLOSSÁRIO) é "paradigma que primeiro elabora um plano de passos e depois os executa, separando planejamento de execução". Ao avaliar respostas de alunos que citarem as anotações, verificar se não herdaram essa troca.

**Conteúdo das anotações sem contradição, apenas resumindo** o e-book: a heurística workflow x agente, os três eixos de decisão, os quatro modos de falha, os três compromissos de projeto (custo multiplicativo, latência sequencial, observabilidade instrumentada desde o início), a regra prática de dimensionamento pelo pior caso, e o fechamento com os templates T2.1/T2.2 conectados ao encontro 6 da Formação 1.

---

## 8. Lista consolidada de vocabulário técnico ("termo: definição")

> Base: GLOSSÁRIO.pdf (fonte primária e oficial), cruzado com e-books e templates. Ordem alfabética.

- **Agente**: sistema que recebe um objetivo, decide por conta própria as ações para alcançá-lo, executa-as sobre um ambiente via ferramentas, observa o resultado e repete até concluir a tarefa ou atingir condição de parada. Distingue-se do assistente por agir sobre o mundo e controlar a própria sequência de passos.
- **Agente single-loop**: padrão em que um único reasoning engine opera um laço de decisão e ação, com conjunto controlado (pequeno e curado) de tools e condição de parada explícita; sem hierarquia de planos, sem múltiplos agentes, sem orquestração complexa.
- **Assistente conversacional**: responde a entradas em linguagem natural numa única passagem do modelo, sem agir sobre o ambiente nem controlar sequência própria de ações.
- **Branching dinâmico**: próximo passo depende de resultados que só surgem durante a execução; não pode ser fixado de antemão. Sinal central que distingue problema de agente de problema de workflow.
- **Cascading error**: erro inicial vira entrada do passo seguinte e se amplifica ao longo do laço; mitiga-se validando a observação antes da próxima decisão.
- **Condição de parada**: critério que encerra o laço (objetivo atingido, limite de iterações, repetição de estado detectada); ausência é causa de loop.
- **Continuum de autonomia**: escala com 4 degraus — chatbot → assistente com 1 chamada de ferramenta → agente single-loop → agente com planejamento multi-passo/multi-agente; cada degrau amplia capacidade de lidar com tarefas abertas ao custo de mais inferência, latência e dificuldade de auditoria.
- **Custo de inferência**: custo incorrido a cada execução do modelo; num agente é multiplicativo (cresce com nº de passos e tentativas de recuperação); deve ser estimado pelo pior caso.
- **Laço (observation loop)**: ciclo perceber → decidir → agir → observar, repetido até objetivo ou condição de parada.
- **Latência**: tempo total de resposta; num agente é sequencial (soma cada chamada ao modelo e execução de tool).
- **Loop (modo de falha)**: repetição de ações sem progredir (refazer busca, alternar ações sem convergir); mitiga-se limitando iterações e detectando repetição de estado.
- **Mapa Técnico do Problema**: instrumento (de outra unidade da Formação 1) em que a leitura workflow/agente/híbrido, justificada pelas 4 perguntas de reconhecimento, se registra.
- **Memória de agente** (curto e longo prazo): componente que retém contexto entre passos; curto prazo = histórico que cabe na janela do modelo; longo prazo = armazenamento externo e durável, recuperado sob demanda.
- **Model Context Protocol (MCP)**: protocolo aberto cliente-servidor que padroniza conexão entre agentes e ferramentas/fontes de dados; reduz acoplamento (de produto N×M para soma N+M).
- **Multiagente**: paradigma com vários agentes especializados, cada um com papel/instrução/tools próprios, coordenados por orquestrador ou protocolo de troca de mensagens.
- **Observabilidade**: capacidade de inspecionar, registrar e auditar comportamento interno em execução; para agente = ter o trace disponível (não só a saída final).
- **Observação**: resultado devolvido pelo ambiente após execução de uma tool; alimenta a próxima decisão.
- **Orquestrador baseado em regras**: camada de controle de caminho fixo que cerca o modelo, cuidando de roteamento, validação e limites.
- **Over-engineering (agentic)**: armadilha de tratar arquitetura agentic como default moderno, envolvendo em laço autônomo tarefas de caminho conhecido, pagando custo/latência/imprevisibilidade sem ganho correspondente.
- **Paradigmas de raciocínio**: ReAct, Plan-and-Execute, Reflexão (Reflection), Multiagente — não são rivais excludentes, podem se combinar.
- **Plan-and-Execute**: elabora plano de passos antes, depois executa (e revisa se necessário), separando planejamento de execução.
- **Planning**: capacidade/etapa de decompor objetivo amplo em sequência de subtarefas (implícito ou explícito).
- **Prompt injection**: conteúdo lido do ambiente (documento, observação de tool) contém instruções que desviam o agente do objetivo original; risco próprio de sistemas que combinam leitura de texto não confiável com capacidade de ação.
- **ReAct (reasoning and acting)**: intercala passos de raciocínio explícito e ação no mesmo laço; transparente e adaptável, custo = mais chamadas ao modelo.
- **Reasoning engine**: componente que decide, a cada passo, a próxima ação; geralmente um LLM, mas a função de decisão é distinta do modelo que a executa.
- **Reflection (reflexão)**: agente avalia criticamente a própria saída e tenta melhorá-la numa nova passagem, usando autocrítica; eleva qualidade sobretudo com critério de sucesso verificável.
- **Seleção de ferramenta errada (tool selection)**: agente escolhe tool inadequada, ou tool certa com argumentos errados; mitiga-se restringindo tools e validando argumentos.
- **Tolerância a falhas**: grau de erro em laço que a solução aceita antes de intervir; decidida em função de custo, transparência e auditoria.
- **Tool**: função externa invocável pelo agente para agir sobre o ambiente ou obter informação.
- **Tool calling**: mecanismo pelo qual o LLM solicita execução de função externa via chamada estruturada (nome + argumentos, esquema declarado); sistema executa e devolve resultado como observação; "contrato que liga decisão a ação".
- **Trace**: registro passo a passo de raciocínio, ação e observação ao longo do laço; artefato principal para depurar e auditar.
- **Workflow com chamadas pontuais de modelo**: pipeline de caminho fixo com 1-2 passos que chamam modelo para tarefa delimitada (classificar, extrair, redigir); meio-termo entre script rígido e agente.
- **Workflow determinista**: caminho e ramificações fixados de antemão pelo projetista; previsível e auditável; sem decisão de sequência em runtime; é o default da heurística de M2.

---

## 9. Tipos de desafios prováveis (banco de referência para avaliação)

Com base na estrutura do módulo e nos dois templates (instrumentos formais de avaliação), os desafios mais prováveis seguem estes formatos:

1. **Classificação workflow vs. agente a partir de uma especificação** — dado um cenário de PD&I industrial, aplicar as 4 perguntas de reconhecimento (passos conhecidos? ramificação por regra ou interpretação? nº de chamadas fixo ou variável? orçamento de custo/latência/auditoria?) e concluir workflow, workflow-com-chamada-pontual, agente, ou híbrido.
2. **Preenchimento do T2.1 (Matriz de Decisão)** — dado um cenário, preencher as 3 linhas (branching dinâmico, custo de inferência, transparência/auditoria) com evidências concretas do caso (não genéricas) e marcar a síntese decisória com justificativa de 1-3 frases, mostrando leitura **conjunta** dos eixos (inclusive reconhecer quando um eixo sozinho veta a autonomia).
3. **Preenchimento do T2.2 (Matriz de Modos de Falha)** — dado um cenário com um agente já decidido, avaliar os 4 modos de falha (loop, seleção de tool errada, prompt injection, cascading error) em probabilidade/severidade (baixa/média/alta), propor mitigação concreta (não vaga) para cada um, identificar o modo de maior risco e a mitigação prioritária, possivelmente identificar um "quinto modo" específico do cenário.
4. **Diagnóstico de trace** — dado um trace (nos moldes do notebook IA_018), identificar: qual passo foi uma seleção de ferramenta/ação incorreta; qual observação permitiu a recuperação; se houve prompt injection, cascading error ou loop; se a condição de parada foi atingida corretamente; estimar quantas chamadas ao modelo o trace representa e qual seria o custo em produção.
5. **Distinção conceitual agente x assistente** — dado um sistema descrito, classificar no continuum de 4 degraus (chatbot / assistente+1 tool / agente single-loop / maior autonomia) e justificar citando a presença ou ausência de laço iterativo (não a presença de um LLM ou de tool calling pontual).
6. **Identificação e correção de armadilha/má prática** — dado um desenho de solução com over-engineering (agente aplicado a problema de caminho fixo), confiança indevida no trace como "prova de correção", orçamento pela média em vez do pior caso, observabilidade "deixada para depois", ou tool calling tratado como "habilidade do modelo" sem validação — identificar a armadilha e propor a correção alinhada ao texto-base.
7. **Cálculo/estimativa de custo e latência em ordem de grandeza** — dado nº de passos típico e pior caso de um agente, e custo de uma chamada direta, estimar o fator multiplicativo de custo, propor teto de iterações, e justificar por que o dimensionamento deve ser pelo pior caso.
8. **Reconhecimento de paradigma de raciocínio** — dado um trace ou uma descrição de comportamento, identificar se o padrão é ReAct, Plan-and-Execute, Reflexão ou Multiagente, e se o paradigma está bem ou mal encaixado ao problema (ex.: ReAct aplicado a tarefa com muitos passos triviais; reflexão sem critério verificável; multiagente para tarefa simples).
9. **Decisão de integração MCP** — dado um cenário com múltiplas ferramentas/agentes, decidir se compensa consumir um servidor MCP homologado ou construir integração própria, justificando pelos critérios do e-book (genérico e bem mantido vs. específico de domínio / requisito de segurança / controle como parte do valor).
10. **Reconhecimento de híbrido workflow+agente** — dado um cenário com fluxo majoritariamente fixo e uma etapa de exceção aberta, identificar corretamente que a autonomia deve ser **localizada** apenas no nó de exceção, não espalhada ao sistema inteiro.
11. **Conexão com os quatro componentes canônicos** — dado o código ou a descrição de um sistema, apontar explicitamente onde estão o reasoning engine, as tools, a memória (curto/longo prazo) e o planning (implícito/explícito).
12. **Pergunta de glossário/definição exata** — pedir a definição formal e exata de um termo (ex.: "defina branching dinâmico", "diferencie loop de cascading error", "o que torna uma tool de escrita mais arriscada que uma de leitura e o que mitiga isso") cobrando fidelidade à redação do GLOSSÁRIO.

### Checklist rápido de correção (para quem for avaliar respostas)
- A resposta cita **evidência concreta do cenário**, não afirmações genéricas tipo "agentes são mais flexíveis"?
- Ao recomendar agente, as **duas condições** (branching irrelutável **e** autonomia agrega valor real) foram verificadas, não apenas uma?
- O custo foi estimado pelo **pior caso**, não pela média?
- A mitigação proposta é uma **ação concreta** (validação, limite, isolamento) e não apenas "melhorar o prompt"?
- A resposta não confunde "presença de modelo" com "arquitetura agente" (workflow pode chamar modelo e continuar sendo workflow)?
- A resposta não trata o **trace como prova de correção** (ele mostra o que foi feito, não que estava certo)?
- Observabilidade e custo foram tratados como decisão de **início de projeto**, não ajuste posterior?

---

*Fim do documento. Fontes integralmente lidas: Aula 1.pdf (26 pág.), AUla 2.pdf (3 pág., guia do Colab), Aula 3.pdf (16 pág.), GLOSSÁRIO.pdf (6 pág.), TEMPLATE 1 - MATRIZ DE DECISAO.pdf (5 pág.), TEMPLATE 2 - MATRIZ DE MODO DE FALHA.pdf (5 pág.), IA_018.ipynb (20 células, código e outputs completos), anotações.md.*
