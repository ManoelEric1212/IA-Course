# Unidade 4 — Dados em PD&I Industrial (CP.B4)

Fonte: e-book `Dados em PDI INdustrial/Aula 1.pdf` (CDP-024) + `Resumo.txt` (CDP-025 Plano de aquisição de dados, CDP-026 Mapa de governança e regulatório) + `Glossário.pdf`.

Premissa do bloco: o repertório técnico de data quality, error analysis e análise de viés (módulo M3 do curso base) é **necessário mas não suficiente** para conduzir o eixo de dados de um projeto industrial. O que falta — e o que este bloco acrescenta — é a articulação dessas competências com **cronograma, custo, dependências externas e regime regulatório**.

Fato empírico estruturante: o eixo de dados é a fonte mais frequente de atraso e de descalibragem de expectativa em projetos de IA industrial (Sambasivan et al., "cascatas de dados" — equipes subinvestem no trabalho de dados porque ele é percebido como preparação, não entrega; o custo aparece tarde, composto). Diferença de postura (ecoa B1): na régua da pesquisa, o dataset é ponto de partida (alguém já o construiu); na régua do PD&I industrial, **o dataset é um entregável intermediário do próprio projeto**, com dono, prazo, custo e qualidade a negociar.

## 1. Aquisição e qualificação operacionais (CP.B4.C1)

### Prontidão de fonte (escala de 5 níveis)
Classificação operacional aplicada a **cada fonte de dados separadamente**, antes de assumir qualquer prazo que dependa dela.

| Nível | Nome | Evidência | Pergunta de verificação |
|---|---|---|---|
| N1 | Existência presumida | Só uma afirmação ("alguém disse que existe"). | Quem é o responsável e onde os dados estão armazenados? |
| N2 | Existência confirmada | Sistema de origem identificado, dono responde por ele; ninguém viu um registro. | — |
| N3 | Amostra inspecionada | Esquema, volume e qualidade vistos em amostra real. | O que a amostra mostra que a conversa não mostrou? |
| N4 | Acesso operacional | Pipeline técnico recorrente, extração/ingestão ponta a ponta, sem intervenção manual. | — |
| N5 | Acesso documentado | Acordo de dados assinado, base legal identificada, qualidade declarada. | — |

**Regra de leitura (instrumento de condução, não taxonomia decorativa)**: N1/N2 sustentam apenas **cronograma de investigação**; só N4/N5 sustentam **compromisso firme de prazo** (milestone + critério de pronto do B2). Fonte em N2 entra no cronograma como incerteza declarada, com milestone de verificação e plano B. **O que a escala proíbe é o meio-termo silencioso**: fonte presumida tratada como disponível, sem que ninguém decidiu correr esse risco.

A escala vale para **toda fonte**, não só a da parceira: dataset público chega rápido a N3 (amostra a um download), mas o N5 dele é a leitura da licença (uso comercial, redistribuição, derivação — chave do fornecedor de dados do B3); dado licenciado de terceiro acrescenta contrato, custo e restrição de uso secundário. Somar fontes sem registrar as restrições de cada uma cria um conjunto cuja licença efetiva é a mais restritiva de todas, descoberta tarde.

### Acordo de dados (instrumento central da relação com a parceira)
Registro operacional negociado com a empresa parceira, quatro campos: **esquema** (quais campos, formato, dicionário), **responsável nomeado** (entrega sem nome é entrega de ninguém), **cadência** (quando e com que frequência, em lotes definidos) e **qualidade declarada** (completude esperada, período coberto, critérios de coleta, lacunas conhecidas). Não substitui o contrato jurídico; é o instrumento operacional que o contrato referencia.

**Qualidade declarada ≠ qualidade efetiva.** Por isso, a cada lote entregue roda a **verificação de entrada** (framework de data quality do M3: completude, consistência, validade, atualidade). Lote conforme → entra no catálogo; lote divergente → registro com evidência (declarado/chegado/diferença medida) e vai ao **gate** como risco materializado (opções: renegociar acordo, ajustar cronograma, revisar escopo) — nunca absorvido em silêncio.

Fluxo: Negociação → Acordo de dados → Entregas em cadência → Verificação de entrada → {Conforme (catálogo) | Divergência (registro + gate, pode renegociar o acordo)}.

**Carga histórica x fluxo contínuo**: entregas diferentes, riscos diferentes. Histórico: risco de heterogeneidade escondida (trocas de sistema/sensor/processo não documentadas); verificação procura quebras internas entre períodos. Fluxo: risco de degradação silenciosa (atraso, campo que some, formato que muda); verificação compara cada lote com os anteriores e a declaração.

### Dimensionamento de custo — anotação humana
Componente de custo mais subestimado. Estimativa por **piloto** (anotar dezenas de itens, medir tempo/item, registrar dúvidas, extrapolar com margem) — nunca por intuição. Exemplo: 40s/imagem × 10.000 imagens = mais de 110h de trabalho contínuo (sem revisão).

Três estratégias de anotação (combináveis, escolha registrada com justificativa):
- **Interna** (squad/parceira) — preserva domínio e confidencialidade, consome tempo escasso.
- **Terceirizada** — escala melhor, exige contrato (confidencialidade, PI sobre rótulos, qualidade com métrica — taxonomia de fornecedores do B3).
- **Assistida por modelo** — reduz custo/item, introduz viés do modelo na rotulagem (revisão precisa ser desenhada para **discordar**, não para confirmar).

Organização: **anotação em lotes**, com **5–15%** dos itens de cada lote anotados por mais de uma pessoa, medindo **concordância entre anotadores** (percentual simples ou kappa). Índices baixos raramente indicam baixo desempenho do anotador — em geral apontam **guia de anotação ambíguo**. Rito: fechar lote → ler concordância → revisar guia com casos limítrofes → liberar lote seguinte. Guia de anotação é artefato vivo (versão datada).

### Qualificação é contínua, não uma fase que termina
A cada lote, a verificação de entrada roda de novo; a cada rodada de modelagem, o error analysis por *slices* (M3) direciona a próxima aquisição/anotação. Essa realimentação é a forma que a cadência de iteração do B2 assume no eixo de dados.

### Perfilamento (barato, antes de comprometer cronograma)
Sobre amostra da fonte: nulos por coluna, cardinalidade, faixas/unidades, distribuição de datas, duplicatas, taxa de preenchimento dos campos que a solução vai consumir. **Não julga o dado, apenas o descreve** — compara-se com a qualidade declarada. **"Prontidão declarada sem perfilamento é promessa."**

### Artefato: Plano de Aquisição de Dados (CDP-025)
Por fonte: nível de prontidão + evidência, atividades até o nível necessário (milestones/critérios de pronto articulados ao cronograma do B2), esforço/custo estimado (anotação decomposta do piloto), dependência com a parceira + mitigação (Matriz de Risco do B2). Lê o Canvas do B3 (dados a adquirir = os que a arquitetura declarou consumir) e a Ficha de Escopo do B2 (lastro de dados).

## 2. Governança operacional de dados (CP.B4.C1)

Premissa econômica: sem registro, conhecimento vira **conhecimento tribal** (mora na cabeça de uma pessoa, sai do projeto com ela). "O projeto que não sabe dizer com que dados treinou o modelo que está no ar não tem um problema técnico, tem um **problema de defesa**."

Calibração de escala: governança de projeto de PD&I cabe, na maioria dos casos, numa **planilha bem mantida** + repositório com convenções — não exige plataforma corporativa. Quatro perguntas que precisam ter resposta sempre:
1. Que conjuntos de dados o projeto tem e quem responde por eles?
2. Com que dados, exatamente, cada modelo foi treinado?
3. Como cada conjunto foi produzido a partir do bruto?
4. A última entrega da parceira correspondeu ao acordo?

### Componente 1 — Catálogo de dados
Uma linha por conjunto: nome, origem (fonte do plano de aquisição), esquema resumido, volume/período, **sensibilidade** (dado pessoal? base legal?), versão corrente, e dois papéis:
- **Dono**: quem decide sobre o conjunto (autoriza acesso/uso/mudança) — na residência, costuma ser a empresa parceira.
- **Curador**: quem cuida no dia a dia (documentação, verificação de entrada, transformações) — papel do squad, **com nome**, não cargo genérico.

Duas disciplinas: nenhum conjunto entra sem passar pelo catálogo; o catálogo é lido **nos gates** junto do cronograma e da matriz de risco.

### Componente 2 — Versionamento de dataset
Responde "com que dados, exatamente, este modelo foi treinado?". Cada estado relevante vira **snapshot imutável**, identificador próprio + nota do que mudou. Regra sem exceção: todo experimento e todo modelo que avance a validação/produção registra a versão do dataset que o gerou. Ferramentas de referência (detalhe na Fase 2): **DVC**, **lakeFS**.

Duas convenções: (1) mudança de conteúdo sempre corta versão nova (chegada de lote, correção, novo guia de anotação); reprocessamento sem efeito semântico não corta; (2) **congelamento** — ao entrar em validação para um gate, a versão congela; evolução segue em versão nova. "Validar um modelo contra dados que continuam mudando é validar uma fotografia contra um rio."

### Componente 3 — Rastreabilidade de transformações (linhagem)
Cadeia de scripts versionados do bruto ao treino (cada limpeza/filtro/junção/recorte, com entrada/saída por versão de dataset). **Proibido**: limpeza manual numa planilha que ninguém reproduz. Para fechar de verdade: parâmetros/sementes aleatórias registrados + ambiente fixado por arquivo de dependências. **Teste prático**: outra pessoa do squad, seguindo só o que está registrado, reproduz o conjunto de treino a partir do bruto — se não, é narrativa, não linhagem.

| Componente | O que registra | Pergunta que responde | Interface com o B5 |
|---|---|---|---|
| Catálogo com dono e curador | Conjuntos, origem, esquema, sensibilidade, base legal, responsáveis. | Que dados o projeto tem e quem responde? | Runbook de operação aponta para o catálogo em incidentes. |
| Versionamento de dataset | Snapshots imutáveis + nota de mudança. | Com que dados este modelo foi treinado? | Cada experimento/modelo em produção referencia a versão. |
| Rastreabilidade de transformações | Cadeia de scripts versionados. | Como foi produzido, o que rodar de novo se a fonte mudar? | Pipeline de dados entra no regime de versionamento/monitoramento do modelo. |
| Verificação de entrada | Resultado da checagem de cada lote vs. acordo. | A entrega correspondeu ao acordado? | Monitoramento de drift estende a verificação para a operação contínua. |

### Controle de acesso (3 regras mínimas)
1. Cada conjunto tem lista restrita de autorizados, definida pelo dono (dado pessoal/NDA → acesso limitado por padrão).
2. Dados moram no **ambiente do projeto**, não em máquinas pessoais (cópia local avulsa = risco clássico de vazamento/divergência).
3. Saída de dados do ambiente é **evento registrado** (o quê, para onde, autorizado por quem).

### Dados sensíveis
Dado pessoal aparece onde não se espera (matrícula em log, rosto em vídeo de linha, escala de turno, coordenadas+horário combinados). Verificação **conjunto a conjunto**, na entrada do catálogo.

- **Anonimização**: remove possibilidade razoável de reidentificação — feita de verdade, retira o dado do regime de dado pessoal.
- **Pseudonimização**: substitui identificadores por códigos, tabela de correspondência em separado (conjunto próprio, dono, acesso restrito) — reduz risco, mas o dado **continua sendo dado pessoal perante LGPD/GDPR**.
- **Dado sintético**: regra sem exceção — validação final sempre contra dados **reais** ("sintético treina, sintético aumenta, sintético não atesta"); entra no catálogo como conjunto derivado, com método de geração documentado, versão do real que o originou e dono definido.

## 3. Regulatório e propriedade intelectual de dados (CP.B4.C2)

Premissa de condução: regulatório **não é checagem final de véspera** — é restrição de projeto identificada cedo. O papel do squad não é substituir o advogado; é saber **que regime incide**, que obrigações gera, e levar as perguntas certas a quem redige contratos.

### LGPD (regime da casa)
- **Dado pessoal**: informação relacionada a pessoa identificada/identificável.
- **Tratamento**: praticamente qualquer verbo aplicado ao dado (coletar, armazenar, transformar, treinar um modelo).
- **Base legal**: fundamento que autoriza o tratamento. Em PD&I industrial, consentimento raramente é via realista (frágil, revogável); mais comuns: **execução de contrato** e **legítimo interesse** (exige teste de balanceamento documentado).
- **Papéis**: empresa parceira = **controladora** (determina finalidades); instituição que trata em nome dela = **operadora** (salvo controladoria conjunta).
- Obrigações operacionais: base legal registrada por conjunto no catálogo; **minimização** (coletar o necessário, não o disponível); prazo de retenção definido; capacidade de responder a direitos do titular (acesso, eliminação). Cada obrigação tem um **gate** de verificação — "obrigação sem gate é obrigação que se cumpre por sorte".

### GDPR (quando há componente europeu)
Portas de entrada largas: titulares na UE, planta/controladora europeia da parceira, cliente europeu do sistema. Mesma espinha da LGPD (que nele se inspirou). Diferenças que importam:
- **Transferência internacional** regulada com rigidez (Capítulo V): exige Cláusulas Contratuais Padrão (SCCs), Normas Corporativas Globais (BCRs) ou decisão de adequação da Comissão Europeia.
- **DPIA** (avaliação de impacto) obrigatória quando o tratamento é de alto risco (treinar modelos com dados de trabalhadores pode se qualificar).
- Régua de sanções de outra ordem de grandeza.

Regra prática: havendo componente europeu, **GDPR é regime principal**, LGPD verificada em paralelo — convivem, não se substituem.

### EU AI Act (lógica diferente — regula o sistema pelo risco, não o dado pela natureza)
Classifica sistemas em faixas (de práticas proibidas a risco mínimo), concentrando obrigações na faixa de **alto risco** (segurança de máquinas, infraestrutura crítica, decisões sobre trabalhadores). **Artigo 10**: exige governança de dados de treinamento documentada — práticas de gestão declaradas, exame de representatividade/relevância/vieses, qualidade adequada à finalidade. Vigência escalonada, obrigações de alto risco entram ao longo de **2026**. Consequência direta: catálogo, versionamento, linhagem e verificação de entrada (tópico 2) deixam de ser boa prática e viram **evidência de conformidade**. No Brasil, o **PL 2338/2023** segue lógica semelhante (em tramitação — acompanhar, não tratar como lei vigente).

### Triagem regulatória (3 perguntas, revistas a cada gate)
1. Há dado pessoal em algum conjunto? → LGPD incide (conjunto a conjunto, nunca por suposição de domínio).
2. Há componente europeu (titulares, operação da parceira, mercado do sistema)? → GDPR como regime principal.
3. O sistema mira aplicação de alto risco em mercado europeu? → Art. 10 do EU AI Act vira obrigação documentada.

**Armadilha comum**: "nossos dados são industriais, não temos dado pessoal" — dados de operação carregam pessoas (matrícula, rosto, escala de turno). Verificação é conjunto a conjunto na entrada do catálogo, nunca suposição sobre o domínio.

### Cláusulas contratuais sobre dados
- **Finalidade** + vedação de uso secundário (impede que dado cedido para um fim alimente outro, inclusive treinar modelo fora do escopo).
- **Confidencialidade** se estende a quem mais toca os dados (NDA precisa alcançar anotadores terceirizados).
- **Devolução/descarte** ao final, com prazo e forma — tensiona com a reprodutibilidade do B5 (resolve-se por escrito: o que pode ser retido, por quanto tempo, sob que guarda).
- **Publicação** — ver abaixo.

### Propriedade intelectual de dados (4 categorias)
| Categoria | O que é | Pergunta de propriedade | O que precisa estar escrito |
|---|---|---|---|
| **Dados brutos** | O que a parceira entrega, coletado de seus processos. | De quem é a matéria-prima? | Finalidade de uso, vedação de uso secundário, devolução/descarte com prazo. |
| **Dados anotados** | Rótulos do squad/terceiros sobre os brutos. | De quem é o trabalho de anotação? | Titularidade dos rótulos, licença de uso, PI no contrato de anotação. |
| **Dados sintéticos** | Gerados a partir dos dados da parceira. | Dado novo ou transformação do original? | Se a geração é permitida, de quem é o sintético, que usos admite. |
| **Dados derivados** | Features, embeddings, agregados, estatísticas (podem permitir reconstrução parcial da fonte). | O que carrega informação da fonte x o que é resultado do projeto? | Fronteira entre derivado e resultado; o que pode circular fora do projeto. |

### Publicação acadêmica (tensão legítima, resolvida operacionalmente)
Três peças: (1) **temporal** — condição de publicação se negocia cedo, junto do acordo de dados, nunca na véspera da submissão; (2) **janela de revisão** — parceira recebe o manuscrito com 30–60 dias de antecedência; (3) **distinção de conteúdo** — publica-se método/arquitetura/resultados agregados; não se publicam os dados nem amostras reconstituíveis; métricas que exponham o processo produtivo passam por agregação combinada. Mesma lógica vale para **patente** (titularidade segue contrato; janela de revisão também evita que a publicação destrua a novidade antes do depósito).

### Artefato: Mapa de Governança e Regulatório (CDP-026)
Regime aplicável (com evidência), base legal por conjunto com dado pessoal, obrigações operacionais (responsável + gate), estado dos componentes de governança (tópico 2), PI de dados nas 4 categorias, condições de publicação. Lê o Plano de Aquisição (tópico 1) e o Mapa de Fornecedores e PI do B3; alimenta o **Datasheet do Dataset** e o **Model Card** do B6.

## Correspondência com o kit de laboratório (Projeto Aroeira)
O caso Aroeira já exercita vários destes conceitos mesmo sem instrumento formal ainda na pasta: a distinção **qualidade declarada x qualidade efetiva** (o indicador do painel vs. o cálculo correto), a **prontidão de fonte** (D1–D4 já chegam em N3/N4, com dicionário em `dossie-camada-0.md`), e `id_tecnico` como dado potencialmente sensível (nunca para ranquear — ver Matriz de Validação do E3). Quando a residência avançar, o **mapa de governança e propriedade intelectual** do kit (seção do Encontro 3) é o equivalente operacional do Mapa de Governança e Regulatório (CDP-026) e do Plano de Aquisição de Dados (CDP-025) deste bloco.

## Bibliografia mínima
- SAMBASIVAN, N. et al. *Everyone Wants to Do the Model Work, Not the Data Work: Data Cascades in High-Stakes AI*. CHI, 2021.
- GEBRU, T. et al. *Datasheets for Datasets*. CACM, 2021 (arXiv:1803.09010) — base do Datasheet do B6.
- BRASIL. Lei nº 13.709/2018 (LGPD).
- UNIÃO EUROPEIA. Regulamento (UE) 2024/1689 (EU AI Act), art. 10.
