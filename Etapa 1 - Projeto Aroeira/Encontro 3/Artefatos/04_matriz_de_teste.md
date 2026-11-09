# Template: Matriz de Teste (KIT-011)

> Kit de formação | Testar a hipótese e refinar. No kit de 5 encontros, o template diz "Encontro 4"; neste arco, é usado no Encontro 3.

## Identificação
| Campo | Preenchimento |
|---|---|
| Squad / Polo | Squad 5 - UFC |
| Data | 15/10/2026 |
| Caso / Desafio | Aroeira Equipamentos Industriais |
| Integrantes e papéis do dia | Registra: ______ · Apresenta: ______ |

## 1. Plano de teste
Hipóteses = alternativas da **Matriz de Alternativas do E2** (KIT-004), por orientação do articulador. A Alt. 2 aparece em duas linhas porque tem duas partes testáveis de formas diferentes.

| Hipótese | Evidência necessária | Forma de teste | Critério de sucesso (a priori) |
|---|---|---|---|
| **Alt. 1: alerta por telemetria para vedação e válvula** (VS-212, VA-118), em equipamento com telemetria diária (C0-07, C0-08), sinaliza a falha antes da troca da peça, sem gerar visitas desnecessárias (risco da Matriz). Com a C3-02, o período recente inclui o lote novo da VS-212 | **Confirma:** no período de teste (posterior ao treino), a maior parte dos alertas é seguida de troca da peça em até 30 dias, com precisão bem acima da prevalência, e o alerta pega parte útil das trocas. **Refuta:** precisão próxima da prevalência (vira visita à toa), ou precisão alta só porque o alerta quase não dispara | **Prática**: notebook KIT-023, caminho B (modelo de referência sobre histórico rotulado, divisão temporal) | **Precisão ≥ 0,50 com sensibilidade ≥ 0,30.** Substitui o "Recall > 80%" do E2, por orientação do articulador: recall alto em falha rara se obtém alertando quase tudo |
| **Alt. 2a: dados do assistente.** O histórico só serve ao assistente com a causa corrigida pela peça, porque a causa registrada esconde a falha real (Matriz: "dados necessários"; premissa 3 da Decisão; C2-01) | **Confirma:** parcela relevante das ordens de VS-212/VA-118 com causa registrada incompatível com a peça, com o relato do técnico coerente com a peça na amostra. **Refuta:** discordância baixa (a causa registrada já é confiável), ou relatos que contradizem a peça | **Analítica**: notebook, caminho C (cálculo sobre D3) + leitura de amostra de 20 ordens | **Taxa de discordância > 0,30** → a correção pela peça é pré-requisito |
| **Alt. 2b: recuperação do assistente.** Responde ao técnico com a OS e a seção do manual corretas, citando a fonte, mais rápido que hoje, em equipamento visitado por outro técnico (C1-03) | **Confirma:** em perguntas reais, a resposta traz OS e trecho certos, com fonte verificável, em menos tempo. **Refuta:** resposta sem fonte ou com OS/trecho errado (alucinação, busca errônea), ou manual inexistente em formato digital | **Conceitual**: argumento contra os critérios da Decisão (prazo, explicabilidade, auditoria C3-01) | Cada resposta rastreável (OS + seção citadas, registro recuperável, C3-01) e viável em 90 dias sem treinar modelo (C2-02). Taxa de acerto sem número: primeiro teste da residência |

Alt. 3 (workflow que cria OS) fora do teste: não está na decisão do dia 90.

**Justificativa da forma de teste: o que impediria o teste prático**
> Para a Alt. 1 nada impede o teste prático: D2 e D3 estão no ambiente da turma e o notebook roda no Colab sem GPU. Para os dados da Alt. 2 basta o teste analítico, um cálculo sobre D3 que já responde à pergunta. A recuperação da Alt. 2 só admite teste conceitual, porque o manual da série CP não foi disponibilizado (C1-03, premissa 2 da Decisão) e não há linha de base de tempo de busca.

## 2. Resultado do teste e limitações
> **Alt. 1 (caminho B, prático):** com precisão ≥ 0,50, sensibilidade de 0,603 (76 de 126 janelas positivas do período de teste); prevalência de 0,088; precisão média de 0,477, cerca de 5,4 vezes a prevalência [nº da saída]. **Sustenta.**
> Limitações:
> - as janelas se sobrepõem (passo de 7 dias, horizonte de 30), então 126 positivos não são 126 trocas;
> - o período de teste cai em boa parte no trimestre do lote novo da VS-212 (43 das 108 trocas em jun–ago/26, C3-02), e o sinal pode ser de lote, não de operação;
> - o ponto de corte foi escolhido no próprio teste (otimista);
> - só equipamentos com telemetria;
> - rótulo = "trocou a peça";
> - versão por limiar ("iniciar sem ML") não medida.
>
> **Alt. 2a (caminho C, analítico):** discordância de 0,639 (69 de 108 ordens), **toda por causa genérica** (0 com causa específica incompatível); estável entre peças (VS-212 0,636; VA-118 0,645) e antes/depois de jun/26 (0,631; 0,651); causa genérica 4,6 vezes mais frequente que nas demais corretivas (0,639 contra 0,139) [nº da saída]. **Intervir nos dados.**
> Limitações: só duas peças; não verifica se a peça trocada era a causa real; relato lido em 20 ordens.
>
> **Alt. 2b (conceitual):** sem teste com dados; o manual não foi disponibilizado. O argumento atende aos critérios declarados enquanto cada resposta citar OS e seção e ficar registrada, mas a taxa de acerto segue sem medida.

## 3. O resultado revisa a decisão? Em quê?
> **Confirma a decisão do E2 com evidência**, com dois ajustes:
> 1. O assistente (Alt. 2) segue como escolha, agora com a **correção da causa pela peça como pré-requisito declarado** no cronograma, antes da consulta ao histórico. A revalidação pelo engenheiro fica dimensionada em 69 ordens nessas duas peças, e a premissa 3 sai fortalecida (toda discordância é genérica).
> 2. O alerta (Alt. 1) **tem sinal**, mas continua em paralelo, só registrando (Canvas), até cumprir o critério de entrada em operação com dados novos. Não entra no plano do dia 90, porque o teste não separa falha de operação de falha do lote novo (C3-02).
>
> O critério "Recall > 80%" da Decisão foi substituído antes do teste pela precisão, por orientação do articulador.

## Critério de pronto
- [x] Há evidência de teste com critério definido a priori
- [x] Resultado e limitações registrados
- [x] Decisão revisada ou confirmada com base em evidência
- [x] A forma de teste está justificada, com o que impediria o teste prático registrado

## Devolutiva do mentor (evidência → interpretação → próximo passo → prazo)
_______________________________________________
