# Análisis experimental TSP

40 ejecuciones reales de 10 ciudades, población 100, 500 generaciones y elitismo 2. Las semillas están en experimentos.csv.

Mejor distancia: 329.318230. Peor: 329.318230. Promedio global: 329.318230 unidades.

| Mutación | Tasa | Mejor | Peor | Promedio | Desv. muestral | Generación media |
|---|---|---|---|---|---|---|
| swap | 0.05 | 329.318230 | 329.318230 | 329.318230 | 0.000000 | 10.80 |
| swap | 0.20 | 329.318230 | 329.318230 | 329.318230 | 0.000000 | 10.60 |
| inversion | 0.05 | 329.318230 | 329.318230 | 329.318230 | 0.000000 | 8.60 |
| inversion | 0.20 | 329.318230 | 329.318230 | 329.318230 | 0.000000 | 8.60 |

## 1. ¿Por qué controlar duplicados?

Cada cromosoma es una permutación: cada ciudad aparece exactamente una vez. Un cruce binario simple puede duplicar ciudades y omitir otras. OX conserva un segmento y completa el resto en el orden circular del otro padre, omitiendo las ciudades ya copiadas. Cada hijo se valida explícitamente.

## 2. ¿Qué pasa si aumenta el número de ciudades?

Teóricamente existen N! permutaciones. En TSP simétrico, al identificar rotaciones y recorridos inversos, quedan (N-1)!/2 ciclos diferentes para N>=3. El crecimiento factorial hace más difícil explorar el espacio; evaluar cada ruta también exige más aristas. Estos experimentos usan sólo 10 ciudades: no demuestran rendimiento para 8 o 15 ciudades.

## 3. ¿Qué mutación encontró mejores rutas?

Promedio agrupado swap: 329.318230; inversión: 329.318230.
Ambas estrategias empataron en distancia promedio dentro de tolerancia numérica.
La primera aparición de la mejor ruta ocurrió en generación media 10.70 para swap. Esto mide rapidez de convergencia, no una mejora adicional de distancia final.
La primera aparición de la mejor ruta ocurrió en generación media 8.60 para inversion. Esto mide rapidez de convergencia, no una mejora adicional de distancia final.

## 4. ¿Qué efecto tuvieron las tasas?

Para swap, pasar de 0.05 a 0.20 cambió la distancia media de 329.318230 a 329.318230 (diferencia +0.000000; negativa significa mejora).
Para inversion, pasar de 0.05 a 0.20 cambió la distancia media de 329.318230 a 329.318230 (diferencia +0.000000; negativa significa mejora).

## Interpretación y límites

Se compara el mejor resultado final de cada corrida, no todos los individuos. La desviación es muestral (divisor n-1). La generación 0 es la población inicial; cada corrida completa el presupuesto y guarda 501 evaluaciones con 500 generaciones. Los tiempos excluyen CSV y gráficas. Menor distancia es mejor; el fitness inverso se maximiza y el torneo usa directamente distancias, con orden equivalente.

No se calculó un óptimo exacto: mejor encontrada no significa óptima demostrada. Diez semillas por combinación y una instancia no permiten generalizar superioridad estadística. Misma semilla y versiones permiten repetir rutas e historiales; los tiempos dependen del equipo.

Las figuras convergencia.png y mejor_ruta.png corresponden al caso individual guardado en ejecucion.csv e historial.csv: semilla 42, población 100, 500 generaciones, swap, tasa 0.10 y dos élites; distancia 329.31823027761055, generación de mejor resultado 12. No corresponde a una de las cuatro configuraciones experimentales (tasas 0.05 y 0.20). comparacion_mutaciones.png utiliza resumen.csv.
