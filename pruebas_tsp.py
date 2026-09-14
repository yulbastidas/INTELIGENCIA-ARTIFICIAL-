"""Pruebas TSP: ejecutar con python -m unittest pruebas_tsp -v."""

import unittest
import numpy as np
from tsp.datos import crear_matriz_distancias, obtener_coordenadas
from tsp.algoritmo import (crear_poblacion, validar_ruta, calcular_distancia,
                           fitness, cruzar_ox, mutar, resolver_tsp)


class CortesFijos:
    def choice(self, *args, **kwargs):
        return np.array([2, 5])

    def random(self):
        return 0.0


class PruebasTSP(unittest.TestCase):
    def test_poblacion_valida(self):
        for ruta in crear_poblacion(100, 10, np.random.default_rng(8)):
            self.assertEqual(sorted(ruta), list(range(10)))
            self.assertEqual(len(set(ruta)), 10)

    def test_distancia_cerrada_y_matriz(self):
        matriz = crear_matriz_distancias([[0, 0], [3, 0], [3, 4]])
        self.assertEqual(calcular_distancia([0, 1, 2], matriz), 12.0)
        self.assertAlmostEqual(fitness([0, 1, 2], matriz), 1 / 12)
        np.testing.assert_array_equal(matriz, matriz.T)
        np.testing.assert_array_equal(np.diag(matriz), np.zeros(3))

    def test_ox_orden_conocido(self):
        padre1 = np.arange(8)
        padre2 = np.array([7, 6, 5, 4, 3, 2, 1, 0])
        hijo = cruzar_ox(padre1, padre2, CortesFijos())
        np.testing.assert_array_equal(hijo, [7, 6, 2, 3, 4, 5, 1, 0])
        np.testing.assert_array_equal(padre1, np.arange(8))

    def test_ox_permutaciones(self):
        rng = np.random.default_rng(1)
        for n in (3, 8, 10, 15):
            for _ in range(100):
                hijo = cruzar_ox(rng.permutation(n), rng.permutation(n), rng)
                self.assertEqual(sorted(hijo), list(range(n)))

    def test_mutaciones(self):
        ruta = np.arange(8)
        np.testing.assert_array_equal(mutar(ruta, 1, "swap", CortesFijos()), [0, 1, 5, 3, 4, 2, 6, 7])
        np.testing.assert_array_equal(mutar(ruta, 1, "inversion", CortesFijos()), [0, 1, 5, 4, 3, 2, 6, 7])
        np.testing.assert_array_equal(ruta, np.arange(8))
        rng = np.random.default_rng(5)
        for tipo in ("swap", "inversion"):
            for _ in range(100):
                self.assertEqual(sorted(mutar(rng.permutation(10), 1, tipo, rng)), list(range(10)))
            np.testing.assert_array_equal(mutar(ruta, 0, tipo, rng), ruta)

    def test_resultado_historial_y_reproducibilidad(self):
        for tipo in ("swap", "inversion"):
            a = resolver_tsp(poblacion=20, generaciones=12, tipo_mutacion=tipo)
            b = resolver_tsp(poblacion=20, generaciones=12, tipo_mutacion=tipo)
            self.assertEqual(a["mejor_ruta"], b["mejor_ruta"])
            self.assertEqual(a["historial"], b["historial"])
            self.assertEqual(sorted(a["mejor_ruta"]), list(range(10)))
            self.assertGreater(a["mejor_distancia"], 0)
            self.assertEqual(a["mejor_distancia"], calcular_distancia(a["mejor_ruta"]))
            self.assertEqual(len(a["historial"]), 13)
            self.assertEqual(a["generaciones_ejecutadas"], 12)
            h = [x["mejor_distancia"] for x in a["historial"]]
            self.assertTrue(all(y <= x for x, y in zip(h, h[1:])))
            self.assertEqual(h[-1], a["mejor_distancia"])
            self.assertEqual(h.index(h[-1]), a["generacion_mejor"])

    def test_limites_y_validacion(self):
        self.assertEqual(len(resolver_tsp(generaciones=0)["historial"]), 1)
        self.assertEqual(resolver_tsp(elitismo=0, generaciones=2)["generaciones_ejecutadas"], 2)
        for n in (8, 15):
            r = resolver_tsp(numero_ciudades=n, generaciones=1)
            self.assertEqual(sorted(r["mejor_ruta"]), list(range(n)))
        for parametros in ({"numero_ciudades": 16}, {"poblacion": 2}, {"elitismo": 100},
                           {"tasa_mutacion": -1}, {"generaciones": -1}, {"tipo_mutacion": "otro"}):
            with self.assertRaises(ValueError):
                resolver_tsp(**parametros)
        with self.assertRaises(ValueError):
            validar_ruta([0, 0, 2], 3)
        with self.assertRaises(ValueError):
            cruzar_ox(np.arange(3), np.array([0, 0, 2]), np.random.default_rng(2))


if __name__ == "__main__":
    unittest.main()
