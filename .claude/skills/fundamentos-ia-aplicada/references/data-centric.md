# Base de Conhecimento — Módulo M3: Data-centric AI
### Curso Base de IA | Fundamentos de IA Aplicada | Prof. Arthur Nascimento (Industr.IA)

> Documento de extração de conhecimento denso, estruturado e fiel aos materiais originais do módulo, destinado a servir de fonte de verdade (skill de referência) para resolver e avaliar desafios sobre Data-centric AI. Terminologia preservada em português exatamente como no curso. Fontes, em `Data Centric IA/`: Aula 1 (e-book IA-024 "Data-centric AI: qualidade de dados, análise de erro e viés"), Aula 2 (guia de acesso ao notebook IA-025, "notebook de análise de erro estruturada por slices"), Aula 3 (e-book IA-026 "Data-centric AI: a decisão dados versus modelo, dados sintéticos e regime regulatório"), GLOSSÁRIO.pdf (GLO-M3), TEMPLATE T3.1 (IA-027, matriz de decisão dados versus modelo) e o notebook `IA_025.ipynb`.
>
> Numeração de seções usada pelo glossário oficial: 3.1 deslocamento data-centric, 3.2 vocabulário regulatório, 3.3 framework de data quality, 3.4 error analysis por slices, 3.5 análise de viés (Aula 1); 3.6 decisão dados x modelo, 3.7 dados reais x sintéticos, 3.8 regime regulatório do dataset (Aula 3).

---

## 0. Mapa do módulo e progressão lógica (resumo executivo)

O M3 é a **lente dos dados**. Por decisão estrutural do curso, **IA responsável (regulação e viés) é tratada dentro deste módulo**, porque é no ciclo de vida do dado que a maior parte das obrigações se materializa. O módulo avança em três camadas:

1. **Camada conceitual** (Aula 1, seções 1–2): o **deslocamento data-centric** (modelo fixo, iteração sobre os dados; os dados fixam o **teto de qualidade**) e o **vocabulário regulatório** (LGPD, GDPR, EU AI Act; base legal; data lineage).
2. **Camada aplicada** (Aula 1, seções 3–5 + notebook IA_025): três instrumentos operacionais. São eles o **framework de data quality em seis dimensões**, a **error analysis por slices em cinco passos** e a **taxonomia de vieses por ponto de entrada no pipeline** (Suresh e Guttag).
3. **Camada decisória** (Aula 3 + template T3.1): a **árvore de decisão dados versus modelo**, a decisão **dados reais versus sintéticos** (papel, proporção e verificação; validação sempre em dado real) e a identificação do **regime regulatório do dataset** com registro de **risco residual**.

Fio condutor (conclusão da Aula 1): **dados e processo, e não o modelo isolado, determinam tanto a qualidade quanto a conformidade de uma solução.** A análise por slice conecta as três práticas aplicadas: revela falhas de qualidade concentradas em recortes, expõe o viés de agregação e orienta a intervenção nos dados de forma mensurável.

Fio condutor (conclusão da Aula 3): **relação entre disponibilidade de dados, cronograma realista e risco residual admitido.** Reanotar um slice, verificar a fidelidade de um gerador ou documentar uma base legal são linhas de plano com custo e prazo. Escondê-las não as elimina, apenas as transfere para o pior momento do projeto.

Conexões declaradas com outros módulos: o **M0** define as métricas (acurácia, precisão, recall, matriz de confusão; GLO-M0). O **M1** fornece os modelos generativos usados para gerar dados sintéticos. O **M5** (transparência) retoma o Art. 22 do GDPR, o Art. 10 do EU AI Act pelo ângulo da explicabilidade e exige o lineage construído aqui. A **Fase 2** (Engenharia de Dados; Machine Learning e Deep Learning) aprofunda concept drift, lineage em escala, augmentation clássica e mitigação algorítmica de viés.

---

## 1. Aula 1 — E-book IA-024: "Data-centric AI: qualidade de dados, análise de erro e viés"

### 1.1 Estrutura (sumário oficial)
1. O deslocamento data-centric · 2. Vocabulário regulatório · 3. Um framework de data quality · 4. Error analysis estruturado por slices · 5. Análise estruturada de viés · 6. Conclusão

### 1.2 O deslocamento data-centric (camada conceitual, seção 3.1)

- **Abordagem centrada no modelo**: dados tratados como insumo fixo, congelado no início do projeto; melhorar = trocar arquitetura, ajustar hiperparâmetros, empilhar camadas, testar algoritmo mais recente. Foi por muito tempo "o reflexo automático de quem buscava ganho de desempenho".
- **Abordagem centrada em dados (data-centric)**: inverte a prioridade. Mantém-se um **modelo de referência (baseline model) fixo** e itera-se de forma sistemática sobre os dados: corrigir rótulos errados, padronizar a coleta, cobrir subgrupos mal representados, remover duplicatas e ambiguidades. Tese popularizada por **Andrew Ng**: "na maioria dos problemas aplicados, o caminho mais curto para um sistema melhor passa pelos dados, e não pela arquitetura".
- **Por quê**: "os dados determinam o **teto de qualidade** alcançável, e o modelo apenas decide quanto desse teto se alcança". Trocar floresta aleatória por rede profunda sobre o mesmo dado defeituoso rende "uma fração de ponto"; sanear o dado pode render vários. Em problemas tabulares e de visão industrial de PD&I, "esse desequilíbrio é a regra, e não a exceção".

#### Figura 1 — Ciclo data-centric (5 etapas, circular)
1. Definir tarefa, métrica e slices → 2. Estabelecer baseline de dados e rótulos → 3. Treinar modelo de referência (fixo) → 4. Error analysis por slices → 5. Melhorar os dados: rótulos e slices fracos → volta a 1.
Centro: "data-centric: o modelo fica fixo; a iteração recai sobre os dados". **Dentro do ciclo, o modelo serve de instrumento de diagnóstico do dado, e não de objeto de otimização.**

#### Quatro condições em que data-centric é mais vantajoso
1. **Poucos dados**: cada exemplo pesa muito; limpar ou enriquecer rende mais que aumentar capacidade.
2. **Ruído de rótulo alto**: o modelo aprende o ruído; nenhuma arquitetura corrige rótulos errados.
3. **Distribution shift** entre treino e produção: o ganho está em alinhar os dados de treino à realidade de uso.
4. **Cauda longa (long tail)**: muitos casos raros que, somados, pesam mais do que parecem; "são poucos exemplos bem escolhidos, e não mais camadas, que fecham a lacuna".

(Data-centric "não substitui a escolha de modelo em todos os casos".)

- **Exemplo aplicado**: fábrica de autopeças, classificador de defeitos por foto estaciona em **88% de recall** apesar de várias trocas de arquitetura. Metade dos defeitos não detectados ocorre sob **iluminação introduzida após a coleta original**. Algumas centenas de imagens nessa condição, sem trocar o modelo, elevam o recall mais que qualquer ajuste anterior.
- **Armadilha comum**: o **reflexo centrado no modelo**. Diante de resultado ruim, partir direto para arquitetura mais nova, gastando tempo e computação onde o retorno é menor, enquanto o gargalo (rótulos ruidosos, cobertura desigual) permanece intocado. "Antes de trocar o modelo, vale perguntar se o dado já está no seu melhor."
- **Glossário: Dataset drift (data drift)**: mudança, ao longo do tempo, na distribuição dos dados recebidos em produção em relação à de treino. Pode ser **gradual** (desgaste de equipamento que altera leituras de sensor) ou **abrupta** (troca de fornecedor, mudança de processo). Explica por que um modelo bom no lançamento degrada "ainda que nada no código mude". Quando muda a **relação entre entradas e saídas**, e não a distribuição das entradas, é **concept drift** (Fase 2).

### 1.3 Vocabulário regulatório (camada conceitual, seção 3.2)

Objetivo: reconhecer onde LGPD, GDPR e EU AI Act incidem no pipeline e nomear base legal e proveniência. Quase toda obrigação legal relevante recai sobre o ciclo de vida do dado: que dado pode ser coletado, com que finalidade, por quanto tempo, com que garantias e com qual rastreabilidade. **A LGPD é a referência que governa e é por ela que o trabalho começa.** GDPR e EU AI Act entram como referência internacional e "parâmetro técnico de governança mesmo a quem opera apenas em território nacional".

- **LGPD**: exige **base legal para cada tratamento** (consentimento, obrigação legal/regulatória, execução de contrato, legítimo interesse, entre outras), impõe os princípios de **finalidade, adequação e minimização** e dá tratamento reforçado a **dados pessoais sensíveis**.
- **GDPR**: papel equivalente; acrescenta, no **Artigo 22**, limites a decisões **inteiramente automatizadas** com efeito significativo sobre a pessoa (retomado no M5).
- **EU AI Act** (2024): organiza sistemas por nível de risco. Para **alto risco**, o **Artigo 10** exige que conjuntos de treino, validação e teste sejam **relevantes, suficientemente representativos e examinados quanto a erros e vieses**. Torna qualidade e representatividade de dados **obrigações legais**, não só boas práticas. No Brasil, o **PL 2338** caminha em direção semelhante e "deve ser acompanhado".

#### Quadro 1 — Onde cada instrumento incide no pipeline (reprodução integral)
| Instrumento | Foco principal | Ponto de incidência no pipeline |
|---|---|---|
| LGPD (Lei 13.709/2018) | dados pessoais, base legal e finalidade | coleta, armazenamento, retenção e compartilhamento |
| GDPR (Reg. 2016/679) | dados pessoais e decisão automatizada | coleta, transferência internacional e uso em decisão (Art. 22) |
| EU AI Act (Reg. 2024/1689) | qualidade e representatividade do dado | construção dos conjuntos de treino, validação e teste (Art. 10) |

- **Armadilhas comuns**: (1) supor que **anonimizar encerra as obrigações**. A reidentificação por atributos combinados é mais frequente do que se imagina, e **dado pseudonimizado continua sob a lei**. (2) **Coletar primeiro e pensar na base legal depois**: a finalidade precisa ser definida **antes** da coleta, não justificada retroativamente.
- **Glossário: Base legal de tratamento**: fundamento jurídico que autoriza tratar um dado pessoal. "Não basta ter o dado disponível; é preciso poder apontar a base legal que justifica usá-lo para a finalidade declarada."
- **Glossário: Data lineage**: registro rastreável da origem de cada dado e de todas as transformações até o conjunto de treino. Sustenta auditoria, reprodutibilidade e resposta a pedidos de titulares; é pré-requisito prático para demonstrar conformidade "quando um regulador pergunta de onde veio determinado dado".

### 1.4 Framework de data quality (camada aplicada, seção 3.3)

"A qualidade de um dataset não é uma impressão geral, e sim um conjunto de propriedades verificáveis, cada uma com um teste próprio". Isso transforma "uma queixa difusa de dado ruim em uma lista de problemas endereçáveis".

Pergunta de cada dimensão:
- **Completude**: há valor onde deveria haver valor?
- **Consistência**: os campos e registros concordam entre si, sem contradições?
- **Acurácia**: o valor registrado corresponde ao mundo real?
- **Atualidade**: o dado reflete o estado vigente relevante para a decisão?
- **Validade**: cada valor respeita o formato e o domínio esperados?
- **Unicidade**: não há duplicatas indevidas inflando a amostra?

#### Quadro 2 — Seis dimensões (reprodução integral)
| Dimensão | Teste objetivo | Falha típica |
|---|---|---|
| Completude | fração de campos preenchidos onde se espera valor | sensor sem leitura em parte dos registros |
| Consistência | ausência de contradição entre campos e fontes | data de reparo anterior à data de falha |
| Acurácia | correspondência com a medida real de referência | rótulo de defeito atribuído à peça errada |
| Atualidade | defasagem entre o dado e o estado atual | cadastro de equipamento desatualizado há meses |
| Validade | conformidade a formato, faixa e domínio | temperatura abaixo do zero absoluto |
| Unicidade | ausência de duplicatas não intencionais | mesmo evento registrado por dois sistemas |

**Atenção**: "acurácia" aqui é dimensão de qualidade **do dado**, não a métrica de classificação do M0.

**Aplicação a um registro de manutenção preditiva** (vibração, temperatura e corrente por motor + coluna de falha):
- completude = fração de leituras ausentes por sensor;
- consistência = nenhuma data de reparo precede a falha que a motivou;
- acurácia = conferir amostra de rótulos contra o registro de ordens de serviço;
- atualidade = cadastro de equipamentos acompanha as trocas recentes;
- validade = rejeitar temperaturas fora da faixa física plausível;
- unicidade = remover eventos contados duas vezes por integração entre sistemas.

"Cada dimensão vira uma verificação automatizável."

- **Exemplo aplicado**: distribuidora de energia, previsão de demanda com erro alto em dias específicos. Duas falhas combinadas: **registros duplicados de medidores reinstalados (unicidade)** e **leituras com fuso horário trocado em uma subestação (validade)**. Nenhuma exigia trocar o modelo; corrigidas, o erro nos dias problemáticos **caiu pela metade**.
- **Ferramentas (alto nível)**:
  - **Great Expectations**: declarar expectativas (faixas válidas, ausência de nulos, unicidade de chaves) e testá-las a cada ingestão, "como testes de unidade para dados";
  - **DVC** (próximo do fluxo de repositório de código) e **lakeFS** (escala de data lake sobre armazenamento de objetos): versionam dados e transformações, suporte a lineage e reprodutibilidade;
  - **Cleanlab**: estima estatisticamente quais rótulos têm maior probabilidade de estar errados (automatiza parte da auditoria de acurácia).

  A escolha entre elas fica para Engenharia de Dados (Fase 2).
- **Armadilha comum**: medir a qualidade **de forma agregada** e declarar o dado bom porque o número global é alto. A falha quase sempre se concentra num subconjunto (um sensor, uma linha, uma faixa de clientes) e "a média dilui o problema até ele desaparecer do relatório". Isso leva à análise por slices.

### 1.5 Error analysis estruturado por slices (camada aplicada, seção 3.4)

"Uma métrica global é uma média, e médias escondem onde o sistema falha." Um modelo com 92% de acurácia geral pode ter 99% num subgrupo e 70% em outro, e "é justamente o subgrupo fraco que costuma importar na operação".

- **Slice** (glossário): subconjunto definido por **critério interpretável** (faixa de valores, categoria, condição de coleta: faixa etária, região, tipo de equipamento, turno, iluminação). Diferente de uma partição aleatória, é escolhido por ter **significado de domínio**.

#### Procedimento em cinco passos (repetível)
1. **Definir os slices relevantes**, a partir do conhecimento do domínio e dos atributos disponíveis.
2. **Medir a métrica que importa** dentro de cada slice.
3. **Ordenar os slices pelo tamanho do gap** em relação ao global, **ponderando pelo número de exemplos**.
4. **Inspecionar manualmente uma amostra de erros dos slices piores**, para entender a causa.
5. **Decidir a intervenção**: coletar mais dados do slice, corrigir rótulos, criar um atributo que capture a distinção ou, em alguns casos, **aceitar o limite e documentá-lo**.

#### Quadro 3 — Leitura de desempenho por slice (reprodução integral)
| Slice | Exemplos (n) | Recall no slice | Gap vs. global |
|---|---|---|---|
| Global | 20.000 | 0,91 | referência |
| Equipamento tipo A | 12.400 | 0,95 | +0,04 |
| Equipamento tipo B | 5.900 | 0,88 | −0,03 |
| Equipamento tipo C | 1.700 | 0,67 | −0,24 |

Leitura oficial: o 0,91 global esconde um slice crítico. O **tipo C** (recall 0,67, gap 0,24) concentra a falha; "como tem 1.700 exemplos, o problema é **real e endereçável**". Intervenção sugerida: reunir e rotular mais casos do tipo C, **ou investigar se seus rótulos são menos confiáveis, antes de qualquer mudança no modelo**. (Pelos cinco passos, o próximo passo é o 4: inspecionar manualmente uma amostra dos erros do tipo C.)

- **Exemplo aplicado**: triagem de crédito com recall global adequado, mas muito inferior para uma faixa de renda sub-representada. A inspeção revelou **rótulos inconsistentes** herdados de processo manual antigo. Corrigir os rótulos do slice, sem trocar o modelo, reduziu a disparidade **e melhorou a métrica geral**.
- **Armadilha comum**: **otimizar a métrica média e piorar um slice crítico** sem perceber. A média recompensa o slice majoritário, e sem leitura por slice a regressão só aparece em produção.
- Transição: a análise por slice diz **onde** cai, não **por que**. Quando a queda se concentra em subgrupos ligados a características de pessoas ou condições de coleta, a causa costuma ser um viés que entrou em algum ponto do pipeline.

### 1.6 Análise estruturada de viés (camada aplicada, seção 3.5)

Tese: **o viés é propriedade dos dados e do processo, e não apenas do modelo**. "Dizer que um modelo é enviesado costuma estar incompleto": o viés entra nos dados e no processo em pontos identificáveis, e o modelo o reproduz e às vezes o amplifica. Tratá-lo como **taxonomia de origens**, não como defeito monolítico, permite detectar e mitigar com método.

#### Figura 2 — Taxonomia de vieses por ponto de entrada no pipeline (adaptada de Suresh e Guttag, 2021)
| Ponto do pipeline | Viés | Descrição |
|---|---|---|
| Dados do mundo | **Histórico** | o mundo já é desigual; os dados o refletem (fielmente, em dados corretos) |
| Coleta e amostragem | **De representação** | a amostra não cobre bem certos grupos |
| Medição e rotulagem | **De medição** | o atributo medido é um proxy imperfeito |
| Medição e rotulagem | **De anotação** | os rótulos carregam a subjetividade do anotador |
| Modelagem | **De agregação** | um só modelo para grupos heterogêneos |
| Avaliação | **De avaliação** | o benchmark não representa o uso real |
| Implantação | **De implantação** | o uso em produção difere do previsto |

#### Como detectar (a localização sugere o teste)
- **Representação**: comparar a distribuição dos grupos na amostra com a da população de uso (em linha com o Art. 10 do EU AI Act). Detectável **antes do treino**.
- **Agregação**: revela-se na **análise por slice**, quando um subgrupo tem desempenho sistematicamente pior.
- **Anotação**: auditar uma amostra de rótulos, **idealmente com mais de um anotador**.

"Cada tipo tem um teste, e **nenhum se resolve apenas trocando de modelo**."

- **Viés histórico** distingue-se dos demais por **não ser defeito de coleta ou de processo**, o que muda a natureza da mitigação possível (glossário).
- **Exemplo aplicado**: inspeção visual treinada com imagens de **uma única planta** cai ao ser implantada em outra (iluminação e câmeras diferentes). O dado sofria **viés de representação** (uma só condição de coleta) e o uso revelou **viés de implantação**. A correção foi nos dados, ampliando a amostra para as condições reais.
- **Armadilha comum**: acreditar que **remover a coluna de um atributo sensível elimina o viés**. Outros atributos funcionam como **proxy** (CEP correlacionado à renda) e o viés persiste por via indireta. "Tratar viés como bug a ser apagado de uma vez, em vez de propriedade a ser **medida e monitorada ao longo do tempo**, leva a uma falsa sensação de resolução."
- Documentação estruturada: Gebru et al. (Datasheets for Datasets), Mitchell et al. (Model Cards). A mitigação algorítmica cabe aos cursos de ML da Fase 2.

---

## 2. Aula 2 — Notebook IA_025: error analysis estruturada por slices

Link Colab (guia): https://colab.research.google.com/drive/1puoAZ6JnZGGHUvHv9vP4J5j28-hABl9v?usp=sharing. Cópia local: `Data Centric IA/IA_025.ipynb` (sem saídas gravadas).

**Objetivo**: transformar a evidência de uma análise por slices em decisão justificada entre intervenção data-centric e troca de modelo, alimentando o **T3.1**.

**Setup**:
- dataset **Adult Income** (Census Income, UCI), 32.561 registros do censo dos EUA de 1994; tarefa: prever renda anual > US$ 50 mil;
- é o "exemplo clássico de **disparidade de slice**";
- classificador de referência: **Random Forest**, com semente fixa e `get_dummies` nas categóricas.

### Seções
1. **Preparação**: pandas e scikit-learn, semente fixada para reprodutibilidade.
2. **Carga com verificação de disponibilidade**: testa a URL antes de tudo ("melhor descobrir agora, com uma mensagem clara, do que no meio da análise"). O arquivo não tem cabeçalho; as colunas são nomeadas em português.
3. **Passada de data quality antes do modelo**: **completude** (faltantes marcados com `?`) e **unicidade** (duplicatas). "Em um projeto real, cada achado viraria uma decisão documentada."
4. **Classificador de referência e visão agregada**:
   - `peso_amostral` fica de fora (artefato do desenho amostral, sem relação causal);
   - `renda` fica de fora (é o alvo);
   - `sexo`, `idade` e `escolaridade` são guardados junto ao teste **só para fatiar**, sem mudar o treino;
   - três métricas agregadas: "o número que costuma ir para o slide de resultados".
5. **Função `desempenho_por_slice`**: cinco números lidos **em conjunto** por slice:
   - **n_exemplos (suporte)**: com poucos exemplos, a métrica vira ruído estatístico;
   - **prop_positivos**: quando muda entre slices, a acurácia deixa de ser comparável;
   - **acurácia, recall e precisão** (métricas do M0, dentro do slice).
6. **Slice de sexo: quando a acurácia engana**:
   - `Female` tem a **maior acurácia** (> 0,90) e o **pior recall**: pouco mais da metade dos positivos, ~10 pontos abaixo de `Male` e do agregado;
   - explicação: `prop_positivos` é ~1 em 9 em `Female` contra ~1 em 3 em `Male`. Acertar a maioria negativa infla a acurácia;
   - **"Comparar acurácias entre slices com proporções de positivos diferentes é comparar réguas diferentes."** O gap relevante é o de **recall**.
7. **Matriz de confusão do slice**: no `Female`, **quase metade dos positivos reais vira falso negativo**; os verdadeiros negativos dominam e sustentam a acurácia. "O gap tem endereço e tem forma: é um problema de recall da classe positiva em um slice específico."
8. **Da evidência à intervenção** (tabela abaixo). No caso do notebook, a hipótese principal é **sub-representação da classe positiva dentro do slice** ("não do slice como um todo"), o que põe coleta ou rebalanceamento no topo. Antes de decidir, **auditar uma amostra de rótulos**, porque sub-representação e ruído podem coexistir.
   - ⚠️ "Remover a coluna `sexo` das features **não** remove a disparidade": ocupação, estado civil e horas por semana carregam a mesma informação. "A disparidade é uma propriedade dos dados, e é nos dados que ela se trata."
9. **Exercício (faixa etária)**:
   - Passo A: `pd.cut` com cortes `[16, 30, 45, 60, 100]` e rótulos `"17 a 30"`, `"31 a 45"`, `"46 a 60"`, `"61 ou mais"`, depois `.astype(str)`;
   - Passo B: tabela por faixa;
   - Passo C: `slice_critico` = faixa de **menor recall** com suporte ≥ 500.
10. **Como ler uma error analysis** (três hábitos):
    - "a visão agregada **abre** a análise, nunca a encerra";
    - cada linha é lida em conjunto: "métrica sem suporte é ruído, e acurácia sem proporção de positivos é régua torta";
    - a análise termina em **hipótese de causa com intervenção associada**, registrada para ser cobrada. A decisão é iterativa.

    Em produção, a análise roda **a cada retreino e a cada janela de monitoramento**.
11. **Perguntas para reflexão** (sem resposta no notebook):
    1. Que única métrica do slice `Female` reportar a um stakeholder não técnico, e como explicar em uma frase?
    2. Em qual folha da árvore M3.fig-3 se chega, e qual gatilho registrar para reavaliar a troca de modelo?
    3. A faixa `61 ou mais` tem o menor suporte. O que isso muda na confiança, e o que fazer antes de intervir?
12. **Solução**:
    - a faixa **`17 a 30`** repete o padrão de forma mais acentuada: maior acurácia e **recall na casa de 0,40**, com prop_positivos < 0,10;
    - todas as faixas têm suporte > 500. A `61 ou mais`, com pouco mais de 500, pede mais cautela;
    - proposta-modelo: "slice crítico 17 a 30, recall ~0,40 contra 0,62 no agregado; prop_positivos < 0,10 e poucos positivos apontam sub-representação da classe positiva dentro da faixa; coletar ou rebalancear positivos dessa faixa, auditando antes uma amostra de rótulos; confirmação por nova error analysis com recall da faixa > 0,55 sem perda relevante nas demais";
    - **erros comuns**: esquecer `.astype(str)`; passar `idade` crua (dezenas de slices minúsculos); escolher a faixa de **menor acurácia** em vez de menor recall ("exatamente a leitura enganosa que este notebook procura desfazer").

#### Tabela "da evidência à intervenção" (reprodução integral, seção 8)
| Padrão observado no slice | Causa provável | Intervenção data-centric |
|---|---|---|
| Poucos exemplos da classe que falha | sub-representação | coletar ou rebalancear exemplos do slice |
| Exemplos existem, mas rótulos inconsistentes numa amostra auditada | ruído de rótulo | reanotar com critério unificado |
| O slice mudou de comportamento depois da coleta | drift | recoletar e retreinar |

---

## 3. Aula 3 — E-book IA-026: "a decisão dados versus modelo, dados sintéticos e regime regulatório"

### 3.1 Estrutura (sumário oficial)
1. Decidir entre intervenção nos dados e troca de modelo · 2. Dados reais versus dados sintéticos · 3. O regime regulatório aplicável ao dataset · 4. Conclusão

### 3.2 Decisão dados versus modelo (camada decisória, seção 3.6)

Pergunta organizadora: "quando o desempenho de uma solução estagna abaixo do necessário, o gargalo está nos dados ou no modelo, e o que a evidência disponível autoriza a concluir?"

- **Entrada obrigatória**: uma **error analysis por slices concluída**. Sem ela, a escolha é feita "por intuição, moda ou familiaridade da equipe", e nenhum desses critérios sobrevive à pergunta de um stakeholder.
- **O reflexo model-centric não é irracional**: trocar de modelo está inteiramente sob controle da equipe técnica, enquanto melhorar dados envolve anotadores, acesso a fontes e negociação com outras áreas. Mas "**conforto operacional não é evidência**". Em datasets pequenos, ruidosos ou desbalanceados, corrigir dados supera com frequência trocar a arquitetura.
- **ATENÇÃO (confusão frequente)**: responder a erro concentrado em um slice com troca de arquitetura. Se a causa está nos dados do recorte, "o novo modelo herda exatamente o mesmo teto". O resultado são semanas de reengenharia por ganho marginal.
- **Glossário: Erro irredutível**: parcela do erro que nenhum modelo elimina (ambiguidade ou ruído intrínsecos). Perto desse piso, trocar de modelo não traz ganho; a margem só se move com dados melhores ou reformulação do problema.

#### Leitura da evidência
1. **Erro concentrado × difuso**:
   - concentrado em poucos slices com gaps grandes → hipótese mais econômica: **dados daqueles recortes**. "Um modelo que acerta 91% no conjunto, mas 60% em um slice específico, não é um modelo fraco: é um modelo treinado sobre uma representação fraca daquele recorte";
   - difuso, sem concentração explicável → a hipótese de limitação do modelo **ganha força, embora ainda não seja a única**.
2. **Qual propriedade dos dados explica o gap**:
   - **sub-representação** → coletar mais;
   - **ruído de rótulo** → reanotar;
   - **drift** (a fonte mudou depois da coleta) → recoletar.

   Todas são intervenções **em dados**. Se nenhuma se sustenta e o slice falha com dados adequados, a troca de modelo volta à mesa.
3. **Quando trocar o modelo é a resposta certa** (três sinais combinados):
   - (i) o dataset atende o **framework de data quality nas seis dimensões**;
   - (ii) o erro é **difuso e estável** entre slices;
   - (iii) há **referência externa ou piloto interno** indicando que outra família captura padrões que a atual não captura (ex.: interações não lineares que um modelo linear não representa).

   "Na ausência dos três sinais, a troca é aposta; na presença deles, é decisão fundamentada", acompanhada de plano de retreino e revalidação.

#### Custos assimétricos e transferibilidade
- **Intervenção em dados**: coleta ou reanotação, reprocessamento do pipeline, novo treino do modelo atual. **Custo dominado por gente e acesso**, costuma ser subestimado.
- **Troca de modelo**: seleção e treino do candidato, revalidação completa, integração e, em setor regulado, novo ciclo de **homologação**. **Custo dominado por engenharia e prazo**.
- **Transferibilidade**: dados corrigidos servem a qualquer arquitetura futura. O ganho de uma troca não corrige defeito de dados e pode ser perdido na próxima troca. **Em empate, é desempate legítimo a favor dos dados.**

#### Ganho esperado (projetado, não presumido)
- **Dados**: teto do ganho agregado = **gap do slice × peso do slice no volume**. Ex.: 30 pontos de gap × 10% do volume = **no máximo 3 pontos** no agregado.
- **Modelo**: exige **piloto ou referência comparável sobre os mesmos dados e a mesma métrica**. "Um número de benchmark obtido sobre outra distribuição não projeta nada."
- Comparação honesta: mesma métrica, mesmo conjunto de teste, mesma janela de tempo.

#### Prazo (costuma decidir empates)
- dados → prazo dominado pela **logística de anotação e coleta**;
- modelo → prazo dominado pela **cauda de revalidação e integração** (e homologação).

Dimensionar pelo **pior caso plausível**, não pela média otimista. Na Formação 1, a alternativa escolhida entra no plano do squad como **compromisso datado**, com custo e ganho projetado registrados, "e é contra esse registro que o resultado será cobrado".

#### Figura 1 — Árvore de decisão dados versus modelo (M3.fig-3)
```
Error analysis por slices concluída (gaps medidos por slice)
└─ Os erros se concentram em slices identificáveis?
   ├─ SIM → A causa no slice está nos dados? (sub-representação, ruído de rótulo, drift na fonte)
   │        ├─ SIM → INTERVENÇÃO DATA-CENTRIC NO SLICE (coletar, reanotar ou rebalancear; retreinar o modelo atual)
   │        └─ NÃO → (vai para a pergunta de data quality)
   └─ NÃO → O dataset atende o framework de data quality? (as seis dimensões)
            ├─ NÃO → INTERVENÇÃO DATA-CENTRIC GLOBAL (limpeza e reanotação orientadas pelo framework, antes de mudar a arquitetura)
            └─ SIM → TROCA DE MODELO (retreinamento e revalidação)
Faixa comum a todos os ramos: registrar no T3.1 com justificativa por eixo e reavaliar com nova error analysis — a decisão é iterativa, não definitiva.
```
Dois traços:
- (1) a **ordem das perguntas**: hipótese de dados antes da de modelo; a troca só aparece depois de verificado o framework. A ordem traduz a assimetria de custos e a transferibilidade, "não é preferência estética";
- (2) a faixa final comum: "cada intervenção muda a evidência sobre a qual a próxima decisão será tomada".

#### Intervenção combinada (caminho do meio)
Corrigir **os dados primeiro** e definir **desde já um gatilho explícito** para reavaliar a troca. Gatilho típico: "se, após a reanotação do slice e o retreino, o erro residual se mostrar difuso e o dataset atender o framework de qualidade, a troca entra em avaliação com piloto dedicado". Preserva a ordem econômica "sem transformar a preferência por dados em dogma".

**O que NÃO autoriza: executar as duas intervenções ao mesmo tempo.** Mudar dados e modelo simultaneamente destrói a capacidade de **atribuir** o ganho a uma causa, "e sem atribuição não há aprendizado para a próxima decisão".

- **Exemplo aplicado**: metalúrgica, classificador de **defeitos de solda** por imagem, acurácia estagnada em **88%**, equipe cogitando arquitetura maior. O erro se concentrava em **uma única classe**, com **rótulos inconsistentes entre dois turnos de anotação**. A reanotação de ~**3 mil imagens** dessa classe com critério unificado elevou a acurácia acima da meta **sem trocar o modelo**, por uma fração do custo da migração.
- Premissa implícita de toda a seção: **existe caminho viável para melhorar os dados reais**. Quando o evento é raro, a coleta é cara ou os dados envolvem pessoas, a alternativa é gerar dados (próxima seção).

### 3.3 Dados reais versus dados sintéticos (camada decisória, seção 3.7)

A decisão "não é sintético sim ou não em abstrato, e sim **para qual papel, em qual proporção e com qual verificação**".

#### Três motivações legítimas
1. **Escassez de casos raros**: falhas graves, defeitos de baixa incidência, eventos de segurança.
2. **Custo de coleta e anotação**: ensaio destrutivo, parada de linha, horas de especialista.
3. **Restrição de privacidade**: dados de pessoas.

"Fora dessas três motivações, a proposta de usar dados sintéticos merece **desconfiança inicial**, porque costuma esconder a tentativa de evitar um trabalho de coleta que era viável."

#### Dois caminhos de geração
- **Simulação**: modelo físico ou regras do domínio, com controle total dos parâmetros (ex.: simulador de processo gerando curvas de sensor para regimes de falha nunca observados). **Limitada pela fidelidade do modelo de domínio.**
- **Geração por modelo**: modelo generativo (família do M1) aprende a estrutura dos dados reais e amostra novos. **Limitada pela qualidade e pela cobertura dos dados reais que a alimentaram.**

#### Dois riscos característicos
1. **Perda de fidelidade**: a aproximação falha "justamente onde o dado é mais valioso: nas caudas, nos casos limítrofes, nas correlações finas". Exemplos: linhas tabulares individualmente plausíveis com correlações conjuntas inexistentes; imagens de defeito convincentes sem a textura do defeito real. O modelo "aprende a resolver um problema vizinho do problema real".
2. **Auto-reforço** (glossário): ciclo em que um modelo é treinado, em proporção crescente, sobre dados produzidos por modelos, próprios ou de terceiros. A cada rodada, reforça padrões e vieses do gerador e **apaga a variabilidade das caudas** → **colapso de modelo** (Shumailov et al., *Nature* 631, 2024).
   - Instala-se **silenciosamente**: conteúdo gerado se acumula nas fontes de coleta.
   - É **cumulativo e de difícil reversão**.
   - Regra de higiene: **registrar no lineage a origem de cada exemplo (real ou sintético) e a versão do gerador**, para que a proporção sintética seja conhecida e controlável.

#### Regra sem exceção
**"A validação final acontece sempre sobre dados reais."** Sintético pode entrar no treino, na exploração e no balanceamento; **não pode entrar no conjunto de teste**, porque "um teste sintético mede o acordo entre dois artefatos, o modelo e o gerador, e não o desempenho no mundo". A **proporção sintética do treino** deve ser **parâmetro explícito do experimento**, variada e observada contra métrica em dado real, não fixada por conveniência.

#### Verificação de fidelidade (três degraus)
1. **Estatístico**: comparar marginais de cada variável e correlações entre pares (sintético × amostra real), marcando divergências acima de um limiar acordado.
2. **Olhar de especialista**: quem conhece o processo procura "o que não existiria na linha". Vale mais nos casos raros.
3. **Teste por consequência**: treinar o mesmo modelo **com e sem** a parcela sintética e medir a diferença **sobre dados reais**, "o único juiz que interessa".

Nenhum exige ferramenta especializada; **a ausência dos três num plano que propõe sintéticos é, por si, sinal de alerta.**

#### Dois papéis
- **Complemento (augmentation, no sentido de ampliação do treino)**: a base real é a espinha; o gerado preenche regiões específicas (tipicamente classes raras) em proporção controlada. É o **caso comum e de menor risco**. A augmentation clássica por transformação de exemplos reais é técnica vizinha (Fase 2).
- **Substituto**: o sintético ocupa o lugar do real (porque o real não pode circular ou não existe em volume). É o **caso excepcional e de maior exigência**: a verificação de fidelidade "vira o centro do projeto", com comparações documentadas antes de qualquer treino.

#### Privacidade: o trade-off que a intuição erra
Quanto mais fiel o gerador, mais útil, e **maior o risco** de exemplos próximos demais de registros reais, permitindo inferências sobre indivíduos. "Fidelidade e proteção puxam em direções opostas." Consequências:
- (1) **sintetizar não é sinônimo de anonimizar**; a afirmação de que o sintético não expõe titulares precisa de verificação, "não de fé no método";
- (2) essa verificação pertence ao **regime regulatório do dataset de origem**.

#### Heurística em três perguntas
1. O dado real é obtenível a custo e prazo compatíveis? **Se sim, prefira o real**; a proposta sintética é **otimização prematura**.
2. A parcela sintética cobrirá regiões que o real não cobre (classes raras controladas por física conhecida, cenários de privacidade)? Se sim, uso defensável **no papel de complemento**.
3. Existe **conjunto real, protegido e rastreável, reservado para a validação**? **Se não, o uso sintético é indefensável em qualquer proporção.**

#### Quadro 1 — Dados reais versus sintéticos (reprodução integral)
| Critério | Dados reais | Dados sintéticos |
|---|---|---|
| Fidelidade à distribuição | referência por definição, incluindo caudas e correlações finas | aproximação; degrada nas caudas e nos casos limítrofes |
| Custo e prazo de obtenção | dominados por coleta e anotação; podem ser proibitivos em eventos raros | dominados por construção e verificação do gerador; escala barata depois |
| Cobertura de casos raros | limitada pela frequência natural do evento | controlável por parâmetro, quando a física ou as regras do caso são conhecidas |
| Privacidade | sujeitos ao regime do tópico 3 quando envolvem pessoas | reduzem exposição de titulares, sem eliminar por si o dever de verificação |
| Risco característico | viés e ruído herdados do processo de coleta | perda de fidelidade e auto-reforço, com rastreio obrigatório no lineage |
| Papel na validação | único aceitável para o teste final | inaceitável no teste final, em qualquer proporção |

- **Exemplo aplicado**: fabricante de vidros planos, detector de **inclusões** (< 1 em mil painéis). Dois anos renderam **400 exemplos reais**. A equipe gerou **6 mil imagens sintéticas por simulação óptica**, usou a mistura **só no treino**, com origem no lineage, e validou em conjunto **exclusivamente real**. Recall da classe rara **de 61% para 83%** medido em dado real, "o único número reportado ao cliente".
- **Sotaque por eixo**:
  - Visão Computacional → imagem simulada ou aumentada; risco dominante = **fidelidade de textura**;
  - LLMs e NLP → texto gerado para corpus de fine-tuning ou RAG; risco dominante = **auto-reforço** (gerador e consumidor da mesma família);
  - Engenharia de Dados e ML tabular → linhas para balanceamento ou compartilhamento; risco dominante = **correlação espúria entre colunas**.
- **Cronograma**: o sintético "parece um atalho", mas **desloca esforço em vez de eliminá-lo**, introduzindo duas etapas (construir ou adaptar o gerador; verificar fidelidade contra o real), e a segunda não pode ser cortada. Num plano honesto, a linha "dados sintéticos" aparece com essas duas etapas e com o **conjunto real de validação como dependência de caminho crítico**, "e não como uma caixa única que promete dados prontos em uma semana".
- Com dados de pessoas, a escolha real, sintético ou mistura muda obrigações jurídicas e bases legais. "Decidir a origem dos dados sem identificar o regime regulatório aplicável é decidir com informação incompleta."

### 3.4 O regime regulatório aplicável ao dataset (camada decisória, seção 3.8)

A pergunta muda de "o que cada norma diz" para "**qual norma incide sobre este dataset e o que isso muda no desenho da solução**". O regime **não é filtro final**, é **propriedade do dataset** que condiciona decisões anteriores: se a fonte pode ser usada, se precisa anonimizar, se sintético reduz exposição, se a coleta exige consentimento. Descobrir tarde = retrabalho de pipeline, renegociação de acesso, descarte de semanas de trabalho.

- **LGPD (âncora brasileira, primeiro a verificar)**: incide sempre que há **pessoa natural identificada ou identificável**. Datasets industriais contêm dados pessoais com mais frequência do que se supõe:
  - matrícula do operador no registro de turno;
  - voz em áudio de inspeção;
  - rosto ao fundo de imagem de linha;
  - padrão de digitação em log de sistema.

  Toda base escolhida deve estar **registrada e defensável**. **Dados sensíveis** (saúde, biometria) têm rol próprio no **artigo 11**, com exigência mais estrita (wearables, ergonomia, controle de acesso).
- **ATENÇÃO, erro recorrente**: tratar **pseudonimização como anonimização**. Trocar o nome do operador por código remove o identificador direto, mas o dado continua pessoal se a reidentificação for razoavelmente possível cruzando turno, função e setor. A equipe "opera sem base legal sem saber", e descobre em auditoria ou incidente, com custo máximo.
- **Escolha da base legal como decisão de projeto**:
  - **Consentimento** em dados de colaboradores é **frágil**: a assimetria da relação de emprego compromete a liberdade e há risco de revogação a qualquer tempo.
  - **Legítimo interesse**, frequente para dados operacionais, "**não é um carimbo**": exige registro de **teste de balanceamento** (interesse da organização × direitos do titular) com minimização documentada.
  - A decisão envolve o **jurídico ou o encarregado de dados desde o desenho**. O papel da equipe técnica é chegar "com o mapa do dataset pronto, não descobrir o problema depois do treino".
- **Anonimização** como saída técnica tem custo: anonimizar de verdade "quase sempre implica perder utilidade" (agregar em janelas, suprimir ou generalizar colunas, adicionar ruído), removendo o detalhe que o modelo exploraria. O ponto de equilíbrio proteção × utilidade precisa ser **escolhido e registrado**. Erro a evitar: o **meio do caminho**, um dataset pseudonimizado tratado como anônimo, que carrega o risco jurídico integral "com a falsa sensação de tê-lo eliminado".
- **GDPR**: incide quando o tratamento alcança **titulares na UE** ou ocorre no **contexto de estabelecimento europeu** (multinacionais, clientes ou plantas na Europa). Regra prática: pipeline que cumpre a LGPD com rigor "fica perto" do GDPR, **mas a equivalência não é automática**. **Transferências internacionais** têm capítulo próprio nos dois instrumentos e pedem análise específica quando treino ou inferência ocorrem fora do país de origem.
- **EU AI Act**: "pertence a outra família": regula **o sistema de IA, não o dado pessoal**, segundo o risco da aplicação. Alto risco (infraestrutura crítica, emprego, crédito) → **Art. 10**: práticas documentadas de gestão, dados relevantes e suficientemente representativos, exame explícito de vieses que afetem saúde, segurança ou direitos fundamentais. Essas exigências "correspondem, em essência, ao framework de data quality e à análise de viés, convertidos em obrigação jurídica", com disposições de alto risco entrando em aplicação **ao longo de 2026**. "Para equipes que pretendem atuar com clientes europeus, a lente dos dados deste módulo é também preparação regulatória."

#### Quadro 2 — Instrumentos pelo ângulo do dataset (reprodução integral)
| Instrumento | Quando incide sobre o dataset | O que exige do projeto na prática |
|---|---|---|
| LGPD (Lei 13.709/2018) | sempre que o dataset contém dados de pessoa natural identificada ou identificável tratados no Brasil ou sobre titulares no Brasil | base legal registrada por tratamento, regras mais estritas para dados sensíveis, direitos de titular atendíveis e lineage que demonstre origem e uso |
| GDPR (Regulamento 2016/679) | tratamento de dados de titulares na União Europeia ou no contexto de estabelecimento europeu da organização | bases legais e documentação análogas às da LGPD, com análise específica para transferências internacionais de dados |
| EU AI Act (Regulamento 2024/1689) | quando o sistema de IA alimentado pelo dataset se enquadra como de alto risco no mercado europeu | governança documentada dos dados de treino, validação e teste, representatividade adequada ao propósito e exame explícito de vieses (artigo 10) |

#### Identificação do regime em três passos (no início do projeto)
1. **Mapear conteúdo e alcance do dataset**: há pessoas identificáveis, diretas ou indiretas? Onde estão os titulares e a operação?
2. **Marcar os instrumentos incidentes**: LGPD pelo conteúdo pessoal, GDPR pelo alcance europeu, EU AI Act pelo enquadramento de risco da aplicação.
3. **Registrar as consequências**: base legal de cada tratamento, lacunas de documentação e ações de adequação, **cada uma com dono e prazo**.

**Pré-requisito técnico dos três passos: o data lineage.** Sem saber de onde cada campo veio, não há como demonstrar base legal nem responder a titular.

- **Onde documentar**: junto ao próprio dataset, no espírito das **datasheets for datasets**: de onde vieram os dados, quem são os titulares, qual base legal sustenta cada uso, que transformações foram aplicadas e que limitações são conhecidas. Nos squads, esse registro "é o **insumo direto do Mapa Técnico do Problema**" e permite a um integrante novo ou avaliador reconstruir as decisões "sem arqueologia de mensagens". **Regra de ouro**: "a resposta à pergunta *podemos usar estes dados para isto* deve estar escrita **antes** de a pergunta ser feita".
- **Paisagem em movimento**: o marco brasileiro de IA tramita com abordagem baseada em risco (M5 retoma). A prática é registrar, junto ao mapa regulatório, a **data da análise e os instrumentos considerados**, e tratar sua revisão como **atividade recorrente do ciclo**. "Projetos com dados bem governados, lineage completo e vieses examinados atravessam mudanças regulatórias com ajustes; projetos sem essa base recomeçam."
- **Regime × cronograma × risco**:
  - identificado **cedo**, a adequação (anonimização, consentimento, documentação de legítimo interesse) corre **em paralelo** ao desenvolvimento;
  - identificado **tarde**, cada ação vira **bloqueio de caminho crítico**.

  Como nenhum projeto elimina todo risco, a saída honesta é registrar o **risco residual admitido**.
- **Glossário: Risco residual**: risco que permanece depois das mitigações planejadas e que o projeto decide **aceitar de forma explícita e documentada**. Na lente dos dados, é a lacuna de qualidade, viés ou adequação regulatória que não será fechada no ciclo atual, registrada **com justificativa e com o gatilho que forçará sua revisão**. É o que diferencia "uma equipe que decidiu conviver com um risco conhecido de uma equipe que simplesmente não olhou".

### 3.5 Conclusão da Aula 3
Três blocos encadeados:
- a árvore dados × modelo (dados antes de modelo; troca só com framework verificado; registro e reavaliação a cada iteração);
- real × sintético como decisão de papel e proporção (três motivações, dois riscos, validação sempre em dado real);
- regime regulatório como procedimento (mapear, marcar, registrar bases legais, lacunas e risco residual).

O participante deve conseguir "olhar para um plano de projeto e apontar onde essas linhas estão faltando". O **quiz do módulo** retoma os três blocos "em cenários curtos orientados a decisão: menos definição, mais escolha justificada".

---

## 4. Template T3.1 (IA-027) — Matriz de decisão dados versus modelo

**Como usar**: a face 1 é o instrumento a preencher, a face 2 instrui cada eixo e há um exemplo preenchido ao final. Os cinco eixos são lidos em conjunto. **A evidência de error analysis é o eixo de entrada: sem ela preenchida, os demais não têm base** ("não preencha o restante da matriz").

### Face 1 — Instrumento (estrutura integral)
| Eixo de decisão | Intervenção nos dados | Troca de modelo | Justificativa (1 a 3 frases) |
|---|---|---|---|
| **Evidência de error analysis.** O que a análise por slices mostra? | Os erros se concentram em slices identificáveis? Nomeie os slices e os gaps medidos. | O erro é difuso e estável entre slices, com o dataset atendendo o framework de qualidade? Descreva o padrão. | Qual alternativa a evidência favorece, citando os números da análise. |
| **Custo da intervenção em dados.** O que custaria coletar, limpar ou reanotar? | Estime esforço, recursos e dependências: anotadores, acesso à fonte, reprocessamento. | A troca evitaria esse custo, ou o problema de dados persistiria sob o novo modelo? | O custo estimado cabe no orçamento e no cronograma do ciclo? Justifique. |
| **Custo da troca de modelo.** O que custaria substituir o modelo atual? | A intervenção preserva o pipeline atual? Registre o que permanece válido. | Estime seleção, retreino, revalidação completa e integração com o sistema existente. | O custo total da troca é menor que o da intervenção? Compare com evidência. |
| **Ganho esperado.** Quanto cada alternativa promete melhorar, e com que confiança? | Projete o ganho agregado a partir do gap e do peso de cada slice corrigido. | Projete o ganho da troca com piloto ou referência medida sobre os mesmos dados. | Compare os ganhos na mesma métrica e no mesmo conjunto de teste; diga qual é maior e mais confiável. |
| **Prazo.** Em quanto tempo cada alternativa entrega efeito mensurável? | Some coleta ou reanotação, reprocessamento e retreino do modelo atual, no pior caso. | Some seleção, retreino, revalidação, integração e eventual homologação, no pior caso. | Qual alternativa cabe nos marcos do projeto? Justifique. |

**Síntese decisória** (marcar uma, justificar em 1–3 frases, nomeando o caso e mostrando coerência com os cinco eixos):
- [ ] **Intervenção data-centric**: a evidência aponta gargalo nos dados e o custo cabe no cronograma.
- [ ] **Troca de modelo**: os dados atendem o framework de qualidade e o teto é do modelo.
- [ ] **Intervenção combinada**: dados primeiro, com gatilho explícito para reavaliar a troca de modelo.

### Face 2 — Instruções por eixo
- **Evidência**: abrir a tabela por slice do notebook e perguntar "**o erro tem endereço?**". Poucos slices com gaps grandes e causa de dados plausível → favorece intervenção. Erro difuso com as seis dimensões atendidas → abre caminho para a troca.
- **Custo dados**: dominado por gente e acesso; anotação industrial costuma ser subestimada. Estimar "em horas de especialista e semanas de calendário, não em impressões".
- **Custo modelo**: trocar não é só treinar outro; inclui seleção, retreino, revalidação, integração e homologação. Registrar também **o que a troca não resolve** (defeito de dados persiste sob qualquer arquitetura).
- **Ganho**: projeção, não presunção. Dados = gap × peso do slice. Modelo = só número medido sobre os mesmos dados e métrica; benchmark externo "não projeta nada".
- **Prazo**: tempo até efeito mensurável, no pior caso plausível, confrontado com os marcos. "Um ganho que chega depois do marco não decide nada."
- **Justificativa adequada**: cita **evidência concreta do cenário** (qual slice, qual gap, quanto custa a reanotação, qual marco elimina uma alternativa), não preferência geral.
- **Lembrete de ordem**: em empate, **comece pelos dados** (transferibilidade). **Não execute as duas intervenções ao mesmo tempo.** Na combinada, registre o gatilho.

### Exemplo preenchido (oficial)
**Cenário**: fabricante de motores elétricos, classificador tabular (gradient boosting) de **defeitos de bobinagem** a partir de testes de fim de linha. Acurácia agregada **90%**; recall de **58% na linha 3** (sensor mais antigo, **12% do volume**) contra 91% nas demais. A dúvida é corrigir os dados da linha 3 ou trocar por rede neural.

| Eixo | Intervenção nos dados | Troca de modelo | Justificativa |
|---|---|---|---|
| Evidência | Erro concentrado na linha 3: recall 58% contra 91% nas demais. | Fora da linha 3, erro baixo e estável; nada sugere teto do modelo. | Concentração favorece dados; gap de **33 pontos** é a evidência central. |
| Custo dados | Recalibrar o sensor da linha 3 e reanotar ~**2.500 registros**: **3 semanas, 2 anotadores**. | A troca não corrigiria a leitura ruidosa do sensor; o novo modelo herdaria o ruído. | Custo conhecido, localizado no slice, cabe no orçamento do trimestre. |
| Custo modelo | Pipeline atual permanece; só o slice é reprocessado e o modelo retreinado. | Selecionar, treinar, revalidar e reintegrar a rede: **6 a 8 semanas**, com nova homologação. | A troca custa mais que o dobro e não ataca a causa. |
| Ganho | Fechar o gap projeta ~**4 pontos** de recall agregado (peso de 12%). | Piloto interno sobre os mesmos dados ruidosos: **+1 ponto** de acurácia agregada. | Ganho da intervenção é maior e explicável pela causa; o da troca é marginal e sem diagnóstico. |
| Prazo | Efeito mensurável em ~**4 semanas** (reanotação + retreino). | **8 semanas ou mais** (revalidação + homologação). | Marco de revisão do squad em **6 semanas**: só a intervenção cabe. |

**Síntese**: intervenção data-centric na linha 3 (recalibrar sensor, reanotar registros), mantendo o gradient boosting. Fica registrado o **gatilho da via combinada**: se, após a correção, o erro residual se mostrar difuso com o framework atendido, a troca entra em avaliação com piloto dedicado.

---

## 5. Glossário consolidado (GLO-M3, termo: definição)

Tags de origem do glossário oficial: `[M3: seção]`, com IA-024 = e-book da Aula 1, IA-025 = notebook, IA-026 = e-book da Aula 3, IA-027 = template T3.1.

- **Abordagem centrada no modelo**: dados como insumo fixo e todo esforço sobre o modelo (arquitetura, hiperparâmetros, algoritmo recente). É o reflexo que o data-centric inverte e "a armadilha mais cara da seção 3.1". [3.1]
- **Abordagem data-centric**: modelo de referência fixo e iteração sistemática sobre os dados (corrigir rótulos, padronizar coleta, cobrir subgrupos), cada volta orientada pela análise de erro por slices. [3.1]
- **Acurácia (dimensão de qualidade)**: o valor registrado corresponde ao mundo real (ex.: rótulo de defeito atribuído à peça certa). Não confundir com a métrica de classificação do GLO-M0; aqui a propriedade é **do dado**. [3.3]
- **Anonimização**: torna a reidentificação impossível em termos razoáveis, retirando o dado do alcance da LGPD. Exige mais que remover identificadores diretos; enquanto o cruzamento de atributos permitir reidentificar, é só pseudonimização. [3.2]
- **Atualidade**: o dado reflete o estado vigente relevante para a decisão (falha típica: cadastro de equipamento desatualizado há meses). [3.3]
- **Augmentation**: papel de ampliação do treino; no módulo, sintéticos como **complemento** da base real, em regiões específicas e proporção controlada. A augmentation clássica por transformação é técnica vizinha (Fase 2). [3.7, IA-026]
- **Auto-reforço** (= colapso de modelo): treino, em proporção crescente, sobre dados produzidos por modelos; reforça padrões e vieses do gerador e apaga as caudas. [3.7, IA-026]
- **Base legal de tratamento**: fundamento jurídico que autoriza tratar dado pessoal (consentimento, obrigação legal, execução de contrato, legítimo interesse, entre outras), apontável para a finalidade declarada. [3.2, IA-024]
- **Baseline**: veja modelo de referência. **Colapso de modelo**: veja auto-reforço. **Drift**: veja data drift.
- **Completude**: há valor onde deveria haver (fração de campos preenchidos; falha típica: sensor sem leitura; no notebook, os `?`). [3.3, IA-025]
- **Concept drift**: mudança na **relação entre entradas e saídas**, distinta do data drift; aqui só para delimitação (Fase 2). [3.1, IA-024]
- **Consistência**: campos e registros concordam entre si, sem contradição entre fontes (falha típica: data de reparo anterior à data da falha). [3.3]
- **Dados sintéticos**: gerados por simulação de domínio ou modelo generativo; legítimos como complemento de treino (casos raros, custo, privacidade), com origem no lineage; **inaceitáveis no teste em qualquer proporção**. [3.7, IA-026]
- **Data drift**: mudança na distribuição dos dados de produção em relação à de treino; gradual ou abrupta (troca de fornecedor, mudança de processo). [3.1, IA-024]
- **Data lineage**: registro rastreável da origem e das transformações de cada dado até o treino; sustenta auditoria, reprodutibilidade e resposta a titulares. [3.2, IA-024]
- **Distribution shift**: diferença de distribuição entre treino e produção (origem, condição de coleta, período). Ao longo do tempo, chama-se data drift. É cenário em que data-centric mais rende. [3.1]
- **Erro irredutível**: parcela do erro que nenhum modelo elimina (ambiguidade ou ruído intrínsecos). Perto dele, trocar de modelo não ajuda. [3.6, IA-026]
- **Error analysis**: desempenho medido dentro de cada slice em cinco passos (definir slices, medir por slice, ordenar por gap ponderado pelo suporte, inspecionar erros dos piores, decidir intervenção). É a evidência de entrada da decisão dados × modelo. [3.4, IA-025]
- **EU AI Act** (Reg. UE 2024/1689): classifica sistemas por risco e **regula o sistema, não o dado pessoal**; Art. 10 para alto risco (relevância, representatividade suficiente, exame de erros e vieses). [3.2]
- **Fidelidade (de dados sintéticos)**: quanto o sintético aproxima a distribuição real, incluindo caudas, limítrofes e correlações finas; verificada por comparação estatística, especialista e teste por consequência em dado real. [3.7, IA-026]
- **Framework de data quality**: seis dimensões verificáveis (completude, consistência, acurácia, atualidade, validade, unicidade); sua verificação **antecede a hipótese de troca de modelo** na árvore. [3.3, IA-025]
- **Gap de desempenho**: diferença entre a métrica do slice e a de referência. Gaps grandes com suporte adequado indicam problema real e endereçável; **gap × peso do slice = teto do ganho agregado**. [3.4, IA-025]
- **GDPR** (Reg. UE 2016/679): bases legais e deveres análogos à LGPD; Art. 22 (decisão inteiramente automatizada, retomado no M5); transferências internacionais em capítulo próprio. [3.2]
- **Intervenção combinada**: dados primeiro com gatilho explícito de reavaliação da troca; **não autoriza executar as duas ao mesmo tempo**. [3.6, IA-027]
- **Intervenção data-centric**: melhoria dirigida aos dados a partir da error analysis (coletar ou rebalancear, reanotar, recoletar após drift). Seu ganho se transfere a qualquer modelo futuro. [3.6, IA-025]
- **LGPD** (Lei 13.709/2018): base legal por tratamento; finalidade, adequação, minimização; sensíveis no Art. 11; incide sempre que há pessoa natural identificada ou identificável. [3.2]
- **Long tail**: muitos casos raros que, somados, pesam mais do que parecem; poucos exemplos bem escolhidos fecham a lacuna. [3.1]
- **Modelo de referência (baseline model)**: treinado no início do ciclo e mantido fixo; instrumento de diagnóstico dos dados. [3.1]
- **Proporção de positivos**: fração da classe positiva no slice. Quando varia entre slices, a acurácia deixa de ser comparável; explica um slice ter a **maior acurácia e o pior recall** ao mesmo tempo. [3.4, IA-025]
- **Pseudonimização**: troca de identificadores diretos por códigos, com reidentificação ainda razoavelmente possível. **Continua dado pessoal**; confundi-la com anonimização é "a armadilha regulatória mais frequente do módulo". [3.2]
- **Risco residual**: risco que permanece após as mitigações e é aceito de forma explícita e documentada, com justificativa e gatilho de revisão. [3.8, IA-026]
- **Ruído de rótulo**: rótulos errados ou inconsistentes (divergência entre turnos, classes trocadas). O modelo aprende o ruído; a mitigação é auditar uma amostra e reanotar com critério unificado. [3.1]
- **Slice**: subconjunto definido por critério interpretável, com significado de domínio (não partição aleatória). [3.4, IA-024]
- **Sub-representação**: escassez de exemplos de um grupo, condição ou classe no treino, **incluindo a classe positiva escassa dentro de um slice**. Aponta para coleta ou rebalanceamento; é a forma localizada do viés de representação. [3.6, IA-025]
- **Suporte**: número de exemplos do slice. Com suporte pequeno, a métrica vira ruído e pede cautela antes de intervir. [3.4, IA-025]
- **Teto de qualidade**: limite que os dados impõem a qualquer modelo; o modelo só decide quanto dele se alcança. [3.1]
- **Unicidade**: sem duplicatas indevidas (mesmo evento em dois sistemas); verificada no notebook junto da completude, antes do treino. [3.3, IA-025]
- **Validade**: valor respeita formato, faixa e domínio (falha típica: temperatura abaixo do zero absoluto). [3.3]
- **Viés de agregação**: um só modelo para grupos heterogêneos; revela-se na análise por slices. [3.5]
- **Viés de anotação**: subjetividade ou inconsistência do anotador; auditoria com mais de um anotador, critério unificado. [3.5]
- **Viés de avaliação**: benchmark ou teste que não representa o uso real. [3.5]
- **Viés de implantação**: uso em produção diferente do previsto (modelo de uma planta operado em outra). [3.5]
- **Viés de medição**: atributo registrado é proxy imperfeito do que se queria medir; o dado carrega distorção mesmo bem coletado e anotado. [3.5]
- **Viés de representação**: a amostra não cobre bem certos grupos ou condições do uso; detectável antes do treino comparando composições. [3.5, IA-024]
- **Viés histórico**: vem do mundo; a desigualdade se reflete fielmente em dados corretos. Não é defeito de coleta, o que muda a mitigação possível. [3.5]

---

## 6. Bibliografia (mínima e complementar)
- NG, A. *A Chat with Andrew Ng on MLOps: From Model-centric to Data-centric AI*. DeepLearning.AI, 2021.
- SAMBASIVAN, N. et al. *Everyone Wants to Do the Model Work, Not the Data Work: Data Cascades in High-stakes AI*. CHI, 2021.
- NORTHCUTT, C.; ATHALYE, A.; MUELLER, J. *Pervasive Label Errors in Test Sets Destabilize ML Benchmarks*. NeurIPS, 2021.
- WHANG, S. E. et al. *Data Collection and Quality Challenges in Deep Learning: A Data-centric AI Perspective*. VLDB Journal, 2023.
- SURESH, H.; GUTTAG, J. *A Framework for Understanding Sources of Harm Throughout the ML Life Cycle*. EAAMO, 2021.
- SHUMAILOV, I. et al. *AI models collapse when trained on recursively generated data*. Nature, v. 631, 2024.
- MITCHELL, M. et al. *Model Cards for Model Reporting*. FAccT, 2019. · GEBRU, T. et al. *Datasheets for Datasets*. CACM, 2021.
- LGPD (Lei 13.709/2018); GDPR (Reg. UE 2016/679); EU AI Act (Reg. UE 2024/1689, Art. 10).
- Ferramentas: Great Expectations, DVC, lakeFS, Cleanlab.

---

## 7. Tipos de desafios prováveis (banco de referência para avaliação)

O módulo declara que o quiz é "menos definição, mais escolha justificada", em cenários curtos. Questões já observadas no quiz do M3 seguem exatamente estes formatos.

1. **Classificar achados nas seis dimensões de data quality**: dado um ou mais achados (data de reparo anterior à falha → **consistência**; temperatura negativa em escala absoluta → **validade**; duplicata por integração → **unicidade**; fuso trocado → **validade**; sensor sem leitura → **completude**; rótulo na peça errada → **acurácia**; cadastro defasado → **atualidade**). Cuidado com alternativas que trazem as dimensões certas **em ordem trocada** ("respectivamente").
2. **Próximo passo de uma error analysis**: dada uma tabela por slice (nos moldes do Quadro 3), identificar o slice crítico pelo gap **ponderado pelo suporte** e aplicar os cinco passos. Após medir e ordenar, o próximo passo é **inspecionar manualmente uma amostra de erros** do slice, não retreinar com arquitetura maior, remover o slice do teste ou otimizar a média.
3. **Percorrer a árvore dados × modelo**: cenário com erro concentrado e causa de dados (ex.: rótulos inconsistentes entre turnos) → intervenção data-centric no slice, retreinando o **modelo atual**. Distratores típicos:
   - "arquitetura maior é robusta a ruído de rótulo";
   - "fazer as duas ao mesmo tempo" (destrói a atribuição);
   - "aceitar como erro irredutível" (há causa endereçável).
4. **Avaliar uma medida de mitigação de viés**: remover a coluna sensível é **insuficiente**, porque proxies carregam a informação e o viés deve ser medido e monitorado ao longo do tempo. Distratores:
   - "o viés nasce só no modelo / corrigir na função de perda";
   - "mais dados diluem a distorção".
5. **Localizar o viés no pipeline**: dado um caso, nomear o tipo e o ponto de entrada (histórico, representação, medição, anotação, agregação, avaliação, implantação) e o teste que o detecta.
6. **Acurácia enganosa por proporção de positivos**: explicar por que um slice tem a maior acurácia e o pior recall, e qual métrica reportar.
7. **Projeção de ganho**: calcular gap × peso do slice (ex.: 33 pontos × 12% ≈ 4 pontos; 30 × 10% = 3 pontos) e comparar com piloto do modelo nos mesmos dados.
8. **Preencher o T3.1**: cinco eixos com evidência concreta, síntese decisória e gatilho da via combinada quando aplicável.
9. **Decisão sobre dados sintéticos**: aplicar as três perguntas (o real é obtenível? cobre região que o real não cobre? há conjunto real reservado para validação?), escolher papel (complemento × substituto) e rejeitar sintético no teste final. Reconhecer o **auto-reforço** (sobretudo em LLM/NLP) e os três degraus de verificação de fidelidade.
10. **Triagem regulatória de um dataset industrial**: achar o dado pessoal escondido (matrícula em log de turno, rosto ao fundo, voz, padrão de digitação), distinguir pseudonimização de anonimização, criticar consentimento de colaboradores e legítimo interesse sem teste de balanceamento, decidir quando GDPR e EU AI Act incidem (EU AI Act regula o **sistema**, por risco; não o dado).
11. **Risco residual**: redigir o registro com lacuna, justificativa e gatilho de revisão.
12. **Definição exata de glossário**: data drift × concept drift; erro irredutível; teto de qualidade; suporte; intervenção combinada.

### Checklist rápido de correção
- A resposta parte de **evidência por slice** (com suporte e proporção de positivos), não do número global?
- A hipótese de **dados foi examinada antes** da de modelo, e a troca só foi proposta com framework de qualidade atendido, erro difuso e piloto nos mesmos dados?
- O ganho foi **projetado** (gap × peso), não presumido? O prazo foi pelo **pior caso**?
- Evitou mudar dados e modelo **simultaneamente**?
- Tratou viés como **propriedade medida e monitorada**, não como coluna a apagar?
- Manteve **validação em dado real** e registrou origem real/sintético no lineage?
- Não confundiu **pseudonimização com anonimização** nem "dado industrial" com "sem dado pessoal"?

---

## 8. Conexão com o Projeto Aroeira e com Condução de Projetos

- **B4 (Dados em PD&I Industrial)** declara o M3 como pré-requisito ("repertório técnico de data quality, error analysis e análise de viés, necessário mas não suficiente"). O M3 dá o **diagnóstico técnico**; o B4 acrescenta cronograma, custo, acordo de dados e governança. A verificação de entrada de lote do B4 usa o framework de seis dimensões do M3.
- **Aroeira, regra peça → causa (C2-01)**: é uma intervenção data-centric de **acurácia** (dimensão) e **ruído de rótulo**. pela peça trocada, 38% das causas genéricas eram na verdade vedação/válvula, e corrigir o rótulo antes de medir é exatamente "dados antes de modelo".
- **Aroeira, lote novo da VS-212 (C3-02)**: é **data drift abrupto por troca de fornecedor**, o exemplo literal do glossário. A falta de campo de lote em `d3_ordens` é lacuna de lineage.
- **Aroeira, `id_tecnico`**: dado pessoal em dataset industrial (LGPD incide); pseudonimizar não o tira da lei.
- **Aroeira, 32% da frota sem telemetria** (`d1_frota.tem_telemetria`): viés de **representação/cobertura** do alerta; slices naturais para error analysis são tipo de equipamento, planta e ambiente.
- **Aroeira, falha de vedação rara**: é o cenário em que sintético por simulação seria tentador. A regra continua: validar só em dado real.
