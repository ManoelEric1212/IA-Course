# Unidade 3 — Decisão de Solução e Arquitetura (CP.B3)

Fonte: e-book `Decisão de soluçâo e arquitetura/MAterial/Aula 1.pdf` (CDP-015) + templates CDP-016 (Ficha de hipóteses e experimentos), CDP-017 (Matriz de alternativas técnicas), CDP-018 (Ficha de decisão build/buy/integrate), CDP-019 (Canvas de arquitetura conceitual), CDP-020 (Mapa de fornecedores e PI).

Esta unidade é a segunda decisão estruturante do projeto, depois da delimitação de escopo (B2). No CRISP-DM adaptado do curso, é a passagem da compreensão do problema para a concepção da solução.

## 1. Da hipótese à decisão build/buy/integrate (CP.B3.C1)

**Regra de sequência**: a decisão de solução não é o começo desta fase, é o fim dela. Antes da decisão vêm as hipóteses; antes da escolha vem a comparação. O erro mais comum não é escolher a técnica errada, é **escolher cedo demais** — "vamos usar um modelo de linguagem" pula duas etapas de trabalho, e o custo aparece depois, quando ninguém sabe responder "por que não uma alternativa mais simples?".

Cadeia de três elos antes do fechamento: **hipóteses formuladas → experimentos que as testam → alternativas comparadas → decisão.**

### Elo 1 — Hipótese técnica
**Hipótese técnica**: enunciado testável sobre a solução, com quatro componentes fixos: **abordagem proposta, condição sob a qual deve funcionar, resultado esperado e critério de teste**. Diferença de um palpite ("acho que deep learning resolve") para uma hipótese: "um classificador de imagens treinado com as fotos já coletadas pela linha (abordagem), operando sobre a iluminação atual das câmeras (condição), deve sinalizar os três defeitos mais frequentes (resultado esperado), com recall mínimo de 85% em um conjunto de teste reservado (critério de teste)".

Dois complementos obrigatórios:
- **Justificativa**: por que esta hipótese merece ser testada antes das outras — nomeia a evidência que a motiva e reconhece o custo assumido ao priorizá-la.
- **"Este é um problema de X e não de Y?"**: evidência que distingue o tipo do problema (ex.: falhas raras e mal rotuladas → detecção de anomalias; histórico rotulado e balanceado → classificação supervisionada). Errar essa distinção no início contamina todas as decisões seguintes.

### Elo 2 — Experimento mínimo
Hipótese sem experimento é opinião com estrutura melhor. **Mínimo** é a palavra operativa: o experimento não constrói a solução, constrói a informação para decidir sobre ela. Dois eixos obrigatórios (vêm do B2): **prazo fechado** (impede que o teste vire projeto dentro do projeto) e **critério de descarte**, declarado antes do resultado (transforma o abandono em cumprimento de acordo, não em derrota). Na régua do PD&I industrial, insistir numa hipótese sem critério é o risco nº1 do cronograma.

### Elo 3 — Matriz de Alternativas Técnicas (CDP-017)
Alternativas nas linhas (**ao menos duas**, três é usual), cinco dimensões nas colunas:

| Dimensão | Pergunta que responde |
|---|---|
| **Aderência ao problema** | O quanto a alternativa resolve o problema como delimitado no B2 — não uma versão conveniente dele. |
| **Dados necessários** | O que a alternativa exige em volume/rotulagem/qualidade, e o quanto disso existe (conversa com o lastro de dados da Ficha de Escopo). |
| **Viabilidade** | O squad consegue executar com a equipe, tempo e infraestrutura declarados? Distingue **viável tecnicamente** de **viável operacionalmente** (manutenibilidade, perfil da equipe, TCO — Total Cost of Ownership). |
| **Riscos** | O que pode falhar de específico naquela alternativa (qualquer categoria da taxonomia do B2). |
| **Explicabilidade / TRL** | Nível de explicabilidade exigido (M5) e maturidade tecnológica (TRL). |

**TRL** (Technology Readiness Level): escala de maturidade de 1 (princípio observado) a 9 (sistema comprovado em operação); calibra a distância entre resultado publicado e sistema operável.

Cada célula exige **justificativa curta** (nomeia o critério, conecta ao cenário, reconhece o custo assumido) — "viabilidade alta" sozinho não é preenchimento válido. Ao final: **abordagem recomendada + pontos de incerteza**. A matriz **recomenda, mas não fecha**: comparar e decidir no mesmo gesto é a receita para a comparação virar racionalização da preferência — a escolha é ato separado.

### Exemplo de referência (compressores de planta química, CDP-016/017)
Três alternativas comparadas: (A) desenvolver detector próprio — alta aderência, TRL baixo até piloto, custo/operação recaem no squad; (B) comprar sistema comercial de condition monitoring — aderência parcial, TRL alto, mas vendor lock-in e nuvem externa fere política de dados; (C) integrar bibliotecas abertas de condition monitoring + lógica de alerta própria — alta aderência, roda local, TRL intermediário. Recomendação: **C, integrar** — preserva política de dados (inferência local), concentra desenvolvimento na lógica diferenciadora, reaproveita componentes maduros.

## Decisão build/buy/integrate — os seis eixos

A pergunta não é "qual técnica funciona melhor", é **"de onde vem a solução"**:
- **Desenvolver (build)**: construir.
- **Comprar (buy)**: adotar solução existente (produto comercial ou serviço gerenciado).
- **Integrar (integrate)**: compor componentes existentes (abertos ou contratados) com desenvolvimento próprio só na lacuna. Com o ecossistema atual de modelos de fundação/APIs/bibliotecas maduras, **a maioria dos projetos reais é algum grau de integração** — a pergunta prática é onde passa a fronteira.

Heurística clássica (4 eixos) **ampliada neste curso para 6**, porque a ausência dos dois últimos é fonte recorrente de retrabalho (os problemas aparecem na operação e na formalização contratual, não na prototipagem):

1. **Custo** — desenvolvimento/operação próprios vs. licenças/assinaturas.
2. **Prazo** — construir vs. adotar.
3. **Controle** — quanto a organização governa comportamento e evolução da solução.
4. **Dependência** — quanto a solução fica amarrada a decisões de terceiro.
5. **Viabilidade operacional** (eixo novo) — distinção crucial: *viável tecnicamente* ≠ *viável operacionalmente*. Decompõe-se em: manutenibilidade, dependência de equipe especializada, integração com infraestrutura existente, custo de operação (inferência, monitoramento, retreinamento, suporte).
6. **Propriedade intelectual** (eixo novo) — a quem pertence o que a escolha produz e o que usa (modelo resultante, dados de treinamento, melhorias sobre componentes de terceiros, o que o contrato permite publicar/reutilizar/comercializar). Ver Tópico 3.

### Árvore de leitura (ponto de partida, não ponto de chegada)
- Prateleira **cobre por inteiro** → partida = **Comprar** (exame: custo recorrente, dependência, controle cedido).
- Prateleira **cobre em parte** → partida = **Integrar** (exame: esforço real de integração, fronteira de PI).
- Prateleira **não cobre** → partida = **Desenvolver** (exame: prazo, equipe, custo total de operar).

A decisão só fecha depois que a justificativa percorre os seis eixos — é comum que o exame mova a escolha para um ramo vizinho.

**Armadilha de postura**: tratar "desenvolver" como opção default. Na régua da pesquisa, construir é o mérito; na régua do PD&I industrial, construir é o custo, e o mérito é resolver dentro do prazo/orçamento com o menor compromisso futuro.

### Artefato: Ficha de Decisão build/buy/integrate (CDP-018)
Seis eixos pré-mapeados, justificativa de 1–3 sentenças por eixo (evidência + cenário + custo assumido), e **síntese decisória**: opção escolhida + fronteira (quando integrar: o que vem de fora, o que é construído, onde passa a divisa).

### Fechamento da decisão (generaliza para qualquer decisão estruturante)
Registrar quatro coisas: **a escolha**; a **justificativa vinculada** aos critérios da matriz/ficha (não à autoridade de quem decidiu); as **premissas** assumidas (candidatas a risco na matriz do B2); os **pontos de incerteza** que permanecem, com gatilho de reabertura ("se uma premissa for invalidada, a decisão deve ser revisada" — maturidade de gestão, não fragilidade).

No laboratório, este fechamento é a **Decisão Justificada** (KIT, Encontro 3) — generaliza o padrão para qualquer escolha estruturante (origem da solução, técnica central, componente crítico).

## 2. Arquitetura conceitual pelas cinco lentes (CP.B3.C2)

**Arquitetura conceitual**: representação da solução no **nível do fluxo** — de onde vêm os dados, que transformações sofrem, que componentes os processam, o que sai e para quem. Precede escolhas de implementação. Instrução central: **"representar o fluxo, não implementar"**. Critério de qualidade: um colega de outro eixo técnico deve entender o diagrama sem explicação oral.

### Espinha do canvas (6 campos, do kit)
1. **Entrada de dados** — fonte e tipo (de onde vêm, formato, frequência).
2. **Pré-processamento e preparação** — limpeza, filtragem, transformação, anotação.
3. **Componentes e modelos** — peças que processam, por **responsabilidade** (não por biblioteca/versão).
4. **Saída esperada** — o que o sistema produz, em que forma, para qual consumidor (humano ou sistema).
5. **Lógica e fluxo** — como as partes se conectam: ordem, condições, caminhos alternativos.
6. **Pontos de risco e falha no fluxo** — onde quebra; que suposições cada seta carrega. **Arquitetura sem pontos de falha declarados é arquitetura que ainda não foi pensada até o fim.**

Nota de granularidade: evitar o canvas **genérico demais** (um único componente "modelo de IA" não decide nada) e o **detalhado demais** (especificar bibliotecas/versões antecipa implementação e fica obsoleto). Granularidade certa = responsabilidades, nomeadas pelo que fazem.

### Camada de leitura: as cinco lentes do curso base, como perguntas ao canvas
| Lente (módulo) | Pergunta dirigida ao canvas |
|---|---|
| **Data Centric (M3)** | Diante da entrada/pré-processamento: que dados sustentam a solução, qual o teto de qualidade que impõem? |
| **Explainable (M5)** | Diante da saída esperada: qual regime de explicabilidade é exigido — regulatório, usabilidade do produto ou depuração? |
| **Generativa (M1)** | Diante dos componentes: este componente gera ou discrimina? A decisão GenAI × ML clássico foi tomada com os critérios do M1? |
| **Agentic (M2)** | Diante da lógica/fluxo: workflow determinista ou agente com autonomia? O branching dinâmico justifica a segunda opção? |
| **Edge (M4)** | Diante do fluxo inteiro: onde a inferência ocorre — compromisso de produto ou acidente de implementação? |

### Ordem típica das lentes
Princípio: decisões que **restringem** o espaço de solução vêm antes das que **otimizam** dentro do espaço restante.

Ordem típica: **1) Data Centric** (disponibilidade/qualidade de dados é a restrição mais dura) → **2) Explainable**, face regulatória (se há obrigação legal, classes inteiras de solução opaca saem do espaço cedo) → **3) Generativa** (paradigma do componente central, espaço já restringido) → **4) Agentic** (orquestração sobre componentes já definidos) → **5) Edge** (posição da inferência, condicionada pelo que Data Centric/Explainable já fixaram).

Duas ressalvas: (a) "por fim" não é *afterthought* — deployment é compromisso de produto desde o primeiro rascunho, apenas se decide condicionado pelas anteriores; (b) a ordem é **típica, não rígida** — se a restrição dominante for latência de chão de fábrica, Edge sobe na fila.

### Teste de coerência: cruzamentos, não slots isolados
A arquitetura coerente não é a que tem as melhores respostas por lente isoladamente; é a que tem respostas que **se sustentam mutuamente**. Armadilha comum: tratar as lentes como checklist isolado (cada slot "localmente ótimo"), ignorando os cruzamentos — a arquitetura aprova em cada revisão temática e falha na primeira leitura de conjunto.

**Caso coerente** (manutenção preditiva de compressores): dados locais → inferência local (Edge condicionado por Data Centric) → par discriminativo (anomalia + classificador de modo de falha, sem o que gerar) → workflow determinista (sem branching que justifique agente) → explicabilidade por features, satisfazível.

**Caso incoerente** (mesmo problema, assistente conversacional com LLM via API + agente): o slot Edge exige dados não saírem da planta, mas a API gerenciada os envia para fora; o slot Explainable promete justificar cada alerta, mas agente+generativo inviabiliza explicação determinista; o slot Data Centric admite poucos exemplos rotulados, mas a proposta exige avaliar linguagem natural (que precisa justamente da rotulagem que não existe). Três decisões defensáveis isoladamente, arquitetura indefensável no conjunto.

**Correção**: não se escolhe o "vencedor" entre slots — volta-se à lente com a restrição mais dura (aqui, soberania de dados) e **propaga-se** a correção pelas demais.

### Artefato: Canvas de Arquitetura Conceitual (CDP-019)
Espinha de 6 campos + slots por lente (com justificativa) + ordem em que as decisões foram tomadas. Coerência cruzada: reflete a Ficha de Decisão (fronteira do integrate aparece no canvas) e alimenta o B4 (entrada/pré-processamento) e o B5 (saída esperada e pontos de falha → plano de validação).

## 3. Fornecedores e propriedade intelectual como restrição arquitetural (CP.B3.C3)

Tese do tópico: fornecedores e PI **não são anexo jurídico resolvido depois do desenho técnico — são restrição arquitetural**, no mesmo sentido que latência ou disponibilidade de dados.

### Taxonomia de fornecedores (5 categorias)
| Categoria | O que fornece | Questões contratuais/PI características |
|---|---|---|
| **Provedor de cloud** | Computação, armazenamento, serviços gerenciados. | Localização/soberania dos dados; custo de saída (egress); disponibilidade contratada; dependência de serviços proprietários. |
| **Provedor de modelo** | Modelo de fundação, pesos ou inferência por API. | Licença de uso comercial; destino/retenção dos dados enviados; PI sobre ajuste fino; estabilidade de versão/preço. |
| **Fornecedor de dados** | Dados externos públicos ou licenciados. | Licença de uso/redistribuição; restrição de uso secundário; responsabilidade por qualidade/origem lícita. |
| **Fornecedor de anotação** | Rotulagem como serviço. | Confidencialidade do material exposto; PI sobre os rótulos; qualidade contratada com métrica/amostragem. |
| **Parceiro técnico** | Desenvolvimento, integração, sustentação. | PI sobre o que é construído; exclusividade; transferência de conhecimento/código ao final. |

As categorias **se acumulam** (restrições se compõem); a coluna de questões é **pauta de conversa com o jurídico**, não desconfiança — o squad não redige cláusula, mas sabe que ela precisa existir.

### PI de modelo — o caso do modelo derivado
**Modelo derivado**: resultado de ajuste fino, destilação ou continuação de treinamento sobre base pré-treinada de terceiros, com dados do cliente e trabalho do squad. A propriedade depende de **três camadas lidas em conjunto**: a licença da base (nem todo modelo "aberto" é livre — pode ter cláusula de escala, AUP, ou ser só para pesquisa), o contrato com o cliente, e os termos do provedor onde o ajuste ocorre. Sem alinhar as três camadas: "criou um objeto com três donos potenciais" → litígio com pesos.

### PI de dados — três regimes que a pesquisa raramente separa
- O que **pode virar publicação**: resultados, métodos, agregados — autorizados pelo contrato, após revisão da parceira.
- O que cai **sob NDA**: dados brutos, detalhes de processo produtivo.
- O que tem **restrição de uso secundário**: dados cedidos para um fim não alimentam outro sem novo acordo.

### Quatro cláusulas típicas e o que cada uma afeta na arquitetura
- **NDA** → define onde os dados podem ser processados → restringe cloud/API externa → conecta-se à lente **Edge**.
- **PI sobre modelos derivados** → define a quem pertence o ajuste fino → afeta a decisão **build/buy/integrate**.
- **Direitos de publicação** → afetam cronograma (revisão da parceira é dependência) e motivação acadêmica do squad.
- **Exclusividade** → define o que não pode ser reutilizado → afeta cálculo de custo de desenvolver.

### Vendor lock-in
Dependência de fornecedor que não vem de uma cláusula isolada, mas da **acumulação** delas (serviços/formatos/APIs proprietários elevam o custo de transição — *switching cost*). Mitigação arquitetural+contratual: preferir formatos/interfaces abertos nas fronteiras entre componentes, isolar serviços proprietários atrás de camadas de abstração, negociar cláusulas de saída com portabilidade. Regra: **dependência aceita conscientemente, com preço registrado, é decisão; dependência descoberta na operação é dívida.**

**Armadilha de postura**: assumir o direito de publicar (default acadêmico). Em PD&I industrial, publicação é cláusula, não default.

### Artefato: Mapa de Fornecedores e PI (CDP-020)
3+ fornecedores identificados, categoria, o que fornecem na arquitetura, questões contratuais aplicáveis, restrição resultante; síntese com o que precisa chegar ao jurídico antes do contrato. Coerência cruzada: cada componente de terceiros do canvas tem linha no mapa; **alimenta a Matriz de Risco do B2** (categorias Dependência Externa e Propriedade Intelectual) com nome, contrato e responsável.

## Cadeia de coerência do bloco
Hipóteses → Experimentos → Matriz de Alternativas → **Ficha de Decisão** (build/buy/integrate) → **Canvas de Arquitetura** (5 lentes) → **Mapa de Fornecedores e PI**. Nenhum artefato vale sozinho; o valor está em percorrer a cadeia nos dois sentidos.

## Correspondência com o kit de laboratório (Formação 1 / Projeto Aroeira)
| Instrumento deste curso (CDP) | Instrumento do kit (KIT) | Encontro |
|---|---|---|
| Ficha de Hipóteses e Experimentos (CDP-016) | Hipótese Técnica (KIT-003) | Encontro 1 |
| Matriz de Alternativas Técnicas (CDP-017) | Matriz de Alternativas (KIT-004) | Encontro 2 |
| Ficha de Decisão build/buy/integrate (CDP-018) | Decisão Justificada (KIT-007/008) | Encontro 2/3 |
| Canvas de Arquitetura Conceitual (CDP-019) | Canvas de Arquitetura Conceitual | Encontro 2/3 |
| Mapa de Fornecedores e PI (CDP-020) | Mapa de governança e propriedade intelectual | Encontro 3 |

## Bibliografia mínima
- HUYEN, C. *Designing Machine Learning Systems*. O'Reilly, 2022 (caps. 1, 2 e 10 — build vs. buy em infraestrutura de ML, custo de saída da nuvem).
- ANTHROPIC. *Building Effective Agents*. Anthropic Engineering, 2024 — base da lente Agentic (workflow determinista x agente).
- WIPO. *Revised Issues Paper on Intellectual Property Policy and Artificial Intelligence* (WIPO/IP/AI/2/GE/20/1 REV), 2020 — PI de modelo e de dados.
