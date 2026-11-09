"""Roda todas as analises e imprime um relatorio texto, hipotese por hipotese.

Uso:
    python relatorio.py
"""

from carregar_dados import carregar_tudo, validar_integridade
from analise import (
    tendencia_duracao_e_volume,
    perfil_tecnicos,
    reincidencia_por_equipamento,
    contaminacao_por_ambiente,
    alerta_telemetria_antes_de_corretiva,
    panorama_garantia,
    indicador_painel_oficial,
    mix_tipo_ordem_por_mes,
)


def linha(titulo: str) -> None:
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def main() -> None:
    dados = carregar_tudo()

    linha("VALIDACAO DE INTEGRIDADE (regras da camada 0)")
    avisos = validar_integridade(dados)
    print("nenhum desvio encontrado." if not avisos else "\n".join(f"- {a}" for a in avisos))

    linha("HIPOTESE 1 — 'tempo medio de atendimento subiu' (C0-05 / C1-02)")
    print("indicador oficial do painel (C1-02) reproduzido a partir de D3 — media sobre TODAS as ordens:")
    painel = indicador_painel_oficial(dados)
    print(painel)
    print("(valores oficiais do painel: 3.4, 3.7, 3.9, 3.8, 3.7, 4.2, 4.2, 3.8, 4.3, 4.4, 4.2, 4.5 — media 4.0h)")

    print("\nmix de tipo_ordem por mes (proporcao):")
    proporcao, duracao_por_tipo = mix_tipo_ordem_por_mes(dados)
    print(proporcao)
    print("\nduracao media por tipo_ordem e mes (estavel dentro de cada tipo?):")
    print(duracao_por_tipo)
    print("\nleitura: a duracao de CADA tipo de ordem fica estavel no tempo (corretiva ~5.6-6.1h,")
    print("preventiva ~2.4-2.6h, inspecao ~1.3-1.4h o tempo todo). O que sobe e a PROPORCAO de")
    print("corretivas no mix (36.9% -> 59.0%), que subtrai espaco de preventivas (35.2% -> 23.0%).")
    print("Como corretiva demora ~2.4x mais que preventiva, essa mudanca de mix explica")
    print("mecanicamente a subida do indicador do painel — nao e atendimento mais lento.")

    print("\n(para referencia: analise anterior, so sobre corretivas)")
    tendencia = tendencia_duracao_e_volume(dados)
    print(tendencia)
    print(f"crescimento do volume de corretivas (ultimo mes / primeiro mes): {tendencia.attrs['crescimento_volume']}x")

    linha("HIPOTESE 2 — 'entraram tecnicos sem experiencia na serie CP'")
    tecnicos = perfil_tecnicos(dados)
    print(tecnicos)
    print(f"\ncorrelacao (ordem de entrada x duracao media): {tecnicos.attrs['correlacao_entrada_x_duracao']}")
    print("leitura: todos os tecnicos aparecem desde o 1o mes do periodo; a hipotese nao e")
    print("testavel com os dados atuais (falta campo de contratacao/senioridade) — registrar")
    print("como lacuna de dado, nao aceitar nem negar sem evidencia.")

    linha("HIPOTESE 3 — 'reincidencia de chamados no mesmo equipamento'")
    pares = reincidencia_por_equipamento(dados)
    quente = pares[pares["reincidencia_quente"]]
    print(f"pares consecutivos de corretiva no mesmo equipamento: {len(pares)}")
    print(f"mesma causa que o atendimento anterior: {pares['mesma_causa'].sum()} ({pares['mesma_causa'].mean()*100:.1f}%)")
    print(f"reincidencia 'quente' (mesma causa em ate 30 dias): {len(quente)} ({len(quente)/len(pares)*100:.1f}%)")
    print(quente["causa"].value_counts())
    print("leitura: reincidencia confirmada e concentrada em 3 causas — aponta para eficacia")
    print("do reparo nessas causas, nao para falta de informacao do tecnico.")

    linha("ACHADO ADICIONAL — contaminacao por particulado x classe de ambiente")
    print(contaminacao_por_ambiente(dados))
    print("leitura: contra-intuitivo — particulado_alto NAO tem mais contaminacao que")
    print("particulado_baixo. Desconfiar de explicacao ambiental simplista.")

    linha("ACHADO ADICIONAL — telemetria como sinal de alerta antes da corretiva")
    alerta = alerta_telemetria_antes_de_corretiva(dados)
    print(alerta if not alerta.empty else "amostra insuficiente")
    print("leitura: sinal de alerta (alta de temperatura) aparece para falha_valvula_admissao")
    print("e falha_vedacao (amostra pequena, tratar como pista); quase nulo para")
    print("falha_eletrica/vazamento_oleo/contaminacao_particulado — as 3 causas mais frequentes.")

    linha("ACHADO ADICIONAL — panorama de garantia")
    garantia = panorama_garantia(dados)
    print("distribuicao das decisoes:")
    print(garantia["distribuicao_decisao"])
    print("\nmotivo por decisao:")
    print(garantia["motivo_por_decisao"])
    print("\ncontestacao do cliente por decisao:")
    print(garantia["contestacao_por_decisao"])


if __name__ == "__main__":
    main()
