---
name: projeto-aroeira
description: Base de referência do projeto prático "Laboratórios de decisão técnica" (Formação 1) do curso Fundamentos de IA Aplicada — o caso fictício da Aroeira Equipamentos Industriais, trabalhado em 3 encontros presenciais de squad (Encontro 1 compreender/delimitar/hipotetizar, Encontro 2 comparar/decidir/desenhar, Encontro 3 testar/validar/defender). Use esta skill sempre que o usuário mencionar o caso Aroeira, qualquer instrumento/template KIT-0xx (Acordo de squad, Mapa Técnico do Problema, Hipótese Técnica, Matriz de Alternativas, Decisão Justificada, Canvas de Arquitetura Conceitual, Matriz de Teste, Matriz de Validação, Proposta Técnica Final, Roteiro de Pitch, Registro de princípios transferíveis), pedir para preencher/revisar/simular um desses instrumentos, perguntar sobre os dados d1_frota/d2_telemetria/d3_ordens/d4_garantia.csv, ou perguntar sobre a dinâmica de um "Encontro" do squad (o que levar, o que produzir, critério de pronto, sequência de tempo). No momento só o material do Encontro 1 foi processado em detalhe; os Encontros 2 e 3 serão adicionados quando o material (KIT-0xx correspondentes) for disponibilizado na pasta Projeto.
---

# Projeto Aroeira — Laboratórios de decisão técnica (Formação 1)

Esta skill cobre a trilha prática do curso: um projeto de squad, sobre um caso único e fictício (Aroeira Equipamentos Industriais, fabricante de compressores industriais), distribuído em 3 encontros presenciais de 4h. É complementar à skill `fundamentos-ia-aplicada` (que cobre o conteúdo dos módulos M0/M1/M2 do curso base) — aqui o foco é a aplicação prática desse conteúdo a um caso concreto, com instrumentos formais de decisão a preencher.

## Estrutura do material até agora

| Arquivo | Conteúdo |
|---|---|
| `references/dossie-camada-0.md` | O dossiê do caso (KIT-025): a empresa, a operação, o pedido da diretoria (ainda não delimitado), o dicionário completo dos 4 datasets (D1 frota, D2 telemetria, D3 ordens de serviço, D4 garantia), o mapa das plantas, os atores, e um gabarito de apoio para o check-in de leitura prévia (KIT-030) |
| `references/encontro-1.md` | Guia operacional completo do Encontro 1 (KIT-022, seções 1–3 + KIT-048): os 3 instrumentos a produzir (Acordo de squad, Mapa Técnico do Problema, Hipótese Técnica) com seus critérios de "pronto", a sequência minuto a minuto da sessão de 240 min, as 4 regras de trabalho do arco inteiro, e como a avaliação formativa funciona |

Os dados brutos ficam em `Projeto/Encontro 1/Dados/*.csv` (d1_frota.csv — 184 linhas, d2_telemetria.csv — 42458 linhas, d3_ordens.csv — 2122 linhas, d4_garantia.csv — 712 linhas); o dicionário de cada campo está reproduzido em `references/dossie-camada-0.md`, não é necessário reabrir os CSVs para responder perguntas conceituais sobre eles.

## Quando os Encontros 2 e 3 chegarem
Quando novos arquivos `KIT-0xx` referentes ao Encontro 2 (ex.: Matriz de Alternativas, Decisão Justificada, Canvas de Arquitetura Conceitual) ou Encontro 3 (Matriz de Teste, Matriz de Validação, Proposta Técnica Final, Roteiro de Pitch, Registro de princípios transferíveis) forem adicionados à pasta `Projeto/`, criar `references/encontro-2.md` e `references/encontro-3.md` seguindo o mesmo formato de `encontro-1.md` (o que produzir + critério de pronto de cada instrumento, pré-requisitos de módulo do curso base, sequência de tempo, regras específicas daquele encontro) e atualizar esta tabela.

## Como usar esta skill

**Para ajudar a preencher um instrumento do Encontro 1**: usar o critério de "pronto quando" de `encontro-1.md` como checklist, e exigir que toda célula tenha proveniência (`C0-xx` do dossiê, ou `conjunto.campo` dos CSVs) — essa é uma regra de trabalho do curso, não uma preferência estilística.

**Para checar uma afirmação sobre os dados**: consultar o dicionário de campos em `dossie-camada-0.md` antes de abrir os CSVs — ele já documenta as regras não óbvias (ex.: por que uma série de telemetria é mais curta, quando `pecas_trocadas` fica vazio, a relação 1-para-0-ou-1 entre ordem corretiva e pedido de garantia).

**Para simular o papel do mentor/ator** (Nelson, Wagner, Cristiane, Simone, Iran, Kleber, Tereza): responder só com informação que já está no dossiê; se a informação não existir na camada 0, a resposta correta é "a empresa vai verificar" (registrar como incerteza), não inventar dado novo — isso preserva a mecânica real do laboratório (orçamento de perguntas, camadas de informação liberadas por encontro).

**Atenção a não vazar a resposta do pedido antes da hora**: o pedido da diretoria (C0-05) é deliberadamente um sintoma, não o problema delimitado — ao ajudar no Mapa Técnico do Problema, não "resolver" a delimitação pelo squad; ajudar a raciocinar com os dados, não entregar a conclusão pronta, já que o critério de pronto exige a autoverificação do próprio squad.
