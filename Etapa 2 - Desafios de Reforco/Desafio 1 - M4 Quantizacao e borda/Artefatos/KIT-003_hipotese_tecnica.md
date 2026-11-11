# Hipótese Técnica (KIT-003): Desafio 1 · M4 Quantização e borda

> Preenchido pela squad **no Encontro 1**. Uma hipótese = abordagem + condição + resultado esperado + critério de teste.
> **Este KIT traz o critério de aceite.** O texto da seção 4 vai **idêntico** para a etapa 1 do notebook 02 (`CRITERIO_METRICA`, `CRITERIO_RECORTE`, `CRITERIO_VALOR`, `CRITERIO_JUSTIFICATIVA`), e o instrutor compara os dois. Depois de fechado em sala, **ninguém muda uma vírgula**.
> Proposta baseada em `../Preparacao/00_PASSO_A_PASSO.md` e `../Preparacao/02_embasamento_pre_E1.md` (EMB-n). Nenhum modelo foi medido.

## Identificação

| Campo | Preenchimento |
|---|---|
| Squad / Polo | Squad 05 · UFC |
| Data | *(preencher: data do Encontro 1)* |
| Caso / Desafio | Desafio de reforço 1 · M4 Quantização e borda |
| Integrantes e papéis do dia (quem registra / quem apresenta) | *(preencher)* |
| Pessoa entregadora do desafio | *(preencher)* |

## 1. Hipóteses técnicas

| # | Abordagem | Condição | Resultado esperado | Critério de teste |
|---|---|---|---|---|
| **H0** (referência) | BERTimbau ajustado, float32, exportado para ONNX, em CPU | Coletor simulado: CPU com 2 threads, um relato por vez, amostra de 300 | Cabe em memória com folga (pesos ~436 MB, EMB-1). **Não sabemos** se responde em < 1 s | É a **linha de base** da perda de qualidade. Também testa se o pedido de GPU parte de uma premissa verdadeira |
| **H1** | Quantização **dinâmica int8** do mesmo modelo (ONNX Runtime, `quantize_dynamic`, pesos `QInt8`) | Mesmas condições de H0, sem novo treino | Arquivo ~4× menor que H0, tempo menor que H0, perda pequena de qualidade | Critério de aceite da seção 4 |
| **H2** | Troca por **TF-IDF + regressão logística** | Mesmas condições, treinado nos mesmos 2.400 relatos | Arquivo e tempo muito menores que H1. Qualidade **próxima** de H0 nesses textos curtos, mas com risco nas palavras desconhecidas (45/300 relatos, EMB-5) | Critério de aceite da seção 4 |
| **H3** (decisão) | Não comprar coletores com GPU | Se H1 **ou** H2 atender ao critério | A frota atual basta, e o custo fica só no software | H3 é aceita se ao menos um entre H1 e H2 atender a **todas** as linhas do critério |

## 2. Justificativa (por que estas hipóteses e não um palpite)

- **Memória não decide; tempo e qualidade decidem.** O `accelerate` mostra o BERTimbau com 415,5 MiB em float32 (~5,4% dos 8 GB) e 103,9 MiB em int8 (EMB-1). Logo, o pedido de GPU só se justifica se o **tempo** em CPU falhar ou se a perda de qualidade dos caminhos leves for grande demais.
- **H1 tem mecanismo de perda conhecido.** Na quantização linear, um peso extremo estica a escala e joga os demais em poucos níveis. No notebook de estudo, a matriz cai de 238 para 14 níveis e 31% dos pesos viram zero (EMB-2). A perda tende a aparecer nos relatos de fronteira, como os mistos.
- **H2 tem vantagem e risco nomeados.** É imune à caixa alta (põe tudo em minúsculas), que no BERT *cased* dobra o número de tokens e trunca 73 relatos (EMB-3). Mas ignora palavras que nunca viu no treino (1,3% das palavras da amostra; EMB-5).

## 3. Este é um problema de X e não de Y?

| Hipótese | Evidência que distingue |
|---|---|
| Problema de **implantação na borda** (compressão e runtime), e não de **escolha edge × cloud** | Os gatilhos de edge já estão dados pela situação: conectividade não assumível e latência como compromisso de produto (M4 Aula 2). A pergunta é qual compressão e qual runtime, e só depois o custo total |
| Problema de **tempo/qualidade**, e não de **memória** | 415,5 MiB contra 8 GB (EMB-1) |
| **Classificação** supervisionada de 5 classes, e não geração | Classe fechada, com rótulo no dado. Um modelo generativo (ex.: Qwen 1,5B) caberia em int4 (736 MiB), mas gera token a token em CPU, o que é incompatível com < 1 s **sem necessidade** (EMB-1) |
| Parte do erro pode ser **do dado**, e não **do modelo** | Rótulo ambíguo em relatos mistos (até ~5 na amostra; EMB-6) e truncamento (7 relatos da amostra; EMB-3). Liga ao M3: olhar os erros por recorte (mistos, caixa alta) na defesa |

## 4. Critério de aceite (texto que vai para a etapa 1 do notebook)

> 🟡 **Proposta para fechar em sala.** Depois de fechada, copiar exatamente para o notebook.

```python
CRITERIO_METRICA = 'Tempo medio por relato (ms), tamanho do arquivo do modelo (MB), acuracia e F1 macro nas 5 classes, com a perda de acuracia e a perda de F1 macro em relacao ao BERTimbau float32.'
CRITERIO_RECORTE = 'Amostra de medicao de 300 relatos do teste (divisao 80/20 estratificada, semente 42), classificados um por vez, em CPU com 2 threads, como no coletor.'
CRITERIO_VALOR = 'Aceito se, ao mesmo tempo: tempo medio < 1000 ms por relato; arquivo <= 1000 MB; perda de acuracia <= 2 p.p.; perda de F1 macro <= 2 p.p., ambas em relacao ao BERTimbau float32.'
CRITERIO_JUSTIFICATIVA = '1 s e o limite da situacao. 1000 MB e 1/8 dos 8 GB do coletor, que tambem roda sistema e app de coleta, e o arquivo nao inclui runtime nem ativacoes. 2 p.p. ficam acima do ruido da amostra (1 relato = 0,33 p.p.; cerca de 5 relatos da amostra tem rotulo ambiguo entre eletrica e seguranca) e abaixo de uma perda que mude o acionamento da especialidade. O F1 macro protege as classes pequenas, como seguranca (39 relatos na amostra), a mais cara de errar.'
ENTREGA_KIT003 = ''  # data e hora da entrega no Classroom, como aparecem la
```

> ⚠️ **No template entregue no Classroom, cole o texto do bloco acima, caractere por caractere**, e não o resumo abaixo. Se a squad preferir texto com acentos, ajuste **o bloco** e use a mesma versão nos dois lugares.

| Campo | Resumo para leitura (não é o texto oficial) |
|---|---|
| **Métrica** | Tempo médio por relato (ms); tamanho do arquivo do modelo (MB); acurácia e F1 macro nas 5 classes, com a perda de cada uma em relação ao BERTimbau float32. |
| **Recorte** | Amostra de medição de 300 relatos do teste (divisão 80/20 estratificada, semente 42), um relato por vez, CPU com 2 threads. |
| **Valor** | Todas ao mesmo tempo: tempo < 1.000 ms; arquivo ≤ 1.000 MB; perda de acurácia ≤ 2 p.p.; perda de F1 macro ≤ 2 p.p. |
| **Justificativa** | Ver o bloco acima. |

**Para a squad saber defender:**
- **Por que 2 p.p. e não 1 ou 5?** Com 1 p.p. (3 relatos), a diferença cabe na variação da amostra e nos ~5 relatos com rótulo "cara ou coroa" (EMB-6). Com 5 p.p. (15 relatos), seriam aceitos erros que mudam o acionamento.
- **Por que 1.000 MB, se o notebook usa 8.000 MB em `cabe_no_coletor`?** O notebook mede o arquivo, não a RAM em execução. A folga de 1/8 cobre runtime, tokenizador e ativações. **Atenção na semana 2:** `cabe_no_coletor = True` não significa "atendeu ao nosso critério".
- **A perda de F1 macro não sai pronta.** A etapa 9 só calcula `perda_de_acuracia`. A de F1 macro é `f1_macro(float32) − f1_macro(linha)`, calculada à mão na conclusão.
- **Por que a média de tempo e não o p95?** O notebook mede a média. Os relatos em caixa alta têm ~2× mais tokens (EMB-3) e formam uma cauda de tempo. O truncamento em 64 tokens limita o pior caso. Registrar como limitação.

## 5. Incertezas registradas (vão para o KIT-007 no E2)

1. **Rótulo dos relatos mistos:** sem regra de prioridade conhecida (pergunta ao instrutor). Isso afeta o teto de acurácia de todos os caminhos.
2. **Truncamento em 64 tokens:** 7 relatos da amostra (todos em caixa alta), 1 deles perde a pista de segurança. Afeta H0 e H1, mas não H2.
3. **Média × p95** da latência.
4. **Tamanho do arquivo × RAM em execução.**
5. **Colab ≠ coletor:** a CPU do Colab com 2 threads simula o coletor, mas não é o hardware real.

## Critério de pronto (autoverificação da squad)

- [ ] Cada hipótese tem abordagem + condição + critério de teste
- [ ] A distinção "problema de X e não de Y" está feita com evidência
- [ ] Justificativa registrada
- [ ] Critério com **métrica, recorte e valor**, e cada pessoa guardou o texto exato
- [ ] Data e hora da entrega anotadas para o `ENTREGA_KIT003`

## Devolutiva do instrutor (evidência → interpretação → próximo passo → prazo)

| Campo | Registro |
|---|---|
| Evidência observada | *(preenchido em sala)* |
| Interpretação técnica | *(preenchido em sala)* |
| Próximo passo | *(preenchido em sala)* |
| Prazo / momento de revisão | *(preenchido em sala)* |
