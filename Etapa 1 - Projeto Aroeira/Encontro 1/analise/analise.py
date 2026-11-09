"""Funcoes de analise que testam, com dado, as tres justificativas da diretoria (C0-05)
e levantam achados adicionais sobre o caso Aroeira.

Cada funcao recebe o dict retornado por carregar_dados.carregar_tudo() e devolve um
DataFrame ou dict pronto para inspecionar, plotar ou citar como proveniencia
(conjunto.campo) num instrumento do encontro.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def ordens_corretivas(dados: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Subconjunto de D3 com tipo_ordem == 'corretiva', com coluna 'mes' auxiliar."""
    d3 = dados["ordens"]
    corr = d3[d3["tipo_ordem"] == "corretiva"].copy()
    corr["mes"] = corr["data_abertura"].dt.to_period("M")
    return corr


def tendencia_duracao_e_volume(dados: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Hipotese 1 (tempo medio subiu): duracao media e volume de corretivas por mes.

    Testa se a duracao por atendimento subiu, ou se foi o volume que cresceu
    (com equipe estavel), o que aponta para gargalo de capacidade em vez de
    atendimento individual mais lento.
    """
    corr = ordens_corretivas(dados)
    tabela = corr.groupby("mes").agg(
        duracao_media_horas=("duracao_horas", "mean"),
        n_ordens=("id_ordem", "count"),
    )
    x = np.arange(len(tabela))
    inclinacao = np.polyfit(x, tabela["duracao_media_horas"].values, 1)[0]
    tabela.attrs["inclinacao_horas_por_mes"] = round(float(inclinacao), 4)
    tabela.attrs["crescimento_volume"] = round(
        tabela["n_ordens"].iloc[-1] / tabela["n_ordens"].iloc[0], 2
    )
    return tabela


def perfil_tecnicos(dados: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Hipotese 2 (tecnicos novos sem experiencia): perfil por id_tecnico.

    Sem um campo de data de contratacao, a melhor proxy disponivel e a data da
    primeira ordem registrada. Retorna tambem a correlacao entre essa proxy de
    "novidade" e o desempenho (duracao media, proporcao de causa nao identificada).
    """
    corr = ordens_corretivas(dados)
    perfil = corr.groupby("id_tecnico").agg(
        primeira_ordem=("data_abertura", "min"),
        ultima_ordem=("data_abertura", "max"),
        n_ordens=("id_ordem", "count"),
        duracao_media=("duracao_horas", "mean"),
        prop_causa_nao_identificada=("causa_registrada", lambda s: (s == "causa_nao_identificada").mean()),
    ).sort_values("primeira_ordem")

    perfil["rank_entrada"] = perfil["primeira_ordem"].rank()
    perfil.attrs["correlacao_entrada_x_duracao"] = round(
        float(perfil[["rank_entrada", "duracao_media"]].corr().iloc[0, 1]), 3
    )
    return perfil


def reincidencia_por_equipamento(dados: dict[str, pd.DataFrame], janela_dias: int = 30) -> pd.DataFrame:
    """Hipotese 3 (reincidencia no mesmo equipamento): pares consecutivos de corretiva
    no mesmo equipamento, com a distancia em dias e se repetem a mesma causa.

    `janela_dias` define o que conta como reincidencia "quente" (reparo que
    provavelmente nao eliminou a causa raiz).
    """
    corr = ordens_corretivas(dados).sort_values(["id_equipamento", "data_abertura"])

    linhas = []
    for equipamento, grupo in corr.groupby("id_equipamento"):
        grupo = grupo.reset_index(drop=True)
        for i in range(1, len(grupo)):
            delta_dias = (grupo.loc[i, "data_abertura"] - grupo.loc[i - 1, "data_abertura"]).days
            linhas.append({
                "id_equipamento": equipamento,
                "causa": grupo.loc[i, "causa_registrada"],
                "causa_anterior": grupo.loc[i - 1, "causa_registrada"],
                "delta_dias": delta_dias,
                "mesma_causa": grupo.loc[i, "causa_registrada"] == grupo.loc[i - 1, "causa_registrada"],
            })

    pares = pd.DataFrame(linhas)
    pares["reincidencia_quente"] = pares["mesma_causa"] & (pares["delta_dias"] <= janela_dias)
    return pares


def contaminacao_por_ambiente(dados: dict[str, pd.DataFrame]) -> pd.Series:
    """Achado adicional: contaminacao_particulado e mais comum em plantas de
    classe_ambiente particulado_alto? (Testa uma hipotese ambiental 'obvia'.)
    """
    d1, d3 = dados["frota"], dados["ordens"]
    corr = d3[d3["tipo_ordem"] == "corretiva"].merge(
        d1[["id_equipamento", "classe_ambiente"]], on="id_equipamento", how="left"
    )
    tabela = pd.crosstab(corr["classe_ambiente"], corr["causa_registrada"], normalize="index")
    return tabela["contaminacao_particulado"].round(3)


def alerta_telemetria_antes_de_corretiva(
    dados: dict[str, pd.DataFrame],
    janela_recente_dias: int = 7,
    janela_base_inicio: int = 60,
    janela_base_fim: int = 30,
    minimo_pontos: int = 3,
) -> pd.DataFrame:
    """Achado adicional: a temperatura de descarga sobe antes de uma corretiva?

    Compara a media de temp_descarga_maxima nos `janela_recente_dias` dias antes
    do atendimento contra uma linha de base (entre `janela_base_inicio` e
    `janela_base_fim` dias antes). Um delta positivo e consistente por causa e
    candidato a sinal de alerta para manutencao preditiva seletiva.

    So considera equipamentos com tem_telemetria=1 e exige pelo menos
    `minimo_pontos` leituras em cada janela (para nao comparar ruido).
    """
    d1, d2 = dados["frota"], dados["telemetria"]
    corr = ordens_corretivas(dados)

    equipamentos_com_telemetria = set(d1.loc[d1["tem_telemetria"] == 1, "id_equipamento"])
    corr_tel = corr[corr["id_equipamento"].isin(equipamentos_com_telemetria)]

    resultados = []
    for _, ordem in corr_tel.iterrows():
        equipamento = ordem["id_equipamento"]
        abertura = ordem["data_abertura"]

        recente = d2[
            (d2["id_equipamento"] == equipamento)
            & (d2["data"] < abertura)
            & (d2["data"] >= abertura - pd.Timedelta(days=janela_recente_dias))
        ]
        base = d2[
            (d2["id_equipamento"] == equipamento)
            & (d2["data"] < abertura - pd.Timedelta(days=janela_base_fim))
            & (d2["data"] >= abertura - pd.Timedelta(days=janela_base_inicio))
        ]

        if len(recente) >= minimo_pontos and len(base) >= minimo_pontos:
            resultados.append({
                "causa": ordem["causa_registrada"],
                "delta_temp_max": recente["temp_descarga_maxima"].mean() - base["temp_descarga_maxima"].mean(),
                "delta_pressao_media": recente["pressao_descarga_media"].mean() - base["pressao_descarga_media"].mean(),
            })

    detalhado = pd.DataFrame(resultados)
    if detalhado.empty:
        return detalhado

    resumo = detalhado.groupby("causa").agg(
        delta_temp_max_medio=("delta_temp_max", "mean"),
        delta_pressao_media_medio=("delta_pressao_media", "mean"),
        n_amostras=("causa", "count"),
    ).round(2).sort_values("delta_temp_max_medio", ascending=False)
    return resumo


def indicador_painel_oficial(dados: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Reproduz o indicador 'tempo medio de atendimento' tal como o painel da
    Aroeira o define (C1-02): media de duracao_horas sobre TODAS as ordens
    abertas no mes, nao apenas as corretivas.

    Usar este indicador (e nao `tendencia_duracao_e_volume`, que filtra só
    corretivas) para comparar contra os valores oficiais do painel citados
    pela diretoria.
    """
    d3 = dados["ordens"].copy()
    d3["mes"] = d3["data_abertura"].dt.to_period("M")
    return d3.groupby("mes")["duracao_horas"].mean().round(2).to_frame("tempo_medio_atendimento_h")


def mix_tipo_ordem_por_mes(dados: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Testa a hipotese de 'mix-shift': a proporcao de corretivas (o tipo de
    ordem mais demorado) cresce no tempo, enquanto a duracao media de CADA
    tipo de ordem permanece estavel?

    Retorna duas tabelas lado a lado: a proporcao de cada tipo_ordem por mes
    e a duracao media de cada tipo_ordem por mes.
    """
    d3 = dados["ordens"].copy()
    d3["mes"] = d3["data_abertura"].dt.to_period("M")

    proporcao = pd.crosstab(d3["mes"], d3["tipo_ordem"], normalize="index").round(3)
    duracao = d3.groupby(["mes", "tipo_ordem"])["duracao_horas"].mean().unstack().round(2)

    return proporcao, duracao


def panorama_garantia(dados: dict[str, pd.DataFrame]) -> dict:
    """Achado adicional: como se distribuem as decisoes de garantia e a contestacao."""
    d4 = dados["garantia"]
    return {
        "distribuicao_decisao": d4["decisao_cobertura"].value_counts(normalize=True).round(3),
        "motivo_por_decisao": pd.crosstab(d4["decisao_cobertura"], d4["motivo_decisao"]),
        "contestacao_por_decisao": d4.groupby("decisao_cobertura")["contestado_pelo_cliente"].mean().round(3),
    }
