from random import randint


def bola_blanca(blancas: int, negras: int) -> bool:
    """Devuelve si la bola que sale es blanca o no."""
    return randint(1, blancas + negras) <= blancas


def jugador(jugada: int) -> str:
    """Devuelve el jugador que gana en la jugada dada."""
    if jugada % 3 == 0:
        return "C"
    elif jugada % 3 == 1:
        return "A"
    else:
        return "B"


def huygens2(
    blancas: int,
    negras: int,
    max_jugadas: int = 1000,
) -> str:
    """Juega una partida del segundo problema de Huygens y devuelve
    si el ganador es "A", "B" o "C" o "N" (ninguno)."""
    for i in range(1, max_jugadas + 1):
        if bola_blanca(blancas, negras):
            return jugador(i)
        
    return "N"


def ratio_resultados(
    blancas: int,
    negras: int,
    max_jugadas: int = 1000,
    partidas: int = 10000,
) -> dict:
    """Devuelve un diccionario con los resultados de jugar un número
    determinado de partidas. Los resultados son el ratio de victorias
    cada jugador con respecto al total de partidas."""
    resultados = {"A": 0, "B": 0, "C": 0, "N": 0}
    for _ in range(partidas):
        resultados[huygens2(blancas, negras, max_jugadas)] += 1

    for jugador in resultados:
        resultados[jugador] /= partidas

    return resultados


def p_blanca(blancas: int, negras: int) -> float:
    """Devuelve la probabilidad de que la bola que sale sea blanca."""
    return blancas / (blancas + negras)

def q_blanca(blancas: int, negras: int) -> float:
    """Devuelve la probabilidad de que la bola que sale sea negra."""
    return 1 - p_blanca(blancas, negras)

def resultados_esperados(jugador: str, blancas: int, negras: int) -> float:
    """Devuelve el resultado esperado para el jugador dado."""
    if jugador == "A":
        q_up = 1
    elif jugador == "B":
        q_up = q_blanca(blancas, negras)
    elif jugador == "C":
        q_up = q_blanca(blancas, negras)**2
    else:
        q_up = 0

    p = p_blanca(blancas, negras)
    q = q_blanca(blancas, negras)
    return (p * q_up) / (1 - q**3)


def resultados_latex(
    turnos_partidas: list[int],
    resultados: list[dict],
    resultados_esperados: dict
) -> str:
    latex = "\\begin{tabular}{cccc}\n"
    latex += "\\toprule\n"
    latex += "Partidas jugadas & $A$ & $B$ & $C$ \\\\\n"
    latex += "\\midrule\n"
    for i, partida in enumerate(resultados):
        latex += f"${turnos_partidas[i]}$ & ${partida['A']:.3f}$ & \
${partida['B']:.3f}$ & \
${partida['C']:.3f}$ \\\\\n"
    latex += "\\midrule\n"
    latex += f"Esperado & ${resultados_esperados['A']:.3f}$ & \
${resultados_esperados['B']:.3f}$ & \
${resultados_esperados['C']:.3f}$ \\\\\n"
    latex += "\\bottomrule\n"
    latex += "\\end{tabular}\n"

    return latex


def main():
    """Función principal del programa."""
    blancas = 4
    negras = 8
    max_jugadas = 1000
    partidas = [10**i for i in range(1, 6)]

    resultados = []
    for turnos in partidas:
        resultados.append(ratio_resultados(
            blancas, negras, max_jugadas, turnos
        ))

    resultados_reales = {
        "A": resultados_esperados("A", blancas, negras),
        "B": resultados_esperados("B", blancas, negras),
        "C": resultados_esperados("C", blancas, negras),
    }

    print(resultados_latex(
        partidas,
        resultados,
        resultados_reales,
    ))

if __name__ == "__main__":
    main()
