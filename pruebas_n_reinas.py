"""Pruebas de invariantes y casos límite. Ejecutar este archivo o unittest."""

import unittest
import numpy as np
from n_reinas.algoritmo import contar_conflictos, fitness, cruzar, mutar, resolver


class PruebasNReinas(unittest.TestCase):
    def test_conflictos(self):
        self.assertEqual(contar_conflictos([1, 3, 0, 2]), 0)
        self.assertEqual(fitness([0, 1, 2, 3]), -6)

    def test_operadores(self):
        rng = np.random.default_rng(10)
        for n in (1, 2, 6, 8):
            for _ in range(100):
                a, b = rng.permutation(n), rng.permutation(n)
                copia = a.copy()
                hijo = cruzar(a, b, rng)
                self.assertEqual(sorted(hijo), list(range(n)))
                mutado = mutar(hijo, 1, rng)
                self.assertEqual(sorted(mutado), list(range(n)))
                np.testing.assert_array_equal(a, copia)
                if n > 1:
                    self.assertEqual(int(np.count_nonzero(mutado != hijo)), 2)

    def test_limites_y_fracaso(self):
        self.assertTrue(resolver(n=1)["exito"])
        r = resolver(n=3, generaciones=5)
        self.assertFalse(r["exito"])
        self.assertEqual(len(r["historial"]), 6)
        self.assertEqual(r["conflictos"], contar_conflictos(r["mejor_solucion"]))
        self.assertEqual(resolver(generaciones=0)["generaciones_ejecutadas"], 0)
        for parametros in ({"n": 0}, {"poblacion": 3}, {"elitismo": 100},
                           {"tasa_mutacion": 1.1}, {"generaciones": -1}):
            with self.assertRaises(ValueError):
                resolver(**parametros)

    def test_reproducibilidad_y_elitismo(self):
        for elites in (0, 2):
            a = resolver(n=8, generaciones=50, elitismo=elites, semilla=99)
            b = resolver(n=8, generaciones=50, elitismo=elites, semilla=99)
            self.assertEqual(a["historial"], b["historial"])
            self.assertEqual(a["mejor_solucion"], b["mejor_solucion"])
            self.assertEqual(a["conflictos"], contar_conflictos(a["mejor_solucion"]))
            if elites:
                h = [x["conflictos_generacion"] for x in a["historial"]]
                self.assertTrue(all(y <= x for x, y in zip(h, h[1:])))


if __name__ == "__main__":
    unittest.main()
