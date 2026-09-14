"""Entrada de las cuatro fases. Abrir este archivo en Spyder y ejecutar con F5."""

from n_reinas.algoritmo import resolver
from n_reinas.experimento import ejecutar_experimentos, guardar_ejecucion
from n_reinas.visualizacion import graficar_convergencia, graficar_tablero


def leer_numero(texto, tipo, defecto):
    entrada = input(f"{texto} [{defecto}]: ").strip()
    return tipo(entrada) if entrada else defecto


def menu_n_reinas():
    ultimo = None
    while True:
        print("\nTALLER DE ALGORITMOS GENÉTICOS - FASE 1: N-REINAS")
        print("1. Ejecutar algoritmo\n2. Ejecutar experimentos\n3. Mostrar gráfica\n4. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                ultimo = resolver(
                    n=leer_numero("N", int, 8),
                    poblacion=leer_numero("Tamaño de población", int, 100),
                    generaciones=leer_numero("Máximo de generaciones", int, 500),
                    tasa_mutacion=leer_numero("Tasa de mutación", float, 0.10),
                    elitismo=leer_numero("Cantidad de élites", int, 2),
                    semilla=leer_numero("Semilla", int, 42))
                guardar_ejecucion(ultimo)
                print({k: v for k, v in ultimo.items() if k != "historial"})
                print("CSV y PNG guardados en resultados/n_reinas.")
            elif opcion == "2":
                ejecutar_experimentos(repeticiones=leer_numero("Repeticiones por combinación", int, 10))
            elif opcion == "3":
                if ultimo is None:
                    print("Ejecuta primero la opción 1. Las gráficas anteriores están en resultados/n_reinas.")
                else:
                    graficar_convergencia(ultimo, mostrar=True)
                    graficar_tablero(ultimo, mostrar=True)
            elif opcion == "4":
                break
            else:
                print("Selecciona una opción entre 1 y 4.")
        except ValueError as error:
            print(f"Entrada inválida: {error}")


def menu_tsp():
    # Imports locales mantienen independiente el menú de N-Reinas.
    import csv
    from tsp.algoritmo import resolver_tsp
    from tsp.experimento import DIRECTORIO, ejecutar_experimentos, guardar_ejecucion
    from tsp.visualizacion import graficar_convergencia, graficar_ruta, graficar_comparacion

    ultimo = None
    while True:
        print("\nTSP - PROBLEMA DEL AGENTE VIAJERO")
        print("1. Ejecutar algoritmo\n2. Ejecutar experimentos\n3. Mostrar gráficas\n4. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                ultimo = resolver_tsp(
                    numero_ciudades=leer_numero("Número de ciudades", int, 10),
                    poblacion=leer_numero("Tamaño de población", int, 100),
                    generaciones=leer_numero("Máximo de generaciones", int, 500),
                    tasa_mutacion=leer_numero("Tasa de mutación", float, 0.1),
                    tipo_mutacion=input("Tipo de mutación [swap]: ").strip().lower() or "swap",
                    elitismo=leer_numero("Cantidad de élites", int, 2),
                    semilla=leer_numero("Semilla", int, 42))
                guardar_ejecucion(ultimo)
                ruta = ultimo["mejor_ruta"]
                print("Mejor ruta:", " -> ".join(map(str, ruta + [ruta[0]])))
                print(f"Distancia total: {ultimo['mejor_distancia']:.6f}")
                print("Generación de la mejor ruta:", ultimo["generacion_mejor"])
                print(f"Tiempo de ejecución: {ultimo['tiempo_segundos']:.6f} segundos")
                print("CSV y PNG guardados en resultados/tsp.")
            elif opcion == "2":
                ejecutar_experimentos()
                print("40 ejecuciones guardadas en resultados/tsp.")
            elif opcion == "3":
                if ultimo is not None:
                    graficar_convergencia(ultimo, mostrar=True)
                    graficar_ruta(ultimo, mostrar=True)
                else:
                    # Permite ver las gráficas del lote incluso tras reiniciar Spyder.
                    import matplotlib.pyplot as plt
                    for nombre in ("convergencia.png", "mejor_ruta.png"):
                        ruta = DIRECTORIO / nombre
                        if ruta.exists():
                            fig, ax = plt.subplots(figsize=(9, 6))
                            ax.imshow(plt.imread(ruta))
                            ax.axis("off")
                            fig.tight_layout()
                            plt.show()
                            plt.close(fig)
                        else:
                            print("Ejecuta primero el algoritmo o los experimentos.")
                            break
                if (DIRECTORIO / "resumen.csv").exists():
                    with (DIRECTORIO / "resumen.csv").open(encoding="utf-8-sig", newline="") as archivo:
                        graficar_comparacion(list(csv.DictReader(archivo)), mostrar=True)
            elif opcion == "4":
                break
            else:
                print("Selecciona una opción entre 1 y 4.")
        except ValueError as error:
            print(f"Entrada inválida: {error}")


def menu_cursos_salas():
    import csv
    from cursos_salas.algoritmo import resolver_cursos_salas, construir_horario, mostrar_horario
    from cursos_salas.experimento import DIRECTORIO, guardar_ejecucion, ejecutar_experimentos
    from cursos_salas.visualizacion import mostrar_guardadas

    while True:
        print("\nASIGNACIÓN DE CURSOS A SALAS")
        print("1. Ejecutar algoritmo\n2. Ejecutar experimentos\n3. Mostrar gráficas\n4. Mostrar horario\n5. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                resultado = resolver_cursos_salas(
                    poblacion=leer_numero("Tamaño de población", int, 100),
                    generaciones=leer_numero("Máximo de generaciones", int, 500),
                    tasa_mutacion=leer_numero("Tasa de mutación", float, 0.1),
                    elitismo=leer_numero("Cantidad de élites", int, 2),
                    semilla=leer_numero("Semilla", int, 42))
                guardar_ejecucion(resultado)
                print("Penalización total:", resultado["penalizacion"])
                print("Desglose:", resultado["detalles_penalizacion"])
                print("Generación de mejor solución:", resultado["generacion_mejor"])
                print(f"Tiempo: {resultado['tiempo_segundos']:.6f} segundos")
                print("Horario encontrado:")
                mostrar_horario(construir_horario(resultado["mejor_individuo"]))
            elif opcion == "2":
                ejecutar_experimentos()
                print("20 ejecuciones guardadas en resultados/cursos_salas.")
            elif opcion == "3":
                if (DIRECTORIO / "convergencia.png").exists():
                    mostrar_guardadas(DIRECTORIO)
                else:
                    print("Ejecuta primero el algoritmo o los experimentos.")
            elif opcion == "4":
                if (DIRECTORIO / "horario.csv").exists():
                    with (DIRECTORIO / "horario.csv").open(encoding="utf-8-sig", newline="") as archivo:
                        mostrar_horario(list(csv.DictReader(archivo)))
                else:
                    print("Ejecuta primero el algoritmo o los experimentos.")
            elif opcion == "5":
                break
            else:
                print("Selecciona una opción entre 1 y 5.")
        except ValueError as error:
            print(f"Entrada inválida: {error}")


def menu_mochila():
    import csv
    import json
    from mochila.algoritmo import resolver_mochila, mostrar_resultado
    from mochila.experimento import DIRECTORIO, guardar_ejecucion, ejecutar_experimentos
    from mochila.visualizacion import mostrar_guardadas

    while True:
        print("\nPROBLEMA DE LA MOCHILA")
        print("1. Ejecutar algoritmo\n2. Ejecutar experimentos\n3. Mostrar gráficas\n4. Mostrar objetos seleccionados\n5. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                resultado = resolver_mochila(
                    capacidad=leer_numero("Capacidad", int, 30),
                    metodo=input("Método [penalizacion]: ").strip().lower() or "penalizacion",
                    poblacion=leer_numero("Tamaño de población", int, 100),
                    generaciones=leer_numero("Máximo de generaciones", int, 500),
                    tasa_mutacion=leer_numero("Tasa de mutación", float, 0.1),
                    elitismo=leer_numero("Cantidad de élites", int, 2),
                    semilla=leer_numero("Semilla", int, 42))
                guardar_ejecucion(resultado)
                mostrar_resultado(resultado)
            elif opcion == "2":
                ejecutar_experimentos()
                print("40 ejecuciones guardadas en resultados/mochila.")
            elif opcion == "3":
                if (DIRECTORIO / "convergencia.png").exists():
                    mostrar_guardadas(DIRECTORIO)
                else:
                    print("Ejecuta primero el algoritmo o los experimentos.")
            elif opcion == "4":
                if (DIRECTORIO / "ejecucion.csv").exists():
                    with (DIRECTORIO / "ejecucion.csv").open(encoding="utf-8-sig", newline="") as archivo:
                        resultado = next(csv.DictReader(archivo))
                    for clave in ("mejor_individuo", "objetos_seleccionados"):
                        resultado[clave] = json.loads(resultado[clave])
                    mostrar_resultado(resultado)
                else:
                    print("Ejecuta primero el algoritmo o los experimentos.")
            elif opcion == "5":
                break
            else:
                print("Selecciona una opción entre 1 y 5.")
        except ValueError as error:
            print(f"Entrada inválida: {error}")


def main():
    while True:
        print("\nTALLER DE ALGORITMOS GENÉTICOS")
        print("1. N-Reinas\n2. Agente Viajero - TSP\n3. Asignación de Cursos a Salas\n4. Problema de la Mochila\n5. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            menu_n_reinas()
        elif opcion == "2":
            menu_tsp()
        elif opcion == "3":
            menu_cursos_salas()
        elif opcion == "4":
            menu_mochila()
        elif opcion == "5":
            break
        else:
            print("Selecciona una opción entre 1 y 5.")


if __name__ == "__main__":
    main()
