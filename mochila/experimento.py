"""40 corridas, estadísticas y conclusiones calculadas de resultados reales."""

import csv
import json
from pathlib import Path
from statistics import mean, stdev
from .datos import CAPACIDADES, FACTOR_PENALIZACION
from .algoritmo import resolver_mochila
from .visualizacion import graficar_convergencia, graficar_objetos, graficar_comparacion

DIRECTORIO = Path(__file__).resolve().parents[1] / "resultados" / "mochila"


def escribir_csv(ruta, filas):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)


def fila_resultado(r):
    return {k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v
            for k, v in r.items() if k != "historial"}


def guardar_ejecucion(resultado, directorio=DIRECTORIO):
    directorio = Path(directorio)
    escribir_csv(directorio / "ejecucion.csv", [fila_resultado(resultado)])
    escribir_csv(directorio / "historial.csv", resultado["historial"])
    graficar_convergencia(resultado, directorio / "convergencia.png")
    graficar_objetos(resultado, directorio / "objetos_seleccionados.png")


def resumir(registros):
    resumen = []
    for capacidad in CAPACIDADES:
        for metodo in ("penalizacion", "reparacion"):
            grupo = [r for r in registros if r["capacidad"] == capacidad and r["metodo"] == metodo]
            valores = [r["valor_total"] for r in grupo]
            resumen.append({"capacidad": capacidad, "metodo": metodo, "repeticiones": len(grupo),
                            "mejor_valor": max(valores), "peor_valor": min(valores),
                            "valor_promedio": mean(valores), "desviacion_estandar_muestral": stdev(valores),
                            "peso_promedio": mean(r["peso_total"] for r in grupo),
                            "generacion_promedio_mejor": mean(r["generacion_mejor"] for r in grupo),
                            "tiempo_promedio_segundos": mean(r["tiempo_segundos"] for r in grupo)})
    return resumen


def escribir_analisis(registros, resumen, directorio):
    lineas = ["# Mochila: análisis de la fase 4", "",
              f"{len(registros)} corridas reales: capacidades 30 y 45, dos métodos, "
              f"población {registros[0]['poblacion']}, {registros[0]['max_generaciones']} generaciones, "
              f"mutación {registros[0]['tasa_mutacion']} por gen y elitismo {registros[0]['elitismo']}. "
              "Semillas registradas en experimentos.csv.", "",
              "| Capacidad | Método | Mejor | Peor | Promedio | Desv. muestral | Peso medio | Generación media | Tiempo medio (s) |",
              "|---|---|---|---|---|---|---|---|---|"]
    for r in resumen:
        lineas.append(f"| {r['capacidad']} | {r['metodo']} | {r['mejor_valor']} | {r['peor_valor']} | "
                      f"{r['valor_promedio']:.3f} | {r['desviacion_estandar_muestral']:.3f} | "
                      f"{r['peso_promedio']:.2f} | {r['generacion_promedio_mejor']:.2f} | {r['tiempo_promedio_segundos']:.6f} |")
    lineas += ["", "## 1. ¿Por qué cromosomas binarios?", "",
               "Cada uno de los 15 genes decide seleccionar (1) o no seleccionar (0) un objeto. "
               "No hay cantidades múltiples ni fracciones de objeto: es una mochila 0/1. "
               "Los cromosomas representan 2^15 combinaciones posibles.", "",
               "## 2. Penalización frente a reparación", "",
               f"Penalización: fitness = valor - max(0, peso-capacidad) × {FACTOR_PENALIZACION}. "
               "El factor es la suma de todos los valores más uno. Los pesos y capacidades son "
               "enteros: todo inválido tiene fitness negativo y no supera a un válido, cuyo valor "
               "es no negativo. No se trunca a cero, para diferenciar individuos inválidos.", "",
               "Reparación: antes de evaluar, elimina seleccionados de menor valor/peso hasta "
               "cumplir capacidad; desempata por ID. No añade objetos. El fitness de un reparado "
               "es su valor porque no tiene exceso. Ambos métodos comparten operadores, "
               "semillas y una mochila vacía inicial. Penalización no repara individuos; "
               "se conserva por separado el mejor válido de todas las generaciones.", "",
               "## 3. ¿Cuál método funcionó mejor?", ""]
    for capacidad in CAPACIDADES:
        a, b = [r for r in resumen if r["capacidad"] == capacidad]
        lineas.append(f"Capacidad {capacidad}: penalización obtuvo media {a['valor_promedio']:.3f} "
                      f"y máximo {a['mejor_valor']}; reparación, media {b['valor_promedio']:.3f} "
                      f"y máximo {b['mejor_valor']}.")
        for campo, titulo, mayor in (("valor_promedio", "mayor valor promedio", True),
                                     ("mejor_valor", "mayor valor máximo", True),
                                     ("generacion_promedio_mejor", "menor generación media", False),
                                     ("tiempo_promedio_segundos", "mayor tiempo medio", True)):
            if a[campo] == b[campo]:
                lineas.append(f"- {titulo}: empate ({a[campo]:.4f}).")
            else:
                ganador = max((a, b), key=lambda r: r[campo]) if mayor else min((a, b), key=lambda r: r[campo])
                lineas.append(f"- {titulo}: {ganador['metodo']} ({ganador[campo]:.4f}).")
    lineas += ["", "## 4. Efecto de la capacidad", ""]
    for metodo in ("penalizacion", "reparacion"):
        a, b = [r for r in resumen if r["metodo"] == metodo]
        lineas.append(f"{metodo}: al pasar de capacidad 30 a 45, el valor promedio pasó de "
                      f"{a['valor_promedio']:.3f} a {b['valor_promedio']:.3f}, y el peso medio "
                      f"de {a['peso_promedio']:.2f} a {b['peso_promedio']:.2f}.")
    lineas += ["", "Conceptualmente, una capacidad mayor amplía el conjunto factible: el óptimo "
               "teórico no puede disminuir. Eso no garantiza que una heurística encuentre siempre "
               "un resultado mejor. Aquí se comparan las corridas reales de la misma instancia.", "",
               "## 5. Ventajas, desventajas y límites", "",
               "Conceptualmente, penalizar mantiene los cromosomas originales y es sencillo, "
               "pero exige un factor adecuado y puede gastar evaluaciones en inválidos. Reparar "
               "garantiza factibilidad antes de evaluar, pero añade trabajo y sesga la búsqueda "
               "hacia objetos eficientes individualmente; la mejor combinación no tiene por qué "
               "obtenerse con una regla voraz. Los tiempos y valores observados arriba son evidencia "
               "de estas corridas, no una demostración general de superioridad.", "",
               "Se completan 500 reemplazos y 501 evaluaciones contando generación 0. No hay "
               "parada por valor objetivo ni óptimo exacto calculado. La generación del mejor "
               "se refiere a su primera aparición. El historial muestra mejor valor válido "
               "acumulado, incluso si no sobrevive sin elitismo. Los tiempos excluyen CSV y PNG. "
               "Desviación muestral usa divisor n-1. Diez semillas por combinación y una instancia "
               "no establecen superioridad estadística general.", "",
               "Al finalizar el lote, ejecucion.csv y las gráficas individuales muestran la "
               "corrida de mayor valor del lote; comparar métodos siempre dentro de cada capacidad. "
               "Una ejecución individual posterior actualiza esos archivos. Los CSV experimentales "
               "conservan el lote. No se modifica ningún resultado de las fases anteriores."]
    (Path(directorio) / "analisis.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def ejecutar_experimentos(repeticiones=10, poblacion=100, generaciones=500,
                         tasa_mutacion=0.1, elitismo=2, semilla_base=2026, directorio=DIRECTORIO):
    if isinstance(repeticiones, bool) or not isinstance(repeticiones, int) or repeticiones < 2:
        raise ValueError("Se requieren al menos dos repeticiones para la desviación muestral.")
    registros, historiales = [], []
    mejor = None
    directorio = Path(directorio)
    for capacidad in CAPACIDADES:
        for metodo in ("penalizacion", "reparacion"):
            for repeticion in range(repeticiones):
                r = resolver_mochila(capacidad, metodo, poblacion, generaciones, tasa_mutacion, elitismo, semilla_base + repeticion)
                numero = len(registros) + 1
                registros.append({"ejecucion": numero, "repeticion": repeticion + 1, **fila_resultado(r)})
                historiales.extend({"ejecucion": numero, **h} for h in r["historial"])
                if mejor is None or r["valor_total"] > mejor["valor_total"]:
                    mejor = r
                print(f"Mochila {numero}/{4 * repeticiones}: capacidad={capacidad}, {metodo}, "
                      f"valor={r['valor_total']}, peso={r['peso_total']}", flush=True)
    resumen = resumir(registros)
    escribir_csv(directorio / "experimentos.csv", registros)
    escribir_csv(directorio / "historiales.csv", historiales)
    escribir_csv(directorio / "resumen.csv", resumen)
    guardar_ejecucion(mejor, directorio)
    graficar_comparacion(resumen, directorio / "comparacion_metodos.png")
    escribir_analisis(registros, resumen, directorio)
    return registros
