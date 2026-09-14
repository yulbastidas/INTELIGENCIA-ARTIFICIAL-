"""40 corridas reproducibles; exportaciones y análisis calculados de los datos."""

import csv
from pathlib import Path
from statistics import mean, stdev
from .algoritmo import resolver_tsp
from .visualizacion import graficar_convergencia, graficar_ruta, graficar_comparacion

DIRECTORIO = Path(__file__).resolve().parents[1] / "resultados" / "tsp"


def escribir_csv(ruta, filas):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)


def guardar_ejecucion(resultado, directorio=DIRECTORIO):
    directorio = Path(directorio)
    escribir_csv(directorio / "ejecucion.csv", [{k: v for k, v in resultado.items() if k != "historial"}])
    escribir_csv(directorio / "historial.csv", resultado["historial"])
    graficar_convergencia(resultado, directorio / "convergencia.png")
    graficar_ruta(resultado, directorio / "mejor_ruta.png")


def resumir(registros):
    resumen = []
    for tipo in ("swap", "inversion"):
        for tasa in (0.05, 0.20):
            grupo = [r for r in registros if r["tipo_mutacion"] == tipo and r["tasa_mutacion"] == tasa]
            valores = [r["mejor_distancia"] for r in grupo]
            resumen.append({"tipo_mutacion": tipo, "tasa_mutacion": tasa,
                            "repeticiones": len(grupo), "mejor_distancia": min(valores),
                            "peor_distancia": max(valores), "distancia_promedio": mean(valores),
                            "desviacion_estandar_muestral": stdev(valores) if len(valores) > 1 else 0.0,
                            "tiempo_promedio_segundos": mean(r["tiempo_segundos"] for r in grupo),
                            "generacion_promedio_mejor": mean(r["generacion_mejor"] for r in grupo)})
    return resumen


def escribir_analisis(registros, resumen, directorio):
    distancias = [r["mejor_distancia"] for r in registros]
    lineas = ["# Análisis experimental TSP", "",
              f"{len(registros)} ejecuciones reales de {registros[0]['numero_ciudades']} ciudades, "
              f"población {registros[0]['poblacion']}, {registros[0]['max_generaciones']} generaciones "
              f"y elitismo {registros[0]['elitismo']}. Las semillas están en experimentos.csv.", "",
              f"Mejor distancia: {min(distancias):.6f}. Peor: {max(distancias):.6f}. "
              f"Promedio global: {mean(distancias):.6f} unidades.", "",
              "| Mutación | Tasa | Mejor | Peor | Promedio | Desv. muestral | Generación media |",
              "|---|---|---|---|---|---|---|"]
    for r in resumen:
        lineas.append(f"| {r['tipo_mutacion']} | {r['tasa_mutacion']:.2f} | {r['mejor_distancia']:.6f} | "
                      f"{r['peor_distancia']:.6f} | {r['distancia_promedio']:.6f} | "
                      f"{r['desviacion_estandar_muestral']:.6f} | {r['generacion_promedio_mejor']:.2f} |")
    lineas += ["", "## 1. ¿Por qué controlar duplicados?", "",
               "Cada cromosoma es una permutación: cada ciudad aparece exactamente una vez. "
               "Un cruce binario simple puede duplicar ciudades y omitir otras. OX conserva un "
               "segmento y completa el resto en el orden circular del otro padre, omitiendo las "
               "ciudades ya copiadas. Cada hijo se valida explícitamente.", "",
               "## 2. ¿Qué pasa si aumenta el número de ciudades?", "",
               "Teóricamente existen N! permutaciones. En TSP simétrico, al identificar rotaciones "
               "y recorridos inversos, quedan (N-1)!/2 ciclos diferentes para N>=3. "
               "El crecimiento factorial hace más difícil explorar el espacio; evaluar cada ruta "
               "también exige más aristas. Estos experimentos usan sólo 10 ciudades: no demuestran "
               "rendimiento para 8 o 15 ciudades.", "", "## 3. ¿Qué mutación encontró mejores rutas?", ""]
    promedios = {tipo: mean(r["mejor_distancia"] for r in registros if r["tipo_mutacion"] == tipo)
                 for tipo in ("swap", "inversion")}
    lineas.append(f"Promedio agrupado swap: {promedios['swap']:.6f}; inversión: {promedios['inversion']:.6f}.")
    if abs(promedios["swap"] - promedios["inversion"]) < 1e-9:
        lineas.append("Ambas estrategias empataron en distancia promedio dentro de tolerancia numérica.")
    else:
        ganador = min(promedios, key=promedios.get)
        lineas.append(f"{ganador} obtuvo la menor distancia promedio observada, agrupando las dos tasas.")
    for tipo in ("swap", "inversion"):
        generacion_media = mean(r["generacion_mejor"] for r in registros if r["tipo_mutacion"] == tipo)
        lineas.append(f"La primera aparición de la mejor ruta ocurrió en generación media "
                      f"{generacion_media:.2f} para {tipo}. Esto mide rapidez de convergencia, "
                      "no una mejora adicional de distancia final.")
    lineas += ["", "## 4. ¿Qué efecto tuvieron las tasas?", ""]
    for tipo in ("swap", "inversion"):
        a, b = [r for r in resumen if r["tipo_mutacion"] == tipo]
        cambio = b["distancia_promedio"] - a["distancia_promedio"]
        lineas.append(f"Para {tipo}, pasar de 0.05 a 0.20 cambió la distancia media de "
                      f"{a['distancia_promedio']:.6f} a {b['distancia_promedio']:.6f} "
                      f"(diferencia {cambio:+.6f}; negativa significa mejora).")
    lineas += ["", "## Interpretación y límites", "",
               "Se compara el mejor resultado final de cada corrida, no todos los individuos. "
               "La desviación es muestral (divisor n-1). La generación 0 es la población inicial; "
               "cada corrida completa el presupuesto y guarda 501 evaluaciones con 500 generaciones. "
               "Los tiempos excluyen CSV y gráficas. Menor distancia es mejor; el fitness inverso "
               "se maximiza y el torneo usa directamente distancias, con orden equivalente.", "",
               "No se calculó un óptimo exacto: mejor encontrada no significa óptima demostrada. "
               "Diez semillas por combinación y una instancia no permiten generalizar superioridad "
               "estadística. Misma semilla y versiones permiten repetir rutas e historiales; "
               "los tiempos dependen del equipo.", "",
               "convergencia.png, mejor_ruta.png y ejecucion.csv corresponden a la mejor corrida "
               "experimental al terminar este lote. Una ejecución individual posterior los actualiza; "
               "experimentos.csv e historiales.csv conservan el lote."]
    (Path(directorio) / "analisis.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def ejecutar_experimentos(repeticiones=10, generaciones=500, poblacion=100,
                         elitismo=2, semilla_base=2026, directorio=DIRECTORIO):
    if isinstance(repeticiones, bool) or not isinstance(repeticiones, int) or repeticiones < 2:
        raise ValueError("Se necesitan al menos dos repeticiones para la desviación muestral.")
    directorio = Path(directorio)
    registros, historiales = [], []
    mejor = None
    for tipo in ("swap", "inversion"):
        for tasa in (0.05, 0.20):
            for repeticion in range(repeticiones):
                r = resolver_tsp(10, poblacion, generaciones, tasa, tipo, elitismo, semilla_base + repeticion)
                numero = len(registros) + 1
                registros.append({"ejecucion": numero, "repeticion": repeticion + 1,
                                  **{k: v for k, v in r.items() if k != "historial"}})
                historiales.extend({"ejecucion": numero, **h} for h in r["historial"])
                if mejor is None or r["mejor_distancia"] < mejor["mejor_distancia"]:
                    mejor = r
                print(f"TSP {numero}/{4 * repeticiones}: {tipo}, tasa={tasa}, distancia={r['mejor_distancia']:.6f}", flush=True)
    resumen = resumir(registros)
    escribir_csv(directorio / "experimentos.csv", registros)
    escribir_csv(directorio / "historiales.csv", historiales)
    escribir_csv(directorio / "resumen.csv", resumen)
    guardar_ejecucion(mejor, directorio)
    graficar_comparacion(resumen, directorio / "comparacion_mutaciones.png")
    escribir_analisis(registros, resumen, directorio)
    return registros
