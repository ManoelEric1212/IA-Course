# Entregáveis do Encontro 2 — Squad 5 (UFC), versão entregue

> Fonte: `Projeto/Encontro 2/Artefatos/` — `IND-KIT-004-EN2-T2 - Squad 5 UFC.docx.pdf` (Matriz de Alternativas), `IND-KIT-007-EN3-T1 - Squad 5 UFC.docx.pdf` (Decisão Justificada), `IND-KIT-008-EN3-T2 - Squad 5 UFC.docx.pdf` (Canvas). Data em todos: **08/10/2026**. Escrita e pasta: Rhuan Nunes. Apresentação: Isac Andrade.
>
> A capa do KIT-007/008 diz "Encontro 3", mas são instrumentos do **Encontro 2** deste arco (ver `encontro-2.md`). É **esta** versão que o mentor tem e que entra na Matriz de Teste (KIT-011) do E3, não os esboços de `Projeto/Encontro 2/Preparacao/`.
>
> Devolutiva do mentor e caixas de critério de pronto: **em branco** nos três PDFs.

## 1. Matriz de Alternativas (KIT-004), transcrição resumida

| Alternativa | Aderência | Dados necessários | Viabilidade | Riscos | Explicab./TRL |
|---|---|---|---|---|---|
| **Alerta por telemetria** para vedação e válvula | Média (era baixa; sobe pela camada 2 / revisões do Wagner) | Telemetria diária (C0-07, C0-08) | Média/alta: começa sem ML, depende da rede do cliente (C0-03) | Alarmes falsos geram visitas desnecessárias | Alta: demonstrativo de temperatura é fácil de explicar |
| **Assistente conversacional** no histórico e no manual (workflow) (`d3_ordens.id_tecnico`, C1-03, C2-02) | Alta: reincidência ligada à troca de técnico; é o pedido aprovado (C2-02) | d3_ordens (C0-09) com causa corrigida pela peça + manual série CP (C1-03), ainda indisponível | Alta: não treina modelo (C2-02) | Alucinação ao redigir a resposta (C2-02) | Alta: cita OS e seção do manual; falta validar com manual real |
| **Workflow de busca e criação de OS** por chamadas determinísticas + preparação de dados para o LLM, com referência às fontes | Alta: há acesso aos dados, montagem de prompts e referência às fontes | OS (C0-09), peças (D1), frota (D1), garantia (D4) | Média: depende de implementar e listar as funções e criar os fluxos | Busca errônea e alucinação do LLM | Alta: buscas SQL referenciam linhas do banco |

**Recomendação:** workflow determinístico com assistente conversacional para histórico de OS + manuais; em paralelo, sistema de alertas por telemetria.
**Incertezas:** ausência de decisão agêntica; falta de confirmação da diretoria; revalidação da base de OS por um engenheiro.

## 2. Decisão Justificada (KIT-007), transcrição

- **Escolha:** a mesma da recomendação da Matriz.
- **Justificativa:** viabilidade no prazo (C2-02); custo dentro do orçamento (C2-02); aderência à reincidência por troca de técnico (C2-02); auditoria e rastreabilidade por fontes citáveis num workflow, diferente de um agente (C0-04; C1-01).
- **Premissas:** (1) diretoria aceita piloto apenas como assistente conversacional (C2-02); (2) existe manual digitalizado (C1-03); (3) regra do Wagner vale para todas as ordens de classificação genérica (C2-01).
- **Incertezas:** qualidade das OS passou de alta para média (C2-01); "Recall > 80% (C2-01)"; ausência de decisão agêntica; falta de confirmação da diretoria; revalidação das OS por engenheiro.

## 3. Canvas (KIT-008), transcrição

- **Entrada:** pergunta do técnico em texto livre; histórico de OS; manual técnico digitalizado; telemetria.
- **Pré-processamento:** reformular a causa registrada pela peça (regras); segmentar o manual; limpar telemetria; associar histórico de OS aos códigos de peça.
- **Componentes:** consulta ao histórico; RAG nos manuais; chamada pontual de LLM; orquestração do workflow; alertas por telemetria.
- **Saída:** resposta em linguagem natural com referências (equipamento, peça, trecho do manual); alerta de telemetria.
- **Fluxo:** pergunta → consulta histórico + manual → LLM responde com referências → técnico atua na OS → nova OS realimenta o fluxo. Telemetria em paralelo, **apenas registrando alertas**.
- **Riscos:** alucinação do LLM; manual desatualizado; "a regra do Wagner não está relacionada à peça"; falsos alarmes de telemetria.
- Não há diagrama, só texto.

## 4. Validação contra os critérios de pronto (feita em 14/10/2026)

### Matriz — parcialmente pronta
- ✅ ≥2 alternativas (3) em todas as 5 dimensões; recomendação + incertezas registradas.
- ❌ **Nenhuma célula cita a matriz do curso base** (T1.1/T1.2/T2.1/T2.2), regra extra do arco (KIT-022 §4.4).
- ❌ **Sem alternativa agêntica.** A 3ª linha é outro workflow, quase sobreposta à 2ª. A Matriz não contrasta workflow × agente, mas a Decisão se justifica "diferentemente de um agente": critério sem célula que o sustente.
- ⚠️ Proveniência errada ou ausente:
  - "Alucinação (C2-02)" e "não treina modelo (C2-02)": a C2-02 é verba e prazo. Alucinação é T1.2; o argumento de viabilidade é "cabe em 90 dias (C2-02)".
  - "peças (D1)": peças estão em `d3_ordens.pecas_trocadas` (C0-09), não em D1 (frota).
  - Linha da telemetria: aderência cita "Camada 2/Wagner" sem C2-01 e sem número (23 → ~92 eventos; 41 de 43 > 3°C); riscos e explicabilidade sem fonte; dados não dizem que só 126 de 184 têm módulo, nem que o rótulo precisa ser corrigido pela peça.
  - 3ª linha: "aderência" descreve viabilidade (acesso a dados, prompts), não o problema; riscos sem fonte.
- ⚠️ "Ausência de decisão agêntica" não é incerteza, é escolha de projeto. "Falta de confirmação da diretoria" não diz do quê.
- ⚠️ Recomendação não separa o que está em operação no dia 90 e o que fica depois, exigência da C2-02. Também não diz que o alerta roda em sombra (o Canvas diz).

### Decisão Justificada — parcialmente pronta
- ✅ Premissas registradas (3) e incertezas registradas.
- ⚠️ Vínculo com a Matriz só implícito: nomeia critérios (viabilidade, aderência, auditoria), mas não cita colunas nem linhas da Matriz.
- ⚠️ "Aderência … (C2-02)": a evidência de troca de técnico é `d3_ordens.id_tecnico` + C1-03, não C2-02.
- ⚠️ A parte de telemetria da escolha não tem justificativa (a evidência é C2-01).
- ⚠️ Falta o **custo aceito**: o que se abre mão (abrir OS / pedir peça no piloto), que o mentor modela na fase 00:25.
- ⚠️ Premissa 1 é quase tautológica (a verba já é para o assistente, C2-02). A premissa útil é "a diretoria aceita um piloto **somente leitura**".
- ⚠️ Registro obrigatório 1 (**célula do E1 que caiu**): presente só de forma fraca. Cita Mapa §3 (qualidade das OS alta → média) sem nomear instrumento e seção, e "Recall > 80%" sem explicar. Não cita a principal, **Hipótese §3/H1** ("poucos casos positivos → detecção de anomalia").
- ❌ Registro obrigatório 2 (**sugestão de IA rejeitada com motivo técnico**): **ausente**.

### Canvas — parcialmente pronto
- ✅ Entrada, preparação, componentes, saída e fluxo descritos; workflow (não agente) e telemetria só registrando são coerentes com a camada 2.
- ❌ **Riscos não localizados no fluxo**: lista genérica, sem dizer em que etapa ocorrem.
- ❌ **Sem diagrama**: o critério "colega de outro eixo entende sem explicação oral" fica difícil de cumprir só com texto.
- ⚠️ Entradas sem tipo e sem proveniência (C0-08, C0-09, C1-03). "Alertas por telemetria" não diz que é limiar estatístico (sem ML).
- ⚠️ O laço "nova OS realimenta o fluxo" não tem risco associado (registro apressado volta a degradar o histórico, C1-04/C2-01). Não há risco ético (uso de `id_tecnico` para ranquear técnicos).
- ⚠️ "A regra do Wagner não está relacionada à peça": redação confusa. O risco real é a regra peça → causa falhar fora do recorte revisado (ex.: 16 `contaminacao_particulado` com VS-212).

### Coerência entre os três
- Matriz e Decisão dizem "criar alertas por telemetria"; o Canvas diz "apenas registrando". Vale alinhar para "modo sombra" nos três.
- As perguntas aos atores (orçamento de 3) e as respostas não aparecem registradas em nenhum instrumento.

## 5. O que levar para o Encontro 3 (Matriz de Teste, KIT-011)
O critério de sucesso é fixado **antes** de rodar o notebook, com número, linha de base e horizonte. Nos entregáveis só existe "Recall > 80%", sem linha de base e sem dizer sobre qual rótulo. Antes do E3, definir:
- **Alerta de telemetria:** recall e taxa de falso alarme medidos contra a causa **corrigida pela peça**, não `causa_registrada`. Linha de base: limiar > 3°C acerta 41/43 reclassificadas e dispara em 7/84 inconclusivas (C2-01).
- **Assistente:** recuperação certa do histórico/trecho do manual (ex.: recall@3), % de respostas com fonte citada, e tempo de busca (sem linha de base: pergunta ao Iran não feita/registrada).
- Corrigir no E3 as lacunas acima que o mentor apontar na devolutiva. Não reescrever no Mapa/Hipótese o que a camada 2 derrubou: o registro fica na Decisão.
