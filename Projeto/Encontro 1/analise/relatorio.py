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

    linha("HIPOTESE 1 — 'tempo medio de atendimento subiu'")
    tendencia = tendencia_duracao_e_volume(dados)
    print(tendencia)
    print(f"\ninclinacao da duracao media (h/mes): {tendencia.attrs['inclinacao_horas_por_mes']}")
    print(f"crescimento do volume de corretivas (ultimo mes / primeiro mes): {tendencia.attrs['crescimento_volume']}x")
    print("leitura: duracao por atendimento quase plana; volume triplicou. Gargalo de capacidade")
    print("e candidato mais forte que 'atendimento individual mais lento'.")

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
