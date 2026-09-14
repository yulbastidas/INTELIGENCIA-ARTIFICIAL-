"""Comprueba menús sin sobrescribir los resultados existentes de N-Reinas."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
import main
from tsp.experimento import guardar_ejecucion


class PruebasIntegracion(unittest.TestCase):
    def test_n_reinas_desde_menu(self):
        # Ejecuta el algoritmo real, pero sustituye únicamente el guardado.
        respuestas = ["1", "1", "8", "100", "20", "0.1", "2", "42", "4", "5"]
        with patch("builtins.input", side_effect=respuestas), patch.object(main, "guardar_ejecucion") as guardar:
            with redirect_stdout(io.StringIO()):
                main.main()
        resultado = guardar.call_args.args[0]
        self.assertEqual(resultado["conflictos"], 0)

    def test_tsp_desde_menu_y_guardado(self):
        respuestas = ["2", "1", "10", "20", "5", "0.2", "inversion", "2", "42", "3", "4", "5"]
        with tempfile.TemporaryDirectory() as directorio:
            def guardar_temporal(resultado):
                guardar_ejecucion(resultado, directorio)
            with patch("builtins.input", side_effect=respuestas), patch("tsp.experimento.guardar_ejecucion", side_effect=guardar_temporal):
                with patch("matplotlib.pyplot.show"), redirect_stdout(io.StringIO()) as salida:
                    main.main()
            self.assertIn("Distancia total:", salida.getvalue())
            for nombre in ("ejecucion.csv", "historial.csv", "convergencia.png", "mejor_ruta.png"):
                self.assertTrue((Path(directorio) / nombre).is_file())


    def test_cursos_salas_desde_menu(self):
        from cursos_salas.experimento import guardar_ejecucion as guardar_cursos
        respuestas = ["3", "4", "3", "1", "20", "10", "0.1", "2", "42", "4", "3", "5", "5"]
        with tempfile.TemporaryDirectory() as directorio:
            def guardar_temporal(resultado):
                guardar_cursos(resultado, directorio)
            with patch("builtins.input", side_effect=respuestas), patch("cursos_salas.experimento.DIRECTORIO", Path(directorio)):
                with patch("cursos_salas.experimento.guardar_ejecucion", side_effect=guardar_temporal), patch("matplotlib.pyplot.show"):
                    with redirect_stdout(io.StringIO()) as salida:
                        main.main()
            self.assertIn("Penalización total:", salida.getvalue())
            self.assertIn("Programación", salida.getvalue())
            for nombre in ("ejecucion.csv", "historial.csv", "horario.csv", "convergencia.png", "horario.png"):
                self.assertTrue((Path(directorio) / nombre).is_file())


    def test_mochila_desde_menu(self):
        from mochila.experimento import guardar_ejecucion as guardar_mochila
        respuestas = ["4", "4", "3", "1", "30", "reparacion", "20", "5", "0.1", "2", "42", "4", "3", "5", "5"]
        with tempfile.TemporaryDirectory() as directorio:
            def guardar_temporal(resultado):
                guardar_mochila(resultado, directorio)
            with patch("builtins.input", side_effect=respuestas), patch("mochila.experimento.DIRECTORIO", Path(directorio)):
                with patch("mochila.experimento.guardar_ejecucion", side_effect=guardar_temporal), patch("matplotlib.pyplot.show"):
                    with redirect_stdout(io.StringIO()) as salida:
                        main.main()
            self.assertIn("Objetos seleccionados:", salida.getvalue())
            self.assertIn("Valor total:", salida.getvalue())
            for nombre in ("ejecucion.csv", "historial.csv", "convergencia.png", "objetos_seleccionados.png"):
                self.assertTrue((Path(directorio) / nombre).is_file())


if __name__ == "__main__":
    unittest.main()
