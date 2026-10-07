# Dossiê do caso — Camada 1 (KIT-026)

> Fonte: `Projeto/KIT-026_camada_01.pdf`. Liberada na fase de **imersão** do Encontro 1 (~30 min após o início), pelo mentor. A camada 0 continua valendo. Códigos de proveniência `C1-01` a `C1-04`.

## C1-01. Extrato da política de garantia de fábrica, série CP
- **Cobertura**: 24 meses a contar da data de início da garantia, ou 16000 horas de operação acumuladas, o que ocorrer primeiro (reafirma C0-04).
- **Abertura do pedido**: pelo cliente, a partir de ordem de serviço já registrada; não depende de o equipamento estar dentro da cobertura.
- **Análise**: a coordenação de garantia analisa em **até 30 dias corridos** da abertura, usando o registro da ordem, o histórico do equipamento e, quando existir, a medição do módulo de monitoramento.
- **Decisão**: cobertura total, parcial ou negativa, sempre com motivo em lista fechada. Cliente pode contestar por escrito.
- **Cláusula de uso fora de especificação**: a cobertura não se aplica quando o equipamento operou fora das condições declaradas na folha de dados do modelo — isso inclui: regime de trabalho contratado, faixas de temperatura e pressão de operação, **qualidade do ar aspirado**, e execução da manutenção prevista no manual com insumos homologados.
- **Ônus da informação**: quando não há medição disponível para o período em análise, a coordenação decide com o registro do atendimento (não a medição). A ausência de medição **não suspende** a contagem dos 30 dias.

## C1-02. Painel de serviço — indicador real de "tempo médio de atendimento"
> Este é o indicador que a diretoria citou ao encomendar o projeto (C0-05). **Definição**: média da duração dos atendimentos das ordens de serviço **abertas no mês**, em horas, **sobre todas as ordens do mês** (não só corretivas).

| Mês | Tempo médio de atendimento (h) |
|---|---|
| 2025-09 | 3,4 |
| 2025-10 | 3,7 |
| 2025-11 | 3,9 |
| 2025-12 | 3,8 |
| 2026-01 | 3,7 |
| 2026-02 | 4,2 |
| 2026-03 | 4,2 |
| 2026-04 | 3,8 |
| 2026-05 | 4,3 |
| 2026-06 | 4,4 |
| 2026-07 | 4,2 |
| 2026-08 | 4,5 |

Média do período inteiro: **4,0h**. O painel só mostra esse valor único por mês — **nenhuma abertura por tipo de ordem, causa, equipamento ou técnico**.

> **Validado contra D3** (ver `analise.py::indicador_painel_oficial`): a série bate quase exatamente calculando a média de `duracao_horas` sobre **todas** as linhas de D3 por mês (não filtrando por `tipo_ordem == 'corretiva'`, como a primeira análise exploratória tinha feito). Esse foi um erro de escopo da análise inicial — importante registrar como aprendizado.

## C1-03. Registro de experiência — Iran, técnico de campo
> "O que me custa tempo na planta não é o serviço em si, é chegar e não saber o que já foi feito naquele equipamento. Às vezes eu vou a um equipamento que outro colega atendeu semanas antes e não tenho como ver o que ele trocou sem ligar para alguém. O manual eu tenho, mas é o manual inteiro no celular, e procurar o procedimento certo no meio do atendimento é ruim. Voltar a um equipamento que eu já atendi acontece, e quando acontece eu gostaria de saber o que foi feito na visita anterior antes de sair."

Dois pontos de dor distintos: (1) falta de acesso rápido ao **histórico do próprio equipamento** entre técnicos diferentes; (2) **busca difícil no manual** (documento extenso, não indexado) durante o atendimento. Note-se que a dor **não é sobre decidir o que fazer** — é sobre **acessar informação que já existe mas está espalhada/difícil de achar**.

## C1-04. Registro de experiência — Kleber, técnico de campo
> "Tem planta em que eu já sei o que vou trocar antes de abrir o equipamento, porque é quase sempre o mesmo conjunto de peças. Não é em toda planta, é em algumas, e eu não sei dizer quantas vezes foi, nunca anotei nada disso. Quando eu registro o atendimento, escolho a causa na lista que o formulário oferece e sigo para o próximo chamado. Se me perguntarem por que acontece mais nessas plantas do que nas outras, eu não tenho número nenhum para mostrar."

Reconhecimento **tácito e não sistematizado** de um padrão de recorrência por planta/equipamento — o técnico já "sabe" informalmente, mas essa informação não é registrada nem agregada em lugar nenhum. É evidência qualitativa que **cruza diretamente** com o achado quantitativo de reincidência concentrada em 3 causas (ver `RESUMO_DESAFIO_1.md`): o que os dados mostram de forma agregada, o técnico já percebe individualmente, sem conseguir provar com número.
