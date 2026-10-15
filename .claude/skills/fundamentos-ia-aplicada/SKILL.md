---
name: fundamentos-ia-aplicada
description: Base de conhecimento do curso "Fundamentos de IA Aplicada" (módulos M0 Introdução a IA, M1 IA Generativa, M2 IA Agentic, M3 Data-centric AI), extraída fielmente dos e-books, glossários, templates e notebooks do curso. Use esta skill sempre que o usuário pedir para propor, responder, corrigir ou avaliar um desafio/exercício/quiz relacionado a este curso, pedir para preencher um dos templates oficiais (matriz de decisão workflow x agente, matriz de modos de falha, matriz GenAI x ML clássico, matriz de riscos, checklist, matriz de decisão dados x modelo T3.1), pedir para explicar/revisar um conceito do curso (paradigma x tarefa, lentes transversais, discriminativo x generativo, RAG, fine-tuning, prompting estruturado, arquitetura de agentes, ReAct, MCP, branching dinâmico, data-centric, framework de data quality em seis dimensões, error analysis por slices, taxonomia de vieses, árvore dados x modelo, dados sintéticos e auto-reforço, LGPD/GDPR/EU AI Act aplicados ao dataset etc.), ou mencionar qualquer um dos quatro módulos por nome. Também use para gerar NOVOS desafios/questões de prova a partir do conteúdo das aulas, já que este é o propósito declarado da pasta. Não é sobre criar agentes de IA em código real — é a base terminológica e conceitual do curso em si.
---

# Fundamentos de IA Aplicada — base de conhecimento do curso

Este repositório guarda o material de um curso de IA aplicada em quatro módulos (M0–M3). Esta skill condensa o conteúdo de todos os PDFs, notebooks e anotações de cada módulo em documentos de referência fiéis ao material original, para servir de **fonte de verdade** ao propor ou corrigir desafios sobre o curso.

## Quando usar cada referência

Carregue apenas o(s) arquivo(s) de `references/` relevante(s) para a pergunta — cada um é extenso (propositalmente denso, para preservar definições exatas), então não é necessário ler os três de uma vez.

| Módulo | Arquivo | Conteúdo |
|---|---|---|
| **M0 — Introdução a IA** | `references/introducao-ia.md` | Vocabulário fundacional de ML (treino/inferência, overfitting, métricas), arco histórico das famílias técnicas (ML clássico → Deep Learning → Foundation Models → Sistemas Agênticos), taxonomia paradigma×tarefa, as cinco lentes transversais × sete eixos técnicos, glossário M0 |
| **M1 — IA Generativa** | `references/ia-generativa.md` | Discriminativo x generativo, famílias arquiteturais (decoder-only, encoder-decoder, difusão, multimodal), Foundation Models e capacidade emergente, os três padrões aplicados (prompting estruturado, RAG, fine-tuning leve) e como reconhecê-los numa especificação, camada decisória (GenAI x ML clássico, modelo aberto x API gerenciada, in-context x fine-tuning, RAG x contexto fechado), templates T1.1/T1.2/T1.3 |
| **M2 — IA Agentic** | `references/ia-agentic.md` | Arquitetura canônica de agente (reasoning engine, tools, memória, planning), agente x assistente, paradigmas (ReAct, Plan-and-Execute, Reflexão, Multi-agente), MCP, workflow determinista x agente single-loop, heurística do branching dinâmico, quatro modos de falha, templates T2.1/T2.2, trace do notebook IA_018 |
| **M3 — Data-centric AI** | `references/data-centric.md` | Deslocamento data-centric (modelo fixo, dados como teto), vocabulário regulatório (LGPD, GDPR Art. 22, EU AI Act Art. 10, base legal, lineage), framework de data quality em seis dimensões, error analysis por slices em cinco passos, taxonomia de vieses por ponto do pipeline, árvore de decisão dados x modelo, dados reais x sintéticos (auto-reforço, validação só em dado real), regime regulatório do dataset e risco residual, template T3.1, notebook IA_025 (Adult Income, acurácia enganosa por proporção de positivos) |

Cada arquivo de referência traz, nessa ordem: conteúdo aula a aula (tema, conceitos, frameworks, exemplos industriais, armadilhas, tabelas/matrizes reproduzidas na íntegra), um resumo executivo da progressão do módulo, um glossário consolidado "termo: definição", e uma lista de **tipos de desafio prováveis** que o próprio conteúdo sugere.

## Como usar esta skill

**Para avaliar/corrigir uma resposta de aluno**: localize a definição ou o eixo de decisão exato no arquivo de referência do módulo em questão e compare literalmente — os documentos preservam a redação original das caixas de glossário e armadilhas do material, que é o padrão de correção mais confiável (mais preciso que paráfrase).

**Para propor um novo desafio**: use a seção "Tipos de desafio" do módulo relevante como ponto de partida, e baseie o enunciado em um dos exemplos industriais/PD&I já catalogados (ou um variante próximo), garantindo que o desafio tenha uma resposta rastreável a uma definição ou heurística específica do material.

**Para preencher um template** (T1.1 Matriz GenAI x ML, T1.2 Matriz de Riscos, T1.3 Checklist, T2.1 Matriz de Decisão Workflow x Agente, T2.2 Matriz de Modos de Falha, T3.1 Matriz de Decisão Dados x Modelo): a estrutura completa de campos/colunas/eixos de cada template, incluindo o exemplo oficial preenchido, está reproduzida na seção de templates do arquivo de referência correspondente (M1 para T1.x, M2 para T2.x, M3 para T3.1).

**Atenção a uma discrepância já identificada**: as anotações pessoais do aluno em `IA Agentic/anotações.md` têm um erro de cópia — o parágrafo rotulado "plan-and-execute" reproduz na verdade a definição de "reflexão". O arquivo `references/ia-agentic.md` (seção 7) já sinaliza isso; não usar as anotações como fonte de verdade nesse ponto específico, usar o e-book/glossário.

## Terminologia transversal ao curso (vale para todos os módulos)

- **Lente vs. eixo técnico** (M0): uma lente é um ângulo de leitura (pergunta recorrente) que atravessa qualquer um dos 7 eixos técnicos do programa; não classifica, não é exclusiva, não é uma tecnologia. M1 (Generativa), M2 (Agentic) e M3 (Data-centric, "lente dos dados") são, cada um, uma dessas cinco lentes aprofundada em módulo próprio.
- **Heurística do "default mais simples, autonomia/sofisticação por exceção"** se repete em todos os módulos sob formas distintas: M0 adverte contra escolher a família mais recente só por ser recente; M1 ordena prompting → RAG → fine-tuning por custo crescente, nunca ao contrário; M2 trata workflow como default e agente como exceção condicionada a branching dinâmico irrelutável + valor real da autonomia; M3 examina a hipótese de dados antes da troca de modelo e trata dado sintético como exceção justificada. Um desafio bem desenhado costuma testar exatamente esse padrão de raciocínio aplicado ao módulo específico.
- **Avaliação como entregável, não detalhe final**: recorrente em M1 (avaliação de saída generativa é difícil, "múltipla") M2 (trace/observabilidade como condição de auditoria) e M3 (métrica por slice, nunca só a global; validação sempre em dado real) — tratar como princípio do curso, não só de um módulo.
