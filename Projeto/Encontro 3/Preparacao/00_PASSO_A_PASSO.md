# Encontro 3: passo a passo do Squad 5 (UFC Sobral)

> 15/10/2026, 17:00–21:00, 240 min. Pergunta do dia: **"A escolha se sustenta?"**
> Fontes: apresentação do E3, camadas 0 a 3 do dossiê, dados D1–D4 e nossos artefatos do E1 e do E2. Nada aqui vem de gabarito.

## As 4 regras (valem o encontro inteiro)
1. **Toda célula diz de onde veio:** código do dossiê (C0, C1, C2, C3), `conjunto.campo` e, hoje, **qual saída do notebook**.
2. **Sorteio:** 4 hoje (Teste, Validação, Proposta, Pitch). O sorteado defende **2 células que não escreveu**. Todos leem tudo.
3. **Critério antes do teste:** critério escrito depois do resultado não conta.
4. **Uso de IA com registro** na Decisão Justificada: sugestão recebida, rejeitada e o motivo técnico.

Temos **3 perguntas** aos atores, da Matriz de Teste até o intervalo. Pergunta mal feita também gasta. Pergunta à Tereza não gasta: o mentor só relê a C3-01.

---

## Hoje à noite
- [ ] Abrir a **Decisão Justificada do E2** e ver se aceita edição. Se estiver só leitura, amanhã alguém cancela o envio, editamos e entregamos de novo.
- [ ] Escrever na Decisão a **sugestão de IA rejeitada**, que está faltando (texto pronto na seção 1).
- [ ] Definir quem escreve, quem apresenta e os **sub-times A e B**.
- [ ] Todos leem este arquivo e os artefatos do E2.

---

## 1. Abertura e camada 3 (00:00–00:25)
**O que acontece:** lista de presença, leitura da C3-01 e da C3-02, e registro **imediato** na Decisão do E2 (campo "Pontos de incerteza"). A fase só fecha com esse registro.

**C3-01, jurídico (PG-0518 contestado):**
> "Com a C3-01, nenhuma célula da Decisão caiu, porque a solução não decide cobertura de garantia e as duas saídas são explicáveis caso a caso (a resposta cita a OS e o manual; o alerta compara com a base do próprio equipamento). A exigência vira requisito: registrar de forma recuperável cada resposta, alerta e causa original e corrigida, o que o Canvas ainda não prevê."

**C3-02, fornecedor novo da VS-212:**
> "Com a C3-02, caiu na Matriz a aderência do alerta por telemetria: a estimativa de ~92 falhas de vedação/válvula (C2-01) foi tratada como taxa estável, mas 35 das 77 corretivas com VS-212 estão no trimestre do lote novo (`d3_ordens.pecas_trocadas`, `data_abertura`). A regra peça → causa continua válida para identificar vedação (28 de 28 com alta > 3°C após jun/26), mas parte das falhas é de fornecedor, o que a solução não resolve, e a base não tem campo de lote para separar as duas."

**Sugestão de IA rejeitada:**
> "A ferramenta de IA sugeriu que 'a proporção de preventivas vem caindo'. Rejeitada: as preventivas são estáveis em número (316 → 340) e quem cresce são as corretivas (411 → 673) (`d3_ordens.tipo_ordem` por semestre)."

**Pergunta do slide 12: "quem pede explicação das decisões de garantia, e de quê?"** Façam no squad:
| Quem (C0-12, C3-01) | O que pergunta | Explicação de um pedido ou do conjunto? | Como precisa receber |
|---|---|---|---|
| | | | |

Dica: comecem pela C3-01 e pela C1-01 (quem decide a garantia, quem contesta, quem precisa provar para terceiros) e incluam quem constrói o sistema.

---

## 2. Matriz de Teste, 1ª parte (00:25–00:50), em 2 sub-times sem conversar
Cada sub-time preenche: **hipótese a testar**, **evidência necessária** e **forma de teste**.

Nossa proposta:
- **Hipótese:** H1 do E1, o alerta de telemetria para vedação/válvula, agora medido com a **causa corrigida pela peça** (C2-01) e considerando o lote novo (C3-02). É a única com dados para testar hoje; o manual do RAG não existe.
- **Confirma:** falhas de vedação/válvula precedidas de alta de `temp_descarga_maxima` sobre a base do próprio equipamento, **nos dois períodos** (antes e depois de jun/26).
- **Refuta:** alerta que dispara igual nas demais falhas, ou sinal que some depois de jun/26.
- **Forma:** prática, no notebook, que roda no Colab gratuito.

**Perguntas (no máximo 3):**
1. Lacuna declarada pela C3-02: "Em que data o lote novo da VS-212 chegou a cada planta?"
2. Das perguntas que sobraram do E2, só as que ainda mudam a decisão (ex.: o manual da série CP existe em formato digital?).
3. Guardar a 3ª para uma dúvida que aparecer na hora.

Resposta "a empresa vai verificar" vira **incerteza registrada**.

## 3. Critério a priori (00:50–01:15), squad inteiro
1. Juntar A e B numa versão só, anotando de qual versão veio cada célula.
2. **Escrever o critério de sucesso ANTES de rodar.** Rascunho para ajustar à métrica do caminho escolhido:
   > "Medido contra a causa corrigida pela peça, o alerta detecta **≥ 80%** das falhas de vedação/válvula com telemetria válida, **antes e depois de jun/26**, e dispara em **≤ 10%** das demais corretivas. Abaixo disso, o alerta não entra no plano do dia 90 e fica só em modo sombra."
3. Escolher o **caminho do notebook** (A, B ou C) e escrever o motivo: qual deles testa a H1.
4. Escrever **por que o teste prático é viável hoje**: dados D2/D3 disponíveis, Colab gratuito, sem GPU.

Pergunta-guia: **"que número, se não aparecer, nos faria mudar a decisão?"** Depois vem o sorteio.

## 4. Intervalo (01:15–01:30)
Janela de perguntas fechada.

## 5. Notebook (01:30–02:20), squad inteiro
O notebook **vem pronto** (tópico Encontro 3 da turma); não vamos programar.
1. Abrir **pela turma**, no Colab, com a conta do Classroom.
2. **Seção 4:** registrar o caminho e o critério, igual ao da Matriz, **antes** de rodar.
3. Rodar o caminho. Nos pontos marcados: **primeiro fixar o corte, depois calcular.**
4. Escrever a resposta em 3 partes:
   - **número obtido** (citar a saída do notebook);
   - **efeito na decisão** (mantém, ajusta ou revisa o E2?);
   - **até onde vale** (recorte, período, só equipamentos com telemetria).
5. Sobrou tempo? Rodar um segundo caminho.

Se o número contrariar o E2, **revisamos a decisão**. Isso conta a favor.

## 6. Resultado e Matriz de Validação (02:20–02:50)
- Na **Matriz de Teste:** resultado, limitações e o que muda na decisão.
- Na **Matriz de Validação**, uma linha por critério, com métrica ou evidência, resultado e origem:

| Critério | Métrica / evidência | Resultado | Origem |
|---|---|---|---|
| Detecção (recall) | % das falhas de vedação/válvula com alerta prévio | (notebook) | saída nº __ |
| Falso alarme | % das demais corretivas com alerta | (notebook) | saída nº __ |
| Estabilidade no tempo | antes × depois de jun/26 | (notebook) | saída nº __ |
| Explicabilidade caso a caso | cada alerta mostra "+X°C sobre a base do equipamento"; cada resposta cita OS e manual | atende ao requisito da C3-01? | C3-01, Canvas |
| Privacidade | `id_tecnico` só como contato, nunca para ranquear | | C0-09 |
| Viés / cobertura | 32% da frota sem telemetria fica fora do alerta | | `d1_frota.tem_telemetria` |

- **Riscos residuais:**
  - falha de lote misturada com falha de operação, sem campo de lote (C3-02);
  - manual indisponível (C1-03);
  - falso alarme ainda não medido em operação;
  - a regra peça → causa só foi validada pelo Wagner nas ordens genéricas (C2-01).
- **Revisar o Canvas:** acrescentar o **registro recuperável** (C3-01) e localizar cada risco na etapa do fluxo.

## 7. Fechamento das matrizes (02:50–03:00)
- [ ] Critério de sucesso definido antes do teste
- [ ] Resultado e limitações registrados
- [ ] Riscos residuais explícitos
- [ ] IA responsável tratada como critério

Depois vem o sorteio.

## 8. Proposta Técnica Final (03:00–03:25), integração sem texto novo
1. **Problema em 1 frase** (do Mapa do E1).
2. **Abordagem** escolhida e justificada (Decisão do E2).
3. **Arquitetura:** dados e validação, citando o Canvas.
4. **Próximos passos:** riscos e o que viria na residência.

- [ ] Integra problema até validação de forma coerente
- [ ] Arquitetura com referência ao Canvas
- [ ] Validação com hipótese, critério, método e resultado
- [ ] Riscos e próximos passos explícitos
- [ ] Fecha com o problema do E1

Depois vem o sorteio. Se o tempo apertar, é a profundidade da Proposta que cede.

## 9. Roteiro de Pitch e defesa curta (03:30–03:45)
| Tempo | Bloco | Rascunho | Quem fala |
|---|---|---|---|
| 30 s | Problema | "A reincidência de corretivas cresce porque o histórico do equipamento não acompanha a troca de técnico e a causa registrada não é confiável. É isso que puxa o tempo médio do painel." | |
| 60 s | Abordagem | Assistente de consulta somente leitura (histórico com causa corrigida + manual) no dia 90; alerta de telemetria em sombra; abrir OS e pedir peça só depois. Workflow, não agente. | |
| 60 s | Justificativa | Prazo e verba (C2-02); auditoria caso a caso (C3-01); evidência da C2-01. | |
| 60 s | Validação, riscos, próximos passos | Número do teste + o que ele não mostra; riscos (lote VS-212, manual, falso alarme); o que vem depois. **Sem esconder risco.** | |

**Defesa curta:** a bancada pergunta **o que a proposta não resolve**. Cada resposta aponta o artefato:
- falha de lote → C3-02 + Matriz de Validação;
- equipamentos sem telemetria → `d1_frota` + riscos;
- manual que não existe → premissa da Decisão.

Depois vem o sorteio. O ensaio cronometrado é fora da sala.

## 10. Princípios transferíveis (03:45–04:00)
Formato: **"Quando ___, decidimos ___, porque ___ (Encontro ___, artefato ___)."** Escrevam de 3 a 5 e um "o que faríamos diferente". Sugestões:
- Quando o rótulo vem do formulário do técnico, corrigimos pela peça antes de medir, porque 38% das causas genéricas estavam erradas (E2, Decisão).
- Quando a verba é para um formato, entregamos o formato com o motor mais auditável, porque a decisão alimenta a garantia (E2, Matriz/Decisão).
- Quando um número sustenta a decisão, escrevemos o corte antes de calcular (E3, Matriz de Teste).
- Quando chega informação nova, registramos a célula que caiu em vez de reescrever o passado (E2 e E3, Decisão).

**Faríamos diferente:** citar a matriz do curso base em cada célula desde o E2 e desenhar o Canvas como diagrama.

## Antes de sair
- [ ] As 5 atividades marcadas como entregues
- [ ] Decisão do E2 entregue de novo, se precisou editar
- [ ] Foto final e lista de presença
