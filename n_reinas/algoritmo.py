"""Permutaciones, selección de mejores padres y cruce reparado, como en clase."""

from time import perf_counter
import numpy as np


def contar_conflictos(tablero):
    """Cuenta cada pareja atacante una vez; índice=columna, valor=fila."""
    return sum(
        int(tablero[i] == tablero[j] or abs(int(tablero[i]) - int(tablero[j])) == j - i)
        for i in range(len(tablero)) for j in range(i + 1, len(tablero))
    )


def fitness(tablero):
    """Maximizar -conflictos equivale a minimizar conflictos; óptimo=0."""
    return -contar_conflictos(tablero)


def crear_poblacion(tamano, n, rng):
    return [rng.permutation(n) for _ in range(tamano)]


def seleccionar(poblacion, aptitudes, cantidad):
    indices = np.argsort(aptitudes, kind="stable")[-cantidad:]
    return [poblacion[i].copy() for i in indices]


def cruzar(padre1, padre2, rng):
    """Cruce de un punto; sustituye repeticiones por filas faltantes."""
    n = len(padre1)
    if n < 2:
        return padre1.copy()
    punto = int(rng.integers(1, n))
    hijo = np.concatenate((padre1[:punto], padre2[punto:]))
    faltantes = [fila for fila in range(n) if fila not in hijo]
    rng.shuffle(faltantes)
    vistos = set()
    for i, fila in enumerate(hijo):
        if int(fila) in vistos:
            hijo[i] = faltantes.pop()
        vistos.add(int(hijo[i]))
    return hijo


def mutar(individuo, tasa, rng):
    """Probabilidad por hijo de intercambiar dos posiciones distintas."""
    hijo = individuo.copy()
    if len(hijo) > 1 and rng.random() < tasa:
        i, j = rng.choice(len(hijo), size=2, replace=False)
        hijo[i], hijo[j] = hijo[j], hijo[i]
    return hijo


def resolver(n=8, poblacion=100, generaciones=500, tasa_mutacion=0.10,
             elitismo=2, semilla=42):
    """Elitismo es cantidad de individuos. Generación 0 = población inicial.

    Devuelve el mejor global incluso al agotar el presupuesto. El historial
    distingue el mejor de cada población y el mejor acumulado.
    """
    for nombre, valor, minimo in (("n", n, 1), ("poblacion", poblacion, 4),
                                  ("generaciones", generaciones, 0),
                                  ("elitismo", elitismo, 0)):
        if isinstance(valor, bool) or not isinstance(valor, (int, np.integer)) or valor < minimo:
            raise ValueError(f"{nombre} debe ser un entero >= {minimo}.")
    if elitismo >= poblacion:
        raise ValueError("El elitismo debe ser menor que la población.")
    if not 0 <= tasa_mutacion <= 1:
        raise ValueError("La tasa de mutación debe estar entre 0 y 1.")
    inicio = perf_counter()
    rng = np.random.default_rng(semilla)
    individuos = crear_poblacion(poblacion, n, rng)
    mejor = None
    mejor_aptitud = -float("inf")
    generacion_mejor = 0
    historial = []
    for generacion in range(generaciones + 1):
        aptitudes = np.array([fitness(ind) for ind in individuos])
        indice = int(np.argmax(aptitudes))
        if int(aptitudes[indice]) > mejor_aptitud:
            mejor_aptitud = int(aptitudes[indice])
            mejor = individuos[indice].copy()
            generacion_mejor = generacion
        historial.append({"generacion": generacion,
                          "conflictos_generacion": -int(aptitudes[indice]),
                          "mejores_conflictos": -mejor_aptitud})
        if mejor_aptitud == 0 or generacion == generaciones:
            break
        padres = seleccionar(individuos, aptitudes, poblacion // 2)
        nueva = seleccionar(individuos, aptitudes, elitismo) if elitismo else []
        while len(nueva) < poblacion:
            a, b = rng.choice(len(padres), size=2, replace=False)
            nueva.append(mutar(cruzar(padres[a], padres[b], rng), tasa_mutacion, rng))
        individuos = nueva
    return {"n": int(n), "poblacion": int(poblacion),
            "tasa_mutacion": float(tasa_mutacion), "elitismo": int(elitismo),
            "max_generaciones": int(generaciones), "semilla": semilla,
            "mejor_solucion": mejor.tolist(), "conflictos": -mejor_aptitud,
            "generacion_mejor": generacion_mejor,
            "generaciones_ejecutadas": generacion,
            "tiempo_segundos": perf_counter() - inicio,
            "exito": mejor_aptitud == 0, "historial": historial}
