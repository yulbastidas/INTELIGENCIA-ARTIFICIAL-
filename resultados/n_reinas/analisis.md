# Resultados reales de la fase 1

Se ejecutaron 180 corridas: 18 configuraciones por 10 semillas (2026..2035),
elitismo 2 y máximo 500 generaciones. Hubo 170 éxitos (94.44 %) y 10 fracasos.
Los CSV contienen las soluciones, tiempos y generaciones efectivamente medidas.

| N | Población | Éxitos con 0.05 | Éxitos con 0.10 | Éxitos con 0.20 |
|---|---|---|---|---|
| 6 | 50 | 6/10 | 7/10 | 9/10 |
| 6 | 100 | 10/10 | 10/10 | 10/10 |
| 6 | 200 | 10/10 | 10/10 | 10/10 |
| 8 | 50 | 8/10 | 10/10 | 10/10 |
| 8 | 100 | 10/10 | 10/10 | 10/10 |
| 8 | 200 | 10/10 | 10/10 | 10/10 |

Con población 50, aumentar la mutación mejoró la tasa de éxito observada. Para
N=8, la generación media entre éxitos bajó de 46.5 a 11.8 y 5.0 al aumentar la
tasa de 0.05 a 0.10 y 0.20. Para N=6, la tasa 0.20 logró rescatar corridas
difíciles: su media entre éxitos fue 44.44 generaciones, frente a 1.67 con 0.05.
La media menor de 0.05 no implica superioridad: excluye cuatro fracasos.

Las poblaciones de 100 y 200 alcanzaron el 100 % de éxito en esta muestra.
Una población mayor ofrece más candidatos iniciales, pero evaluar una
generación cuesta más. Las medias inferiores a una generación incluyen
soluciones presentes en la población inicial (generación 0); no se deben
atribuir únicamente a los operadores evolutivos.

Los diez fracasos conservaron un tablero con un conflicto. Esto es compatible
con pérdida de diversidad por selección de los mejores y elitismo. No se midió
diversidad directamente, por lo que esa explicación es una interpretación,
no una causa demostrada. No se modificó el algoritmo para ocultar fracasos.

Una prueba individual N=8, población 100, mutación 0.10 y semilla 42 encontró
`[2, 6, 1, 7, 5, 3, 0, 4]`, sin conflictos, en generación 4. Después, la prueba
del menú con población 20 y límite 10 sobrescribió los archivos individuales
con un ejemplo de fracaso controlado (un conflicto). Los experimentos se
conservan separados en `experimentos.csv` y `historiales.csv`.

## Verificación

- Cuatro pruebas unittest aprobadas, incluyendo 400 ensayos de operadores.
- Compilación de todos los archivos Python nuevos sin errores de sintaxis.
- Imports del menú, algoritmo, experimentos y visualización correctos.
- Menú probado con entradas simuladas: gráfica sin ejecución previa,
  ejecución configurable, guardado y salida.
- 180 cromosomas comprobados como permutaciones válidas y conflictos
  recalculados independientemente de los valores guardados.
- 180 PNG experimentales generadas; gráfica individual revisada visualmente.
- SHA-256 de los originales idénticos antes y después:
  - nreinas.py: `2ACC719B4B3CD25D2E54B24DFF34A719A84B661F903E95099B3ACDCD137B8944`
  - taller_ia_geneticos.pdf: `9B1321C8E388FBE9CC26C1E8E8DFF3DE3B3F48164086E6D0F4A410063B3786E0`

Entorno de los experimentos: Python 3.12, NumPy 2.5.3 y Matplotlib 3.11.2.
La interfaz de Spyder no se abrió; la compatibilidad se basa en Python normal,
imports de paquete y rutas respecto a los archivos. Los tiempos dependen del
equipo y su carga, y diez semillas no bastan para asegurar superioridad
estadística general. La siguiente fase es TSP; no se implementó en esta entrega.
