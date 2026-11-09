# Fundamentos de IA Aplicada

Repositório pessoal de estudo de dois cursos complementares — **Fundamentos de IA Aplicada** (módulos teóricos M0 a M5) e **Condução de Projetos** (cinco unidades de gestão de PD&I industrial, B2–B6) — e da prática em squad (Squad 05 UFC), em duas etapas:

- **Etapa 1** — projeto **Aroeira**, um caso único em 3 encontros presenciais (concluída).
- **Etapa 2** — **desafios de reforço** curtos (2 semanas e 2 encontros cada), no repositório oficial da squad [`irede-industr-ia/squad-05-ufc`](https://github.com/irede-industr-ia/squad-05-ufc) (em andamento).

## Estrutura

```
.
├── INTRODUÇÃO A IA/                 # M0 — Introdução a IA
├── IA GENERATIVA/                   # M1 — IA Generativa
├── IA Agentic/                      # M2 — IA Agentic
├── Data Centric IA/                 # M3 — Data-centric AI
├── Edge_AI/                         # M4 — Edge AI (base do Desafio 1 da Etapa 2)
├── Explainable_IA/                  # M5 — Explicabilidade (XAI)
├── COnducao de projetos/            # Curso Condução de Projetos (B2–B6)
├── Etapa 1 - Projeto Aroeira/       # Caso prático Aroeira (Encontros 1, 2 e 3) + templates KIT
├── Etapa 2 - Desafios de Reforco/   # Desafios M4, M2, M3 + submódulo squad-05-ufc
└── .claude/skills/                  # Bases de conhecimento usadas pelo Claude Code neste repo
```

> Depois de clonar: `git submodule update --init` para baixar `Etapa 2 - Desafios de Reforco/squad-05-ufc`.

### M0 — Introdução a IA (`INTRODUÇÃO A IA/`)
Slides das aulas 1 a 5 (PDF). Conceitos-base: paradigma x tarefa, discriminativo x generativo, lentes transversais do curso.

### M1 — IA Generativa (`IA GENERATIVA/`)
Aulas 1–3 (PDF), guia e exemplo em Colab, notebook `IA_010.ipynb`, anotações (`anotações.md`) e os templates entregues: Matriz de Decisão GenAI x ML clássico e Matriz de Riscos.

### M2 — IA Agentic (`IA Agentic/`)
Aulas 1–3 (PDF), glossário, notebook `IA_018.ipynb`, anotações (`anotações.md`) e os templates: Matriz de Decisão (workflow x agente) e Matriz de Modo de Falha.

### M3 — Data-centric AI (`Data Centric IA/`)
Aulas 1 e 3 (e-books), Aula 2 (guia do notebook), glossário, notebook `IA_025.ipynb` (error analysis por slices no Adult Income) e o template T3.1 Matriz de Decisão Dados x Modelo. Conceitos: dados como teto de qualidade, seis dimensões de data quality, error analysis por slices, taxonomia de vieses, árvore dados x modelo, dados sintéticos e regime regulatório do dataset (LGPD, GDPR, EU AI Act).

### M4 — Edge AI (`Edge_AI/`)
Aula 1 (continuum cloud-edge, hardware e runtimes, técnicas de compressão, exemplo industrial), Aula 2 (decisão de deployment como compromisso de produto: posicionamento no continuum, compressão e runtime, custo total/TCO), glossário, guia do notebook de quantização feita à mão (MLP no *digits*) e o template Matriz de Decisão Edge x Cloud. Conceitos: os três gatilhos de edge (latência como compromisso de produto, privacidade regulatória, conectividade não assumível), quantização (PTQ/QAT, int8/int4), poda, destilação, ONNX Runtime, TCO.

### M5 — Explicabilidade (`Explainable_IA/`)
Aula 1 (dimensão regulatória da explicação, taxonomia de técnicas, SHAP na prática, limites para LLMs), Aula 2 (regime de exigência, técnica certa por stakeholder, profundidade de entrega), glossário, guia do notebook SHAP (XGBoost no German Credit) e o template Matriz de Decisão XAI por stakeholder.

### Condução de Projetos (`COnducao de projetos/`)
Curso complementar sobre gestão de projetos de PD&I industrial em IA (programa Industr.IA — Residência em TIC 49), em 5 unidades (cada uma com e-book, glossário e templates oficiais CDP-0xx):

- **Escopo e Fundamentos de Gestão de Projetos** (`ESCOPO E FUNDAMENTOS DE GESTAO DE PROJETOS/`) — tradução de problema de negócio em problema técnico, Ficha de Escopo, Matriz de Stakeholders, Cronograma com Gates, Matriz de Risco.
- **Decisão de Solução e Arquitetura** (`Decisão de soluçâo e arquitetura/`) — hipótese técnica, Matriz de Alternativas, decisão build/buy/integrate, Canvas de Arquitetura Conceitual pelas 5 lentes do curso base, Mapa de Fornecedores e PI.
- **Dados em PD&I Industrial** (`Dados em PDI INdustrial/`) — prontidão de fonte, Acordo de Dados, catálogo/versionamento/linhagem, Plano de Aquisição de Dados, Mapa de Governança e Regulatório (LGPD/GDPR/EU AI Act).
- **Operação, MLOps e Ciclo de Vida** (`Operacao MLOps e ciclo de vida/`) — ciclo de vida do modelo, MLOps essencial, débito técnico de ML, Runbook, Checklist de Prontidão, Plano de Validação e Matriz de Avaliação Contínua.
- **Transparência, Comunicação e Defesa** (`Transparencia comunicacao e defesa/`) — comunicação por audiência, defesa de decisão (6 elementos), Model Card, Datasheet do Dataset, contestabilidade.

### Etapa 1 — Projeto Aroeira (`Etapa 1 - Projeto Aroeira/`)
Na raiz da pasta ficam também os templates KIT em branco (KIT-001, 003, 020) e os guias (KIT-022, KIT-048), reaproveitados na Etapa 2.

Laboratório de decisão técnica aplicado a um caso fictício industrial (Aroeira Equipamentos Industriais), trabalhado pelo **Squad 5 (UFC)** ao longo de 3 encontros presenciais:

- **Encontro 1** — compreender, delimitar e formular hipótese.
  - `Dados/`: CSVs d1_frota, d2_telemetria, d3_ordens, d4_garantia.
  - `Instrumentos/`: Acordo de Squad, Mapa Técnico do Problema, Hipótese Técnica.
  - `analise/`: código Python de apoio (independente do notebook) para testar as justificativas do pedido original com dado real.
  - `notebook_analise_exploratoria.ipynb`: análise exploratória em notebook.
  - `RESUMO_DESAFIO_1.md`: leitura narrativa dos achados da análise.
  - `entregaveis1/`: instrumentos entregues em PDF.
- **Encontro 2** — comparar alternativas, decidir e desenhar a arquitetura, à luz de uma nova camada de informação (camada 2).
  - `Preparacao/`: mapa técnico e hipótese revisados, matriz de alternativas, decisão justificada e canvas de arquitetura (esboços de preparo).
  - `Artefatos/` e `Documentos/`: entregáveis finais do squad em PDF.
- **Encontro 3** (15/10/2026) — testar a hipótese de telemetria com dado, validar a decisão à luz de uma nova camada (camada 3: questão jurídica e fornecedor), e defender a proposta técnica final em pitch.
  - `Preparacao/00_PASSO_A_PASSO.md`: roteiro completo do encontro.
  - `Documentos/`: apresentação do encontro.

Decisão vigente ao fim do Encontro 2: um **assistente conversacional somente leitura** (histórico de atendimentos com causa corrigida + manual) para o piloto de 90 dias, com o **alerta de telemetria rodando em modo sombra** — abertura de OS e pedido de peça ficam para uma fase posterior. É um workflow, não um agente.

### Etapa 2 — Desafios de reforço (`Etapa 2 - Desafios de Reforco/`)
Três desafios curtos, cada um em duas semanas com dois encontros (E1: delimitar, decidir e fixar o critério de aceite no KIT-003; E2: testar no notebook e defender, com apresentador sorteado). O material oficial vem do repositório da squad, incluído como **submódulo** em `squad-05-ufc/` (somente leitura: a entrega é gravada pela célula de envio do notebook no Colab, pela pessoa entregadora).

- **Desafio 1 · M4 Quantização e borda** (`Desafio 1 - M4 Quantizacao e borda/`): quantizar o BERTimbau (ONNX int8) ou trocar por TF-IDF + regressão logística, para classificar relatos de campo num coletor sem GPU (8 GB, < 1 s, offline), contra a proposta da TI de comprar coletores com GPU.
  - `Documentos/`: situação e roteiro de estudos (PDF).
  - `Preparacao/00_PASSO_A_PASSO.md`: roteiro das duas semanas, com rascunhos de critério de aceite e da Matriz de Alternativas.
  - `Preparacao/01_leitura_dos_dados.md`: leitura descritiva de `relatos_de_campo.csv` (inclui o achado dos relatos com dois problemas e rótulo inconsistente).
  - `Artefatos/`: KITs entregues.
- **Desafio 2 · M2 Agente ou fluxo fixo** e **Desafio 3 · M3 Erro por recortes**: só a pasta com o resumo, por enquanto.

### `.claude/skills/`
Skills do Claude Code que encapsulam o conhecimento dos cursos e do projeto para uso assistido:
- `fundamentos-ia-aplicada`: base conceitual dos módulos M0/M1/M2/M3, usada para responder, revisar ou propor desafios e preencher os templates oficiais.
- `conducao-de-projetos`: base conceitual das unidades B2–B6 do curso Condução de Projetos, usada para preencher/revisar os templates CDP-0xx e para aprofundar com teoria formal as decisões do Projeto Aroeira.
- `projeto-aroeira`: dossiê do caso Aroeira (camadas 0–2), resumo dos 3 encontros e entregáveis do Squad 5, usada para apoiar o preenchimento dos instrumentos (KIT-0xx) e a preparação de cada encontro — referencia `conducao-de-projetos` para a base teórica de cada instrumento.

## Status

**Etapa 1 — Aroeira**
- ✅ Encontro 1 — concluído (instrumentos produzidos e entregues).
- ✅ Encontro 2 — concluído (decisão e arquitetura entregues).
- ✅ Encontro 3 — realizado em 15/10/2026 (teste, validação, proposta final e pitch).

**Etapa 2 — Desafios de reforço**
- 🔜 Desafio 1 · M4 Quantização e borda — semana 1 (preparação para o Encontro 1).
- ⏳ Desafio 2 · M2 Agente ou fluxo fixo.
- ⏳ Desafio 3 · M3 Erro por recortes.
