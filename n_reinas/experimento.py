"""18 combinaciones, semillas registradas y resultados reales en CSV."""

import csv
from pathlib import Path
from .algoritmo import resolver
from .visualizacion import graficar_convergencia, graficar_tablero

DIRECTORIO = Path(__file__).resolve().parents[1] / "resultados" / "n_reinas"


def escribir_csv(ruta, filas):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)


def guardar_ejecucion(resultado, directorio=DIRECTORIO):
    directorio = Path(directorio)
    escribir_csv(directorio / "ejecucion.csv",
                 [{k: v for k, v in resultado.items() if k != "historial"}])
    escribir_csv(directorio / "historial.csv", resultado["historial"])
    graficar_convergencia(resultado, directorio / "convergencia.png")
    graficar_tablero(resultado, directorio / "tablero.png")


def ejecutar_experimentos(repeticiones=10, generaciones=500, elitismo=2,
                         semilla_base=2026, directorio=DIRECTORIO):
    if not isinstance(repeticiones, int) or repeticiones < 1:
        raise ValueError("Las repeticiones deben ser un entero positivo.")
    directorio = Path(directorio)
    registros, historiales, resumen = [], [], []
    for n in (6, 8):
        for poblacion in (50, 100, 200):
            for tasa in (0.05, 0.10, 0.20):
                grupo = []
                for repeticion in range(repeticiones):
                    # Misma semilla entre configuraciones para facilitar comparación.
                    r = resolver(n, poblacion, generaciones, tasa, elitismo,
                                 semilla_base + repeticion)
                    identificador = f"n{n}_p{poblacion}_m{tasa:.2f}_r{repeticion + 1:02d}"
                    fila = {"ejecucion": identificador, "repeticion": repeticion + 1,
                            **{k: v for k, v in r.items() if k != "historial"}}
                    registros.append(fila)
                    grupo.append(fila)
                    historiales.extend({"ejecucion": identificador, **h} for h in r["historial"])
                    graficar_convergencia(r, directorio / "graficas" / f"{identificador}.png")
                exitos = [r for r in grupo if r["exito"]]
                resumen.append({"n": n, "poblacion": poblacion, "tasa_mutacion": tasa,
                                "repeticiones": repeticiones, "exitos": len(exitos),
                                "porcentaje_exito": 100 * len(exitos) / repeticiones,
                                "conflictos_promedio": sum(r["conflictos"] for r in grupo) / repeticiones,
                                "generacion_media_exitos": (sum(r["generacion_mejor"] for r in exitos) / len(exitos)) if exitos else "",
                                "tiempo_medio_segundos": sum(r["tiempo_segundos"] for r in grupo) / repeticiones})
                print(f"N={n}, población={poblacion}, mutación={tasa}: {len(exitos)}/{repeticiones} éxitos")
    escribir_csv(directorio / "experimentos.csv", registros)
    escribir_csv(directorio / "historiales.csv", historiales)
    escribir_csv(directorio / "resumen.csv", resumen)
    return registros
