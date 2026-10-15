# Fundamentos de IA Aplicada

Repositório pessoal de estudo de dois cursos complementares — **Fundamentos de IA Aplicada** (três módulos teóricos, M0/M1/M2) e **Condução de Projetos** (cinco unidades de gestão de PD&I industrial, B2–B6) — e um projeto prático em squad (caso **Aroeira**), estruturado em 3 encontros presenciais, que aplica o conteúdo dos dois cursos.

## Estrutura

```
.
├── INTRODUÇÃO A IA/        # M0 — Introdução a IA
├── IA GENERATIVA/          # M1 — IA Generativa
├── IA Agentic/             # M2 — IA Agentic
├── COnducao de projetos/   # Curso Condução de Projetos (B2–B6)
├── Projeto/                # Caso prático Aroeira (Encontros 1, 2 e 3)
└── .claude/skills/         # Bases de conhecimento usadas pelo Claude Code neste repo
```

### M0 — Introdução a IA (`INTRODUÇÃO A IA/`)
Slides das aulas 1 a 5 (PDF). Conceitos-base: paradigma x tarefa, discriminativo x generativo, lentes transversais do curso.

### M1 — IA Generativa (`IA GENERATIVA/`)
Aulas 1–3 (PDF), guia e exemplo em Colab, notebook `IA_010.ipynb`, anotações (`anotações.md`) e os templates entregues: Matriz de Decisão GenAI x ML clássico e Matriz de Riscos.

### M2 — IA Agentic (`IA Agentic/`)
Aulas 1–3 (PDF), glossário, notebook `IA_018.ipynb`, anotações (`anotações.md`) e os templates: Matriz de Decisão (workflow x agente) e Matriz de Modo de Falha.

### Condução de Projetos (`COnducao de projetos/`)
Curso complementar sobre gestão de projetos de PD&I industrial em IA (programa Industr.IA — Residência em TIC 49), em 5 unidades (cada uma com e-book, glossário e templates oficiais CDP-0xx):

- **Escopo e Fundamentos de Gestão de Projetos** (`ESCOPO E FUNDAMENTOS DE GESTAO DE PROJETOS/`) — tradução de problema de negócio em problema técnico, Ficha de Escopo, Matriz de Stakeholders, Cronograma com Gates, Matriz de Risco.
- **Decisão de Solução e Arquitetura** (`Decisão de soluçâo e arquitetura/`) — hipótese técnica, Matriz de Alternativas, decisão build/buy/integrate, Canvas de Arquitetura Conceitual pelas 5 lentes do curso base, Mapa de Fornecedores e PI.
- **Dados em PD&I Industrial** (`Dados em PDI INdustrial/`) — prontidão de fonte, Acordo de Dados, catálogo/versionamento/linhagem, Plano de Aquisição de Dados, Mapa de Governança e Regulatório (LGPD/GDPR/EU AI Act).
- **Operação, MLOps e Ciclo de Vida** (`Operacao MLOps e ciclo de vida/`) — ciclo de vida do modelo, MLOps essencial, débito técnico de ML, Runbook, Checklist de Prontidão, Plano de Validação e Matriz de Avaliação Contínua.
- **Transparência, Comunicação e Defesa** (`Transparencia comunicacao e defesa/`) — comunicação por audiência, defesa de decisão (6 elementos), Model Card, Datasheet do Dataset, contestabilidade.

### Projeto Aroeira (`Projeto/`)
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

### `.claude/skills/`
Skills do Claude Code que encapsulam o conhecimento dos cursos e do projeto para uso assistido:
- `fundamentos-ia-aplicada`: base conceitual dos módulos M0/M1/M2, usada para responder, revisar ou propor desafios e preencher os templates oficiais.
- `conducao-de-projetos`: base conceitual das unidades B2–B6 do curso Condução de Projetos, usada para preencher/revisar os templates CDP-0xx e para aprofundar com teoria formal as decisões do Projeto Aroeira.
- `projeto-aroeira`: dossiê do caso Aroeira (camadas 0–2), resumo dos 3 encontros e entregáveis do Squad 5, usada para apoiar o preenchimento dos instrumentos (KIT-0xx) e a preparação de cada encontro — referencia `conducao-de-projetos` para a base teórica de cada instrumento.

## Status

- ✅ Encontro 1 — concluído (instrumentos produzidos e entregues).
- ✅ Encontro 2 — concluído (decisão e arquitetura entregues).
- 🔜 Encontro 3 — agendado para 15/10/2026 (teste, validação, proposta final e pitch).
