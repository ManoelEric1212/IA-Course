# Template: Roteiro de Pitch (KIT-016)

> Kit de formação | Defender tecnicamente. No kit de 5 encontros, o template diz "Encontro 5"; neste arco, é usado no Encontro 3. Pitch de 3 a 5 minutos, ensaiado cronometrado, falas divididas, riscos explícitos.

## Identificação
| Campo | Preenchimento |
|---|---|
| Squad / Polo | Squad 5 - UFC |
| Data | 15/10/2026 |
| Caso / Desafio | Aroeira Equipamentos Industriais |
| Integrantes e papéis do dia | Registra: ______ · Apresenta: ______ |

## 1. Estrutura do pitch
Tempos são teto por momento e somam 3 min 30 s. O momento que estoura tira tempo do seguinte, e o que costuma ser sacrificado é a validação.

| Momento | Tempo | Conteúdo (o que dizer) | Quem fala |
|---|---|---|---|
| Problema | 30 s | "A reincidência de corretivas cresce porque o técnico não vê o histórico do equipamento atendido por outro colega, e a causa registrada não diz qual foi a falha. É isso que puxa o tempo médio do painel." | |
| Abordagem | 60 s | "Propomos um assistente de consulta, somente leitura, sobre o histórico das ordens com a causa corrigida pela peça e sobre o manual, entregue no dia 90. Em paralelo, um alerta por telemetria para vedação e válvula, só registrando. É um workflow, não um agente. O custo que assumimos: não abrir OS automaticamente no piloto, e 32% da frota sem telemetria fica sem alerta." | |
| Justificativa | 60 s | "Escolhemos pelo prazo e pela verba de 90 dias (C2-02), pela troca de técnico, que é a causa da reincidência (C1-03), e pela auditoria: o jurídico agora exige explicação caso a caso (C3-01), e um workflow com fonte citada dá isso; um agente não." | |
| Validação e riscos | 30 s | "Testamos as duas alternativas que estão na decisão. O alerta acerta metade das vezes, cinco vezes acima do acaso, e pega 60% das janelas com troca: tem sinal. Mas o período de teste cai no lote novo da VS-212, então ainda não sabemos se é falha de operação ou de fornecedor. Nas ordens dessas peças, 64% têm causa genérica, contra 14% nas demais: corrigir a causa pela peça vem antes do assistente." | |
| Próximos passos | 30 s | "Plano de revisão: o alerta só passa a valer depois de cumprir o critério em operação, e volta para revisão se a precisão cair abaixo de 0,50 por duas janelas. Pedimos campo de lote e o manual digital. Assim o técnico chega sabendo o que já foi feito e qual foi a falha real: é isso que ataca a reincidência." | |

## 2. Preparação da defesa
| Pergunta provável da bancada | Resposta em uma frase | Artefato do arco que a sustenta |
|---|---|---|
| Por que esta abordagem e não a Alt. 3 (workflow que cria OS)? | A Alt. 3 depende de mais funções e fluxos (viabilidade média) e o pedido aprovado é o assistente de consulta (C2-02); criar OS fica para depois do piloto. | Matriz de Alternativas + Decisão (E2) |
| Por que não um agente? | O caminho é fixo (alerta → busca → resposta) e a auditoria exige fonte citável; a ausência de alternativa agêntica já estava registrada como incerteza. | Matriz de Alternativas + Decisão (E2) |
| Qual critério decidiu? | Viabilidade no prazo, custo, aderência à troca de técnico e auditabilidade; o alerta foi testado pela precisão, porque o risco registrado é o falso alarme. | Decisão (E2) + Matriz de Teste |
| Por que trocaram o "Recall > 80%"? | Em falha rara, recall alto se consegue alertando quase tudo, o risco de visita à toa; trocamos antes do teste, por orientação do articulador, e registramos na Decisão. | Registro na Decisão + Matriz de Teste |
| Precisão de 0,50 não é pouco? | É cerca de 5,7 vezes o acaso (prevalência de 0,088), e o número foi declarado antes, a partir do risco de visita desnecessária. | Matriz de Teste + Matriz de Alternativas |
| Se o alerta passou, por que não entra no dia 90? | O teste usou histórico e o período de teste coincide com o lote novo; entrar em operação exige o critério cumprido em paralelo, com dados novos. | Matriz de Teste (limitações) + C3-02 |
| Que premissa foi assumida? | Que a peça corrige a causa (fortalecida hoje: toda discordância é genérica) e que o manual existe em formato usável (ainda não verificada). | Decisão, premissas 2 e 3 + caminho C |
| O que a evidência cobre e o que não cobre? | Cobre equipamentos com telemetria e duas peças no período testado; não separa lote de operação e não mede a recuperação do manual. | Matriz de Teste + Matriz de Validação |
| O que faria vocês mudarem de ideia? | Precisão do alerta abaixo de 0,50 em operação, ou o campo de lote mostrar que o sinal é só do fornecedor. | Critério a priori + riscos residuais |
| (Tereza) O sistema sustenta a negativa do PG-0518? | Não decide cobertura: mostraria a temperatura do EQ-0129 sobre a base dele, sinal de vedação, mas **não afirma uso fora de especificação**; usar para negar garantia está fora de escopo, e cada saída fica registrada. | C3-01 + Proposta (uso fora de escopo) + Canvas |
| E o caminho que vocês não rodaram? | O A mede ciclo × ambiente, que é a pergunta da garantia, não a nossa; fica como próximo passo. | Notebook (seção 4) + Proposta |

**Limitação × erro:** a premissa de "taxa estável" da C2-01 caiu com a C3-02. Dizer que caiu, onde está registrado e o que muda. Conta a favor.

## Critério de pronto
- [ ] Pitch dentro do tempo (3 a 5 min), ensaiado cronometrado
- [x] Riscos explícitos, não escondidos
- [x] A fala fecha com o problema do Encontro 1
- [ ] Divisão de falas entre integrantes (preencher "Quem fala")
- [x] Cada resposta da defesa aponta o artefato do arco que a sustenta

## Devolutiva do mentor (evidência → interpretação → próximo passo → prazo)
_______________________________________________
