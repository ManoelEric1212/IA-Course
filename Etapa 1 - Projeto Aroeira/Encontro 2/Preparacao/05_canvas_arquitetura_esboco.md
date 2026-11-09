# Canvas de Arquitetura Conceitual (KIT-008) — ESBOÇO, já com a camada 2

> Conceitual: representar, não implementar. Teste do critério de pronto: **uma pessoa de outro eixo entende sem explicação oral**. Desenhem à mão ou num slide, com os riscos (⚠) marcados no ponto do fluxo onde acontecem.

**Identificação:** Squad 5 – UFC · Data: __/10/2026 · Caso: caso da Aroeira · Registra: Rhuan Nunes · Apresenta: Isac

## Diagrama do fluxo (piloto de 90 dias)

```
 ┌────────── PREPARAÇÃO (roda 1x e a cada OS nova) ──────────┐
 │ d3_ordens ─► [0] CORRIGE CAUSA PELA PEÇA (regra do Wagner)│
 │               VS-212 → falha_vedacao                      │  ⚠ R0
 │               VA-118 → falha_valvula_admissao             │
 │ Manual CP ─► divide em seções ─► índice de busca (embeddings)
 └───────────────────────────────────────────────────────────┘

  [1] TÉCNICO PERGUNTA no celular:
      "O que foi feito no EQ0123?"  /  "Como troco a vedação do CP-75?"
                     │
          ┌──────────┴───────────┐
          ▼                      ▼
 [2] HISTÓRICO             [3] MANUAL (RAG)
 últimas ordens do         3 trechos mais próximos
 equipamento: data,        da pergunta + nº da seção
 peças, causa corrigida
          └──────────┬───────────┘
                     ▼
  [4] LLM REDIGE A RESPOSTA usando SÓ o que veio de [2] e [3],
      sempre citando "OS-000758" / "Manual CP, seção 4.3"     ⚠ R4
                     ▼
  [5] RESPOSTA NO CELULAR do técnico
                     ▼
  [6] TÉCNICO ATENDE e REGISTRA a nova OS ─► volta para [0]   ⚠ R5

 ┌──── MODO SOMBRA (equipamentos com telemetria) ────┐
 │ d2_telemetria ─► [7] temp_descarga_maxima         │
 │   7 dias vs. média de 30–60 dias antes            │
 │   alta > 3°C ─► ALERTA REGISTRADO (não gera visita)│ ⚠ R6
 │   comparado depois com as corretivas reais         │
 └────────────────────────────────────────────────────┘

 FORA DOS 90 DIAS: abrir OS e pedir peça pela conversa.
```

## Campos do template

**Entrada de dados (fonte, tipo)**
- Pergunta do técnico em texto livre (C1-03).
- Histórico `d3_ordens`: `id_equipamento`, `data_abertura`, `causa_registrada`, `pecas_trocadas`, `relato_tecnico`, `id_tecnico` (C0-09). Tabela + texto curto.
- Manual técnico da série CP (C1-03): documento longo, não estruturado.
- Telemetria `d2_telemetria.temp_descarga_maxima`, diária, só em 126 de 184 equipamentos (C0-08).

**Pré-processamento / preparação**
- **Correção da causa pela peça** (C2-01): regra fixa, não é modelo.
- Ordenar o histórico por equipamento e data, e traduzir os códigos de peça (C0-09).
- Dividir o manual em seções, gerar embeddings e indexar uma vez.
- Telemetria: descartar dias com `transmissao_incompleta=1` e calcular a linha de base de 30 a 60 dias por equipamento.

**Componentes / modelo(s)**
- Consulta de histórico: filtro por `id_equipamento`, sem modelo.
- Recuperador: modelo de embeddings pré-treinado (auto-supervisionado) + busca por similaridade.
- LLM em **uma chamada pontual**, só para redigir a resposta a partir do que foi recuperado.
- Alerta de telemetria: **limiar estatístico** (alta > 3°C sobre a linha de base). Começa sem ML.
- Orquestração: **workflow fixo, não agente** (T2.1).

**Saída esperada**
- Resposta em linguagem natural no celular, sempre com a fonte (número da OS e seção do manual).
- Log de alertas da telemetria (sombra) para medir acerto e falso alarme ao fim dos 90 dias.

**Lógica / fluxo**
- A pergunta entra, histórico e manual são buscados em paralelo, o LLM redige com fonte e o técnico recebe. A nova OS realimenta o histórico.
- A telemetria roda separada, só registrando.
- Nenhum passo decide qual é o próximo passo, e por isso é um workflow.

**Pontos de risco / falha no fluxo**

| Ponto | Risco | Mitigação |
|---|---|---|
| **R0** [0] | Regra peça→causa errada fora do recorte do Wagner (ex.: 16 `contaminacao_particulado` com VS-212) | Mostrar a causa original **e** a corrigida, e validar a regra com o Wagner |
| **R1** [2] | Relato curto e causa genérica, com 62% de inconclusivas no lote (C2-01) | Destacar as peças trocadas (campo objetivo) |
| **R2** [3] | Manual indisponível ou desatualizado | Premissa a validar com a Simone. Versionar o índice. |
| **R3** [3] | Trecho errado recuperado | Sempre exibir a seção. Medir recall@3 no E3. |
| **R4** [4] | **Alucinação** do LLM (T1.2) | Responder só com o que foi recuperado; sem fonte, a resposta é "não encontrado" |
| **R5** [6] | Registro apressado degrada o histórico (C1-04, C2-01) | Sugerir a causa pela peça no momento do registro |
| **R6** [7] | Falso alarme (~6–8% no histórico) e dia sem transmissão | Modo sombra: medir antes de despachar visita |
| Geral | Uso de `id_tecnico` para julgar técnicos | O técnico aparece só como contato, sem ranking |

**Critério de pronto:** ☐ fluxo, componentes, modelo e saída · ☐ riscos localizados no fluxo · ☐ entendível sem explicação oral
