"""PNG y gráficas compatibles con el panel Gráficos de Spyder."""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from .datos import OBJETOS, CAPACIDADES


def terminar(fig, destino, mostrar):
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
            [h["mejor_valor_valido"] for h in resultado["historial"]], label="Mejor valor válido acumulado")
    ax.set(title="Convergencia - Problema de la Mochila", xlabel="Generación (0 = población inicial)",
           ylabel="Valor válido (mayor es mejor)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    terminar(fig, destino, mostrar)


def graficar_comparacion(resumen, destino=None, mostrar=False):
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(CAPACIDADES))
    for i, metodo in enumerate(("penalizacion", "reparacion")):
        filas = sorted((r for r in resumen if r["metodo"] == metodo), key=lambda r: int(r["capacidad"]))
        barras = ax.bar(x + (i - 0.5) * 0.35, [float(r["valor_promedio"]) for r in filas], width=0.35, label=metodo)
        ax.bar_label(barras, fmt="%.2f", padding=3)
    ax.set(title="Comparación de métodos - Problema de la Mochila", xlabel="Capacidad",
           ylabel="Valor promedio (mayor es mejor)", xticks=x, xticklabels=CAPACIDADES)
    ax.margins(y=0.2)
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    terminar(fig, destino, mostrar)


def graficar_objetos(resultado, destino=None, mostrar=False):
    objetos = [o for gen, o in zip(resultado["mejor_individuo"], OBJETOS) if gen]
    fig, ejes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    for ax, clave in zip(ejes, ("peso", "valor")):
        if objetos:
            barras = ax.barh([o["nombre"] for o in objetos], [o[clave] for o in objetos])
            ax.bar_label(barras, padding=3)
            ax.margins(x=0.2)
        else:
            ax.text(0.5, 0.5, "Mochila vacía", ha="center", transform=ax.transAxes)
        ax.set_xlabel(clave.capitalize())
        ax.grid(axis="x", alpha=0.3)
    fig.suptitle(f"Objetos seleccionados | peso {resultado['peso_total']}/{resultado['capacidad']} | valor {resultado['valor_total']}")
    terminar(fig, destino, mostrar)


def mostrar_guardadas(directorio):
    for nombre in ("convergencia.png", "objetos_seleccionados.png", "comparacion_metodos.png"):
        ruta = Path(directorio) / nombre
        if ruta.exists():
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(plt.imread(ruta))
            ax.axis("off")
            terminar(fig, None, True)
