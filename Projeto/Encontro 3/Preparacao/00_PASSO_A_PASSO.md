# Encontro 3: passo a passo do Squad 5 (UFC Sobral)

> 15/10/2026, 17:00–21:00, 240 min. Pergunta do dia: **"A escolha se sustenta?"**
> Fontes: apresentação do E3, camada 3 (KIT-028), templates KIT-011 (Matriz de Teste), KIT-012 (Matriz de Validação) e KIT-016 (Roteiro de Pitch), notebook KIT-023, camadas 0 a 2, dados D1–D4 e nossos artefatos do E1 e do E2. Nada aqui vem de gabarito.
> Reforços do curso de Condução de Projetos: B4 (prontidão de fonte), B5 (critério a priori, modo sombra) e B6 (defesa em 6 elementos, uso fora de escopo). Do M3: proporção de positivos, dados antes de modelo.
> Os templates dizem "Encontro 4/5" e "tutor" porque são do kit de 5 encontros. Neste arco, valem para hoje e "tutor" = mentor. Os templates da Proposta Técnica Final (KIT-015) e dos Princípios (KIT-021) não estão na pasta; para eles vale a apresentação.

## As 4 regras (valem o encontro inteiro)
1. **Toda célula diz de onde veio:** código do dossiê (C0, C1, C2, C3), `conjunto.campo` e, hoje, **qual saída do notebook**.
2. **Sorteio:** 4 hoje (Teste, Validação, Proposta, Pitch). O sorteado defende **2 células que não escreveu**. Todos leem tudo.
3. **Critério antes do teste:** critério escrito depois do resultado não conta. O notebook impõe isso: o critério vai no primeiro `# TODO`, antes do cálculo.
4. **Uso de IA com registro** na Decisão Justificada: sugestão recebida, rejeitada e o motivo técnico.

Temos **3 perguntas** aos atores, da Matriz de Teste até o intervalo. Pergunta mal feita também gasta. Pergunta à Tereza não gasta: o mentor só relê a C3-01.

---

## Antes de começar
- [ ] Abrir a **Decisão Justificada do E2** e ver se aceita edição. Se estiver só leitura, cancelar o envio, editar e entregar de novo.
- [ ] Escrever na Decisão a **sugestão de IA rejeitada**, que está faltando (texto pronto na seção 1).
- [ ] Definir quem registra, quem apresenta e os **sub-times A e B** (os templates pedem "papéis do dia" na identificação).
- [ ] Todos leem este arquivo e os artefatos do E2.
- [ ] **Ninguém roda os caminhos do notebook antes da seção 3.** Os números só valem se o critério vier antes.

---

## 1. Abertura e camada 3 (00:00–00:25)
**O que acontece:** lista de presença, leitura da C3-01 e da C3-02 (KIT-028), e registro **imediato** na Decisão do E2 (campo "Pontos de incerteza"). A fase só fecha com esse registro.

**C3-01, jurídico (PG-0518 contestado):** o cliente alega que a Aroeira "não demonstrou em que se baseou" para negar por uso fora de especificação. Exigência que vira **requisito do produto**: decisão de cobertura apoiada em modelo precisa de explicação **caso a caso**, auditável, apresentável a terceiros e **registrada para recuperação**. Explicação do conjunto não serve.
> "Com a C3-01, nenhuma célula da Decisão caiu, porque a solução não decide cobertura de garantia e as duas saídas são explicáveis caso a caso (a resposta cita a OS e o manual; o alerta compara com a base do próprio equipamento). A exigência vira requisito: registrar de forma recuperável cada resposta, alerta e causa original e corrigida, o que o Canvas ainda não prevê."

**C3-02, fornecedor novo da VS-212:** lote no último trimestre (jun–ago/26), sem volume nem data por planta. Suprimentos pede o registro "com o mesmo cuidado" para acompanhar o lote.
> "Com a C3-02, caiu na Matriz a aderência do alerta por telemetria: a estimativa de ~92 falhas de vedação/válvula (C2-01) foi tratada como taxa estável, mas 35 das 77 corretivas com VS-212 estão no trimestre do lote novo (`d3_ordens.pecas_trocadas`, `data_abertura`). A regra peça → causa continua válida para identificar vedação, mas parte das falhas pode ser de fornecedor, o que a solução não resolve, e a base não tem campo de lote para separar as duas."

**Sugestão de IA rejeitada:**
> "A ferramenta de IA sugeriu que 'a proporção de preventivas vem caindo'. Rejeitada: as preventivas são estáveis em número (316 → 340) e quem cresce são as corretivas (411 → 673) (`d3_ordens.tipo_ordem` por semestre)."

**Pergunta do slide 12: "quem pede explicação das decisões de garantia, e de quê?"** Façam no squad:
| Quem (C0-12, C3-01) | O que pergunta | Explicação de um pedido ou do conjunto? | Como precisa receber |
|---|---|---|---|
| | | | |

Dica: comecem pela C3-01 e pela C1-01 (quem decide a garantia, quem contesta, quem precisa provar para terceiros) e incluam quem constrói o sistema.

---

## 2. O que o notebook permite testar (ler antes da Matriz de Teste)
O notebook KIT-023 **vem pronto**. Ele não testa uma regra de limiar como a que esboçamos antes. Ele oferece **três caminhos fixos**, todos sobre as peças `VS-212` e `VA-118` (`PECAS_SOB_SUSPEITA`, compatível com nosso Mapa):

| Caminho | O que mede | Critério que pede (antes de rodar) | Decide por | Alternativa nossa que testa (Matriz E2) |
|---|---|---|---|---|
| **A, analítico** | taxa de falha por equipamento-ano, por faixa de ciclo × ambiente, com intervalo por reamostragem | razão mínima > 1 entre o grupo e o resto | **limite inferior** do intervalo ≥ critério | nenhuma (é a pergunta "uso/ambiente" da garantia) |
| **B, preditivo** | Random Forest sobre janelas de 30 dias de telemetria prevendo troca da peça nos 30 dias seguintes, divisão **temporal** 70/30 | precisão fixada + sensibilidade mínima (sensibilidade = recall) | sensibilidade obtida na precisão fixada ≥ mínima | **Alternativa 1**: alerta por telemetria para vedação e válvula |
| **C, sobre dados** | concordância entre `causa_registrada` e peça trocada (VS-212 → vedação/particulado; VA-118 → válvula/particulado) | taxa de discordância limite | observada > limite → "intervir nos dados"; senão "trocar de modelo" | **Alternativa 2**, eixo "dados necessários": o assistente "necessita da causa corrigida pela peça" (= premissa 3 da Decisão) |

**De onde vêm as hipóteses de hoje.** A **Matriz de Alternativas do E2** (KIT-004, 08/10) reformulou as hipóteses do E1, e é dela que a Matriz de Teste parte. Linhagem (fonte: PDFs em `Encontro 1/entregaveis1/` e `Encontro 2/Artefatos/`, não os esboços):

| E1, Hipótese Técnica (01/10) | E2, Matriz de Alternativas (08/10) | O que mudou | Na Decisão / Canvas (E2) |
|---|---|---|---|
| **H1**: ML clássica supervisionada (classificação) sobre telemetria; condição "ter telemetria"; critério **Recall > 80%** | **Alt. 1**: alerta por telemetria para vedação e válvula. Aderência **média** (subiu de baixa com a C2-01); dados: telemetria diária (C0-07, C0-08); viabilidade média/alta, **"é possível iniciar sem ML"**, depende da rede do cliente (C0-03); risco: **alarmes falsos que geram visitas desnecessárias**; explicabilidade alta (demonstrativo de temperatura) | restrita a vedação e válvula; deixa de exigir ML; ganha o risco de falso alarme | "sistema de alertas por telemetria" **em paralelo**, que no Canvas fica "apenas registrando os alertas". Incerteza da Decisão: **"Recall > 80% (C2-01)"** |
| **H2**: RAG (recuperação) do manual e histórico; condição "visitado por outro técnico"; critério "taxa de acerto e precisão" | **Alt. 2**: assistente conversacional no histórico e no manual (workflow). Aderência **alta** (troca de técnico, pedido aprovado C2-02); dados: `d3_ordens` **com causa corrigida pela peça** + manual série CP (**ainda não disponibilizado**); viabilidade alta (sem treino de modelo); risco: **alucinação**; explicabilidade alta (cita OS e seção do manual, **falta validar com o manual real**) | vira assistente conversacional; passa a depender da causa corrigida pela peça | **abordagem escolhida**. Premissas 2 (manual digitalizado) e 3 (regra do Wagner) |
| **H3**: workflow determinístico H1+H2 | **Alt. 3**: workflow de busca e **criação de ordens de serviço**, chamadas determinísticas + LLM com humano no laço e fonte citada. Aderência alta; dados: OS, peças, frota (D1), garantia (D4); viabilidade **média** (depende de implementar funções e fluxos); risco: busca errônea e alucinação; explicabilidade alta (SQL referencia as linhas) | passa de "compor H1+H2" a "criar OS" | **não escolhida para o piloto**: a recomendação é a Alt. 2 com a Alt. 1 em paralelo |

**Orientação do articulador (15/10):** a Matriz de Teste parte **do que foi feito no E2** (as alternativas), e **recall não é a métrica certa para a Alt. 1**. Motivo: a falha é rara e, nesse caso, recall alto se consegue alertando quase tudo, que é justamente o risco que a Matriz registrou ("alarmes falsos que geram visitas desnecessárias"). A métrica que mede esse risco é a **precisão** (de cada alerta, quantos precedem troca real), lida contra a **prevalência**. O "Recall > 80%" que estava como incerteza na Decisão é **substituído antes do teste**, e isso fica registrado (seção 4).

Riscos do Canvas (E2): **alucinação da LLM**, manual desatualizado, regra do Wagner, falsos alarmes.

Fatos descritivos (a seção 3 do notebook os imprime antes da escolha, então não contaminam o critério):
- período das ordens: 2025-09-01 a 2026-08-31;
- 108 ordens trocaram VS-212 ou VA-118, **todas corretivas**;
- **43 delas em jun–ago/26**, o trimestre do lote novo (C3-02).

**Recomendação: caminho B como principal, C como segundo** se sobrar tempo.
- **B** testa a **Alternativa 1**, e o resultado é **desconhecido**. Lido pela precisão (falso alarme), é o número que decide se o alerta continua em paralelo, sai do plano ou ganha força.
- **C** testa o **requisito de dados da Alternativa 2**, a abordagem escolhida: a causa corrigida pela peça. A C2-01 já trouxe a evidência do Wagner, mas só nas ordens genéricas. O C mede nas 108 ordens das duas peças e responde a outra incerteza da Decisão: "revalidação das bases de OS por um engenheiro". Rodem se der tempo; é o segundo mais importante.
- **A** fica de fora hoje. Na defesa, dizer qual ficou de fora "é parte da defesa" (notebook, seção 11). Ele mede ciclo × ambiente: é a pergunta da negativa por uso fora de especificação (C3-01), e nenhuma das nossas alternativas.
- A **parte de recuperação da Alt. 2** (acerto da resposta) e a **Alt. 3** não têm caminho no notebook: ficam como teste conceitual.

Pelas definições do KIT-011, o **B é prático** (executa um modelo sobre histórico rotulado) e o **C é analítico** (cálculo sobre dados já disponíveis, sem modelo).

> Atenção: o "28 de 28" e o "+3°C em 7 dias" são análise nossa de preparo, não estão em nenhum artefato entregue e não são resultado do teste. Não citar como evidência.

---

## 3. Matriz de Teste, 1ª parte (00:25–00:50), em 2 sub-times sem conversar
**Template KIT-011, seção 1 "Plano de teste": uma linha por hipótese**, com colunas *Hipótese · Evidência necessária · Forma de teste (conceitual, analítico ou prático) · Critério de sucesso (a priori)*.

Nossa proposta: **as alternativas da Matriz do E2**, com o texto e os riscos que estão nela, mais o que a camada 3 mudou. A Alt. 2 tem duas linhas porque tem duas partes testáveis de formas diferentes (dados e recuperação). Na coluna de evidência, sempre **o que confirmaria** e **o que refutaria**.

| Hipótese (Matriz de Alternativas, E2) | Evidência necessária | Forma de teste | Critério de sucesso (a priori) |
|---|---|---|---|
| **Alt. 1 — Alerta por telemetria para vedação e válvula** (VS-212, VA-118), em equipamento com telemetria diária (C0-07, C0-08), sinaliza a falha antes da troca da peça, sem gerar visitas desnecessárias (risco registrado na Matriz). Com a C3-02, o período recente inclui o lote novo da VS-212 | **Confirma:** no período de teste (posterior ao treino), a maior parte dos alertas é seguida de troca de VS-212/VA-118 em até 30 dias, com precisão bem acima da prevalência, e o alerta ainda pega uma parte útil das trocas. **Refuta:** precisão próxima da prevalência (o alerta não distingue e vira visita desnecessária), ou precisão alta só com sensibilidade irrisória (o alerta quase não dispara) | **Prática**: notebook, caminho B (modelo de referência sobre histórico rotulado, divisão temporal) | **Precisão ≥ 0,50** (de cada 2 alertas, ao menos 1 precede troca real) com **sensibilidade ≥ 0,30** nessa precisão. Ver seção 4 |
| **Alt. 2a — Dados do assistente**: o histórico só serve ao assistente com a causa corrigida pela peça, porque a causa registrada esconde a falha real (Matriz, "dados necessários"; premissa 3 da Decisão; C2-01) | **Confirma:** parcela relevante das 108 ordens de VS-212/VA-118 com causa registrada incompatível com a peça, e a leitura da amostra de 20 ordens mostra o relato do técnico coerente com a peça. **Refuta:** discordância baixa (a causa registrada já é confiável e a correção não é pré-requisito), ou relatos da amostra que contradizem a peça (a regra peça → causa erraria) | **Analítica**: notebook, caminho C (cálculo sobre D3) + leitura da amostra | **Taxa de discordância > 0,30** → a correção pela peça é pré-requisito do assistente. Ver seção 4 |
| **Alt. 2b — Recuperação do assistente**: o assistente conversacional responde ao técnico com a OS e a seção do manual corretas, citando a fonte, mais rápido que o processo atual, em equipamento visitado por outro técnico (C1-03; Matriz: aderência alta, explicabilidade "cita a OS e a seção do manual") | **Confirma:** em perguntas reais de técnicos, a resposta traz a OS e o trecho certos, com fonte verificável, em menos tempo que hoje. **Refuta:** resposta sem fonte ou com OS/trecho errado (alucinação e busca errônea, riscos da Matriz), ou manual que não existe em formato digital | **Conceitual**: argumento contra os critérios da Decisão (prazo, explicabilidade, auditoria C3-01). O manual não foi disponibilizado (premissa 2) e não há linha de base de tempo | Atende se cada resposta for **rastreável** (OS + seção citadas, registro recuperável, C3-01) e cabe em **90 dias sem treinar modelo** (C2-02). A taxa de acerto fica sem número: primeiro teste da residência |

**Alt. 3 (workflow que cria OS)** não entra: não foi escolhida para o piloto (Decisão). Escrever abaixo da tabela: "Alt. 3 fora do teste: não está na decisão do dia 90."

**Justificativa da forma de teste** (campo obrigatório: *o que impediria o teste prático*), 1 a 3 frases:
> "Para a Alt. 1 nada impede o teste prático: D2 e D3 estão no ambiente da turma e o notebook roda no Colab sem GPU. Para os dados da Alt. 2 basta o teste analítico, um cálculo sobre D3 que já responde à pergunta. A recuperação da Alt. 2 só admite teste conceitual, porque o manual da série CP não foi disponibilizado (C1-03, premissa 2) e não há linha de base de tempo de busca."

**Perguntas (no máximo 3):**
1. Lacuna declarada pela C3-02: "Em que data o lote novo da VS-212 chegou a cada planta?" (Sem ela, o teste do B mistura os dois lotes.)
2. **"O manual da série CP existe em arquivo digital pesquisável, e quem responde por ele?"** Muda a decisão: sem isso o manual não entra com prazo no dia 90 (seção 9).
3. Guardar a 3ª para uma dúvida que aparecer na hora.

Resposta "a empresa vai verificar" vira **incerteza registrada**.

## 4. Critério a priori (00:50–01:15), squad inteiro
1. Juntar A e B numa versão só, anotando de qual versão veio cada célula.
2. **Escrever o critério do caminho B (Alt. 1) antes de rodar** (vai no `# TODO` do Passo A, seção 8 do notebook). A métrica principal é a **precisão**, porque é a que mede o risco que a Matriz registrou para a Alt. 1. O notebook pede também uma sensibilidade mínima: ela entra como **piso**, para o alerta não ser "preciso" só porque quase nunca dispara. Rascunho, com números para o squad fechar **antes** de rodar:
   > "Por orientação do articulador, substituímos antes do teste o 'Recall > 80%' (incerteza da Decisão do E2) pela precisão. Recall alto em falha rara se obtém alertando quase tudo, que é o risco de visitas desnecessárias registrado na Matriz. Critério: **precisão ≥ 0,50** (de cada 2 alertas, ao menos 1 precede troca real de VS-212/VA-118 em 30 dias) com **sensibilidade ≥ 0,30** nessa precisão (o alerta pega ao menos 3 de cada 10 trocas). O alerta roda em paralelo ao assistente e não substitui nada, então pegar parte das trocas já tem valor, desde que não gere visita à toa. Abaixo disso, a Alt. 1 não se sustenta neste teste: o alerta continua só registrando, como no Canvas, e não entra no plano do dia 90."
   - **Registrar a troca de métrica na Decisão do E2** (pontos de incerteza), com data e motivo, **antes** de rodar. É revisão declarada, não critério escolhido depois.
   - Comparar com a **prevalência** (linha tracejada do gráfico): uma precisão de 0,50 só tem valor se ficar bem acima dela.
   - A Matriz diz que a Alt. 1 "pode iniciar sem ML" (por limiar). O caminho B mede o **sinal da telemetria** com um modelo de referência. Se o modelo não acha sinal, um limiar simples também não tem base. A versão por limiar em si **não é medida hoje**: registrar como limitação.
3. **Regra de entrada e saída do modo sombra** (B5):
   > "O alerta só passa a valer para o técnico depois de N trocas de VS-212/VA-118 observadas em paralelo (só registrando, como no Canvas), com precisão ≥ 0,50 e sensibilidade ≥ 0,30. Volta para revisão se a precisão cair abaixo de 0,50 por duas janelas seguidas."

   Contar em eventos, não em semanas: a falha é rara.
4. **Critério do caminho C (Alt. 2a)**, declarado já, mesmo que só rodem se sobrar tempo. Este número é **novo** (a Matriz não tinha): **taxa de discordância limite 0,30**, abaixo dos 38% que o Wagner achou nas genéricas (C2-01).
   > "Se mais de 30% das ordens de VS-212/VA-118 tiverem causa registrada incompatível com a peça, a correção pela peça é pré-requisito do assistente e entra no cronograma antes da consulta (o notebook chama isso de 'intervir nos dados'). Abaixo disso, a correção continua, mas deixa de ser bloqueante."
5. Registrar a escolha do caminho e o porquê: "B, porque testa a Alt. 1 pelo risco que a Matriz registrou (falso alarme); C em seguida, porque testa o dado que a Alt. 2 exige; abrimos mão do A, que é a pergunta da garantia".

Pergunta-guia: **"que número, se não aparecer, nos faria mudar a decisão?"** Resposta: **precisão de 0,50** do alerta no caminho B, com o piso de sensibilidade de 0,30. Para a Alt. 2: discordância acima de 0,30. Depois vem o sorteio.

## 5. Intervalo (01:15–01:30)
Janela de perguntas fechada.

## 6. Notebook (01:30–02:20), squad inteiro
Não vamos programar além dos `# TODO`.
1. Abrir **pela turma**, no Colab, com a conta do Classroom. Se os CSV não estiverem na sessão, a célula 2 avisa: subir os 4 arquivos com os mesmos nomes.
2. Rodar seções 1 a 3. Na **seção 4**, escrever na célula de resposta: caminho, por que este e qual abrimos mão, e o critério (copiar da seção 4 deste arquivo).
3. **Caminho B**:
   - Rodar a seção 7: janelas, treino de referência e curva. Anotar **corte temporal**, **positivos no treino e no teste** e a **prevalência**.
   - Exercício da seção 8:
     - **Passo A**: `precisao_fixada = 0.50`, `sensibilidade_minima_declarada = 0.30` (ou os números que o squad fechou na seção 4).
     - **Passo B**: atributos só de `ATRIBUTOS_DA_JANELA`. Sugestão: `["temp_maxima_media", "temp_maxima_pico", "ciclo_medio", "pressao_media"]`, porque a temperatura é o sinal da C2-01. Passar pelo `teste_sanidade_atributos`, treinar com `treinar_referencia`, calcular com `sensibilidade_na_precisao` e a decisão por comparação.
   - **Nunca** usar campos do horizonte (`duracao_horas_no_horizonte`, `pecas_no_horizonte`, `valor_pleiteado_no_horizonte`): é vazamento, "resultado excelente e falso".
4. Rodar a autoverificação e escrever a resposta em 3 partes:
   - **número obtido**: sensibilidade alcançada com precisão ≥ 0,50, quantos positivos do teste ela representa e a prevalência (citar a saída);
   - **efeito na decisão**: a Alt. 1 se sustenta ou não; o alerta continua "em paralelo, apenas registrando" (Canvas), sai do plano ou ganha força;
   - **até onde vale**: período de teste, prevalência, só equipamentos com telemetria, versão por limiar não medida.
5. Sobrou tempo? **Caminho C (Alt. 2a)** (seções 9–10):
   - ler a amostra de 20 ordens;
   - `taxa_discordancia_limite = 0.30`;
   - taxa observada = ordens **sem** causa compatível ÷ total;
   - `ganho_em_ordens` = número dessas ordens = esforço da revalidação pelo engenheiro (incerteza da Matriz e da Decisão);
   - resposta em 3 partes: número, efeito na Alt. 2 (a correção pela peça é bloqueante ou não), limite (só duas peças; não diz se a peça trocada era a causa real).

Se o número contrariar o E2, **revisamos a decisão**. Isso conta a favor.

## 7. Resultado e Matriz de Validação (02:20–02:50)
**Matriz de Teste, seções 2 e 3 do KIT-011:**
- **Resultado e limitações.** "Resultado sem limitação declarada não é resultado." Limitações já previstas para o B:
  - o período de teste (últimos ~30% das janelas) cai em boa parte no **trimestre do lote novo** (43 das 108 trocas em jun–ago/26). A prevalência no teste é maior que no treino, e o modelo pode estar detectando falha de lote, não de operação (C3-02);
  - só equipamentos com telemetria (`d1_frota.tem_telemetria`);
  - o rótulo é "trocou a peça", não "falhou por vedação": inclui trocas por causas genéricas;
  - o ponto de corte é escolhido sobre o próprio teste (`sensibilidade_na_precisao`), o que é otimista.
- **O resultado revisa a decisão? Em quê?** Registrar também se nada muda: "confirmar é uma revisão, desde que sustentada pela evidência".

**Matriz de Validação (KIT-012):** colunas *Critério · Métrica ou evidência · Resultado ou status · Risco associado* (técnico, ético ou operacional). "Consolida o que o teste produziu, e não o status desejado." O template pede que cada critério **herde do escopo ou da decisão**. Os critérios sugeridos (aderência, qualidade dos dados, explicabilidade, viabilidade) são os mesmos eixos da nossa Matriz de Alternativas do E2: citar a célula da Matriz em cada linha.

| Critério | Métrica ou evidência | Resultado ou status | Risco associado |
|---|---|---|---|
| Aderência técnica, Alt. 1 (Matriz E2: aderência "média") | precisão dos alertas (≥ 0,50) contra a prevalência, com sensibilidade ≥ 0,30 (caminho B) | saída nº __ | **Técnico**: alerta pode só detectar falha de lote (C3-02) |
| Aderência técnica, Alt. 2 (Matriz E2: aderência "alta") | taxa de acerto e precisão da recuperação | **não testado**: manual indisponível | **Técnico**: alucinação da LLM e busca errônea (riscos da Matriz e do Canvas) |
| Qualidade dos dados, Alt. 2 (Matriz E2: "necessita da causa corrigida pela peça") | taxa de discordância causa × peça (caminho C) ou C2-01 | saída nº __ ou C2-01 | **Técnico**: corrigir pela peça foi validado só nas genéricas; sem campo de lote em D3 |
| Explicabilidade | cada alerta mostra "+X°C sobre a base do equipamento"; cada resposta cita OS e manual; registro recuperável | atende a C3-01? | **Ético/operacional**: saída usada como base para negar garantia (fora de escopo) |
| Vieses e privacidade | 32% da frota sem telemetria fica fora do alerta; `id_tecnico` só como contato, nunca para ranquear | `d1_frota.tem_telemetria`, C0-09 | **Ético**: cobertura desigual; dado pessoal sob LGPD |
| Viabilidade (Matriz E2: Alt. 1 "média/alta", depende da rede do cliente; Alt. 2 "alta") | prazo e verba de 90 dias (C2-02); manual digital disponível?; rede do cliente (C0-03) | resposta à pergunta 2 | **Operacional**: manual não verificado; alerta depende da rede |

**Riscos residuais (seção 2 do KIT-012):** registrar **quem aceita cada risco e sob qual condição**: "risco sem aceite declarado volta como surpresa no pitch". Os nomes são proposta; confirmar com o mentor.

| Risco residual | Quem aceita (C0-12) | Sob qual condição |
|---|---|---|
| Falha de lote misturada com falha de operação | Nelson, com suprimentos | enquanto o alerta for só sombra; reabre se as trocas de VS-212 seguirem ~2,5× acima da base |
| Manual indisponível | Nelson | o dia 90 entrega só o histórico; manual entra quando houver arquivo |
| Falso alarme ainda não medido em operação | Wagner | alerta em sombra até atingir o critério de entrada |
| Regra peça → causa validada só nas genéricas | Wagner | revisar amostra das ordens não genéricas antes do piloto |
| Alucinação da LLM na resposta (Canvas E2) | Nelson | toda resposta cita OS e trecho do manual; resposta sem fonte não é exibida |
| Frota sem telemetria fora do alerta | Nelson | assistente de histórico cobre 100% da frota; alerta não |

**Revisar o Canvas:** acrescentar o **registro recuperável** (C3-01) e localizar cada risco na etapa do fluxo. Para cada alerta ou resposta, guardar:
- versão da regra/modelo e do limiar;
- janela de telemetria usada e base do equipamento;
- OS e trecho do manual citados;
- causa **original** e **corrigida**, sem sobrescrever a original.

Exemplo: EQ-0129, OS-001537.

## 8. Fechamento das matrizes (02:50–03:00)
KIT-011:
- [ ] Evidência de teste com critério definido a priori
- [ ] Resultado e limitações registrados
- [ ] Decisão revisada ou confirmada com base em evidência
- [ ] Forma de teste justificada, com o que impediria o teste prático

KIT-012:
- [ ] Validação consolida critérios, riscos e métricas
- [ ] Riscos residuais explícitos
- [ ] IA responsável tratada como critério

Depois vem o sorteio.

## 9. Proposta Técnica Final (03:00–03:25), integração sem texto novo
(Template KIT-015 ausente da pasta; estrutura da apresentação.)
1. **Problema em 1 frase** (do Mapa do E1).
2. **Abordagem** escolhida e justificada (Decisão do E2, revista pelo teste).
3. **Arquitetura:** dados e validação, citando o Canvas. Separar o que tem prazo do que é investigação (B4):
   - **o dia 90 garante o histórico com causa corrigida** (D3, já testado);
   - **o manual vira verificação com data e plano B** (link para a seção do PDF), porque ninguém do squad viu o arquivo.
4. **Uso pretendido e fora de escopo** (uma linha):
   > "Uso pretendido: o técnico consultar histórico e manual e ver alertas de VS-212/VA-118. **Fora de escopo:** servir de base para negar garantia e avaliar ou ranquear técnicos (`id_tecnico`)."
5. **Próximos passos:** riscos e o que viria na residência:
   - modo sombra com plano de validação;
   - matriz de avaliação contínua com gatilho e destinatário;
   - runbook;
   - model card e datasheet;
   - pedido de **campo de lote/fornecedor** em D3;
   - o caminho A (ciclo × ambiente) como pergunta aberta para a garantia.

Checklist:
- [ ] Integra problema até validação de forma coerente
- [ ] Arquitetura com referência ao Canvas
- [ ] Validação com hipótese, critério, método e resultado
- [ ] Riscos e próximos passos explícitos
- [ ] Fecha com o problema do E1

Depois vem o sorteio. Se o tempo apertar, é a profundidade da Proposta que cede.

## 10. Roteiro de Pitch e defesa curta (03:30–03:45)
**KIT-016, seção 1.** Tempos são **teto, somam 3 min 30 s**; a folga até 5 min é para transição. "Momento que estoura tira o tempo do seguinte, e o que costuma ser sacrificado é a validação."

| Momento | Tempo | Conteúdo | Quem fala |
|---|---|---|---|
| Problema | 30 s | "A reincidência de corretivas cresce porque o histórico do equipamento não acompanha a troca de técnico e a causa registrada não é confiável. É isso que puxa o tempo médio do painel." | |
| Abordagem | 60 s | Assistente de consulta somente leitura (histórico com causa corrigida pela peça + manual) no dia 90; alerta de telemetria em sombra; abrir OS e pedir peça só depois. Workflow, não agente. **Custo assumido:** "abrimos mão de abrir OS no dia 90, e 32% da frota sem telemetria fica sem alerta." | |
| Justificativa | 60 s | Prazo e verba (C2-02); auditoria caso a caso (C3-01); evidência da C2-01; o que o teste disse. | |
| Validação e riscos | 30 s | Precisão do alerta (Alt. 1) contra a prevalência + o que ele não mostra (lote novo no período de teste; recuperação do assistente não testada sem o manual); riscos: lote VS-212, manual, falso alarme, alucinação. **Sem esconder risco.** | |
| Próximos passos | 30 s | **Plano de revisão:** "o alerta volta para revisão se a precisão cair abaixo de 0,50 por duas janelas em paralelo; se a empresa criar o campo de lote, revisamos a causa raiz." Residência. **Fechar com o problema do E1.** | |

**KIT-016, seção 2, preparação da defesa.** Colunas *Pergunta provável · Resposta em uma frase · Artefato que sustenta*. As perguntas seguem o template:

| Pergunta provável da bancada | Resposta em uma frase | Artefato |
|---|---|---|
| Por que esta abordagem e não a alternativa 3 (workflow que cria ordens de serviço)? | A 3 depende de mais funções e fluxos (viabilidade média na Matriz) e o pedido aprovado é o assistente de consulta (C2-02); criar OS fica para depois do piloto. | Matriz de Alternativas + Decisão (E2) |
| Por que não um agente? | O caminho é fixo (alerta → busca → resposta); a Decisão escolheu workflow pela auditoria com fontes citáveis (C0-04, C1-01). A ausência de alternativa agêntica já estava registrada como incerteza. | Matriz de Alternativas + Decisão (E2) |
| Qual critério decidiu? | Viabilidade no prazo, custo, aderência à troca de técnico e auditabilidade; o alerta (Alt. 1) foi testado pela precisão, porque o risco que a Matriz registrou é o falso alarme. | Decisão (E2) + Matriz de Teste |
| Que premissa foi assumida? | Que a peça corrige a causa (C2-01) e que o manual existe em formato usável. | Decisão, premissas 2 e 3 |
| O que a evidência cobre e o que não cobre? | Cobre equipamentos com telemetria no período testado; não separa falha de lote de falha de operação. | Matriz de Teste (limitações) + C3-02 |
| O que faria vocês mudarem de ideia? | Precisão do alerta abaixo de 0,50 (visitas à toa), ou o campo de lote mostrar que o sinal é só do fornecedor. | Critério a priori + riscos residuais |
| (Tereza) O sistema sustenta a negativa do PG-0518? | Não decide cobertura: mostraria +4,5°C sobre a base do EQ-0129, sinal de vedação, mas **não afirma uso fora de especificação**. Usar para negar garantia está fora de escopo. | C3-01 + Proposta (uso fora de escopo) |
| E o caminho que vocês não rodaram? | O A mede ciclo × ambiente, a pergunta da garantia, não a nossa; fica como próximo passo. | Notebook seção 4 + Proposta |

**Limitação × erro (B6):** a premissa de "taxa estável" da C2-01 caiu com a C3-02. Dizer que caiu, onde está registrado e o que muda. Conta a favor.

Checklist KIT-016:
- [ ] Pitch dentro do tempo (3 a 5 min)
- [ ] Riscos explícitos, não escondidos
- [ ] A fala fecha com o problema do Encontro 1
- [ ] Divisão de falas entre integrantes
- [ ] Cada resposta da defesa aponta o artefato

Depois vem o sorteio. O ensaio cronometrado é fora da sala.

## 11. Princípios transferíveis (03:45–04:00)
(Template KIT-021 ausente; formato da apresentação.) **"Quando ___, decidimos ___, porque ___ (Encontro ___, artefato ___)."** Escrevam de 3 a 5 e um "o que faríamos diferente". Sugestões:
- Quando o rótulo vem do formulário do técnico, corrigimos pela peça antes de medir, porque a causa genérica escondia vedação/válvula (E2, Decisão; C2-01).
- Quando a verba é para um formato, entregamos o formato com o motor mais auditável, porque a decisão alimenta a garantia (E2, Matriz/Decisão).
- Quando um número sustenta a decisão, escrevemos o critério antes de calcular, e o teste prático cabe no notebook gratuito (E3, Matriz de Teste).
- Quando o evento é raro, medimos sensibilidade numa precisão fixada, e não acurácia (E3, Matriz de Teste/Validação).
- Quando chega informação nova, registramos a célula que caiu em vez de reescrever o passado (E2 e E3, Decisão).
- Quando uma fonte só existe por relato (o manual), não comprometemos prazo nela (E3, Proposta).

**Faríamos diferente:** citar a matriz do curso base em cada célula desde o E2, desenhar o Canvas como diagrama e não fazer análise do limiar antes de ter o critério escrito.

## Antes de sair
- [ ] As 5 atividades marcadas como entregues
- [ ] Decisão do E2 entregue de novo, se precisou editar
- [ ] Notebook com as células de resposta preenchidas (seções 4 e 8, e 10 se rodou o C)
- [ ] Foto final e lista de presença
