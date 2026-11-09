# Desafio 1 · M4 Quantização e borda: passo a passo do Squad 05 UFC

> Fontes: `Documentos/M4-C-situacao-v1.pdf`, `Documentos/M4-C-roteiro-de-estudos-v1.pdf`, README e notebooks de `squad-05-ufc/desafio-1-m4/`, material do M4 em `Edge_AI/` e a leitura dos dados em `01_leitura_dos_dados.md`.
> Datas dos encontros: **E1 = [a confirmar]**, **E2 = [a confirmar]**.
> Rascunhos marcados com 🟡 são **propostas para a squad discutir**, não respostas fechadas. Nenhum número de modelo aqui foi medido: o critério vem antes do teste.

## A situação em 6 linhas
- Uma empresa de manutenção classifica cada relato de campo em 5 classes: `eletrica`, `mecanica`, `hidraulica` (inclui pneumática), `instrumentacao` e `seguranca`. A classe decide **qual especialidade é acionada** e **que peças são consultadas**.
- Hoje quem classifica é um modelo de linguagem (BERTimbau ajustado) que **só roda em servidor com GPU**. Muitas plantas não têm nuvem.
- Meta: classificar **no próprio coletor, sem conexão**. O coletor tem **8 GB de RAM, nenhuma GPU, e a resposta precisa sair em menos de 1 s**.
- A TI propõe **comprar coletores com GPU**.
- No coletor atual há dois caminhos: **(1) quantizar o modelo atual** (int8) ou **(2) trocar por um modelo menor** (TF-IDF com regressão logística).
- A squad fixa o critério **antes**, mede antes e depois, e justifica.

---

## Semana 1: compreender, delimitar e decidir

### Até 4 dias antes do E1 (cada um)
- [ ] Ler a situação (PDF).
- [ ] Leitura principal: **Leonarczyk et al., *Proposta de Arcabouço Teórico para a Avaliação Sistemática de Modelos de Linguagem Quantizados*, ERAMIA-RS 2025** (o link está no PDF do roteiro). Foco: **dimensões de qualidade e de eficiência** para avaliar um modelo quantizado.
- [ ] Do curso M4 (`Edge_AI/`): Aula 1 (continuum, compressão, runtimes), Aula 2 (seções 1 e 2: posicionamento e compressão/runtime), template *Matriz de decisão Edge x Cloud*.

**Pergunta para levar:** o pedido da TI é um problema ou uma solução? Que limite do coletor o modelo precisa respeitar?
> 🟡 É uma **solução** ("comprar coletor com GPU"). O **problema** é classificar o relato no ponto de operação, sem conexão, em menos de 1 s, com o hardware que já existe (8 GB, CPU). Pelo M4, o gatilho de edge aqui é a **conectividade não assumível** (plantas sem nuvem), somado à **latência como compromisso de produto** (o técnico espera a classe para acionar a especialidade). Então a pergunta não é edge ou cloud, porque o edge já está decidido pelos gatilhos. A pergunta é **qual compressão e qual runtime**, e só depois o **custo total**: GPU para toda a frota de coletores contra trabalho de software.

### Até a véspera (cada um)
- [ ] DeepLearning.AI, *Quantization Fundamentals with Hugging Face* (1h14): tipos de dado, quantização linear e carregamento em precisão menor.
- [ ] ONNX Runtime, *Quantize ONNX models* (onnxruntime.ai/docs/performance/model-optimizations/quantization.html): seção de **quantização dinâmica** e a função `quantize_dynamic`.
- [ ] Estimador de memória do Accelerate (`accelerate estimate-memory`, ou o Space *hf-accelerate/model-memory-usage*).
- [ ] **Folha técnica** (primeiro desafio desta etapa): tokens `GH_TOKEN` (fine-grained, só o repo da squad, Contents R/W) e `HF_TOKEN` (Read) nos *Secrets* do Colab.
- [ ] (Opcional, ajuda muito) Guia do notebook do M4: *Quantização de um modelo small* (`Edge_AI/Guia notebook - ...pdf`), a quantização feita à mão em numpy.

**Pergunta para levar:** o que muda num modelo quando os pesos passam de float32 para int8, e o que pode piorar?
> 🟡 Cada peso passa de 4 bytes para 1 byte, então o arquivo fica **~4x menor**. Com int8, a CPU também multiplica mais rápido. **Não muda**: a arquitetura, o número de pesos, o tokenizador e as classes. **Pode piorar**: a qualidade, porque cada peso é arredondado para um de 255 níveis (erro máximo = escala/2), e **um peso extremo infla a escala** e degrada todos os outros. Na quantização **dinâmica**, as ativações são quantizadas em tempo de execução, sem novo treino. A perda costuma ser pequena no total, mas pode se concentrar em **classes pequenas ou textos raros**, e por isso medimos também o F1 macro.

> **Conta de padaria (confirmar com o `accelerate`):** o BERTimbau base tem ~110 milhões de pesos. Em float32, ~110 M × 4 B ≈ **0,44 GB (~5–6% dos 8 GB)**; em int8, ≈ **0,11 GB**. Ou seja, **memória provavelmente não é o gargalo**. O limite que importa é o **tempo por relato em CPU com 2 threads**. Isso é hipótese até a etapa 4 do notebook.

### Véspera (squad reunida)
Rascunho em 3 blocos:
1. **Que decisão a empresa precisa tomar:** comprar ou não coletores com GPU; se não comprar, qual modelo vai no coletor atual.
2. **Restrição:** 8 GB, sem GPU, sem conexão, < 1 s por relato, um relato por vez.
3. **O que ainda é hipótese:** (a) que o BERT float32 já não caiba no tempo em CPU; (b) que o int8 perca pouca acurácia; (c) que o TF-IDF chegue perto do BERT nesses textos curtos e cheios de abreviação; (d) que o rótulo seja consistente (ver `01_leitura_dos_dados.md`: relatos com dois problemas).

**Pergunta para levar:** que medidas de eficiência e de qualidade o artigo propõe, e quais delas a situação exige?
> 🟡 Fechar depois da leitura. A situação exige no mínimo: **eficiência**, com tamanho em disco/memória e latência por amostra (batch 1, CPU, 2 threads); **qualidade**, com acurácia e F1 macro, mais a **perda em relação à referência float32**. Vale discutir se precisamos olhar **por classe** (`seguranca` é a menor e a mais cara de errar).

### No Encontro 1 (squad + instrutor)
- [ ] **KIT-001 Mapa Técnico do Problema**: pedido (GPU) separado do problema (classificar offline < 1 s no coletor atual); restrições; o dado (`relatos_de_campo.csv`, 3.000 relatos de jun/2026, sintético).
- [ ] **KIT-003 Hipótese Técnica**, com o **critério de aceite** (rascunho abaixo).
- [ ] **KIT-004 Matriz de Alternativas** (rascunho abaixo).
- [ ] **KIT-020 Acordo de squad**: é o 1º desafio da Etapa 2. Perguntar ao instrutor se vale o acordo da Etapa 1 ou se é preciso um novo.
- [ ] **Escolher a pessoa entregadora** do desafio: **[nome]**.
- [ ] **Cada um guarda o texto exato do critério**, porque ele vai para a etapa 1 do notebook, igual ao KIT-003.
- [ ] Anotar **data e hora da entrega do KIT-003 no Classroom**. O notebook pede (`ENTREGA_KIT003`).

**Pergunta para levar:** o critério tem métrica, recorte e valor?

#### 🟡 Rascunho do critério de aceite (KIT-003 = etapa 1 do notebook)
O notebook tem 5 campos: `CRITERIO_METRICA`, `CRITERIO_RECORTE`, `CRITERIO_VALOR`, `CRITERIO_JUSTIFICATIVA` e `ENTREGA_KIT003`.

| Campo | Proposta para discutir |
|---|---|
| **Métrica** | Tempo médio por relato (ms); tamanho do arquivo do modelo (MB); acurácia e F1 macro na classificação das 5 classes, com a perda em relação ao BERTimbau float32. |
| **Recorte** | Amostra de medição de 300 relatos do teste (divisão 80/20 estratificada, semente 42), classificados um por vez, em CPU com 2 threads, como no coletor. |
| **Valor** | Tempo < 1.000 ms por relato **e** tamanho ≤ 1.000 MB **e** perda de acurácia ≤ 2 p.p. **e** perda de F1 macro ≤ 2 p.p. em relação ao BERTimbau float32. |
| **Justificativa** | 1 s é o limite da situação. 1.000 MB é 1/8 da memória do coletor, que também roda sistema e aplicativo de coleta, e não pode ser consumido só pelo modelo. 2 p.p. ficam acima do ruído da amostra (1 relato = 0,33 p.p., então 2 p.p. ≈ 6 relatos) e abaixo de uma perda que mude o acionamento da especialidade. O F1 macro protege as classes pequenas, como `seguranca` (10,6%). |

Pontos para a squad decidir (e saber defender):
- **Por que 2 p.p. e não 1 ou 5?** Abaixo de ~1 p.p., a diferença é variação da amostra (aviso da etapa 9 do notebook).
- **A média de tempo basta?** O notebook mede a **média** por relato. Um p95 seria mais honesto para "a resposta precisa sair em < 1 s". Registrar como limitação, ou pedir ao instrutor para medir p95 também.
- **A memória medida é o arquivo, não a RAM em execução**, que inclui tokenizador, runtime e ativações. Por isso a folga de 1/8.
- **Recorte por classe:** com ~32 relatos de `seguranca` na amostra, cada erro vale ~3 p.p. de recall, o que é ruidoso demais para virar critério. Usar o F1 macro e **olhar** a classe na defesa.

#### 🟡 Rascunho da Matriz de Alternativas (KIT-004)

| Alternativa | Tamanho | Tempo em CPU | Qualidade | Custo / operação | Risco principal |
|---|---|---|---|---|---|
| **A. Comprar coletores com GPU (pedido da TI)** | não é problema | não é problema | igual à atual | **capex por coletor × frota**, troca de hardware, gestão de frota | gastar sem precisar, se B ou C atenderem |
| **B. Quantizar o BERTimbau (ONNX, int8 dinâmica)** | ~1/4 do float32 | menor que float32 (medir) | perda pequena esperada (medir) | só software; mesmo pipeline de treino | perda concentrada em classes pequenas |
| **C. Trocar por TF-IDF + regressão logística** | muito pequeno | muito rápido | depende do vocabulário (medir) | só software; retreino barato | não reconhece palavra fora do treino (abreviações e erros novos) |
| **D. Manter servidor e enviar quando houver conexão** | n/a | n/a | n/a | n/a | **descartada:** fere o requisito offline, porque a classe é necessária na hora |

Pelo M4 (Aula 2, seção 3), a comparação A × (B/C) é de **custo total de propriedade**, e não de preço de compra: aquisição, instalação, operação, atualização de modelo e substituição de unidades.

### Até 2 dias depois do E1 (entregadora)
- [ ] Entregar KIT-001, KIT-003, KIT-004 (+ KIT-020, se for o caso) no Classroom. Os outros não entregam.
- [ ] Salvar os PDFs entregues em `../Artefatos/`.

---

## Semana 2: testar e defender

### Até 4 dias antes do E2 (cada um)
- [ ] Rodar `01_estudo_memoria_e_precisao.ipynb` (qualquer ambiente) e responder às 4 perguntas do fim.
- [ ] Abrir `02_desafio_quantizar_ou_trocar.ipynb` **a partir do GitHub no Colab**, com **GPU T4**.
- [ ] Etapa 1: colar o critério **idêntico** ao KIT-003.
- [ ] Completar as **duas lacunas** (cada um precisa saber explicar, porque o apresentador é sorteado):
  - **Etapa 5, `medir_latencia(prever, textos)`:** para cada texto, chamar `prever(t)` **um por vez**, guardar as previsões, medir o total com `time.perf_counter()` e devolver `(previsoes, ms_total / len(textos))`. Não passar a lista inteira de uma vez, porque isso mediria lote, e o coletor classifica um relato por vez.
  - **Etapa 8, quantização:** uma linha com `quantize_dynamic(...)` saindo de `ARQ_FLOAT32` para `ARQ_INT8`, pesos em `QuantType.QInt8`. Ver a assinatura na página do ONNX Runtime e **apagar o `raise NotImplementedError`**.
- [ ] Rodar até o fim com **`ENVIAR = False`**.

**Pergunta para levar:** quanto o modelo atual ocupa e quanto tempo leva por relato em CPU?

### Até 2 dias antes do E2
- [ ] Cada um responde **sozinho** às 5 perguntas da conclusão.
- [ ] A squad compara as respostas e fecha **um texto por pergunta**, sempre citando o número da tabela da etapa 9.

**Pergunta para levar:** o que a quantização mudou em tamanho, tempo e acurácia?

### Véspera do E2 (só a entregadora)
- [ ] Numa **mesma sessão** do Colab: rodar tudo, colar as respostas fechadas, trocar para `ENVIAR = True` e rodar **só** a célula de envio.
- [ ] Conferir no GitHub: notebook com saídas, `mlflow.db` e `execucoes.csv` em `desafio-1-m4/`, commit "entrega de ... por <conta>".
- [ ] Atualizar o submódulo aqui (`git submodule update --remote`) e marcar o checklist do README da squad.

**Pergunta para levar:** a compra de coletores com GPU é necessária?

### No Encontro 2
- [ ] Defender o resultado **contra o critério**, número a número.
- [ ] **KIT-011 Matriz de Teste**: cada linha do critério, o valor medido, atendeu ou não, e de qual saída do notebook veio.
- [ ] **KIT-007 Decisão Justificada**: caminho escolhido, alternativas descartadas e o motivo, incertezas, e o **uso de IA com registro** (sugestão recebida, rejeitada e o motivo técnico).

**Pergunta para levar:** o critério foi atendido? O que a squad recomenda?

### Até 2 dias depois do E2 (entregadora)
- [ ] Entregar KIT-011 e KIT-007 no Classroom e salvar cópia em `../Artefatos/`.

---

## Problemas comuns
- **Conta, token ou acesso ao repositório:** falar com o instrutor da squad.
- **Cota de GPU do Colab é variável:** rodar no **início da semana** e desligar o ambiente ao terminar.
- Se trocar o tipo de ambiente no meio, o Colab reinicia e é preciso rodar tudo desde o início.
- Se a célula de envio disser que outra pessoa já enviou, não insistir: avisar o instrutor.
