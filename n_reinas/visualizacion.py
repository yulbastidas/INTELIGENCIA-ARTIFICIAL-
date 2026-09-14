"""Gráficas independientes de la ejecución del algoritmo."""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def graficar_convergencia(resultado, destino=None, mostrar=False):
    historial = resultado["historial"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot([h["generacion"] for h in historial],
            [h["conflictos_generacion"] for h in historial],
            label="Mejor de la generación", marker=".")
    ax.plot([h["generacion"] for h in historial],
            [h["mejores_conflictos"] for h in historial],
            label="Mejor acumulado", linestyle="--")
    ax.set(title=f"N-Reinas: N={resultado['n']}, población={resultado['poblacion']}, "
                 f"mutación={resultado['tasa_mutacion']}",
           xlabel="Generación (0 = población inicial)", ylabel="Conflictos (menor es mejor)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    if destino is not None:
        Path(destino).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(destino, dpi=150)
    if mostrar:
        plt.show()
    plt.close(fig)


def graficar_tablero(resultado, destino=None, mostrar=False):
    n = resultado["n"]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(np.indices((n, n)).sum(axis=0) % 2, cmap="Pastel1", vmin=0, vmax=1)
    ax.scatter(range(n), resultado["mejor_solucion"], s=180, color="black", marker="*")
    ax.set(xticks=range(n), yticks=range(n), xlabel="Columna", ylabel="Fila",
           title=f"N={n}: {resultado['conflictos']} conflictos")
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", alpha=0.4)
    fig.tight_layout()
    if destino is not None:
        Path(destino).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(destino, dpi=150)
    if mostrar:
        plt.show()
    plt.close(fig)
