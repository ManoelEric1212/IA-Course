# Encontro 3 — Artefatos do Squad 5 (UFC Sobral)

> 15/10/2026. Pergunta do dia: **"A escolha se sustenta?"**
> Versão em markdown dos instrumentos do E3, preenchida com os resultados do notebook KIT-023 rodados em sala. Serve de base para transcrever nos templates oficiais (Classroom).

## Arquivos

| # | Arquivo | Instrumento | Template |
|---|---|---|---|
| 01 | `01_registro_decisao_E2.md` | Registro nos pontos de incerteza da Decisão Justificada do E2 (camada 3, IA rejeitada, troca de métrica) | KIT-007 (edição) |
| 02 | `02_quem_pede_explicacao.md` | Discussão do slide 12: quem pede explicação das decisões de garantia | — (atividade de abertura) |
| 03 | `03_resultados_notebook.md` | O que cada caminho executou, saídas obtidas e respostas das células | KIT-023 |
| 04 | `04_matriz_de_teste.md` | Matriz de Teste | KIT-011 |
| 05 | `05_matriz_de_validacao.md` | Matriz de Validação | KIT-012 |
| 06 | `06_proposta_tecnica_final.md` | Proposta Técnica Final | KIT-015 (template ausente; estrutura da apresentação) |
| 07 | `07_roteiro_de_pitch.md` | Roteiro de Pitch e preparação da defesa | KIT-016 |
| 08 | `08_principios_transferiveis.md` | Registro de princípios transferíveis | KIT-021 (template ausente; formato da apresentação) |

## Linhagem das informações (para não descompassar entre encontros)
- **E1 (01/10), entregue:** Mapa Técnico do Problema (KIT-001), Hipótese Técnica com H1/H2/H3 (KIT-003). PDFs em `Projeto/Encontro 1/entregaveis1/`.
- **E2 (08/10), entregue:** Matriz de Alternativas (KIT-004), que reformulou as hipóteses em Alt. 1/2/3; Decisão Justificada (KIT-007); Canvas (KIT-008). PDFs em `Projeto/Encontro 2/Artefatos/`.
- **E3 (15/10):** as hipóteses testadas são **as alternativas da Matriz do E2**, por orientação do articulador. O critério "Recall > 80%" (H1 do E1, incerteza da Decisão do E2) foi **substituído antes do teste** pela precisão, também por orientação do articulador.

## Resultado em uma linha
A decisão do E2 **se sustenta**:
- **Alt. 1, alerta:** tem sinal (precisão 0,50 com sensibilidade 0,603; prevalência 0,088), mas continua em paralelo por causa do lote novo da VS-212.
- **Alt. 2, assistente:** precisa da causa corrigida pela peça (64% de causa genérica nas ordens dessas peças, contra 14% nas demais corretivas).

## Pendências antes de entregar
- [ ] Preencher identificação (integrantes e papéis do dia) em cada instrumento
- [ ] Trocar `[nº da saída]` pelo número real da saída do notebook
- [ ] Confirmar com o mentor os nomes em "quem aceita" os riscos residuais
- [ ] Transcrever para os templates oficiais e marcar as 5 atividades como entregues
