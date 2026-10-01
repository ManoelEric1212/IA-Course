# Encontro 1 — Compreender, delimitar e hipotetizar

> Fonte: `Projeto/KIT-022_guia_do_aluno.pdf` (seções 1 a 3) e `Projeto/KIT-048_guia_classroom_colab.pdf`. Semana 1 do arco de 3 encontros (Laboratórios de decisão técnica, Formação 1), 240 minutos presenciais, foco **"compreender, delimitar e hipotetizar"**. É o único encontro sem artefato de entrada (não herda nada de um encontro anterior).

## Contexto do arco (para situar o Encontro 1 no todo)

Três encontros presenciais de 4h, um por semana, mesmo squad e mesmo mentor, sobre um caso único (Aroeira). O instrumento produzido em um encontro é entrada do seguinte.

| Encontro | Semana | Foco | Pré-requisito no curso base (Homero) |
|---|---|---|---|
| **Encontro 1** | 1 | Compreender, delimitar e hipotetizar | M0 concluído |
| Encontro 2 | 2 | Comparar, decidir e desenhar | M1 (IA Generativa) + M2 (IA Agentic) concluídos |
| Encontro 3 | 3 | Testar, validar e defender | M3 (Data Centric) + M4 (Edge) + M5 (Explainable) concluídos |

Regra válida nos 3 encontros (Acordo de squad): **nenhuma tecnologia é escolhida antes de o problema ser compreendido**. No Encontro 1 o squad só delimita o problema e formula hipótese técnica — não escolhe abordagem nem tecnologia ainda (isso é Encontro 2).

Mapa completo dos 11 instrumentos do arco (ordem de produção): Acordo de squad (KIT-020, E1) → Mapa Técnico do Problema (KIT-001, E1) → Hipótese Técnica (KIT-003, E1) → Matriz de Alternativas (KIT-004, E2) → Decisão Justificada (KIT-007, E2) → Canvas de Arquitetura Conceitual (KIT-008, E2) → Matriz de Teste (KIT-011, E3) → Matriz de Validação (KIT-012, E3) → Proposta Técnica Final (KIT-015, E3) → Roteiro de Pitch (KIT-016, E3) → Registro de princípios transferíveis (KIT-021, E3).

## As quatro regras de trabalho (valem nos 3 encontros, anunciadas na abertura do E1)
1. Toda justificativa aponta a proveniência: código do dossiê (`C0-xx`), código de ficha, ou recorte de dados como `conjunto.campo`. **Célula sem proveniência é devolvida.**
2. Ao fechar cada instrumento, o mentor sorteia um integrante para justificar duas células que não foram escritas por ele.
3. O critério de sucesso de um teste é fixado **antes** de rodar o teste (relevante já a partir do Encontro 3, mas a disciplina de "critério antes do resultado" já vale para o critério de pronto de cada instrumento deste encontro).
4. Uso de ferramenta de IA não é proibido; sugestão recebida e rejeitada entra, com motivo técnico, no campo de pontos de incerteza da Decisão Justificada (KIT-007) — relevante a partir do Encontro 2.

## O que preparar antes (checklist individual)
- [ ] Acesso à turma do polo no Google Classroom testado (abrir material + enviar arquivo)
- [ ] Módulo M0 do curso base concluído (Panorama de IA aplicada) — ver skill `fundamentos-ia-aplicada`, `references/introducao-ia.md`
- [ ] Camada 0 do dossiê lida (`references/dossie-camada-0.md` desta skill, itens C0-01 a C0-12)
- [ ] Check-in de leitura prévia (KIT-030) respondido no prazo — gabarito de apoio em `dossie-camada-0.md`
- [ ] Restrições de disponibilidade de cada integrante levantadas (entram no Acordo de squad)

## O que o squad produz no Encontro 1

### 1. Acordo de squad (KIT-020) — registro obrigatório, não pontuado na rubrica
Pronto quando:
- [ ] Papéis atribuídos e rodízio definido para os 3 encontros (o instrumento original fala em 5 encontros — neste arco, preencher só as colunas dos Encontros 1–3 e deixar as 2 últimas em branco)
- [ ] Procedimento de decisão sem consenso escrito (não presumido)
- [ ] Lugar de registro da discordância técnica nomeado
- [ ] Canal e janela de resposta combinados entre encontros
- [ ] Responsável pela pasta do squad nomeado, com o que entra nela e o prazo

No campo de identificação, usar "caso da Aroeira"; onde o instrumento diz "tutor", ler "mentor".

### 2. Mapa Técnico do Problema (KIT-001)
Pronto quando:
- [ ] Problema enunciado como **raiz**, não sintoma
- [ ] Sintomas e causas diferenciados
- [ ] Dados e qualidade registrados
- [ ] Restrições em ao menos 3 dimensões (técnicas, éticas e regulatórias, operacionais)
- [ ] Oportunidades de IA listadas como **candidatas, sem escolha** ainda

Ponto de atenção direto do dossiê: o pedido da diretoria (C0-05, "assistente conversacional com IA") é a solicitação **tal como chegou**, não o problema delimitado — o enunciado do Mapa precisa separar o sintoma relatado (tempo médio de atendimento subindo, técnicos novos sem experiência na série CP, reincidência de chamados) da causa raiz provável, usando os dados disponíveis (D1–D4) como evidência, não suposição.

### 3. Hipótese Técnica (KIT-003)
Pronta quando:
- [ ] Cada hipótese tem **abordagem + condição + critério de teste**
- [ ] A distinção "problema de X e não de Y" está feita com evidência
- [ ] Justificativa registrada

A hipótese diz **sob que condição o efeito aparece**. Neste encontro, nomear a tarefa e o paradigma (vocabulário do módulo M0 — ver skill `fundamentos-ia-aplicada`) e justificar essa classificação com evidência do dossiê/dados.

> Critério de "pronto" nos três instrumentos é a **autoverificação do squad**, feita antes de o instrumento fechar — não é o mentor que avisa, é o squad que confere a própria lista antes de encerrar.

## O que levar
Único encontro sem artefato de entrada herdado. Levar: a camada 0 à mão (os códigos `C0-xx` entram nas justificativas), acesso à turma do Classroom testado, e as restrições de disponibilidade de cada integrante (entram no Acordo de squad).

## Sequência do encontro (240 min)

| Horário | Min | Fase | O que o squad faz |
|---|---|---|---|
| 00:00–00:20 | 20 | Abertura, retomada do arco, Acordo de squad | Recebe o arco das 3 semanas, as 4 regras, o orçamento de perguntas do encontro (4). Preenche o Acordo de squad. |
| 00:20–00:30 | 10 | Modelagem do mentor | Observa o mentor raciocinar em voz alta sobre um mini-exemplo (não é o caso do dia). |
| 00:30–01:00 | 30 | Imersão no caso | Recebe material novo do caso (camada 1, liberada pelo mentor ~30 min após o início). Levanta, sem resolver: o que é pedido, quais atores, qual a dor por trás do pedido, o que já se sabe/falta. **Janela de perguntas abre aqui.** |
| 01:00–01:25 | 25 | Mapa Técnico do Problema — enunciado, sintomas×causas, dados | Em **2 sub-times** (trabalham em paralelo, sem se consultar): escrevem o enunciado em 1–2 frases, separam sintomas observáveis de causas prováveis, registram disponibilidade/qualidade dado a dado. |
| 01:25–01:40 | 15 | Intervalo | — |
| 01:40–02:10 | 30 | Mapa Técnico do Problema — restrições e oportunidades | Mapeia restrições em ≥3 dimensões (técnicas, éticas/regulatórias, operacionais) e lista ≥2 oportunidades de IA candidatas, **sem escolher nenhuma**. **Janela de perguntas fecha aqui** — orçamento não usado não passa para o Encontro 2. |
| 02:10–02:30 | 20 | Confronto, fechamento do Mapa, sorteio | Os 2 sub-times apresentam (até 3 min cada), o outro aponta uma divergência, squad fecha versão única. Confere critério de pronto. Sorteio de defesa. |
| 02:30–03:25 | 55 | Hipótese Técnica | Squad inteiro (sem divisão): escreve abordagem + condição + resultado esperado + critério de teste; nomeia tarefa e paradigma (M0) com evidência. |
| 03:25–03:45 | 20 | Confronto, fechamento da Hipótese, sorteio | Confere critério de pronto. Sorteio de defesa. |
| 03:45–04:00 | 15 | Fechamento e ponte | Devolutiva do mentor em 4 passos (evidência observada, interpretação técnica, próximo passo, prazo/momento de revisão) sobre Mapa e Hipótese; ponte para o Encontro 2. |

### Mecânica de confronto e sorteio
- **Divisão em sub-times**: só no primeiro bloco de produção do Mapa Técnico do Problema (e, em encontros futuros, da Matriz de Alternativas e da Matriz de Teste). Cada sub-time trabalha a mesma célula em paralelo, sem consultar o outro.
- **Apresentação pareada**: no fechamento do Mapa — cada sub-time apresenta em até 3 min, o outro aponta uma divergência, squad funde numa versão única.
- **Hipótese Técnica**: produzida pelo squad inteiro, sem divisão — o "confronto" aqui é só o fechamento contra o critério de pronto + sorteio de defesa.
- **Sorteio de defesa**: ao fechar cada instrumento, o mentor sorteia um integrante para justificar 2 células que não foram escritas por ele (regra de trabalho nº 2) — reforça que todo o squad precisa entender (não só escrever) cada célula.

## Como a informação chega e como é avaliado (vale para o arco todo)
- A camada 0 é lida **antes** do Encontro 1. Informação adicional (camada 1, 2, 3) é liberada **em sala**, pelo mentor, no início de cada encontro — e normalmente invalida parte do que o squad já tinha escrito; registrar essa queda de justificativa é parte do trabalho.
- Avaliação é **formativa**, com rubrica de 8 critérios (compreensão do problema, aderência da abordagem técnica, qualidade da justificativa, análise de dados e restrições, identificação de riscos, coerência da validação, coerência cruzada entre artefatos, clareza da comunicação técnica) — sem nota visível ao squad. Acordo de squad e Registro de princípios transferíveis **não são pontuados** (são registro obrigatório).
- Devolutiva ao fechar cada encontro, sempre em 4 passos: evidência observada → interpretação técnica → próximo passo → prazo/momento de revisão.

## Ambiente operacional (Classroom / dados — ref. KIT-048)
- Turma do polo no Google Classroom, tópico "Antes do Encontro 1" traz: guia do aluno, camada 0, os 4 CSVs, o guia de ambiente e o check-in.
- No **Encontro 1 e no Encontro 2** os dados (D1–D4) são lidos **direto nos arquivos**, citados na justificativa por `conjunto.campo` — **não** se usa notebook/Colab ainda (isso só entra no Encontro 3, para a Matriz de Teste).
- Cada instrumento é um único arquivo compartilhado que o squad inteiro edita (sem cópia por participante); o coordenador de célula lê e devolve, não escreve.
