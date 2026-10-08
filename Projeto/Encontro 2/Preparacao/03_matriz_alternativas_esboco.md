# Matriz de Alternativas (KIT-004) — ESBOÇO, já com a camada 2

> Base para os sub-times. Cada célula traz: **avaliação + justificativa curta + proveniência + [matriz do curso base]**. Reescrevam com as palavras de vocês, porque o sorteio cobra a defesa oral.
> Mudanças por causa da camada 2 estão marcadas com **(C2)**.

**Identificação:** Squad 5 – UFC · Data: __/10/2026 · Caso: caso da Aroeira · Registra: Rhuan Nunes · Apresenta: Isac

## 1. Comparação de alternativas

### A1 — Consulta conversacional ao histórico + manual (workflow com chamada pontual de modelo, somente leitura)
O técnico pergunta em linguagem natural ("o que foi feito no EQ0123?", "como troco a vedação?"). O sistema busca o histórico do equipamento e o trecho do manual e responde **citando a fonte**. Não executa ações.

| Critério | Avaliação |
|---|---|
| **Aderência ao problema** | **Alta.** Ataca a reincidência ligada à troca de técnico: 93% das visitas consecutivas mudam de técnico, e 67 de 70 reincidências rápidas envolvem troca (`d3_ordens.id_tecnico`, C1-03). É também a forma do pedido aprovado, o assistente conversacional (C2-02). [M0 tarefa: recuperação] |
| **Dados necessários** | Histórico em `d3_ordens` (C0-09), **com a causa corrigida pela peça**, porque 38% das genéricas revisadas estavam erradas (C2-01). Manual da série CP: ainda não disponível ao squad (C1-03). [T1.1 disponibilidade de dados] |
| **Viabilidade** | **Alta em 90 dias (C2-02).** Consulta + recuperação + 1 chamada de LLM para formular a resposta, com custo e latência baixos e previsíveis. Não exige treinar modelo. [T1.1 custo/latência; T2.1 custo de inferência] |
| **Riscos** | **Alucinação** na redação da resposta. **(C2)** O histórico pode repetir a causa errada (C2-01), mitigado mostrando peças + causa corrigida. Trecho errado do manual. [T1.2 alucinação, deriva temporal] |
| **Explicab. / TRL** | **Alta:** toda resposta cita a OS e a seção do manual. TRL 4–5: componentes maduros, falta validar com o manual real. [T2.1 transparência/auditoria] |

### A2 — Alerta por telemetria para vedação e válvula (detecção de anomalia / limiar)
Monitora a alta de `temp_descarga_maxima` contra a linha de base do próprio equipamento e gera alerta para antecipar a corretiva.

| Critério | Avaliação |
|---|---|
| **Aderência ao problema** | **Média (C2: subiu de baixa).** Com a causa corrigida pela peça, vedação + válvula passam de 23 para ~92 corretivas (~8,5%) (C2-01, `d3_ordens.pecas_trocadas`). Ainda não cobre elétrica, vazamento e contaminação, as causas que mais reincidem. [M0 tarefa: detecção de anomalia] |
| **Dados necessários** | Telemetria diária em 126 de 184 equipamentos (C0-07, C0-08). **(C2)** Os eventos rotulados válidos sobem de 16 para ~59 com telemetria, mas o rótulo exige correção pela peça. [T1.1 disponibilidade] |
| **Viabilidade** | **Média-alta.** Um limiar simples (alta > 3°C sobre a linha de base) separa 41 de 43 eventos reclassificados, contra 7 de 84 inconclusivos (`d2_telemetria.temp_descarga_maxima`). Dá para começar sem ML. O envio depende da rede do cliente (C0-03). [T1.1 custo, reprodutibilidade] |
| **Riscos** | Falso alarme (~6–8% nos grupos sem sinal) gera visita desnecessária. Dia de transmissão incompleta perde o sinal. 32% da frota fica de fora. [T2.2 cascading error: alerta errado → visita errada] |
| **Explicab. / TRL** | **Alta:** "temperatura máxima +X°C sobre a sua média" é explicável a qualquer técnico. TRL 3–4: sinal confirmado em histórico, sem piloto. [T2.1 transparência] |

### A3 — Assistente agêntico completo (pedido original: consulta + abre OS + pede peça, C0-05)

| Critério | Avaliação |
|---|---|
| **Aderência ao problema** | **Média.** Contém a A1, mas acrescenta ações (abrir OS, pedir peça) que nenhum relato aponta como dor (C1-03, C1-04). É exatamente o que a verba aprovou (C2-02). [M0 tarefa: geração + controle] |
| **Dados necessários** | Os da A1, mais integração de **escrita** com o sistema de OS e de peças. O squad não tem dado sobre esses sistemas (C0-02). [T1.1 disponibilidade] |
| **Viabilidade** | **Baixa em 90 dias (C2-02).** Integrações de escrita + controle de agente. O caminho é fixável (consultar → responder → abrir OS → pedir peça), então o branching dinâmico é baixo. O agente faz de 4 a 8 chamadas por interação no pior caso. [T2.1 branching + custo de inferência] |
| **Riscos** | Peça errada pedida (seleção de tool errada). Prompt injection via texto livre. **(C2)** Erro em cascata: a OS aberta com causa errada contamina o histórico e a garantia, e a causa errada já é frequente hoje (C2-01, C0-04). [T2.2: 4 modos de falha] |
| **Explicab. / TRL** | **Baixa:** cada passo do laço precisa de trace, e a OS alimenta a garantia, que tem efeito contratual (C1-01). TRL 2–3 neste contexto. [T2.1 transparência/auditoria] |

## 2. Abordagem recomendada + pontos de incerteza

**Recomendação:** entregar o **assistente conversacional em fases**, como o comunicado pede (C2-02):
- **Em operação no dia 90:** a **A1**, assistente **somente leitura** sobre histórico (com causa corrigida pela peça) e manual. É um workflow com uma chamada pontual de modelo, não um agente.
- **Em paralelo, modo sombra:** a **A2**, alerta de telemetria para vedação e válvula, registrando alertas sem despachar visita, para medir o falso alarme.
- **Depois dos 90 dias:** as ações da **A3** (abrir OS, pedir peça), e só se a T2.1 justificar.

Por quê: a A1 tem a maior aderência e a maior viabilidade no prazo, e é auditável. A A2 ganhou força com a C2-01, mas precisa medir o falso alarme antes de gerar visita. A A3 é a que mais falha (T2.2) e não cabe em 90 dias.

**Pontos de incerteza:**
1. O manual ainda não está disponível ao squad.
2. A regra peça→causa só foi validada pelo Wagner em ordens genéricas. Há 16 ordens de `contaminacao_particulado` com VS-212 (C2-01, fora do recorte).
3. A taxa de falso alarme da A2 não foi medida em operação.
4. Não há linha de base do tempo de busca (pergunta ao Iran).
5. Falta confirmar se a diretoria aceita um assistente sem ações no piloto (pergunta ao Nelson).

**Critério de pronto:** ☐ ≥2 alternativas em todas as dimensões · ☐ cada célula com justificativa · ☐ recomendação + incertezas
