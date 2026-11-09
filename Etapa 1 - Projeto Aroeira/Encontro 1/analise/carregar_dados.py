"""Carregamento e validacao basica dos 4 datasets do caso Aroeira."""

from pathlib import Path
import pandas as pd

PASTA_DADOS_PADRAO = Path(__file__).resolve().parent.parent / "Dados"


def carregar_tudo(pasta_dados: Path | str = PASTA_DADOS_PADRAO) -> dict[str, pd.DataFrame]:
    """Le d1_frota, d2_telemetria, d3_ordens e d4_garantia com os tipos corretos."""
    pasta = Path(pasta_dados)

    d1 = pd.read_csv(pasta / "d1_frota.csv", parse_dates=["data_inicio_garantia"])
    d2 = pd.read_csv(pasta / "d2_telemetria.csv", parse_dates=["data"])
    d3 = pd.read_csv(pasta / "d3_ordens.csv", parse_dates=["data_abertura"])
    d4 = pd.read_csv(pasta / "d4_garantia.csv", parse_dates=["data"])

    return {"frota": d1, "telemetria": d2, "ordens": d3, "garantia": d4}


def validar_integridade(dados: dict[str, pd.DataFrame]) -> list[str]:
    """Confere as regras de consistencia descritas na camada 0 (C0-07 a C0-10).

    Retorna uma lista de avisos (vazia se tudo bateu com o esperado).
    """
    d1, d2, d3, d4 = dados["frota"], dados["telemetria"], dados["ordens"], dados["garantia"]
    avisos = []

    # C0-07: ano_instalacao deve coincidir com o ano de data_inicio_garantia
    divergente = d1[d1["ano_instalacao"] != d1["data_inicio_garantia"].dt.year]
    if len(divergente):
        avisos.append(f"{len(divergente)} equipamento(s) com ano_instalacao != ano de data_inicio_garantia")

    # C0-07: equipamento sem telemetria nao deve aparecer em D2
    sem_telemetria = set(d1.loc[d1["tem_telemetria"] == 0, "id_equipamento"])
    aparecem_em_d2 = set(d2["id_equipamento"]) & sem_telemetria
    if aparecem_em_d2:
        avisos.append(f"{len(aparecem_em_d2)} equipamento(s) sem telemetria aparecem em D2: {sorted(aparecem_em_d2)[:5]}...")

    # C0-08: linha com transmissao_incompleta=1 deve ter os 6 campos de medicao vazios
    campos_medicao = [
        "horas_operacao", "ciclo_trabalho_medio", "pressao_descarga_media",
        "temp_descarga_media", "temp_descarga_maxima", "contagem_partidas",
    ]
    incompletas = d2[d2["transmissao_incompleta"] == 1]
    com_medicao_presente = incompletas[campos_medicao].notna().any(axis=1).sum()
    if com_medicao_presente:
        avisos.append(f"{com_medicao_presente} linha(s) com transmissao_incompleta=1 mas com alguma medicao preenchida")

    completas = d2[d2["transmissao_incompleta"] == 0]
    com_medicao_vazia = completas[campos_medicao].isna().any(axis=1).sum()
    if com_medicao_vazia:
        avisos.append(f"{com_medicao_vazia} linha(s) com transmissao_incompleta=0 mas com alguma medicao vazia")

    # C0-09: pecas_trocadas vazio so deveria aparecer fora de ordem corretiva
    vazio_em_corretiva = d3[(d3["tipo_ordem"] == "corretiva") & (d3["pecas_trocadas"].isna())]
    if len(vazio_em_corretiva):
        avisos.append(f"{len(vazio_em_corretiva)} ordem(ns) corretiva(s) sem peca trocada registrada")

    # C0-10: D4 so deveria existir sobre ordem corretiva
    ordens_corretivas = set(d3.loc[d3["tipo_ordem"] == "corretiva", "id_ordem"])
    pedidos_fora_de_corretiva = d4[~d4["id_ordem"].isin(ordens_corretivas)]
    if len(pedidos_fora_de_corretiva):
        avisos.append(f"{len(pedidos_fora_de_corretiva)} pedido(s) de garantia sobre ordem que nao e corretiva")

    # cada ordem corretiva deve ter no maximo 1 pedido
    duplicados = d4["id_ordem"].value_counts()
    duplicados = duplicados[duplicados > 1]
    if len(duplicados):
        avisos.append(f"{len(duplicados)} ordem(ns) com mais de um pedido de garantia")

    return avisos


if __name__ == "__main__":
    dados = carregar_tudo()
    for nome, df in dados.items():
        print(f"{nome}: {df.shape[0]} linhas, {df.shape[1]} colunas")

    print("\nValidacao de integridade (regras da camada 0):")
    avisos = validar_integridade(dados)
    if not avisos:
        print("  nenhum desvio encontrado.")
    else:
        for a in avisos:
            print(f"  - {a}")
