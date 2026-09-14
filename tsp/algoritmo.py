"""Torneo, OX, swap/inversión y elitismo para minimizar distancia cerrada."""

from time import perf_counter
import numpy as np
from .datos import obtener_coordenadas, crear_matriz_distancias, MATRIZ_DISTANCIAS


def validar_ruta(ruta, numero_ciudades):
    """Detecta ciudades duplicadas, faltantes y genes fuera del dominio."""
    if (len(ruta) != numero_ciudades
            or any(isinstance(x, (bool, np.bool_)) or not isinstance(x, (int, np.integer)) for x in ruta)
            or sorted(ruta) != list(range(numero_ciudades))):
        raise ValueError("La ruta debe ser una permutación de todas las ciudades.")


def calcular_distancia(ruta, matriz=None):
    """Suma todas las aristas, incluida última -> primera. Menor es mejor.

    Sin matriz utiliza la instancia principal de diez ciudades.
    """
    matriz = MATRIZ_DISTANCIAS if matriz is None else np.asarray(matriz)
    validar_ruta(ruta, len(matriz))
    # Ordenar los sumandos estabiliza empates entre rotaciones del mismo ciclo.
    tramos = [float(matriz[ruta[i], ruta[(i + 1) % len(ruta)]]) for i in range(len(ruta))]
    return sum(sorted(tramos))


def fitness(ruta, matriz=None):
    """Mayor aptitud equivale a menor distancia; epsilon evita dividir por cero."""
    return 1.0 / (calcular_distancia(ruta, matriz) + 1e-12)


def crear_poblacion(tamano, numero_ciudades, rng):
    return [rng.permutation(numero_ciudades) for _ in range(tamano)]


def seleccionar_torneo(poblacion, distancias, rng, tamano=3):
    candidatos = rng.choice(len(poblacion), size=min(tamano, len(poblacion)), replace=False)
    ganador = min(candidatos, key=lambda i: distancias[i])
    return poblacion[ganador].copy()


def cruzar_ox(padre1, padre2, rng):
    """Copia un segmento inclusivo y rellena circularmente desde su final."""
    n = len(padre1)
    validar_ruta(padre1, n)
    validar_ruta(padre2, n)
    inicio, fin = sorted(rng.choice(n, size=2, replace=False))
    hijo = np.full(n, -1, dtype=int)
    hijo[inicio:fin + 1] = padre1[inicio:fin + 1]
    usados = set(hijo[inicio:fin + 1])
    posicion = (fin + 1) % n
    for desplazamiento in range(n):
        ciudad = padre2[(fin + 1 + desplazamiento) % n]
        if ciudad not in usados:
            hijo[posicion] = ciudad
            posicion = (posicion + 1) % n
    validar_ruta(hijo, n)  # Obligatorio después de cada cruzamiento.
    return hijo


def mutar(ruta, tasa, tipo, rng):
    """Probabilidad por individuo; no modifica al padre recibido."""
    if tipo not in ("swap", "inversion"):
        raise ValueError("Tipo de mutación: swap o inversion.")
    hijo = ruta.copy()
    if rng.random() < tasa:
        i, j = sorted(rng.choice(len(hijo), size=2, replace=False))
        if tipo == "swap":
            hijo[i], hijo[j] = hijo[j], hijo[i]
        else:
            hijo[i:j + 1] = hijo[i:j + 1][::-1]
    validar_ruta(hijo, len(hijo))
    return hijo


def resolver_tsp(numero_ciudades=10, poblacion=100, generaciones=500,
                 tasa_mutacion=0.1, tipo_mutacion="swap", elitismo=2, semilla=42):
    coordenadas = obtener_coordenadas(numero_ciudades)
    for nombre, valor, minimo in (("poblacion", poblacion, 3),
                                  ("generaciones", generaciones, 0), ("elitismo", elitismo, 0)):
        if isinstance(valor, bool) or not isinstance(valor, (int, np.integer)) or valor < minimo:
            raise ValueError(f"{nombre} debe ser un entero >= {minimo}.")
    if elitismo >= poblacion:
        raise ValueError("El elitismo debe ser menor que la población.")
    if not 0 <= tasa_mutacion <= 1:
        raise ValueError("La tasa de mutación debe estar entre 0 y 1.")
    if tipo_mutacion not in ("swap", "inversion"):
        raise ValueError("Tipo de mutación: swap o inversion.")
    inicio = perf_counter()
    rng = np.random.default_rng(semilla)
    matriz = crear_matriz_distancias(coordenadas)
    individuos = crear_poblacion(poblacion, numero_ciudades, rng)
    mejor_distancia = float("inf")
    historial = []
    for generacion in range(generaciones + 1):
        distancias = [calcular_distancia(ind, matriz) for ind in individuos]
        indice = int(np.argmin(distancias))
        if distancias[indice] < mejor_distancia:
            mejor_distancia = distancias[indice]
            mejor_ruta = individuos[indice].copy()
            generacion_mejor = generacion
        historial.append({"generacion": generacion,
                          "distancia_generacion": distancias[indice],
                          "mejor_distancia": mejor_distancia})
        if generacion == generaciones:
            break
        orden = np.argsort(distancias, kind="stable")
        nueva = [individuos[i].copy() for i in orden[:elitismo]]
        while len(nueva) < poblacion:
            padre1 = seleccionar_torneo(individuos, distancias, rng)
            padre2 = seleccionar_torneo(individuos, distancias, rng)
            nueva.append(mutar(cruzar_ox(padre1, padre2, rng), tasa_mutacion, tipo_mutacion, rng))
        individuos = nueva
    return {"numero_ciudades": int(numero_ciudades), "poblacion": int(poblacion),
            "tasa_mutacion": float(tasa_mutacion), "tipo_mutacion": tipo_mutacion,
            "elitismo": int(elitismo), "max_generaciones": int(generaciones),
            "semilla": semilla, "mejor_ruta": mejor_ruta.tolist(),
            "mejor_distancia": mejor_distancia, "generacion_mejor": generacion_mejor,
            "generaciones_ejecutadas": generacion,
            "tiempo_segundos": perf_counter() - inicio, "historial": historial}
