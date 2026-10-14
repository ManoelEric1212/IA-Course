# Encontro 2 — Comparar, decidir e desenhar

> Fonte: `Projeto/KIT-022_guia_do_aluno.pdf` (seção 4, mais as seções 1.2–1.4, que valem para o arco todo) e os templates em `Projeto/Encontro 2/Documentos/`: `IND-KIT-004-EN2-T2` (Matriz de Alternativas), `IND-KIT-007-EN3-T1` (Decisão Justificada), `IND-KIT-008-EN3-T2` (Canvas de Arquitetura Conceitual). A mesma pasta traz cópias do Mapa (KIT-001) e da Hipótese (KIT-003) **já preenchidos pelo Squad 5 no Encontro 1**, idênticos aos de `Projeto/Encontro 1/entregaveis1/`. São o artefato de entrada do encontro.
>
> Semana 2, 240 min. Pré-requisito: **M1 (IA Generativa) e M2 (IA Agentic) concluídos**. Levar: Mapa Técnico do Problema e Hipótese Técnica na pasta da turma.

## Numeração impressa x numeração deste arco
Os templates foram impressos para um arco de 5 encontros. O que vale é o mapa do KIT-022 §1.2:

| Instrumento | Impresso como | Preenchido neste arco |
|---|---|---|
| Matriz de Alternativas (KIT-004) | Encontro 2 | **Encontro 2** |
| Decisão Justificada (KIT-007) | Encontro 3 | **Encontro 2** |
| Canvas de Arquitetura Conceitual (KIT-008) | Encontro 3 | **Encontro 2** |

**Armadilha**: o KIT-004 diz "sem escolher ainda (a escolha é no Encontro 3)". Neste arco, a escolha é feita **no próprio Encontro 2**, na Decisão Justificada, logo depois da Matriz. A Matriz termina com uma *recomendação* que decorre dos critérios, e a Decisão a fecha.

Também vale em todos os instrumentos: no campo de caso, escrever "caso da Aroeira", e ler "mentor" onde o template diz "tutor".

## O que o squad produz

### 1. Matriz de Alternativas (KIT-004)
Colunas: **Alternativa | Aderência ao problema | Dados necessários | Viabilidade | Riscos | Explicabilidade/TRL**. Seção 2: abordagem recomendada + pontos de incerteza.

Pronta quando:
- [ ] Ao menos **duas** alternativas comparadas em **todas** as dimensões
- [ ] Cada célula com justificativa curta (não basta "alta/baixa"), **com proveniência**
- [ ] Abordagem recomendada registrada com pontos de incerteza. A recomendação decorre dos critérios, não de preferência

Regra extra do arco (KIT-022 §4.4): na justificativa de cada célula, **indicar qual matriz do curso base sustentou o critério**. As matrizes disponíveis (ver skill `fundamentos-ia-aplicada`) são:
- **T1.1** Matriz de decisão GenAI x ML clássico (M1). Eixos: custo, latência, reprodutibilidade, precisão, disponibilidade de dados.
- **T1.2** Matriz de riscos de soluções generativas (M1). Categorias fixas: alucinação, viés, propriedade intelectual, custo, deriva temporal.
- **T1.3** Checklist (M1).
- **T2.1** Matriz de decisão Workflow x Agente (M2). Eixos: branching dinâmico, custo de inferência, transparência/auditoria.
- **T2.2** Matriz de modos de falha (M2). Modos: loop, seleção de tool errada, prompt injection, cascading error.

Mapeamento natural coluna → matriz:

| Coluna KIT-004 | Matriz do curso base |
|---|---|
| Aderência | paradigma × tarefa (M0) + T1.1 (GenAI x ML) |
| Dados necessários | T1.1, eixo disponibilidade de dados |
| Viabilidade | T1.1 (custo, latência) + T2.1 (custo de inferência) |
| Riscos | T1.2 (generativo) / T2.2 (agente) |
| Explicab./TRL | T2.1 (transparência/auditoria) + T1.1 (reprodutibilidade) |

### 2. Decisão Justificada (KIT-007)
Campos: 1. abordagem escolhida, 2. justificativa (critérios que pesaram), 3. premissas assumidas, 4. pontos de incerteza.

Pronta quando:
- [ ] Escolha **vinculada aos critérios da Matriz** (citar as colunas/células)
- [ ] Premissas registradas
- [ ] Pontos de incerteza registrados

**Dois registros obrigatórios a mais no campo de incerteza, só neste arco:**
1. **Qual célula do Encontro 1 caiu** com a informação nova (camada 2) liberada na abertura. Registrado já na fase de abertura.
2. **Uma sugestão de ferramenta de IA recebida e rejeitada, com o motivo técnico** (regra de trabalho nº 4).

### 3. Canvas de Arquitetura Conceitual (KIT-008)
Campos: entrada de dados (fonte, tipo) · pré-processamento/preparação · componentes/modelo(s) · saída esperada · lógica/fluxo (como as partes se conectam) · pontos de risco/falha no fluxo. É **conceitual: representar, não implementar**, e "realiza a decisão tomada".

Pronto quando:
- [ ] Mostra fluxo de dados, componentes, modelo e saída esperada
- [ ] Riscos **localizados no fluxo** (em qual etapa, não lista genérica)
- [ ] Um colega de **outro eixo** entenderia o diagrama **sem explicação oral**

## Sequência (240 min)

| Horário | Min | Fase | O que o squad faz |
|---|---|---|---|
| 00:00–00:25 | 25 | Abertura + **camada 2** | Retoma o problema delimitado **em uma frase**; recebe informação nova; registra **na hora** qual célula do E1 caiu (campo de incerteza da Decisão Justificada). A fase só fecha com esse registro feito. |
| 00:25–00:35 | 10 | Modelagem | Mentor fecha uma decisão em voz alta: escolha, critérios em que supera a alternativa, custo aceito. |
| 00:35–01:05 | 30 | Matriz, 1ª metade | **2 sub-times** em paralelo, sem se consultar: aderência, dados necessários, viabilidade, para ≥2 abordagens, com proveniência. **Janela de perguntas abre.** |
| 01:05–01:35 | 30 | Matriz, 2ª metade | Riscos, explicabilidade/TRL, recomendação + incertezas; cada célula cita a matriz do curso base. **Janela de perguntas fecha no intervalo.** |
| 01:35–01:50 | 15 | Intervalo | — |
| 01:50–02:10 | 20 | Confronto da Matriz + sorteio | Cada sub-time defende a recomendação, o outro questiona os critérios; versão única; critério de pronto; sorteio de defesa. |
| 02:10–02:45 | 35 | Decisão Justificada | Escolha + justificativa vinculada à Matriz + premissas + incertezas. |
| 02:45–02:55 | 10 | Fechamento da Decisão + sorteio | Critério de pronto; sorteio. |
| 02:55–03:35 | 40 | Canvas | Squad inteiro, sem divisão. |
| 03:35–03:45 | 10 | Fechamento do Canvas + sorteio | Critério de pronto; sorteio. |
| 03:45–04:00 | 15 | Fechamento e ponte | Devolutiva em 4 passos sobre Matriz, Decisão e Canvas; ponte para o E3. |

Orçamento de perguntas: **3** (consumido mesmo por pergunta mal formulada; não acumula do E1). Sem resposta → "a empresa vai verificar" → registrar como incerteza.

## Entregue pelo Squad 5
Versão entregue em 08/10/2026 (`Projeto/Encontro 2/Artefatos/`), transcrita e validada em `entregaveis-e2-squad5.md`. Os esboços de preparação ficam em `Projeto/Encontro 2/Preparacao/` e são mais completos que o entregue em vários pontos.

## Ponte para o Encontro 3
A Decisão e o Canvas viram entrada da Matriz de Teste (KIT-011). Lá, o critério de sucesso é fixado **antes** de rodar o notebook no Colab. Por isso, os critérios de teste das hipóteses precisam chegar ao fim do E2 com número, linha de base e horizonte definidos. Pré-requisito do E3: M3 (Data Centric), M4 (Edge) e M5 (Explainable) concluídos.
