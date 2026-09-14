"""Cromosoma de pares (sala, franja); restricciones por penalización, sin reparación."""

from collections import Counter
from time import perf_counter
import numpy as np
from .datos import CURSOS, SALAS, FRANJAS


def validar_individuo(individuo):
    if len(individuo) != len(CURSOS):
        raise ValueError("Se requiere una asignación por curso (8 genes).")
    for gen in individuo:
        if len(gen) != 2 or any(isinstance(x, (bool, np.bool_)) or not isinstance(x, (int, np.integer)) for x in gen):
            raise ValueError("Cada gen debe contener dos enteros: sala y franja.")
        if not (0 <= gen[0] < len(SALAS) and 0 <= gen[1] < len(FRANJAS)):
            raise ValueError("Sala o franja fuera del dominio permitido.")


def evaluar_penalizacion(individuo):
    """Devuelve total, desglose aditivo y observaciones por curso.

    Duras: 100 por condición incumplida; choques: 200 por pareja.
    Blanda: 1 por curso que excede ceil(cursos/salas) o ceil(cursos/franjas).
    Para estos datos su máximo es 12: nunca compensa una infracción dura.
    """
    validar_individuo(individuo)
    detalles = dict.fromkeys(("sobrecupo", "computadores", "software", "recursos",
                             "choques", "bloqueo_curso", "bloqueo_sala", "equilibrio"), 0)
    observaciones = [[] for _ in CURSOS]
    for i, (sala_id, franja) in enumerate(individuo):
        curso, sala = CURSOS[i], SALAS[sala_id]
        condiciones = [
            ("sobrecupo", curso["cantidad_estudiantes"] > sala["capacidad"], "Sobrecupo"),
            ("computadores", curso["requiere_computadores"] and curso["cantidad_estudiantes"] > sala["cantidad_computadores"], "Computadores insuficientes"),
            ("software", not set(curso["software_requerido"]).issubset(sala["software_disponible"]), "Software faltante"),
            ("recursos", curso["recurso_especial"] is not None and curso["recurso_especial"] not in sala["recursos"], "Recurso indispensable faltante"),
            ("bloqueo_curso", franja in curso["franjas_bloqueadas"], "Franja no permitida para el curso"),
            ("bloqueo_sala", franja in sala["franjas_bloqueadas"], "Sala bloqueada"),
        ]
        for clave, incumple, mensaje in condiciones:
            if incumple:
                detalles[clave] += 100
                observaciones[i].append(mensaje)
    for i in range(len(individuo)):
        for j in range(i + 1, len(individuo)):
            if tuple(individuo[i]) == tuple(individuo[j]):
                detalles["choques"] += 200
                observaciones[i].append(f"Choque con {CURSOS[j]['nombre']}")
                observaciones[j].append(f"Choque con {CURSOS[i]['nombre']}")
    salas = Counter(int(gen[0]) for gen in individuo)
    franjas = Counter(int(gen[1]) for gen in individuo)
    limite_salas = (len(CURSOS) + len(SALAS) - 1) // len(SALAS)
    limite_franjas = (len(CURSOS) + len(FRANJAS) - 1) // len(FRANJAS)
    detalles["equilibrio"] = sum(max(0, n - limite_salas) for n in salas.values()) + sum(max(0, n - limite_franjas) for n in franjas.values())
    for i, (sala, franja) in enumerate(individuo):
        if salas[sala] > limite_salas or franjas[franja] > limite_franjas:
            observaciones[i].append("Concentración excesiva (restricción blanda)")
    return {"total": sum(detalles.values()), "detalles": detalles, "observaciones": observaciones}


def fitness(individuo):
    return 1.0 / (1 + evaluar_penalizacion(individuo)["total"])


def crear_poblacion(tamano, rng):
    return [np.column_stack((rng.integers(len(SALAS), size=len(CURSOS)),
                             rng.integers(len(FRANJAS), size=len(CURSOS)))) for _ in range(tamano)]


def seleccionar_torneo(poblacion, penalizaciones, rng):
    indices = rng.choice(len(poblacion), size=3, replace=False)
    return poblacion[min(indices, key=lambda i: penalizaciones[i])].copy()


def cruzar(padre1, padre2, rng):
    punto = int(rng.integers(1, len(CURSOS)))
    hijo = np.concatenate((padre1[:punto], padre2[punto:])).copy()
    validar_individuo(hijo)
    return hijo


def mutar(individuo, tasa, rng):
    """Con probabilidad por hijo cambia sala, franja o ambas a valores distintos."""
    hijo = individuo.copy()
    if rng.random() < tasa:
        curso = int(rng.integers(len(CURSOS)))
        cambio = int(rng.integers(3))
        if cambio in (0, 2):
            hijo[curso, 0] = (hijo[curso, 0] + int(rng.integers(1, len(SALAS)))) % len(SALAS)
        if cambio in (1, 2):
            hijo[curso, 1] = (hijo[curso, 1] + int(rng.integers(1, len(FRANJAS)))) % len(FRANJAS)
    validar_individuo(hijo)
    return hijo


def resolver_cursos_salas(poblacion=100, generaciones=500, tasa_mutacion=0.1, elitismo=2, semilla=42):
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
    mejor_penalizacion = float("inf")
    historial = []
    for generacion in range(generaciones + 1):
        penalizaciones = [evaluar_penalizacion(ind)["total"] for ind in individuos]
        indice = int(np.argmin(penalizaciones))
        if penalizaciones[indice] < mejor_penalizacion:
            mejor_penalizacion = penalizaciones[indice]
            mejor = individuos[indice].copy()
            generacion_mejor = generacion
        historial.append({"generacion": generacion, "penalizacion_generacion": penalizaciones[indice],
                          "mejor_penalizacion": mejor_penalizacion})
        if mejor_penalizacion == 0 or generacion == generaciones:
            break
        orden = np.argsort(penalizaciones, kind="stable")
        nueva = [individuos[i].copy() for i in orden[:elitismo]]
        while len(nueva) < poblacion:
            padre1 = seleccionar_torneo(individuos, penalizaciones, rng)
            padre2 = seleccionar_torneo(individuos, penalizaciones, rng)
            nueva.append(mutar(cruzar(padre1, padre2, rng), tasa_mutacion, rng))
        individuos = nueva
    detalles = evaluar_penalizacion(mejor)["detalles"]
    return {"poblacion": int(poblacion), "tasa_mutacion": float(tasa_mutacion), "elitismo": int(elitismo),
            "max_generaciones": int(generaciones), "semilla": semilla, "mejor_individuo": mejor.tolist(),
            "penalizacion": mejor_penalizacion, "generacion_mejor": generacion_mejor,
            "generaciones_ejecutadas": generacion, "tiempo_segundos": perf_counter() - inicio,
            "historial": historial, "detalles_penalizacion": detalles,
            "exito": mejor_penalizacion == 0,
            "valida_restricciones_duras": mejor_penalizacion - detalles["equilibrio"] == 0}


def construir_horario(individuo):
    evaluacion = evaluar_penalizacion(individuo)
    return [{"Curso": CURSOS[i]["nombre"], "Estudiantes": CURSOS[i]["cantidad_estudiantes"],
             "Sala": SALAS[sala]["nombre"], "Capacidad sala": SALAS[sala]["capacidad"],
             "Franja": FRANJAS[franja], "Software requerido": ", ".join(CURSOS[i]["software_requerido"]) or "Ninguno",
             "Estado / observaciones": "; ".join(evaluacion["observaciones"][i]) or "OK"}
            for i, (sala, franja) in enumerate(individuo)]


def mostrar_horario(filas):
    columnas = list(filas[0])
    anchos = {c: max(len(c), max(len(str(f[c])) for f in filas)) for c in columnas}
    print(" | ".join(c.ljust(anchos[c]) for c in columnas))
    print("-+-".join("-" * anchos[c] for c in columnas))
    for fila in filas:
        print(" | ".join(str(fila[c]).ljust(anchos[c]) for c in columnas))
