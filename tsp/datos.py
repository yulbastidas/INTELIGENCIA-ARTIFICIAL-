"""Coordenadas fijas en unidades abstractas; no cambian entre ejecuciones."""

import numpy as np

# Las primeras diez ciudades son la instancia principal del experimento.
# Las cinco últimas permiten explorar 15 ciudades sin datos aleatorios nuevos.
COORDENADAS = np.array([
    [10, 20], [20, 80], [35, 45], [45, 10], [50, 65],
    [60, 30], [70, 90], [80, 55], [90, 15], [95, 75],
    [15, 55], [30, 95], [55, 50], [75, 5], [100, 40],
], dtype=float)
COORDENADAS.setflags(write=False)


def obtener_coordenadas(numero_ciudades=10):
    """Permite de 3 a 15 ciudades, siempre tomando el mismo prefijo."""
    if (isinstance(numero_ciudades, bool)
            or not isinstance(numero_ciudades, (int, np.integer))
            or not 3 <= numero_ciudades <= len(COORDENADAS)):
        raise ValueError("El número de ciudades debe ser un entero entre 3 y 15.")
    return COORDENADAS[:numero_ciudades].copy()


def crear_matriz_distancias(coordenadas):
    coordenadas = np.asarray(coordenadas, dtype=float)
    if (coordenadas.ndim != 2 or coordenadas.shape[1] != 2
            or len(coordenadas) < 2 or not np.isfinite(coordenadas).all()):
        raise ValueError("Las coordenadas deben ser una matriz finita de pares X,Y.")
    diferencias = coordenadas[:, None, :] - coordenadas[None, :, :]
    return np.sqrt(np.sum(diferencias ** 2, axis=2))


MATRIZ_DISTANCIAS = crear_matriz_distancias(obtener_coordenadas())
MATRIZ_DISTANCIAS.setflags(write=False)
