# Unidade 5 — Operação, MLOps e Ciclo de Vida (CP.B5)

Fonte: `Operacao MLOps e ciclo de vida/resumo.txt` (extraído de Aula 1/e-book, Glossário, e os 4 artefatos CDP-031 a CDP-034). Prof. Raimundo Valter.

Artefatos analisados: Aula 1 (e-book), Glossário, Plano de validação e teste (CDP-031), Matriz de avaliação contínua (CDP-032), Checklist de prontidão para produção (CDP-033), Runbook mínimo de operação (CDP-034).

## Ideia central do bloco
O bloco trata do intervalo que mais separa o engenheiro de PD&I industrial do pesquisador: **o que acontece depois que o modelo funciona**. Premissa: projetos tecnicamente bons fracassam não na métrica do teste, mas no terceiro mês de operação, quando ninguém monitora o sistema. Caso-fio-condutor: manutenção preditiva dos compressores de uma planta química, com inferência local (on-premises).

## 1. Entrega pontual x entrega continuada
- **Entrega pontual**: termina no aceite do artefato (relatório, protótipo).
- **Entrega continuada**: o artefato é um **sistema** que segue operando sobre dados que mudam, com responsabilidade declarada por monitoramento, resposta a falhas e retreinamento — exige orçar horas de operação recorrentes e nomear responsáveis **desde o escopo do projeto** (B2).
- Exemplo de falha real: previsão de demanda comprada como projeto pontual; 18 meses depois o erro dobrou sem que ninguém percebesse, por falta de monitoramento e responsável.

## 2. Ciclo de vida do modelo em produção (6 fases, circular, não linear)
**Treinamento inicial → Validação → Deployment → Operação → Monitoramento contínuo → Retreinamento ou substituição** (volta à validação) **/ Aposentadoria**.

Condições de cada transição:
- Treinamento → Validação: **reprodutibilidade** (dados, código, configuração versionados).
- Validação → Deployment: **critério de corte definido a priori** (antes do resultado).
- Deployment → Operação: **prontidão** (checklist verificado, runbook entregue).
- Operação em diante: monitoramento contínuo decide, por **gatilhos declarados**, entre retreinamento ou aposentadoria.

### Estratégias de exposição do candidato (registradas no plano de validação)
- **Shadow deployment**: candidato recebe o mesmo tráfego e gera predições em paralelo, sem consumo real — risco zero, custo de rodar 2 modelos.
- **Lançamento canário**: fração pequena e reversível do tráfego real.
- Caso dos compressores: shadow de **4 semanas** antes de qualquer promoção.

**Mudança de regime chave**: em produção, **avaliação contínua substitui avaliação pontual** — a aprovação vence a cada janela de apuração; o modelo é bom até que os indicadores digam o contrário.

### Local de inferência (nuvem x borda/on-premises) — decisão arquitetural com custo operacional diferente
- **Nuvem**: atualização simples, escala elástica; custo recorrente por inferência, dependência de conectividade, dado sai do ambiente da empresa.
- **Local/planta**: atende regime de repouso do dado, latência previsível; equipe herda manutenção da máquina, procedimento de atualização, alcance limitado do monitoramento.
- **Protocolo de atualização local** (4 passos): pacote chega com versão e checksum → instalação em janela combinada (nunca durante operação crítica) → verificação pós-instalação contra lote de referência → pacote anterior disponível para rollback imediato.

**Armadilha comum**: tratar a validação como linha de chegada (como um artigo aceito) — gera "sistema órfão" sem monitoramento, responsável ou critério de retreinamento.

## 3. MLOps essencial (6 práticas)
Princípio unificador: **reprodutibilidade operacional** — não a de artigo científico, mas a capacidade de reconstruir qualquer versão do sistema (dados+código+config+ambiente) quando um gate, auditoria ou incidente exigir. "Resultado que não se reconstrói não sustenta decisão."

a) **Versionamento** — 5 elementos com linhagem rastreável: código, dados de treino, modelo, configuração (hiperparâmetros/limiares/janelas), ambiente de execução.

b) **Pipeline de dados sob o mesmo regime do pipeline de modelo** — versionado e monitorado, com validação de esquema/intervalos/taxa de preenchimento a cada lote. Armadilha: monitorar só o modelo e deixar o pipeline de dados solto (mudança de esquema na fonte derruba a qualidade sem nenhum indicador de modelo acusar a causa).

c) **Pipeline de retreinamento** — agendado (calendário) x por evidência (gatilhos de monitoramento). Regras inegociáveis: dados de retreinamento passam pelas mesmas verificações de entrada; candidato retreinado **sempre** passa por validação antes de ser promovido (nunca promoção automática).

d) **Monitoramento em produção — 4 famílias de indicadores**:
   - **Drift de dados**: distribuição das entradas mudou vs. treinamento.
   - **Drift de conceito** (mais traiçoeiro): a relação entrada→saída muda mesmo com entradas estáveis.
   - **Qualidade do modelo**: métrica da tarefa, mas rótulos chegam com atraso em produção (usa-se indicador substituto/proxy).
   - **Operação**: latência, disponibilidade, custo, saúde do pipeline.

   Regras de leitura: (1) gatilho sem janela declarada não é gatilho, é opinião; (2) drift detectado **não** implica retreinar de imediato — primeiro investigar a causa (sensor, esquema, evento transitório), pois retreinar sobre dado defeituoso ensina o defeito ao modelo.

e) **Registro de experimentos** — cada execução registra identificador, hipótese, versão de dados/código, configuração completa, métricas e decisão com justificativa. Sem isso, o veredito vira "memória de reunião". Armadilha: tratar AutoML como substituto dos critérios do projeto — ele otimiza a métrica que recebe, não o critério de negócio.

f) **Orquestração de pipelines** — decisão de **responsabilidade**, não de ferramenta. 3 perguntas: o que precisa rodar sem pessoa olhando? quem responde quando falha (nome, não time)? o que entra no runbook/checklist? Não orquestrar também é decisão legítima, se registrada. É decisão **caso a caso** dentro do mesmo projeto, não regra única: ingestão horária recorrente pede orquestração com alerta e responsável; notebook exploratório sob demanda não precisa; retreinamento pode ser agendado, mas a **promoção nunca é automática**.

Ferramentas citadas (categoria, não prescrição): DVC/lakeFS (versionamento), MLflow/Weights & Biases (experimentos), Airflow/Prefect (orquestração), Evidently/Grafana (monitoramento).

### Dois artefatos operacionais
- **Runbook mínimo** (CDP-034) — 4 seções: identificação do sistema; procedimentos "quando X, faça Y" (mín. 3); responsáveis com escalada; gatilhos coerentes com a matriz. Teste de qualidade: **pessoa que nunca viu o projeto consegue seguir e resolver o incidente**.
- **Checklist de prontidão para produção** (CDP-033) — gate objetivo e verificável entre deployment e operação: versões reproduzíveis, validação aprovada, monitoramento ativo, runbook entregue, pipeline sob verificação, acordo de dados vigente. Deve ser verificado por quem **não** construiu o item (verificação cruzada).

## 4. Débito técnico de ML (Sculley et al., NeurIPS 2015)
Débito técnico de ML não é falha moral, é **propriedade estrutural** de sistemas cujo comportamento depende de dados. Pergunta certa: não "como zerar?", mas **"quanto carregamos, onde, e quando pagamos?"**. Débito técnico identificado = **risco operacional**: entra na matriz de risco (B2) com probabilidade, severidade, mitigação com responsável e gatilho de reavaliação a cada gate.

Cinco formas:
1. **Erosão de fronteiras** — o modelo dissolve contratos de abstração. Sintomas: correção em cascata (modelo B corrige modelo A, grafo rígido) e consumidor não declarado (sistema a jusante usa a predição sem contrato formal).
2. **Emaranhamento** (CACE — *Changing Anything Changes Everything*) — mudar uma única feature redistribui pesos em todo o sistema; não existe "mudança pequena" num modelo em produção.
3. **Inferno de dependências** — de código (bibliotecas/versões) e, mais caras, de **dados** (sem compilador que as verifique). Versão contemporânea: modelo de terceiro atrás de API que muda de comportamento quando o provedor atualiza.
4. **Feedback loops** — as predições alteram dados futuros. **Loop direto**: o sucesso "consome" os próprios exemplos de falha (ex.: manutenção preditiva que evita falhas empobrece o treino futuro — risco de confundir degradação com vitória). **Loop oculto**: dois sistemas desconhecidos entre si se influenciam via o mundo físico/operacional.
5. **Débito de configuração** — thresholds, janelas, features, flags espalhados em planilhas/variáveis/hardcode mudam comportamento sem revisão (inclui prompts e limiares de modelos generativos). Tratamento: configuração como código, versionada e revisada.

Anti-padrões associados: *glue code* (integração sem testes), *pipeline jungle* (pipelines que crescem sem refatoração), caminhos experimentais mortos (flags esquecidas). Mitigações já construídas ao longo do curso: contratos de dados + mapa de consumidores; verificação de entrada + monitoramento por feature + retreinamento sempre validado; inventário de fornecedores com versão fixada; registrar intervenções como metadados + manter grupo de controle (holdout); configuração versionada como código.

## 5. Os quatro artefatos práticos do bloco (cadeia de dependência)
**Plano de validação → Matriz de avaliação contínua → Runbook → Checklist de prontidão** (que verifica se os três anteriores existem e estão coerentes entre si).

- **CDP-031 Plano de validação e teste** — critérios de sucesso/descarte **a priori**, estratégia de exposição (shadow/canário), critério de promoção e de retorno do candidato. Preencher a Parte A antes da B; usar partição **temporal** (nunca aleatória) em séries temporais, para não vazar dado (*data leakage*).
- **CDP-032 Matriz de avaliação contínua** — "contrato do monitoramento": herda os critérios do plano de validação como indicadores; cada linha tem o que monitorar, como medir, frequência, **gatilho com janela declarada** e **destinatário nomeado**. Sem gatilho+destinatário, é "painel bonito, não contrato".
- **CDP-033 Checklist de prontidão** — gate material único por promoção, evidência objetiva por item, 6 grupos (versionamento, validação aprovada, monitoramento ativo, pipelines/orquestração, operação/dados/responsáveis, riscos/transparência). Pendências viram "prontidão condicionada", nunca são ignoradas.
- **CDP-034 Runbook mínimo** — opera o sistema sem depender da memória de quem construiu; cada gatilho espelha uma linha da matriz; cada procedimento traz uma "decisão de segurança" antecipada (ex.: suspender alertas após 8h sem dados, porque alerta sobre dado ausente é pior que ausência de alerta).

## Reforços de aplicação (pontos que a prova/avaliação costuma cobrar)
- **Drift de dados x drift de conceito**: entradas **estáveis** mas taxa de confirmação dos alertas cai de forma sustentada por ciclos consecutivos → **drift de conceito**, mesmo sem causa óbvia. Ação correta: revisar hipótese e retreinar com validação — nunca esperar a apuração trimestral passivamente.
- Mesmo com causa aparente evidente (ex.: desvio começou um dia após recalibração de sensor), a sequência correta é **investigar como incidente de dados no pipeline antes de qualquer retreinamento** — nunca retreinar direto "para reduzir o tempo de exposição".
- **Item não demonstrável x pendência aceitável** no checklist: matriz de avaliação contínua sem gatilho de janela nem destinatário não é "pendência a resolver depois" — é item do Grupo 3 **não atendido**. Pendência aceitável é algo diferente: verificação ainda não realizada sobre um artefato já correto.
- Gatilho de **operação** (latência/disponibilidade) ≠ gatilho de **saúde do pipeline** (ausência de dados) — cada família tem seu próprio procedimento. O limiar de suspensão de alertas por ausência de dados é especificamente **>8h**; entre 0–8h a ação é investigar/registrar, nunca suspender adiantado.
- Superfície do indicador deve casar com **velocidade de ação exigida e raridade do sinal**, não com conveniência de relatório: indicadores de operação pedem superfície contínua/automática com alerta imediato; indicadores com rótulo raro/atrasado (qualidade do modelo) pedem superfície narrativa e periódica (ex.: trimestral) — alta frequência sobre evento raro é ruído disfarçado de tendência.
- Orquestração é decisão **caso a caso** dentro do mesmo projeto, não regra única para todos os pipelines.
- Reabrir uma decisão arquitetural já fixada (ex.: trocar inferência local por nuvem) **nunca é mudança neutra** — tem efeito em cadeia: regime de repouso do dado, runbook (protocolo local deixa de existir), matriz de avaliação contínua (indicador de operação muda de natureza), acordo de dados com a parceira.
- **Feedback loop oculto** (vs. loop direto): dois sistemas autônomos que não se conhecem se influenciam mutuamente via o ambiente físico/operacional. Mitigação: tornar o acoplamento visível via mapa de consumidores das predições — não há como simplesmente proibi-lo.

## Conclusão do bloco
"Gerenciar débito conscientemente é a última fronteira entre operar um sistema e ser operado por ele." O ciclo de vida, o MLOps essencial e o débito técnico fecham o arco iniciado nos blocos anteriores (hipóteses com critério a priori do B3, arquitetura/local de inferência do B3, governança de dados do B4), transformando-os em **regime permanente de operação**.

## Correspondência com o kit de laboratório (Projeto Aroeira)
A proposta vigente do Squad 5 (assistente conversacional somente leitura no piloto de 90 dias + **alerta de telemetria em modo sombra**) é literalmente o padrão de **shadow deployment** deste bloco. O conceito de "revisar o Canvas para acrescentar o registro recuperável" (C3-01, Encontro 3) corresponde à interface do catálogo/versionamento (B4) com o **runbook** (B5). Quando a residência avançar, os 4 artefatos deste bloco (plano de validação, matriz de avaliação contínua, runbook, checklist de prontidão) são o detalhamento operacional que viria depois da Proposta Técnica Final do Encontro 3 — a "residência" citada no roteiro do E3 ("o que viria na residência").
