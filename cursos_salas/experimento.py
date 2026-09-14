"""Ejecuciones, horario, estadísticas y análisis de datos realmente obtenidos."""

import csv
import json
from pathlib import Path
from statistics import mean, stdev
from .algoritmo import resolver_cursos_salas, construir_horario
from .visualizacion import graficar_convergencia, graficar_comparacion, graficar_horario

DIRECTORIO = Path(__file__).resolve().parents[1] / "resultados" / "cursos_salas"


def escribir_csv(ruta, filas):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)


def fila_resultado(resultado):
    return {k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
            for k, v in resultado.items() if k != "historial"}


def guardar_ejecucion(resultado, directorio=DIRECTORIO):
    directorio = Path(directorio)
    escribir_csv(directorio / "ejecucion.csv", [fila_resultado(resultado)])
    escribir_csv(directorio / "historial.csv", resultado["historial"])
    escribir_csv(directorio / "horario.csv", construir_horario(resultado["mejor_individuo"]))
    graficar_convergencia(resultado, directorio / "convergencia.png")
    graficar_horario(resultado, directorio / "horario.png")


def resumir(registros):
    resumen = []
    for elitismo in (0, 2):
        grupo = [r for r in registros if r["elitismo"] == elitismo]
        valores = [r["penalizacion"] for r in grupo]
        resumen.append({"elitismo": elitismo, "repeticiones": len(grupo),
                        "mejor_penalizacion": min(valores), "peor_penalizacion": max(valores),
                        "penalizacion_promedio": mean(valores), "desviacion_estandar_muestral": stdev(valores),
                        "tiempo_promedio_segundos": mean(r["tiempo_segundos"] for r in grupo),
                        "generacion_promedio_mejor": mean(r["generacion_mejor"] for r in grupo),
                        "soluciones_cero": sum(r["penalizacion"] == 0 for r in grupo),
                        "validas_restricciones_duras": sum(r["valida_restricciones_duras"] for r in grupo)})
    return resumen


def escribir_analisis(registros, resumen, directorio):
    lineas = ["# Asignación de cursos a salas: análisis", "",
              f"Se realizaron {len(registros)} corridas reales con 8 cursos, 4 salas y 5 franjas, "
              f"población {registros[0]['poblacion']}, máximo {registros[0]['max_generaciones']} generaciones "
              f"y tasa {registros[0]['tasa_mutacion']}. Semillas registradas en experimentos.csv.", "",
              "| Elitismo | Mejor | Peor | Promedio | Desv. muestral | Generación media | Éxitos (cero) |",
              "|---|---|---|---|---|---|---|"]
    for r in resumen:
        lineas.append(f"| {r['elitismo']} | {r['mejor_penalizacion']} | {r['peor_penalizacion']} | "
                      f"{r['penalizacion_promedio']:.3f} | {r['desviacion_estandar_muestral']:.3f} | "
                      f"{r['generacion_promedio_mejor']:.2f} | {r['soluciones_cero']}/{r['repeticiones']} |")
    lineas += ["", "## 1. Restricciones duras y blandas", "",
               "Duras: sobrecupo, computadores insuficientes cuando se requieren, software faltante, "
               "recurso indispensable faltante, franja prohibida del curso y bloqueo de sala: "
               "100 puntos por condición y curso. Choques: 200 puntos por pareja de cursos en "
               "la misma sala y franja, contada una sola vez. Tres cursos producen tres parejas.", "",
               "Blanda: un punto por curso que excede dos asignaciones en una sala, más un punto "
               "por curso que excede dos en una franja. El máximo blando para 8 cursos es 12, "
               "menor que cualquier infracción dura. Total cero implica cumplimiento duro y "
               "equilibrio. Un horario sin conflictos duros puede tener penalización blanda positiva: "
               "se registra también valida_restricciones_duras, pero éxito exige total cero.", "",
               "## 2. Penalizar frente a reparar", "",
               "Se implementó exclusivamente penalización. Permite explorar horarios inviables "
               "con operadores simples y un desglose explicable, pero exige elegir pesos y puede "
               "converger sin resolver todos los conflictos. Reparar puede recuperar factibilidad "
               "tras los operadores, pero requiere reglas adicionales, puede introducir sesgo y "
               "resolver un conflicto creando otro. No se experimentó con reparación, por lo que "
               "no se afirma que sea mejor o peor empíricamente.", "",
               "## 3. Aumentar el número de cursos", "",
               "Con 4 salas y 5 franjas, el espacio estructural es 20^C para C cursos; para ocho "
               "es 25 600 000 000 cromosomas antes de aplicar restricciones. Más cursos aumentan "
               "las posibilidades de choque y pueden exigir más población o generaciones, o "
               "hacer imposible el horario por falta de recursos. Sólo se experimentó con ocho "
               "cursos; esto es una explicación conceptual, no un resultado medido.", "",
               "## 4. Efecto observado del elitismo", ""]
    a, b = resumen
    lineas.append(f"Sin elitismo: media {a['penalizacion_promedio']:.3f}, {a['soluciones_cero']} éxitos, "
                  f"generación media {a['generacion_promedio_mejor']:.2f}. Con elitismo: media "
                  f"{b['penalizacion_promedio']:.3f}, {b['soluciones_cero']} éxitos, generación media "
                  f"{b['generacion_promedio_mejor']:.2f}.")
    if a["penalizacion_promedio"] == b["penalizacion_promedio"]:
        lineas.append("Las versiones empataron en penalización promedio final.")
    else:
        ganador = "con elitismo" if b["penalizacion_promedio"] < a["penalizacion_promedio"] else "sin elitismo"
        lineas.append(f"La versión {ganador} obtuvo menor penalización promedio final en estas corridas.")
    lineas += ["", "Elitismo copia individuos a la siguiente población; guardar el mejor histórico "
               "sólo conserva el resultado para informar y no lo reintroduce cuando elitismo=0. "
               "La gráfica muestra mejor acumulada; el CSV también incluye mejor de cada generación. "
               "Generación 0 es la población inicial. Se detiene al alcanzar cero o el límite.", "",
               "Desviación muestral: divisor n-1. La generación media incluye todas las corridas, "
               "también fracasos; debe interpretarse con la tasa de éxito. Tiempo excluye CSV y "
               "gráficas. Diez semillas por variante y una instancia no permiten generalizar "
               "superioridad estadística. No se ha probado la interfaz de Spyder desde este entorno.", "",
               "El horario y las gráficas individuales representan la mejor corrida del lote "
               "al terminar los experimentos. Una ejecución individual posterior los actualiza "
               "sin cambiar experimentos.csv. Los resultados de N-Reinas y TSP no se escriben."]
    (Path(directorio) / "analisis.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def ejecutar_experimentos(repeticiones=10, poblacion=100, generaciones=500,
                         tasa_mutacion=0.1, semilla_base=2026, directorio=DIRECTORIO):
    if isinstance(repeticiones, bool) or not isinstance(repeticiones, int) or repeticiones < 2:
        raise ValueError("Se requieren al menos dos repeticiones para la desviación muestral.")
    registros, historiales = [], []
    mejor = None
    directorio = Path(directorio)
    for elitismo in (0, 2):
        for repeticion in range(repeticiones):
            r = resolver_cursos_salas(poblacion, generaciones, tasa_mutacion, elitismo, semilla_base + repeticion)
            numero = len(registros) + 1
            registros.append({"ejecucion": numero, "repeticion": repeticion + 1, **fila_resultado(r)})
            historiales.extend({"ejecucion": numero, **h} for h in r["historial"])
            if mejor is None or r["penalizacion"] < mejor["penalizacion"]:
                mejor = r
            print(f"Cursos/salas {numero}/{2 * repeticiones}: elitismo={elitismo}, "
                  f"penalización={r['penalizacion']}, generación={r['generacion_mejor']}", flush=True)
    resumen = resumir(registros)
    escribir_csv(directorio / "experimentos.csv", registros)
    escribir_csv(directorio / "historiales.csv", historiales)
    escribir_csv(directorio / "resumen.csv", resumen)
    guardar_ejecucion(mejor, directorio)
    graficar_comparacion(resumen, directorio / "comparacion_elitismo.png")
    escribir_analisis(registros, resumen, directorio)
    return registros
