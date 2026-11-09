# Etapa 2: Desafios de reforço (Squad 05 UFC)

Segunda etapa do programa Industr.IA. Em vez de um caso único em vários encontros (Aroeira, Etapa 1), a squad resolve **desafios de reforço curtos**. Cada um dura duas semanas e tem dois encontros com o instrutor. A squad está no nível **Consolidado**.

Repositório oficial da squad: <https://github.com/irede-industr-ia/squad-05-ufc>. Ele está aqui como submódulo em `squad-05-ufc/`. Para atualizar:

```bash
git submodule update --remote "Etapa 2 - Desafios de Reforco/squad-05-ufc"
```

> O submódulo serve só de **leitura e referência**. A entrega oficial (notebook executado, `mlflow.db`, `execucoes.csv`) é gravada no repositório da squad pela **célula de envio do notebook, no Colab**, e só a pessoa entregadora faz isso. Não editar nem dar push pelo submódulo.

## Os três desafios

| # | Pasta aqui | Pasta no repo da squad | Módulo | Pergunta | Status |
|---|---|---|---|---|---|
| 1 | `Desafio 1 - M4 Quantizacao e borda/` | `desafio-1-m4/` | M4 Edge AI | Quantizar o modelo atual ou trocar por um menor, para rodar no coletor sem GPU? | 🔜 **Em andamento** |
| 2 | `Desafio 2 - M2 Agente ou fluxo fixo/` | `desafio-2-m2/` | M2 IA Agentic | Agente com ferramentas ou fluxo fixo para planejar ordens de manutenção? | ⏳ Depois |
| 3 | `Desafio 3 - M3 Erro por recortes/` | `desafio-3-m3/` | M3 Data-centric | O erro está no modelo ou na distribuição do dado entre recortes? | ⏳ Depois |

## Estrutura de cada desafio

```
Desafio N - .../
├── Documentos/    # situação e roteiro de estudos (PDFs oficiais)
├── Preparacao/    # passo a passo, leitura dos dados e rascunhos da squad
└── Artefatos/     # KITs preenchidos e entregues no Classroom
```

## Ritmo de cada desafio (igual para os três)

| Semana | Quando | Quem | O quê | Artefatos |
|---|---|---|---|---|
| 1 | até 4 dias antes do E1 | cada um | situação e leitura principal | n/a |
| 1 | até a véspera | cada um | curso e documentação técnica do roteiro | n/a |
| 1 | véspera | squad | rascunho: decisão, restrição, hipóteses | n/a |
| 1 | **Encontro 1** | squad + instrutor | delimitar e decidir a abordagem; escolher a **pessoa entregadora** | KIT-001, KIT-003 (critério de aceite), KIT-004 (+ KIT-020 se for o 1º desafio) |
| 2 | até 4 dias antes do E2 | cada um | notebook de estudo + notebook do desafio com `ENVIAR = False` | n/a |
| 2 | até 2 dias antes | cada um, depois squad | responder a conclusão sozinho, depois fechar um texto da squad | n/a |
| 2 | véspera | entregadora | rodar tudo numa sessão, `ENVIAR = True`, conferir o commit no GitHub | notebook, `mlflow.db`, `execucoes.csv` |
| 2 | **Encontro 2** | squad + instrutor | defender o resultado contra o critério (**apresentador sorteado**) | KIT-011, KIT-007 |

Regra que vem da Etapa 1 e continua valendo: **o critério de aceite é escrito antes do teste.** O notebook exige o critério na etapa 1, igual ao texto do KIT-003, e o instrutor compara os dois.

## Templates KIT (em branco, da Etapa 1)

| KIT | Nome | Onde está |
|---|---|---|
| KIT-001 | Mapa Técnico do Problema | `../Etapa 1 - Projeto Aroeira/IND-KIT-001-EN1-T1.pdf` |
| KIT-003 | Hipótese Técnica (traz o critério de aceite) | `../Etapa 1 - Projeto Aroeira/IND-KIT-003-EN2-T1.pdf` |
| KIT-004 | Matriz de Alternativas | `../Etapa 1 - Projeto Aroeira/Encontro 2/Documentos/IND-KIT-004-EN2-T2.docx.pdf` |
| KIT-007 | Decisão Justificada | `../Etapa 1 - Projeto Aroeira/Encontro 2/Documentos/IND-KIT-007-EN3-T1.docx.pdf` |
| KIT-011 | Matriz de Teste | `../Etapa 1 - Projeto Aroeira/Encontro 3/Documentos/IND-KIT-011-EN4-T1.docx.pdf` |
| KIT-020 | Acordo de squad | `../Etapa 1 - Projeto Aroeira/IND-KIT-020-EN1-T3.pdf` |
