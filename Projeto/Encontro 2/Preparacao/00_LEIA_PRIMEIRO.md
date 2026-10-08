# Preparação para o Encontro 2 — Squad 5 (UFC)

## Em uma frase
No Encontro 2 o squad **recebe informação nova (camada 2), registra o que ela derrubou, compara as alternativas, escolhe uma e desenha como ela funciona.**

## Os arquivos, na ordem de leitura
| Arquivo | O que é |
|---|---|
| `06_camada2_impacto.md` | **Comecem por aqui.** O que a camada 2 diz, as contas que o Wagner não fez e quais células caem. |
| `03_matriz_alternativas_esboco.md` | Matriz com 3 alternativas, já ajustada pela camada 2 |
| `04_decisao_justificada_esboco.md` | A escolha, com premissas e incertezas (célula que caiu + sugestão de IA rejeitada) |
| `05_canvas_arquitetura_esboco.md` | O desenho da solução, com riscos marcados no fluxo |
| `01_mapa_tecnico_v2.md` / `02_hipotese_tecnica_v2.md` | Correções do E1 que **não dependem** da camada 2 (coerência, códigos, números) |

> **Importante sobre o E1:** **não reescrevam** no Mapa e na Hipótese o que a camada 2 derrubou. O que caiu deve ficar **registrado** na Decisão Justificada, e esse registro é avaliado. As correções dos arquivos 01 e 02 são outra coisa: são erros que já existiam antes da camada 2.

## O resumo da camada 2
1. **C2-01 (Wagner):** 38% das ordens com causa genérica eram, na verdade, **vedação ou válvula**, identificadas pela peça trocada. Essas falhas são ~92, não 23, e todas têm o aviso de temperatura antes. A ideia da telemetria **ganha força**, e a causa registrada pelo técnico **não é confiável**.
2. **C2-02 (diretoria):** a verba é **do assistente conversacional**, e o piloto tem **90 dias**. Precisamos dizer o que funciona no dia 90 e o que fica para depois.

**Nossa resposta:** um assistente conversacional **somente leitura** (histórico com causa corrigida + manual) em operação no dia 90. O alerta de telemetria roda **em sombra**. Abrir OS e pedir peça fica **depois**. É um workflow, não um agente.

## No encontro, minuto a minuto
| Tempo | O quê | Base |
|---|---|---|
| 0:00–0:25 | Falar o problema em 1 frase, ler a camada 2, registrar **qual célula caiu** | `06`, tabela "Quais células caem" |
| 0:25–0:35 | Assistir o mentor fechar uma decisão | — |
| 0:35–1:35 | **Matriz** em 2 sub-times. Fazer as perguntas. | `03` |
| 1:35–1:50 | Intervalo (a janela de perguntas fecha) | — |
| 1:50–2:10 | Confronto entre sub-times, Matriz única, sorteio | `03` |
| 2:10–2:55 | **Decisão Justificada** + sorteio | `04` |
| 2:55–3:45 | **Canvas** + sorteio | `05` |
| 3:45–4:00 | Devolutiva do mentor | — |

## Perguntas aos atores (temos **3**; parar na 3ª)
1. **Nelson (diretor):** "A diretoria aceita que o assistente do piloto de 90 dias seja só de consulta, deixando abrir OS e pedir peça para a fase seguinte?" → valida a premissa central (C2-02).
2. **Simone (TI):** "O manual da série CP existe em formato digital pesquisável e pode ser disponibilizado?" → viabilidade do RAG.
3. **Wagner (engenheiro):** "A regra VS-212 → vedação e VA-118 → válvula vale também para ordens com causa específica, como as 16 de contaminação por particulado que trocaram VS-212?" → valida o pré-processamento.
4. *(reserva)* **Iran:** "Quanto tempo você leva hoje para descobrir o que foi feito na visita anterior?"

## Antes do encontro
- [ ] Todos leem `06`, `03`, `04` e `05`, porque qualquer um pode ser sorteado
- [ ] Rhuan sobe as correções do Mapa e da Hipótese (`01`, `02`) na pasta da turma
- [ ] Definir os 2 sub-times
- [ ] Isac se prepara para apresentar
- [ ] Revisar M1 (T1.1, T1.2) e M2 (T2.1, T2.2)
- [ ] Lembrar: os códigos são **C0**, **C1**, **C2** com zero. C0-07 = frota, C0-08 = telemetria, C0-09 = ordens, C0-10 = garantia.
