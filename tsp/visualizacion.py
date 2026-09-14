"""Gráficas compatibles con Matplotlib y el panel Gráficos de Spyder."""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from .datos import obtener_coordenadas


def terminar_figura(fig, destino, mostrar):
    fig.tight_layout()
    if destino is not None:
        Path(destino).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(destino, dpi=150)
    if mostrar:
        plt.show()
    plt.close(fig)


def graficar_convergencia(resultado, destino=None, mostrar=False):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot([h["generacion"] for h in resultado["historial"]],
            [h["mejor_distancia"] for h in resultado["historial"]], label="Mejor distancia acumulada")
    ax.set(title="Convergencia del Algoritmo Genético - TSP",
           xlabel="Generación (0 = población inicial)", ylabel="Distancia (menor es mejor)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    terminar_figura(fig, destino, mostrar)


def graficar_ruta(resultado, destino=None, mostrar=False):
    coordenadas = obtener_coordenadas(resultado["numero_ciudades"])
    ruta = resultado["mejor_ruta"]
    cerrada = coordenadas[ruta + [ruta[0]]]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(cerrada[:, 0], cerrada[:, 1], "o-", label=f"Distancia: {resultado['mejor_distancia']:.4f}")
    ax.scatter(*coordenadas[ruta[0]], s=120, marker="s", label="Inicio / regreso", zorder=3)
    for ciudad, (x, y) in enumerate(coordenadas):
        ax.annotate(str(ciudad), (x, y), xytext=(6, 6), textcoords="offset points")
    ax.set(title="Mejor Ruta Encontrada - TSP", xlabel="X", ylabel="Y")
    ax.set_aspect("equal", adjustable="datalim")
    ax.margins(0.15)
    ax.grid(True, alpha=0.3)
    ax.legend()
    terminar_figura(fig, destino, mostrar)


def graficar_comparacion(resumen, destino=None, mostrar=False):
    fig, ax = plt.subplots(figsize=(8, 5))
    posiciones = np.arange(2)
    for i, tipo in enumerate(("swap", "inversion")):
        filas = sorted((r for r in resumen if r["tipo_mutacion"] == tipo), key=lambda r: float(r["tasa_mutacion"]))
        barras = ax.bar(posiciones + (i - 0.5) * 0.35,
                        [float(r["distancia_promedio"]) for r in filas], width=0.35, label=tipo)
        ax.bar_label(barras, fmt="%.2f", padding=3)
    ax.set(xticks=posiciones, xticklabels=["0.05", "0.20"],
           xlabel="Tasa de mutación", ylabel="Distancia promedio (menor es mejor)",
           title="TSP: comparación de mutaciones")
    ax.set_ylim(bottom=0)
    ax.margins(y=0.15)
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    terminar_figura(fig, destino, mostrar)
