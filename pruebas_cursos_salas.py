"""Casos conocidos e invariantes de los operadores y la penalización."""

import unittest
import numpy as np
from cursos_salas.algoritmo import (crear_poblacion, validar_individuo, evaluar_penalizacion,
                                    cruzar, mutar, resolver_cursos_salas, construir_horario)


class PruebasCursosSalas(unittest.TestCase):
    def setUp(self):
        # Testigo construido a mano para probar que cero es alcanzable, no resultado experimental.
        self.valido = np.array([(0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 3), (3, 2), (3, 3)])

    def test_solucion_cero(self):
        self.assertEqual(evaluar_penalizacion(self.valido)["total"], 0)
        self.assertTrue(all(f["Estado / observaciones"] == "OK" for f in construir_horario(self.valido)))

    def test_poblacion_estructura(self):
        for ind in crear_poblacion(100, np.random.default_rng(8)):
            self.assertEqual(ind.shape, (8, 2))
            self.assertTrue(np.all((ind[:, 0] >= 0) & (ind[:, 0] < 4)))
            self.assertTrue(np.all((ind[:, 1] >= 0) & (ind[:, 1] < 5)))

    def test_sobrecupo_y_computadores(self):
        self.valido[0] = (3, 0)
        d = evaluar_penalizacion(self.valido)["detalles"]
        self.assertEqual(d["sobrecupo"], 100)
        self.assertEqual(d["computadores"], 100)

    def test_software_y_recursos(self):
        self.valido[2] = (0, 2)
        d = evaluar_penalizacion(self.valido)["detalles"]
        self.assertEqual(d["software"], 100)
        self.assertEqual(d["recursos"], 100)

    def test_choques_por_pareja(self):
        self.valido[1] = self.valido[0]
        self.assertEqual(evaluar_penalizacion(self.valido)["detalles"]["choques"], 200)
        self.valido[2] = self.valido[0]
        self.assertEqual(evaluar_penalizacion(self.valido)["detalles"]["choques"], 600)

    def test_bloqueos(self):
        self.valido[0] = (0, 4)
        d = evaluar_penalizacion(self.valido)["detalles"]
        self.assertEqual(d["bloqueo_curso"], 100)
        self.assertEqual(d["bloqueo_sala"], 100)

    def test_equilibrio_y_desglose(self):
        self.valido[7] = (0, 3)
        evaluacion = evaluar_penalizacion(self.valido)
        self.assertEqual(evaluacion["detalles"]["equilibrio"], 1)
        self.assertEqual(evaluacion["total"], sum(evaluacion["detalles"].values()))

    def test_operadores(self):
        rng = np.random.default_rng(3)
        original = self.valido.copy()
        for _ in range(100):
            hijo = cruzar(self.valido, crear_poblacion(1, rng)[0], rng)
            self.assertEqual(hijo.shape, (8, 2))
            mutado = mutar(hijo, 1, rng)
            validar_individuo(mutado)
            self.assertEqual(np.count_nonzero(np.any(hijo != mutado, axis=1)), 1)
        np.testing.assert_array_equal(original, self.valido)

    def test_resolver_historial_reproducibilidad(self):
        for elites in (0, 2):
            r = resolver_cursos_salas(poblacion=20, generaciones=5, elitismo=elites)
            validar_individuo(r["mejor_individuo"])
            self.assertEqual(r["penalizacion"], evaluar_penalizacion(r["mejor_individuo"])["total"])
            self.assertEqual(len(r["historial"]), r["generaciones_ejecutadas"] + 1)
            h = [x["mejor_penalizacion"] for x in r["historial"]]
            self.assertTrue(all(b <= a for a, b in zip(h, h[1:])))
            self.assertEqual(h.index(min(h)), r["generacion_mejor"])
            self.assertEqual(r["historial"], resolver_cursos_salas(poblacion=20, generaciones=5, elitismo=elites)["historial"])

    def test_parametros_y_cero_generaciones(self):
        self.assertEqual(len(resolver_cursos_salas(generaciones=0)["historial"]), 1)
        for kwargs in ({"poblacion": 2}, {"elitismo": 100}, {"tasa_mutacion": 2}, {"generaciones": -1}):
            with self.assertRaises(ValueError):
                resolver_cursos_salas(**kwargs)


if __name__ == "__main__":
    unittest.main()
