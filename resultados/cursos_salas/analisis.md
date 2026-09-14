# Asignación de cursos a salas: análisis

Se realizaron 20 corridas reales con 8 cursos, 4 salas y 5 franjas, población 100, máximo 500 generaciones y tasa 0.1. Semillas registradas en experimentos.csv.

| Elitismo | Mejor | Peor | Promedio | Desv. muestral | Generación media | Éxitos (cero) |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0.000 | 0.000 | 15.90 | 10/10 |
| 2 | 0 | 0 | 0.000 | 0.000 | 19.30 | 10/10 |

## 1. Restricciones duras y blandas

Duras: sobrecupo, computadores insuficientes cuando se requieren, software faltante, recurso indispensable faltante, franja prohibida del curso y bloqueo de sala: 100 puntos por condición y curso. Choques: 200 puntos por pareja de cursos en la misma sala y franja, contada una sola vez. Tres cursos producen tres parejas.

Blanda: un punto por curso que excede dos asignaciones en una sala, más un punto por curso que excede dos en una franja. El máximo blando para 8 cursos es 12, menor que cualquier infracción dura. Total cero implica cumplimiento duro y equilibrio. Un horario sin conflictos duros puede tener penalización blanda positiva: se registra también valida_restricciones_duras, pero éxito exige total cero.

## 2. Penalizar frente a reparar

Se implementó exclusivamente penalización. Permite explorar horarios inviables con operadores simples y un desglose explicable, pero exige elegir pesos y puede converger sin resolver todos los conflictos. Reparar puede recuperar factibilidad tras los operadores, pero requiere reglas adicionales, puede introducir sesgo y resolver un conflicto creando otro. No se experimentó con reparación, por lo que no se afirma que sea mejor o peor empíricamente.

## 3. Aumentar el número de cursos

Con 4 salas y 5 franjas, el espacio estructural es 20^C para C cursos; para ocho es 25 600 000 000 cromosomas antes de aplicar restricciones. Más cursos aumentan las posibilidades de choque y pueden exigir más población o generaciones, o hacer imposible el horario por falta de recursos. Sólo se experimentó con ocho cursos; esto es una explicación conceptual, no un resultado medido.

## 4. Efecto observado del elitismo

Sin elitismo: media 0.000, 10 éxitos, generación media 15.90. Con elitismo: media 0.000, 10 éxitos, generación media 19.30.
Las versiones empataron en penalización promedio final.

Elitismo copia individuos a la siguiente población; guardar el mejor histórico sólo conserva el resultado para informar y no lo reintroduce cuando elitismo=0. La gráfica muestra mejor acumulada; el CSV también incluye mejor de cada generación. Generación 0 es la población inicial. Se detiene al alcanzar cero o el límite.

Desviación muestral: divisor n-1. La generación media incluye todas las corridas, también fracasos; debe interpretarse con la tasa de éxito. Tiempo excluye CSV y gráficas. Diez semillas por variante y una instancia no permiten generalizar superioridad estadística. No se ha probado la interfaz de Spyder desde este entorno.

El horario y las gráficas individuales representan la mejor corrida del lote al terminar los experimentos. Una ejecución individual posterior los actualiza sin cambiar experimentos.csv. Los resultados de N-Reinas y TSP no se escriben.
