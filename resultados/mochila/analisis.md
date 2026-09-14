# Mochila: análisis de la fase 4

40 corridas reales: capacidades 30 y 45, dos métodos, población 100, 500 generaciones, mutación 0.1 por gen y elitismo 2. Semillas registradas en experimentos.csv.

| Capacidad | Método | Mejor | Peor | Promedio | Desv. muestral | Peso medio | Generación media | Tiempo medio (s) |
|---|---|---|---|---|---|---|---|---|
| 30 | penalizacion | 422 | 422 | 422.000 | 0.000 | 30.00 | 14.90 | 4.145976 |
| 30 | reparacion | 422 | 422 | 422.000 | 0.000 | 30.00 | 1.60 | 5.563907 |
| 45 | penalizacion | 552 | 552 | 552.000 | 0.000 | 45.00 | 25.30 | 4.127337 |
| 45 | reparacion | 552 | 552 | 552.000 | 0.000 | 45.00 | 8.70 | 5.742110 |

## 1. ¿Por qué cromosomas binarios?

Cada uno de los 15 genes decide seleccionar (1) o no seleccionar (0) un objeto. No hay cantidades múltiples ni fracciones de objeto: es una mochila 0/1. Los cromosomas representan 2^15 combinaciones posibles.

## 2. Penalización frente a reparación

Penalización: fitness = valor - max(0, peso-capacidad) × 813. El factor es la suma de todos los valores más uno. Los pesos y capacidades son enteros: todo inválido tiene fitness negativo y no supera a un válido, cuyo valor es no negativo. No se trunca a cero, para diferenciar individuos inválidos.

Reparación: antes de evaluar, elimina seleccionados de menor valor/peso hasta cumplir capacidad; desempata por ID. No añade objetos. El fitness de un reparado es su valor porque no tiene exceso. Ambos métodos comparten operadores, semillas y una mochila vacía inicial. Penalización no repara individuos; se conserva por separado el mejor válido de todas las generaciones.

## 3. ¿Cuál método funcionó mejor?

Capacidad 30: penalización obtuvo media 422.000 y máximo 422; reparación, media 422.000 y máximo 422.
- mayor valor promedio: empate (422.0000).
- mayor valor máximo: empate (422.0000).
- menor generación media: reparacion (1.6000).
- mayor tiempo medio: reparacion (5.5639).
Capacidad 45: penalización obtuvo media 552.000 y máximo 552; reparación, media 552.000 y máximo 552.
- mayor valor promedio: empate (552.0000).
- mayor valor máximo: empate (552.0000).
- menor generación media: reparacion (8.7000).
- mayor tiempo medio: reparacion (5.7421).

## 4. Efecto de la capacidad

penalizacion: al pasar de capacidad 30 a 45, el valor promedio pasó de 422.000 a 552.000, y el peso medio de 30.00 a 45.00.
reparacion: al pasar de capacidad 30 a 45, el valor promedio pasó de 422.000 a 552.000, y el peso medio de 30.00 a 45.00.

Conceptualmente, una capacidad mayor amplía el conjunto factible: el óptimo teórico no puede disminuir. Eso no garantiza que una heurística encuentre siempre un resultado mejor. Aquí se comparan las corridas reales de la misma instancia.

## 5. Ventajas, desventajas y límites

Conceptualmente, penalizar mantiene los cromosomas originales y es sencillo, pero exige un factor adecuado y puede gastar evaluaciones en inválidos. Reparar garantiza factibilidad antes de evaluar, pero añade trabajo y sesga la búsqueda hacia objetos eficientes individualmente; la mejor combinación no tiene por qué obtenerse con una regla voraz. Los tiempos y valores observados arriba son evidencia de estas corridas, no una demostración general de superioridad.

Se completan 500 reemplazos y 501 evaluaciones contando generación 0. No hay parada por valor objetivo ni óptimo exacto calculado. La generación del mejor se refiere a su primera aparición. El historial muestra mejor valor válido acumulado, incluso si no sobrevive sin elitismo. Los tiempos excluyen CSV y PNG. Desviación muestral usa divisor n-1. Diez semillas por combinación y una instancia no establecen superioridad estadística general.

Al finalizar el lote, ejecucion.csv y las gráficas individuales muestran la corrida de mayor valor del lote; comparar métodos siempre dentro de cada capacidad. Una ejecución individual posterior actualiza esos archivos. Los CSV experimentales conservan el lote. No se modifica ningún resultado de las fases anteriores.
