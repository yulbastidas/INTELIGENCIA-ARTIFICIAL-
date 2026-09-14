"""Maximización con torneo, cruce de un punto, bit-flip y elitismo."""

from time import perf_counter
import numpy as np
from .datos import OBJETOS, FACTOR_PENALIZACION


def validar_individuo(individuo):
    a = np.asarray(individuo)
    if a.shape != (len(OBJETOS),) or not np.all((a == 0) | (a == 1)):
        raise ValueError("El cromosoma debe tener exactamente 15 genes binarios.")


def validar_capacidad(capacidad):
    if isinstance(capacidad, bool) or not isinstance(capacidad, (int, np.integer)) or capacidad < 0:
        raise ValueError("La capacidad debe ser un entero no negativo.")


def calcular_peso(individuo):
    validar_individuo(individuo)
    return sum(o["peso"] for gen, o in zip(individuo, OBJETOS) if gen == 1)


def calcular_valor(individuo):
    validar_individuo(individuo)
    return sum(o["valor"] for gen, o in zip(individuo, OBJETOS) if gen == 1)


def fitness(individuo, capacidad):
    """Valor - max(0, peso-capacidad)*FACTOR; se conservan valores negativos."""
    validar_capacidad(capacidad)
    return calcular_valor(individuo) - max(0, calcular_peso(individuo) - capacidad) * FACTOR_PENALIZACION


def reparar(individuo, capacidad):
    """Elimina seleccionados de menor valor/peso; empates por ID. No altera al padre."""
    validar_individuo(individuo)
    validar_capacidad(capacidad)
    hijo = np.asarray(individuo, dtype=int).copy()
    peso = calcular_peso(hijo)
    orden = sorted((i for i, gen in enumerate(hijo) if gen),
                   key=lambda i: (OBJETOS[i]["valor"] / OBJETOS[i]["peso"], i))
    for i in orden:
        if peso <= capacidad:
            break
        hijo[i] = 0
        peso -= OBJETOS[i]["peso"]
    return hijo


def crear_poblacion(tamano, rng):
    return [rng.integers(0, 2, size=len(OBJETOS)) for _ in range(tamano)]


def seleccionar_torneo(poblacion, aptitudes, rng):
    candidatos = rng.choice(len(poblacion), size=3, replace=False)
    ganador = max(candidatos, key=lambda i: aptitudes[i])
    return poblacion[ganador].copy()


def cruzar(padre1, padre2, rng):
    punto = int(rng.integers(1, len(OBJETOS)))
    hijo = np.concatenate((padre1[:punto], padre2[punto:]))
    validar_individuo(hijo)
    return hijo


def mutar(individuo, tasa, rng):
    """Cada gen cambia de forma independiente con probabilidad tasa."""
    hijo = np.asarray(individuo, dtype=int).copy()
    cambios = rng.random(len(hijo)) < tasa
    hijo[cambios] = 1 - hijo[cambios]
    validar_individuo(hijo)
    return hijo


def resolver_mochila(capacidad, metodo="penalizacion", poblacion=100, generaciones=500,
                     tasa_mutacion=0.1, elitismo=2, semilla=42):
    validar_capacidad(capacidad)
    if metodo not in ("penalizacion", "reparacion"):
        raise ValueError("Método: penalizacion o reparacion.")
    for nombre, valor, minimo in (("poblacion", poblacion, 3), ("generaciones", generaciones, 0), ("elitismo", elitismo, 0)):
        if isinstance(valor, bool) or not isinstance(valor, (int, np.integer)) or valor < minimo:
            raise ValueError(f"{nombre} debe ser un entero >= {minimo}.")
    if elitismo >= poblacion:
        raise ValueError("El elitismo debe ser menor que la población.")
    if not 0 <= tasa_mutacion <= 1:
        raise ValueError("La tasa de mutación debe estar entre 0 y 1.")
    inicio = perf_counter()
    rng = np.random.default_rng(semilla)
    individuos = crear_poblacion(poblacion, rng)
    individuos[0] = np.zeros(len(OBJETOS), dtype=int)  # Garantía factible común a ambos métodos.
    if metodo == "reparacion":
        individuos = [reparar(ind, capacidad) for ind in individuos]
    mejor = individuos[0].copy()
    mejor_valor = -1
    generacion_mejor = 0
    historial = []
    for generacion in range(generaciones + 1):
        pesos = [calcular_peso(ind) for ind in individuos]
        valores = [calcular_valor(ind) for ind in individuos]
        aptitudes = [v - max(0, p - capacidad) * FACTOR_PENALIZACION for v, p in zip(valores, pesos)]
        validos = [i for i, peso in enumerate(pesos) if peso <= capacidad]
        if validos:
            indice = max(validos, key=lambda i: valores[i])
            if valores[indice] > mejor_valor:
                mejor = individuos[indice].copy()
                mejor_valor = valores[indice]
                generacion_mejor = generacion
        historial.append({"generacion": generacion, "mejor_valor_valido": mejor_valor,
                          "mejor_fitness_generacion": max(aptitudes), "individuos_validos": len(validos)})
        if generacion == generaciones:
            break
        orden = np.argsort(aptitudes, kind="stable")[::-1]
        nueva = [individuos[i].copy() for i in orden[:elitismo]]
        while len(nueva) < poblacion:
            a = seleccionar_torneo(individuos, aptitudes, rng)
            b = seleccionar_torneo(individuos, aptitudes, rng)
            hijo = mutar(cruzar(a, b, rng), tasa_mutacion, rng)
            if metodo == "reparacion":
                hijo = reparar(hijo, capacidad)
            nueva.append(hijo)
        individuos = nueva
    return {"capacidad": int(capacidad), "metodo": metodo, "poblacion": int(poblacion),
            "tasa_mutacion": float(tasa_mutacion), "elitismo": int(elitismo),
            "max_generaciones": int(generaciones), "semilla": semilla,
            "mejor_individuo": mejor.tolist(),
            "objetos_seleccionados": [o["nombre"] for gen, o in zip(mejor, OBJETOS) if gen],
            "peso_total": calcular_peso(mejor), "valor_total": mejor_valor,
            "fitness": fitness(mejor, capacidad), "generacion_mejor": generacion_mejor,
            "generaciones_ejecutadas": generacion, "tiempo_segundos": perf_counter() - inicio,
            "historial": historial}


def mostrar_resultado(resultado):
    print("Capacidad:", resultado["capacidad"])
    print("Método:", resultado["metodo"])
    print("Cromosoma:", resultado["mejor_individuo"])
    print("Objetos seleccionados:")
    for nombre in resultado["objetos_seleccionados"]:
        print("-", nombre)
    if not resultado["objetos_seleccionados"]:
        print("Ninguno (mochila vacía)")
    print("Peso total:", resultado["peso_total"])
    print("Valor total:", resultado["valor_total"])
    print("Generación del mejor resultado:", resultado["generacion_mejor"])
    print(f"Tiempo: {float(resultado['tiempo_segundos']):.6f} segundos")
