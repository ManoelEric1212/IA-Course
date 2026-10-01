# Dossiê do caso — Camada 0 (KIT-025)

> Fonte: `Projeto/KIT-025_camada_00.pdf`. Leitura obrigatória antes do Encontro 1, junto ao módulo M0. Cada item tem código de proveniência `C0-01` a `C0-12` — toda célula de instrumento preenchida com informação daqui deve citar o código correspondente na justificativa (célula sem proveniência é devolvida pelo mentor). Este documento **não traz análise, não traz indicador de painel, não traz hipótese de causa** — é só o material bruto para começar o Encontro 1 já na análise.

## C0-01. A empresa
Aroeira Equipamentos Industriais fabrica compressores de ar de parafuso e secadores de ar comprimido. Fabricante de porte médio, fábrica única, atua em todo o território nacional. Opera assistência técnica própria e administra a garantia contratual de fábrica.

Base instalada relevante: linha de compressores de parafuso **série CP**, em três potências — **CP-40, CP-75, CP-110**. Instalados em plantas de clientes industriais de quatro setores: alimentos, transformação de plástico, metalurgia leve, cerâmica.

(Empresa, pessoas, plantas e códigos de peça são fictícios.)

## C0-02. Atendimento técnico
Cliente abre chamado → Aroeira gera ordem de serviço → desloca técnico de campo. O técnico registra: causa (lista fechada), relato curto em texto livre, lista de peças trocadas, duração em horas. O mesmo fluxo de ordem de serviço atende manutenção preventiva contratada, inspeção, comissionamento de equipamento novo e atendimento corretivo.

## C0-03. Telemetria
Parte da base instalada tem módulo de monitoramento. O módulo envia medições agregadas por dia para um concentrador na planta do cliente, que envia para a Aroeira. O envio depende da rede do cliente, liberada caso a caso.

## C0-04. Garantia contratual
Garantia de fábrica: 24 meses a contar da data de início da garantia do equipamento, **ou** 16000 horas de operação acumuladas, **o que ocorrer primeiro**. Pedido de garantia é aberto a partir de uma ordem de serviço; quem pleiteia é o cliente; a abertura **não** depende de o equipamento estar dentro da cobertura. A coordenação de garantia decide cobertura total/parcial/negativa com motivo em lista fechada. Cliente pode contestar.

## C0-05. O pedido da diretoria de serviços (ponto de partida do problema — ainda não delimitado)
A diretoria de serviços encomendou: **"um assistente conversacional com IA para os técnicos de campo, capaz de responder em linguagem natural sobre histórico do equipamento, manuais e procedimentos, e capaz de abrir a ordem de serviço e solicitar a peça sem sair da conversa."**

Justificativa apresentada (três partes):
1. Tempo médio de atendimento subiu no painel de serviço da empresa.
2. Entraram recentemente técnicos sem experiência na série CP.
3. Há reincidência de chamados no mesmo equipamento.

> **Atenção**: este é o pedido tal como chegou, **não** uma delimitação de problema. "Delimitar é trabalho do Encontro 1." Não confundir a solução pedida (assistente conversacional) com o problema raiz — distinguir sintoma de causa é parte central do Mapa Técnico do Problema (KIT-001).

## C0-06. Os quatro conjuntos de dados
Arquivos na turma do Classroom, em `Projeto/Encontro 1/Dados/`:

| Arquivo | Conteúdo | Granularidade | Campos | Linhas |
|---|---|---|---|---|
| `d1_frota.csv` | frota de equipamentos | 1 linha/equipamento instalado | 9 | 184 |
| `d2_telemetria.csv` | telemetria diária | 1 linha/equipamento/dia | 9 | 42458 |
| `d3_ordens.csv` | ordens de serviço | 1 linha/ordem | 9 | 2122 |
| `d4_garantia.csv` | pedidos de garantia | 1 linha/pedido | 7 | 712 |

Convenções: separador vírgula, cabeçalho na primeira linha, datas `AAAA-MM-DD`, decimais com ponto, lógicos 0/1, campo vazio = sem valor (cada dicionário abaixo diz quando). **Período coberto por D2 e D3: `2025-09-01` a `2026-08-31`.**

### D1 — `d1_frota.csv`
| Campo | Significado | Valores |
|---|---|---|
| `id_equipamento` | identificador | `EQ` + 4 dígitos |
| `modelo` | modelo da série CP | `CP-40`, `CP-75`, `CP-110` |
| `ano_instalacao` | ano de entrada em operação | inteiro |
| `id_planta` | planta do cliente | `PL` + 2 dígitos |
| `setor` | setor industrial da planta | `alimentos`, `plastico`, `metalurgia_leve`, `ceramica` |
| `classe_ambiente` | concentração de particulado | `particulado_baixo`, `particulado_medio`, `particulado_alto` |
| `tem_telemetria` | módulo de monitoramento | 1 com módulo, 0 sem |
| `tipo_contrato` | contrato de serviço vigente | `preventivo_mensal`, `preventivo_trimestral`, `sob_demanda` |
| `data_inicio_garantia` | início da garantia | data |

Regras: `ano_instalacao` coincide com o ano de `data_inicio_garantia` em todos os equipamentos. Equipamento com `tem_telemetria=0` **não tem nenhuma linha em D2**.

### D2 — `d2_telemetria.csv`
| Campo | Significado | Valores |
|---|---|---|
| `id_equipamento` | equipamento (chave para D1) | texto |
| `data` | dia da medição | data |
| `horas_operacao` | horas em operação no dia | decimal |
| `ciclo_trabalho_medio` | fração da capacidade | decimal 0–1 |
| `pressao_descarga_media` | pressão média (bar) | decimal |
| `temp_descarga_media` | temperatura média (°C) | decimal |
| `temp_descarga_maxima` | temperatura máxima (°C) | decimal, ≥ `temp_descarga_media` na mesma linha |
| `contagem_partidas` | nº de partidas no dia | inteiro |
| `transmissao_incompleta` | indicador | 1 incompleta, 0 completa |

**Duas situações distintas produzem "menos dado" em D2 — não confundir:**
1. **Transmissão incompleta**: a linha do dia **existe**, `transmissao_incompleta=1`, os 6 campos de medição vêm **vazios**. Todo indicador=1 tem os 6 campos vazios; nenhum indicador=0 tem campo vazio.
2. **Série curta**: equipamento com módulo tem linha desde o momento em que passou a transmitir, não desde o início do período (ex.: equipamento instalado dentro do período). Não é erro de transmissão. Série mais curta: 11 dias; mais longa: 365 dias.

### D3 — `d3_ordens.csv`
| Campo | Significado | Valores |
|---|---|---|
| `id_ordem` | identificador | `OS` + 6 dígitos |
| `id_equipamento` | equipamento atendido (chave para D1) | texto |
| `data_abertura` | data de abertura | data |
| `tipo_ordem` | natureza do atendimento | `corretiva`, `preventiva`, `inspecao`, `comissionamento` |
| `causa_registrada` | causa (lista fechada, 10 valores) | ver abaixo |
| `duracao_horas` | duração do atendimento | decimal |
| `pecas_trocadas` | códigos de peça trocados | lista separada por `;`, pode ser vazia |
| `relato_tecnico` | relato livre do técnico | texto, 1–3 frases |
| `id_tecnico` | técnico executor | `TEC` + 2 dígitos |

`causa_registrada` (10 valores): `causa_nao_identificada`, `contaminacao_particulado`, `corretiva_geral`, `desgaste_natural`, `falha_eletrica`, `falha_valvula_admissao`, `falha_vedacao`, `instalacao`, `manutencao_programada`, `vazamento_oleo`.

`pecas_trocadas` vazio aparece em ordens de inspeção, comissionamento e manutenção preventiva; **não** aparece em ordem corretiva.

Códigos de peça: `FL-070` filtro de ar · `LU-010` óleo lubrificante · `OR-330` anel de vedação · `SE-045` sensor de pressão · `TR-220` transdutor · `VA-118` válvula de admissão · `VS-212` conjunto de vedação do estágio de compressão.

### D4 — `d4_garantia.csv`
| Campo | Significado | Valores |
|---|---|---|
| `id_pedido` | identificador | `PG` + 4 dígitos |
| `id_ordem` | ordem de origem (chave para D3) | texto |
| `data` | abertura do pedido | data (mesmo dia da ordem ou até 11 dias depois; **não** é a data da decisão) |
| `valor_pleiteado` | valor pleiteado pelo cliente | decimal |
| `decisao_cobertura` | decisão | `total`, `parcial`, `negativa` |
| `motivo_decisao` | motivo (lista fechada) | `dentro_da_cobertura`, `desgaste_parcial`, `falta_de_evidencia`, `peca_nao_coberta`, `prazo_expirado`, `uso_fora_de_especificacao` |
| `contestado_pelo_cliente` | contestação | 1 contestada, 0 não |

D4 existe **somente** sobre ordem corretiva; ordens de inspeção/comissionamento/preventiva não geram pedido; parte das ordens corretivas não tem pedido. No máximo 1 pedido por ordem corretiva.

## C0-11. Mapa das plantas
Onze plantas, cada uma com **um único** setor e **uma única** classe de ambiente (atributo da planta, medido pela Aroeira na instalação, vale para todos os equipamentos dela):

| Planta | Setor | Classe de ambiente |
|---|---|---|
| PL-01 | alimentos | particulado_baixo |
| PL-02 | alimentos | particulado_baixo |
| PL-03 | alimentos | particulado_medio |
| PL-04 | plastico | particulado_medio |
| PL-05 | plastico | particulado_medio |
| PL-06 | plastico | particulado_baixo |
| PL-07 | metalurgia_leve | particulado_alto |
| PL-08 | metalurgia_leve | particulado_alto |
| PL-09 | metalurgia_leve | particulado_medio |
| PL-10 | ceramica | particulado_alto |
| PL-11 | ceramica | particulado_alto |

## C0-12. Atores (o squad fala com eles só por meio do mentor)
| Ator | Papel |
|---|---|
| Nelson | diretor de serviços da Aroeira, encomendou o projeto |
| Wagner | engenheiro de campo sênior |
| Cristiane | coordenadora de garantia |
| Simone | analista de dados e TI, responsável pelos bancos e concentradores |
| Iran e Kleber | técnicos de campo |
| Tereza | jurídico da Aroeira |

Orçamento de perguntas por encontro (consumido mesmo por pergunta mal formulada): **4 no Encontro 1, 3 no Encontro 2, 3 no Encontro 3**. Sem resposta disponível → registrar como incerteza no instrumento, não inventar.

## Gabarito de apoio — Check-in de leitura prévia (KIT-030)
8 questões de escolha única, todas respondíveis só com a camada 0 (sem abrir os CSVs). Usar para autoverificação antes do Encontro 1 — se uma questão parecer ambígua, registrar a dúvida no comentário da atividade em vez de chutar.

| # | Pergunta (resumo) | Resposta | Onde está |
|---|---|---|---|
| Q-01 | Período coberto por D2/D3 | `2025-09-01` a `2026-08-31` | C0-06 |
| Q-02 | Como aparece dia sem transmissão em D2 | linha existe, indicador=1, 6 campos vazios | C0-08 |
| Q-03 | Por que uma série em D2 é mais curta | equipamento passou a transmitir dentro do período (instalação mais recente) | C0-08 |
| Q-04 | Equipamento sem módulo em D2 | não aparece nenhuma linha | C0-07/C0-08 |
| Q-05 | Conteúdo de `pecas_trocadas` | zero, um ou vários códigos separados por `;`, vazio em inspeção/comissionamento/preventiva | C0-09 |
| Q-06 | Relação D4↔D3 | só existe pedido sobre ordem corretiva; parte das corretivas não tem pedido | C0-10 |
| Q-07 | O que o mapa das plantas estabelece | cada planta tem um único setor e uma única classe de ambiente, válidos para todos os equipamentos nela | C0-11 |
| Q-08 | Natureza do pedido da diretoria | descrição do assistente conversacional + justificativa da diretoria; delimitar o problema é trabalho do Encontro 1 | C0-05 |
