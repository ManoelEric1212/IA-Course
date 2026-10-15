# Unidade 6 — Transparência, Comunicação e Defesa (CP.B6 / Bloco B6)

Fonte: `Transparencia comunicacao e defesa/resumo.txt` (extraído de Aula 1/e-book CDP-038, Roteiro de status report CDP-039, Defesa de decisão arquitetural CDP-040, Model card CDP-041, Datasheet do dataset CDP-042, Glossário CDP-044).

## Visão geral
O bloco fecha o curso "pelo lado de fora": tudo que o caderno do projeto registrou desde o escopo (B2) até a matriz de avaliação contínua (B5) vira matéria-prima para três competências:
1. Comunicar progresso e incerteza para múltiplas audiências (CP.B6.C1).
2. Defender decisões técnicas perante audiência crítica (CP.B6.C2).
3. Produzir artefatos de transparência regulatória e tratar contestabilidade de decisões automatizadas (CP.B6.C3).

**Princípio central**: "Um projeto bem conduzido não precisa preparar a prestação de contas; ela é o subproduto natural dos registros que a condução já produziu." Caso de exemplo do bloco: manutenção preditiva de compressores (detecção de anomalias via vibração/temperatura, piloto em shadow deployment, inferência em lote on-premise).

## Tópico 1 — Comunicação por audiência

Comunicação é tratada como competência de **engenharia** (requisitos, projeto e teste), não como talento social. PD&I industrial exige várias audiências simultâneas e ritmo periódico — ao contrário do regime acadêmico (um público, um ritmo de publicação).

### Três audiências permanentes + 1 ocasional (mesma evidência, profundidades diferentes)
| Audiência | O que recebe | Cadência | Pergunta que responde |
|---|---|---|---|
| **Time técnico do squad** | Profundidade máxima: métricas por subgrupo (*subpopulation slices*), traces, decisões em aberto. | Contínua (painel) + semanal (report). | O que mudou no sistema e por quê. |
| **Empresa parceira** | Efeito no negócio: risco, cronograma, dependências. | Reports periódicos + gate reviews. | O que muda na operação e o que o projeto precisa de vocês. |
| **Mentor da residência** | Método: hipóteses, critérios, coerência dos artefatos. | Pontos de revisão do percurso. | — |
| **Stakeholder não técnico** (ocasional) | Camada executiva do report da parceira: 1 página, sem jargão, decisão pedida explícita. | — | — |

**Regra-chave**: adaptar a **camada** (profundidade/cadência/pergunta) sem adaptar o **conteúdo**. Quando o conteúdo diverge entre audiências, isso é **inconsistência**, não "comunicação por audiência" — custa mais caro que notícia ruim a tempo.

### Status report em cadência fixa (CDP-039)
4 campos fixos: **o que foi entregue / o que foi aprendido / o que vem a seguir / bloqueios e riscos**. Cadência declarada no início do projeto (semanal/quinzenal) e **mantida mesmo sem boa notícia**. Campo "aprendido" distingue o report de lista de tarefas (registra mudança de entendimento, inclusive hipóteses descartadas, e alimenta a revisão de processo dos gates). Pedido de decisão sempre destacado **no topo**, nunca escondido no meio. Formato mínimo: 1 página.

### Superfície do indicador
Para cada indicador da matriz de avaliação contínua (B5), declarar: (a) o que é contínuo/automático (painel, alerta); (b) o que é narrativo/periódico (report, gate review); (c) quem é o destinatário de cada camada. Sem superfície declarada, todo indicador tende ao painel — e painel que ninguém é obrigado a ler não sustenta decisão nenhuma. Exemplo: drift de vibração = contínuo/time técnico; qualidade da priorização = narrativa semanal/squad; dias de parada evitados = narrativa mensal/parceira.

### Tradução por audiência
Mesmo número, leitura diferente: para o squad, "precisão e cobertura"; para a parceira, "de 10 inspeções recomendadas, 7 encontram problema real (vs. 3 no critério antigo)". Caminho de volta da ficha de escopo do B2 (negócio → métrica técnica → de novo efeito no negócio).

### Incerteza honesta x indecisão paralisante
- **Incerteza honesta**: nomeia o limite de conhecimento + o plano que o enfrenta + o prazo da resposta.
- **Indecisão paralisante**: apresenta o não-saber sem plano nem prazo, transferindo a ansiedade ao interlocutor.

Credibilidade não vem de esconder o limite, vem de acompanhá-lo do plano.

**Armadilha de postura**: comunicar "como quem escreve paper" — acumular resultados em silêncio e entregar tudo no final. Consequência: stakeholder descobre risco tarde e passa a interpretar silêncio como sinal de problema.

**Report (fluxo) ≠ gate review (comporta)**: report registra o período sem exigir decisão; gate review consome os reports acumulados e produz decisão de continuar/pivotar/parar (B2). Report bem escrito torna o gate rápido.

## Tópico 2 — Defesa de decisão

Contraste de postura: pesquisador defende **achados** (critério: validade); engenheiro de PD&I defende **decisões** (critério: trade-off — por que esta alternativa, a este custo, sob estas premissas). Confundir os dois regimes produz defesas corretas que não respondem o que foi perguntado. Ocorre em: gate reviews, pontos de revisão com mentor, chegada de interlocutor novo com poder de veto (cenário mais traiçoeiro — só herda a conclusão).

### Estrutura canônica — 6 elementos (a ordem importa, é parte do argumento)
1. **Premissa** — o que se assume verdadeiro e de onde vem (ficha de escopo, acordo de dados, resultado de experimento).
2. **Alternativas consideradas** — ao menos 2 opções reais, tratadas a sério (não espantalhos).
3. **Eixos de avaliação** — declarados **antes** do veredito, os mesmos da matriz de alternativas do B3. Eixo inventado depois da escolha = racionalização.
4. **Decisão tomada** — a escolha + o custo assumido. Decisão sem custo declarado é propaganda.
5. **Riscos residuais** — o que fica em aberto, com dono e gatilho.
6. **Plano de revisão** — condição e gate que reabrem a decisão.

**Por que começar pela premissa, não pela decisão**: defesa que começa pela decisão soa como preferência buscando justificativa (convida a atacar a conclusão); defesa que começa pela premissa conduz a audiência pelo caminho do squad e transforma questionamento em revisão de etapas.

### Endereço de cada elemento no caderno (auditável)
- premissa → ficha de escopo + acordo de dados (B2, B4)
- alternativas/eixos → matriz de alternativas técnicas + ficha de decisão build/buy/integrate (B3)
- riscos residuais → matriz de risco (B2) + plano de validação e teste (B5)
- plano de revisão → cronograma de gates (B2)

### Preparação (2 movimentos)
1. **Antecipar perguntas por audiência**: gestor da parceira ataca custo/prazo; engenheiro sênior ataca premissa técnica e eixo ausente; mentor audita coerência entre decisão e artefatos. Pergunta sem artefato que a sustente = lacuna a fechar **antes** da reunião.
2. **Ensaio com o próprio squad como audiência crítica**, alguém atacando a premissa de verdade.

### Postura diante do questionamento (duas distinções)
- **Defender ≠ ser inflexível**: o plano de revisão já declara as condições de mudança de posição; ceder diante de evidência prevista é o processo funcionando.
- **Reconhecer limitação** (risco residual já registrado) **≠ admitir erro** (premissa era falsa e o processo não detectou). Para erro: reabrir o gate e registrar o que muda nos próximos ciclos — não minimizar.

**Armadilha de postura**: tratar questionamento como ataque e responder "como quem defende tese" (reafirmar com mais ênfase). O cliente não quer vencer o debate, quer saber se pode confiar no processo.

**Registro pós-defesa**: decisões aceitas voltam para a ficha de decisão com: quando foi defendida, para quem, que objeções surgiram, o que foi combinado no plano de revisão. Evita "defesa repetida" a cada troca de interlocutor.

Artefato do caderno: **Roteiro de defesa de decisão arquitetural (CDP-040)**.

## Tópico 3 — Transparência regulatória

Pergunta central: **o que alguém que nunca falou com o squad precisa saber para usar, auditar ou contestar o modelo/dados com segurança?**
- **Model Card** → responde pela solução (Mitchell et al., 2019).
- **Datasheet do Dataset** → responde pelos dados (Gebru et al., 2021).

Em setores regulados, são a diferença entre entrega auditável e caixa-preta bem intencionada.

### Model Card simplificado (CDP-041)
Campos: identificação e versão; **uso pretendido**; **usos fora de escopo**; dados de treino e avaliação; métricas com desagregação por *slice*; limitações e vieses conhecidos; condições de revisão. "Simplificado" = registra só o que o projeto sustenta com **evidência** dos próprios artefatos — campo com aspiração é "passivo esperando auditoria".

Par mais importante: **uso pretendido + usos fora de escopo** — funciona como o "escopo negativo" do B2 voltado para fora. Sem o campo negativo, todo uso vira uso implícito e toda falha vira falha do modelo. Exemplo compressores: uso pretendido = priorizar inspeções; fora de escopo = desligamento automático de equipamento e qualquer decisão sobre pessoas (ex.: avaliar desempenho de operadores).

Cada campo tem artefato de origem rastreável (ficha de escopo, canvas de arquitetura, plano de aquisição, mapa de governança, plano de validação, matriz de avaliação contínua). Campo sem lastro = invenção; decisão/limitação do ciclo que não aparece em campo nenhum = omissão.

### Datasheet do Dataset (CDP-042)
Campos: motivação (por que existe e quem responde por ele); composição (cobertura, lacunas, vieses); coleta e pré-processamento; usos recomendados e desaconselhados; distribuição e manutenção (responsável nomeado). Consolida o plano de aquisição e o mapa de governança do B4 para leitor externo. Exemplo compressores: 2 anos de séries de vibração/temperatura de 3 famílias; viés conhecido = sub-representação de partida a frio (*cold start*) e concentração de carga parcial na família maior.

**Regra geral dos dois artefatos**: alegação ("dois anos de dados") não é evidência; o **relatório de perfilamento estatístico** (nulos, cardinalidade, distribuições, vieses — ver B4) é a evidência técnica auditável.

**Transparência ≠ publicação**: o nível de detalhe respeita o acordo de dados (B4); há campos que circulam só entre as partes ou em versão resumida para auditoria — isso é marcado explicitamente no documento.

**Versionamento e momento**: model card e datasheet carregam a versão do modelo/dataset; mudança que atravessa gatilho de retreinamento gera **nova versão**, nunca edição silenciosa (ver versionamento no B4/B5). Nascem amarrados ao cronograma (ao gate que autoriza o piloto), nunca na véspera da entrega final.

**Coerência cruzada** é testável nos dois sentidos entre os dois documentos (ex.: "dados de treino" do card deve bater com "composição" do datasheet, na mesma versão). Falha célebre de exemplo: card prometia "alertas em tempo real" enquanto canvas/runbook registravam "inferência em lote" — um auditor acharia a contradição em minutos.

### Contestabilidade de decisões automatizadas
**Definição**: capacidade de uma pessoa afetada obter explicação inteligível de uma decisão automatizada e contestá-la perante um responsável, com prazo e possibilidade de revisão humana.

| Norma | O que exige | Implicação operacional (vira backlog com dono e evidência) |
|---|---|---|
| **EU AI Act** (Reg. 2024/1689) | Art. 13: transparência/informação ao *deployer* de sistema de alto risco; art. 86: direito à explicação de decisão individual. | Model card/datasheet completos + registro de versão/entrada que reconstrua uma decisão específica. |
| **GDPR** (Reg. 2016/679), art. 22 | Restringe decisões **exclusivamente** automatizadas com efeito jurídico/similar sobre pessoas; exige supervisão humana e canal de contestação. | Supervisão humana desenhada na arquitetura + canal de contestação com responsável e prazo. |
| **PL 2338/2023** (Brasil, em tramitação) | Direitos de informação, explicação, contestação e revisão humana, graduados pelo risco. | Triagem regulatória revisitada a cada gate + documentação pronta antes da entrega. |
| **LGPD**, art. 20 (vigente) | Direito de solicitar revisão de decisão automatizada — **sem** exigir revisão por pessoa natural (parágrafo que previa isso foi vetado em 2019). | — |

**Triagem regulatória importa mais que reflexo automático**: no caso dos compressores, a decisão é sobre **máquinas**, não pessoas → art. 22 GDPR e art. 20 LGPD não incidem, não é "alto risco" no EU AI Act. O regime muda se a mesma esteira passar a avaliar desempenho de operadores (pessoas) — por isso a triagem (do B4) deve ser revisitada a cada gate.

Lição final: contestabilidade não é parágrafo jurídico de rodapé, é **arquitetura e monitoramento** — exige reprodutibilidade operacional (B5) para explicar uma decisão específica, e runbook (canal/prazo/responsável) para responder contestação.

## Glossário consolidado (CDP-044)
- **Comunicação por audiência** — adaptar camada (abstração/cadência/pergunta) sem adaptar conteúdo. Divergência de conteúdo = inconsistência.
- **Contestabilidade** — ver Tópico 3.
- **Datasheet do dataset** — artefato Gebru et al. (2021) que documenta os dados para leitor externo.
- **Defesa de decisão** — estrutura de 6 elementos (premissa → alternativas → eixos → decisão/custo → riscos residuais → plano de revisão). Decisão se defende por trade-off; achado, por validade.
- **Incerteza honesta e indecisão paralisante** — ver Tópico 1.
- **Leitura executiva** — 1 página sem jargão para stakeholder não técnico, com decisão pedida explícita, derivada do report da parceira.
- **Model card simplificado** — artefato Mitchell et al. (2019) que documenta o modelo; "simplificado" = só o que há evidência.
- **Plano de revisão** — elemento final da defesa: condição + gate que reabrem a decisão; distingue firmeza de inflexibilidade.
- **Registro pós-defesa** — linha de contexto na ficha de decisão após defesa aceita (quando, para quem, objeções, combinado). Evita defesa repetida.
- **Status report em cadência fixa** — 4 campos (entregue/aprendido/a seguir/bloqueios), cadência mantida mesmo sem boa notícia, decisão no topo.
- **Superfície do indicador** — para cada indicador da matriz B5: o que é contínuo/automático vs. narrativo/periódico, e o destinatário de cada camada.
- **Uso pretendido e usos fora de escopo** — par do model card que delimita cenários homologados e desaconselhados (escopo negativo do B2 voltado para fora).

## Quadro-resumo: artefatos do bloco B6
1. **Roteiro de status report** (CDP-039) — comunicação periódica por audiência, cadência fixa, 4 campos + superfície do indicador declarada.
2. **Roteiro de defesa de decisão arquitetural** (CDP-040) — 6 elementos + preparação por audiência + registro pós-defesa.
3. **Model card simplificado** (CDP-041) — transparência sobre o modelo.
4. **Datasheet do dataset** (CDP-042) — transparência sobre os dados.

Todos nascem amarrados ao cronograma de gates (nunca escritos de memória, na véspera) e são consolidações/traduções do que já foi registrado em artefatos anteriores (B2–B5), não documentos escritos do zero.

## Correspondência com o kit de laboratório (Projeto Aroeira)
O **Roteiro de Pitch e defesa curta** do Encontro 3 ("a bancada pergunta o que a proposta não resolve") é a aplicação direta da estrutura de 6 elementos deste bloco — cada resposta do squad já aponta o artefato (C3-02 + Matriz de Validação; `d1_frota` + riscos; premissa da Decisão) exatamente como o padrão "endereço no caderno" prescreve. O **Registro de princípios transferíveis** do E3 é próximo, em espírito, ao registro pós-defesa. Quando a residência avançar além do Encontro 3, os artefatos formais **Model Card** e **Datasheet do Dataset** deste bloco são o próximo passo natural de documentação do alerta de telemetria e do dataset de ordens de serviço — especialmente relevantes dado que `id_tecnico` é dado potencialmente sensível (ver B4) e que a C3-01 (jurídico) já exige "registro recuperável" de cada resposta/alerta/causa.
