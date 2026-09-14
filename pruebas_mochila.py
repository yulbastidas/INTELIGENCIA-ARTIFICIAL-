"""Pruebas de operadores, factibilidad final y casos límite de Mochila."""

import unittest
from unittest.mock import patch
import numpy as np
from mochila.datos import OBJETOS
from mochila.algoritmo import (crear_poblacion, calcular_peso, calcular_valor, fitness,
                               reparar, cruzar, mutar, resolver_mochila)


class PruebasMochila(unittest.TestCase):
    def test_quince_objetos(self):
        self.assertEqual(len(OBJETOS), 15)
        self.assertEqual([o["id"] for o in OBJETOS], list(range(15)))

    def test_poblacion_binaria(self):
        for ind in crear_poblacion(100, np.random.default_rng(7)):
            self.assertEqual(len(ind), 15)
            self.assertTrue(set(ind).issubset({0, 1}))

    def test_peso(self):
        ind = np.zeros(15, dtype=int)
        ind[:2] = 1
        self.assertEqual(calcular_peso(ind), 12)

    def test_valor(self):
        ind = np.zeros(15, dtype=int)
        ind[:2] = 1
        self.assertEqual(calcular_valor(ind), 165)

    def test_penalizacion(self):
        ind = np.ones(15, dtype=int)
        self.assertLess(fitness(ind, 30), 0)
        self.assertEqual(fitness(ind, 1000), calcular_valor(ind))

    def test_reparacion_factible(self):
        for capacidad in (0, 1, 30, 45):
            ind = reparar(np.ones(15, dtype=int), capacidad)
            self.assertLessEqual(calcular_peso(ind), capacidad)
            self.assertTrue(set(ind).issubset({0, 1}))

    def test_reparacion_orden_y_copias(self):
        ind = np.zeros(15, dtype=int)
        ind[[0, 4]] = 1  # Laptop ratio 12.5; carpa ratio 7.5.
        r = reparar(ind, 12)
        self.assertEqual(r[0], 1)
        self.assertEqual(r[4], 0)
        self.assertEqual(ind[4], 1)

    def test_cruce(self):
        rng = np.random.default_rng(10)
        for _ in range(100):
            a, b = crear_poblacion(2, rng)
            hijo = cruzar(a, b, rng)
            self.assertEqual(len(hijo), 15)
            self.assertTrue(set(hijo).issubset({0, 1}))

    def test_mutacion(self):
        ind = np.arange(15) % 2
        rng = np.random.default_rng(5)
        np.testing.assert_array_equal(mutar(ind, 1, rng), 1 - ind)
        np.testing.assert_array_equal(mutar(ind, 0, rng), ind)
        self.assertTrue(set(mutar(ind, 0.1, rng)).issubset({0, 1}))

    def test_resolver_penalizacion(self):
        r = resolver_mochila(30, poblacion=20, generaciones=10)
        self.assertLessEqual(r["peso_total"], 30)
        self.assertEqual(r["valor_total"], calcular_valor(r["mejor_individuo"]))
        self.assertEqual(r["fitness"], r["valor_total"])

    def test_resolver_reparacion(self):
        r = resolver_mochila(45, "reparacion", poblacion=20, generaciones=10)
        self.assertLessEqual(r["peso_total"], 45)
        self.assertTrue(all(h["individuos_validos"] == 20 for h in r["historial"]))

    def test_historial_y_reproducibilidad(self):
        for metodo in ("penalizacion", "reparacion"):
            r = resolver_mochila(30, metodo, poblacion=20, generaciones=8)
            s = resolver_mochila(30, metodo, poblacion=20, generaciones=8)
            self.assertEqual(r["historial"], s["historial"])
            self.assertEqual(r["mejor_individuo"], s["mejor_individuo"])
            self.assertEqual(len(r["historial"]), 9)
            self.assertEqual(r["generaciones_ejecutadas"], 8)
            h = [x["mejor_valor_valido"] for x in r["historial"]]
            self.assertTrue(all(b >= a for a, b in zip(h, h[1:])))
            self.assertEqual(h.index(h[-1]), r["generacion_mejor"])

    def test_fallback_vacio(self):
        with patch("mochila.algoritmo.crear_poblacion", return_value=[np.ones(15, dtype=int) for _ in range(3)]):
            r = resolver_mochila(0, poblacion=3, generaciones=0, elitismo=0)
        self.assertEqual(r["peso_total"], 0)
        self.assertEqual(r["valor_total"], 0)
        self.assertEqual(r["objetos_seleccionados"], [])

    def test_parametros(self):
        for kwargs in ({"capacidad": -1}, {"capacidad": 1.5}, {"capacidad": 30, "metodo": "otro"},
                       {"capacidad": 30, "elitismo": 100}, {"capacidad": 30, "tasa_mutacion": 2}):
            with self.assertRaises(ValueError):
                resolver_mochila(**kwargs)


if __name__ == "__main__":
    unittest.main()
