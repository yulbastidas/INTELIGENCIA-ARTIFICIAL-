"""Gráficas sencillas para archivos PNG y el panel Gráficos de Spyder."""

from pathlib import Path
import matplotlib.pyplot as plt
from .datos import CURSOS, SALAS, FRANJAS


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
            [h["mejor_penalizacion"] for h in resultado["historial"]], label="Mejor acumulada")
    ax.set(title="Convergencia - Asignación de Cursos a Salas",
           xlabel="Generación (0 = población inicial)", ylabel="Penalización (menor es mejor)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    terminar(fig, destino, mostrar)


def graficar_comparacion(resumen, destino=None, mostrar=False):
    fig, ejes = plt.subplots(1, 2, figsize=(11, 5))
    for ax, campo, titulo in zip(ejes, ("penalizacion_promedio", "generacion_promedio_mejor"),
                                 ("Penalización promedio", "Generación media del mejor resultado")):
        barras = ax.bar(["Sin elitismo", "Con elitismo"], [float(r[campo]) for r in resumen],
                        color=["#de8f05", "#0173b2"])
        ax.bar_label(barras, fmt="%.2f", padding=3)
        ax.set(title=titulo, ylabel=titulo)
        ax.set_ylim(0, max(1, max(float(r[campo]) for r in resumen) * 1.25))
        ax.grid(axis="y", alpha=0.3)
    fig.suptitle("Cursos y salas: comparación de elitismo")
    terminar(fig, destino, mostrar)


def graficar_horario(resultado, destino=None, mostrar=False):
    celdas = [[[] for _ in SALAS] for _ in FRANJAS]
    for i, (sala, franja) in enumerate(resultado["mejor_individuo"]):
        celdas[franja][sala].append(CURSOS[i]["nombre"])
    textos = [["\n".join(cursos) or ("BLOQUEADA" if f in SALAS[s]["franjas_bloqueadas"] else "Libre")
               for s, cursos in enumerate(fila)] for f, fila in enumerate(celdas)]
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.axis("off")
    tabla = ax.table(cellText=textos, rowLabels=FRANJAS,
                     colLabels=[s["nombre"] for s in SALAS], cellLoc="center", loc="center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 3)
    for f, fila in enumerate(celdas):
        for s, cursos in enumerate(fila):
            tabla[f + 1, s].set_facecolor("#f8d7da" if len(cursos) > 1 else "#e8f1f8")
    ax.set_title(f"Horario - Cursos y Salas | Penalización total: {resultado['penalizacion']}\n"
                 "Consultar horario.csv para el detalle de incumplimientos", pad=20)
    terminar(fig, destino, mostrar)


def mostrar_guardadas(directorio):
    for nombre in ("convergencia.png", "horario.png", "comparacion_elitismo.png"):
        ruta = Path(directorio) / nombre
        if ruta.exists():
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(plt.imread(ruta))
            ax.axis("off")
            terminar(fig, None, True)
