# N-Reinas — análisis verificado

## Diseño y resultados
180 corridas: N=6 y N=8; poblaciones 50, 100 y 200; tasas 0.05, 0.10 y 0.20; diez semillas (2026–2035) por grupo, máximo 500 generaciones y dos élites.
Se obtuvieron 170 soluciones sin conflictos (94.44%); los diez fracasos terminaron con un conflicto.

| N | Población | Mutación | Éxitos de 10 | Generación media de éxitos | Tiempo medio s |
|---|---|---|---|---|---|
| 6 | 50 | 0.05 | 6 | 1.67 | 0.671643 |
| 6 | 50 | 0.1 | 7 | 1.43 | 0.477156 |
| 6 | 50 | 0.2 | 9 | 44.44 | 0.300736 |
| 6 | 100 | 0.05 | 10 | 1.70 | 0.014038 |
| 6 | 100 | 0.1 | 10 | 1.70 | 0.012857 |
| 6 | 100 | 0.2 | 10 | 15.40 | 0.110811 |
| 6 | 200 | 0.05 | 10 | 0.80 | 0.015457 |
| 6 | 200 | 0.1 | 10 | 0.70 | 0.012634 |
| 6 | 200 | 0.2 | 10 | 0.80 | 0.016387 |
| 8 | 50 | 0.05 | 8 | 46.50 | 0.583322 |
| 8 | 50 | 0.1 | 10 | 11.80 | 0.049156 |
| 8 | 50 | 0.2 | 10 | 5.00 | 0.023548 |
| 8 | 100 | 0.05 | 10 | 2.00 | 0.019817 |
| 8 | 100 | 0.1 | 10 | 3.40 | 0.036269 |
| 8 | 100 | 0.2 | 10 | 1.90 | 0.021414 |
| 8 | 200 | 0.05 | 10 | 1.20 | 0.023235 |
| 8 | 200 | 0.1 | 10 | 1.00 | 0.021629 |
| 8 | 200 | 0.2 | 10 | 1.50 | 0.032917 |

La población 50 concentra todos los fracasos: para N=6, éxitos 6/10, 7/10 y 9/10 al aumentar la mutación; para N=8, 8/10, 10/10 y 10/10. Las poblaciones 100 y 200 alcanzan 10/10 en todos sus grupos. Esto describe estas semillas; no prueba que una población grande siempre garantice solución.
La generación media se calcula sólo sobre los éxitos. Por ello 44.44 generaciones para N=6, población 50 y mutación 0.20 no se interpreta aisladamente como peor comportamiento que 1.67 con tasa 0.05: la primera configuración resuelve nueve casos y la segunda sólo seis. No se midió diversidad directamente.

## Implementación
Permutación de filas; índice = columna. Fitness = −conflictos por pares. Selección desde la mejor mitad; cruce de un punto con reparación de duplicados; mutación swap por individuo; reemplazo con élites. Parada al alcanzar cero o el máximo. Guardar mejor histórico no equivale a elitismo.

## Evidencia gráfica actual
convergencia.png y tablero.png corresponden a ejecucion.csv e historial.csv: N=8, población 100, mutación 0.10, élites 2 y semilla 42; solución [2,6,1,7,5,3,0,4], cero conflictos en generación 4. Es una ejecución representativa adicional, no una fila nueva de experimentos.csv.
comparacion_parametros.png se calculó directamente de resumen.csv. Todos los historiales experimentales están en historiales.csv. No se regeneraron 180 PNG individuales porque duplicarían evidencia disponible.

## Límites
El fitness negativo se maximiza; las gráficas muestran conflictos, que se minimizan. Cero certifica ausencia de ataques, no una garantía de éxito del algoritmo en cualquier corrida. Los tiempos excluyen exportación. Los 180 experimentos completos se conservaron; sólo se regeneró el caso representativo y se corrigió la documentación obsoleta.
