# Taller de Inteligencia Artificial: algoritmos genéticos

## Alcance actual

FASES 1, 2, 3 y 4 completas: N-Reinas, TSP, cursos/salas y mochila. Los originales `nreinas.py` y
`taller_ia_geneticos.pdf` se conservan intactos, al igual que los módulos y
resultados existentes de las tres fases anteriores. La web y el informe final
completo quedan fuera de esta etapa. El menú principal permite las cuatro fases y salir.

El PDF tiene tres páginas. Solicita conceptos, experimentación con los cuatro
problemas, informe comparativo y un aplicativo web. El aplicativo web de la
entrega final es un requisito adicional a la aplicación de consola pedida aquí.

## Archivos

```text
TALLER_IA/
├── taller_ia_geneticos.pdf       Original: instrucciones
├── nreinas.py                   Original: referencia de clase
├── main.py                      Menú principal y submenús de las cuatro fases
├── requirements.txt             Dependencias de ejecución
├── README.md                    Guía y metodología
├── pruebas_n_reinas.py          Pruebas de operadores y algoritmo
├── n_reinas/
│   ├── __init__.py              Exportaciones del paquete
│   ├── algoritmo.py             Algoritmo genético manual
│   ├── experimento.py           Experimentos y exportación CSV
│   └── visualizacion.py         Convergencia y tablero
└── resultados/n_reinas/
    ├── ejecucion.csv            Última ejecución individual
    ├── historial.csv            Historial de esa ejecución
    ├── convergencia.png         Curva de esa ejecución
    ├── tablero.png              Mejor tablero de esa ejecución
    ├── experimentos.csv         Una fila por corrida experimental
    ├── historiales.csv          Historial completo de todas las corridas
    ├── resumen.csv              Comparación de las 18 configuraciones
    ├── analisis.md              Análisis de las ejecuciones realizadas
    └── graficas/                Una PNG por corrida (180 por defecto)
```

La carpeta auxiliar `.dependencias_pruebas/` contiene dependencias instaladas
para verificar el proyecto en el entorno de desarrollo; no forma parte del
código ni debe copiarse a Spyder. Python puede crear carpetas `__pycache__/`.

## Instalación y ejecución

Se recomienda Python 3.10 o superior. Instalar en el mismo entorno que usa Spyder:

```bash
python -m pip install -r requirements.txt
```

Sólo se necesitan NumPy y Matplotlib. CSV, pathlib, time y unittest pertenecen
a Python. No se usa pandas, PySpark ni librerías de algoritmos genéticos.

En Visual Studio Code: abrir la carpeta del proyecto y ejecutar `python main.py`
desde una consola de Python de ese entorno. No se necesitan extensiones ni
archivos de configuración propios de VS Code.

En Spyder:

1. Copiar la carpeta del proyecto completa, conservando `n_reinas/`.
2. Abrir primero `main.py`.
3. En el selector de directorio de trabajo de Spyder, elegir la carpeta
   `TALLER_IA` que contiene `main.py`, no la subcarpeta `n_reinas`.
4. Configurar la ejecución del archivo para usar ese directorio y pulsar F5.
5. Responder al menú en la consola IPython; Enter acepta cada valor por defecto.

Las rutas de salida se calculan respecto a los archivos del proyecto con
`pathlib`, sin rutas absolutas específicas del equipo. Los módulos del paquete
pueden abrirse y editarse en Spyder; el punto de entrada de la aplicación es
`main.py`. Las gráficas pueden aparecer en el panel Gráficos de Spyder.

## Conceptos y relación con el ejemplo

Un algoritmo genético busca soluciones mediante una población que evoluciona
por selección y variación. Explora un espacio de combinaciones sin enumerarlo
completo; es una técnica de búsqueda y optimización de IA, no garantiza éxito.

- Población: lista de tableros candidatos.
- Individuo/cromosoma: permutación de las filas `0..N-1`.
- Gen: fila de la reina en la columna indicada por su posición.
- Fitness: negativo del número de parejas que se atacan; se maximiza hasta 0.
- Selección: mejores individuos, correspondientes a la mitad de la población.
- Cruce: un punto entre padres y reparación de filas repetidas con las faltantes.
- Mutación: intercambio de dos posiciones distintas, con probabilidad por hijo.
- Elitismo: cantidad configurable de mejores individuos copiados sin alteración.
- Reemplazo: élites más hijos hasta conservar el tamaño de población.
- Parada: cero conflictos o alcanzar el máximo de generaciones.

La permutación evita conflictos de fila y columna. Las diagonales se detectan
cuando `abs(fila_i-fila_j) == abs(i-j)`. Cada pareja se cuenta una sola vez.
La función también cuenta filas iguales, como la referencia. Una aptitud mal
diseñada favorece soluciones que no resuelven el problema real.

La referencia usa `fitness=-ataques`: mayor es mejor, aunque su etiqueta de
gráfica indica lo contrario. Aquí se grafican conflictos (menor es mejor).
Se agregan elitismo, semillas locales, validación de parámetros y devolución
del mejor global incluso cuando no se consigue cero. No se ejecuta el original
al importar el paquete. El cruce admite N pequeños y el swap nunca elige dos
veces la misma posición. N=2 y N=3 no tienen solución; agotarán el presupuesto.

Para permutaciones son apropiados OX/PMX o cruces reparados y swap/inversión;
el cruce simple sin reparación puede repetir y perder elementos. Para binarios,
cruce de uno/dos puntos y bit-flip conservan el dominio. Una mutación muy baja
reduce diversidad; una muy alta puede deshacer combinaciones favorables.
La selección de mejores padres también puede llevar a convergencia prematura.

## Parámetros y experimentación

`resolver(n=8, poblacion=100, generaciones=500, tasa_mutacion=0.10,
elitismo=2, semilla=42)` devuelve parámetros, solución, conflictos, éxito,
generación de primera aparición del mejor, generaciones ejecutadas, tiempo e
historial. Elitismo es una cantidad entera, no un porcentaje; cero lo desactiva.
Población mínima: 4. Generaciones: entero no negativo. Tasa: entre 0 y 1.

La generación 0 es la población inicial; 500 generaciones permiten hasta 500
reemplazos y 501 evaluaciones. Se evalúa también la última población creada.
El tiempo mide sólo el algoritmo, excluyendo gráficas y escritura de archivos.

La opción 2 ejecuta N=6/8, población=50/100/200, mutación=0.05/0.10/0.20:
18 combinaciones y 10 repeticiones por defecto, total 180 corridas. Semillas
2026..2035, presupuesto 500 y elitismo 2. Misma semilla y versiones reproducen
los resultados, excepto tiempos, que dependen del equipo. No se descartan
fracasos. La generación media se calcula sólo sobre éxitos y debe interpretarse
junto a su tasa de éxito. Una solución inicial se registra con generación cero.

Los CSV usan UTF-8 con BOM, coma como separador y punto decimal. Cada ejecución
tiene identificador para relacionar su fila con su historial y gráfica. Volver
a ejecutar reemplaza los CSV de igual nombre; copiar resultados antes de una
comparación histórica. Los archivos originales nunca se modifican.

## Comprobaciones

```bash
python -m unittest pruebas_n_reinas -v
python -m compileall main.py n_reinas pruebas_n_reinas.py
```

Las pruebas revisan conteo conocido, preservación de permutaciones, swap,
reproducibilidad, elitismo, entradas inválidas, generación cero y fracaso
conservando el mejor tablero. Los experimentos comprueban N=6 y N=8.
El usuario confirmó que N-Reinas funciona en Spyder con Anaconda y Python 3.13.
Las pruebas automatizadas de esta integración se realizan con Python normal;
no se ha abierto la interfaz de Spyder desde el entorno de desarrollo.

## FASE 2: TSP

Archivos añadidos:

```text
tsp/
├── __init__.py          Exporta resolver_tsp, calcular_distancia y fitness
├── datos.py             Coordenadas fijas y matriz euclidiana
├── algoritmo.py         Torneo, OX, mutaciones, elitismo y reemplazo
├── experimento.py       40 corridas, CSV, estadísticas y análisis automático
└── visualizacion.py     Convergencia, recorrido cerrado y comparación
pruebas_tsp.py           Pruebas de validez y comportamiento
pruebas_integracion.py   Menús y guardado temporal sin alterar N-Reinas
verificacion_preservacion.json  Huellas previas de los archivos protegidos
resultados/tsp/
├── ejecucion.csv        Ejecución individual o mejor corrida del último lote
├── historial.csv        Historial de la ejecución seleccionada
├── experimentos.csv    40 resultados finales
├── historiales.csv     40 × 501 evaluaciones
├── resumen.csv         Estadísticas por tipo y tasa
├── convergencia.png    Mejor distancia acumulada
├── mejor_ruta.png      Ciudades y recorrido con regreso al inicio
├── comparacion_mutaciones.png  Distancias promedio
└── analisis.md          Respuestas al PDF basadas en las corridas
```

La instancia principal usa las primeras 10 coordenadas de `tsp/datos.py`.
El menú permite entre 3 y 15 ciudades tomando prefijos de la misma tabla fija;
las cinco coordenadas adicionales permiten explorar 15 ciudades. Las distancias
son euclidianas en unidades abstractas, con diagonal cero y matriz simétrica.
Los experimentos oficiales de esta fase usan exclusivamente 10 ciudades.

Cada cromosoma contiene todas las ciudades una sola vez. `calcular_distancia`
incluye la arista desde la última a la primera, aunque el cromosoma no repite
esa ciudad. Sin argumento matriz utiliza la instancia principal de 10 ciudades.
La aptitud es `1/(distancia+1e-12)`; el torneo selecciona la menor distancia
entre tres candidatos aleatorios, lo que equivale a maximizar esa aptitud.

OX copia un segmento entre dos posiciones inclusivas del primer padre y
completa circularmente desde el final del segmento siguiendo el segundo padre,
sin duplicados. Valida cada hijo. Swap intercambia posiciones; inversion invierte
un segmento inclusivo. La probabilidad de mutación se aplica por hijo.
Los padres no se modifican. Las mejores dos rutas pasan sin cambios por defecto;
el resto de la población se reemplaza por hijos. Elitismo admite cero.

`resolver_tsp(numero_ciudades=10, poblacion=100, generaciones=500,
tasa_mutacion=0.1, tipo_mutacion="swap", elitismo=2, semilla=42)` conserva la
mejor ruta global y su primera generación. Completa siempre el presupuesto:
generación 0 más 500 reemplazos = 501 entradas de historial. No afirma haber
encontrado el óptimo global. Menor distancia significa mejor solución.

En Spyder: abrir `main.py`, elegir `TALLER_IA` como directorio de trabajo y
pulsar F5. Elegir **2 → 1**, aceptar valores por defecto o escribir `inversion`
como mutación. Al terminar, **3** muestra convergencia y recorrido en el panel
Gráficos. **2** ejecuta las 40 corridas. **4** vuelve al menú principal.
N-Reinas sigue disponible en **1**, con sus mismas opciones.
No hay dependencias adicionales ni cambios de configuración de Spyder.

Experimentos: swap/inversion × 0.05/0.20 × 10 repeticiones, población 100,
500 generaciones, elitismo 2 y semillas 2026..2035 para cada combinación.
`resumen.csv` informa mínimo, máximo, media, desviación estándar muestral
(divisor n-1), tiempo medio y generación media de la mejor solución.
Los tiempos sólo incluyen el algoritmo. `analisis.md` se calcula a partir
del lote real; no supone anticipadamente que alguna mutación sea mejor.
Los CSV se guardan con UTF-8 BOM y separador coma.

Al finalizar un lote, las gráficas individuales muestran su mejor corrida.
Una ejecución individual posterior actualiza esos archivos sin alterar el lote
experimental; para guardar varios lotes, usar un `directorio` distinto al llamar
`ejecutar_experimentos`. La opción de mostrar gráficas también puede recuperar
las imágenes guardadas si no hay una ejecución individual en memoria.

Pruebas de ambas fases:

```bash
python -m unittest pruebas_tsp pruebas_n_reinas pruebas_integracion -v
python -m compileall main.py tsp pruebas_tsp.py
```

## FASE 3: asignación de cursos a salas

Implementación con penalización, sin reparación. Usa los mismos NumPy y
Matplotlib y librerías estándar; no requiere dependencias adicionales.

```text
cursos_salas/
├── __init__.py          Exporta el solucionador y la evaluación
├── datos.py             Ocho cursos, cuatro salas, cinco franjas y bloqueos
├── algoritmo.py         Penalización, torneo, cruce, mutación, horario y AG
├── experimento.py       Veinte corridas, CSV, resumen y análisis calculado
└── visualizacion.py     Convergencia, comparación y tabla de horario
pruebas_cursos_salas.py  Diez pruebas de restricciones y operadores
verificacion_preservacion_fase3.json  Huellas de los 210 archivos protegidos
resultados/cursos_salas/
├── ejecucion.csv
├── historial.csv
├── horario.csv
├── experimentos.csv
├── historiales.csv
├── resumen.csv
├── analisis.md
├── convergencia.png
├── comparacion_elitismo.png
└── horario.png
```

Los cursos incluyen Programación, Bases de Datos, Diseño Multimedia, Modelado
3D, Análisis de Datos, Inteligencia Artificial, Redes y Ética Profesional.
Las salas difieren en capacidad, computadores, software y recursos como GPU,
tabletas gráficas y equipos de red. Cada curso ocupa exactamente una franja de
dos horas. No se modelan docentes, grupos compartidos ni cursos de varias franjas.
Los IDs de salas/cursos son índices desde cero. Hay bloqueos por sala y por curso.

El cromosoma es una matriz de ocho filas y dos columnas: cada fila corresponde
al curso en `CURSOS`, con `(sala, franja)`. Repetir sala o franja es permitido;
repetir el par para dos cursos produce choque. La población inicial es aleatoria
sin filtrar factibilidad. El torneo elige la menor penalización entre tres
candidatos. El cruce de un punto copia genes completos y la mutación, con
probabilidad por hijo, cambia una sala, una franja o ambas a valores distintos.

Penalizaciones duras: 100 por condición incumplida y curso (sobrecupo,
computadores insuficientes, software faltante, recurso indispensable faltante,
bloqueo de curso o bloqueo de sala); 200 por pareja en la misma sala y franja.
Varias restricciones pueden penalizar simultáneamente una asignación.
Software se penaliza una vez por curso si falta al menos un programa.

La penalización blanda suma los cursos que exceden `ceil(8/4)=2` por sala y
`ceil(8/5)=2` por franja. Su máximo es 12: nunca compensa una infracción dura.
Cero exige cumplir las restricciones duras y el objetivo de equilibrio. Un
horario sin infracciones duras puede aún tener desequilibrio; se registra como
`valida_restricciones_duras=True`, pero `exito` sólo es verdadero si el total
es cero. El testigo de factibilidad en las pruebas se construyó a mano y no
se usa para inicializar ni resolver los experimentos.

`resolver_cursos_salas(poblacion=100, generaciones=500, tasa_mutacion=0.1,
elitismo=2, semilla=42)` devuelve la mejor programación histórica, desglose,
éxito, tiempo e historial. Elitismo 0 no reintroduce el mejor histórico; sólo
lo recuerda para informar. Elitismo 2 copia dos individuos a la nueva población.
La generación 0 representa la población inicial. Se para al encontrar cero
o alcanzar el máximo; la última población creada también se evalúa.

Experimentos oficiales: 10 semillas (2026..2035) para cada elitismo (0 y 2),
población 100, máximo 500 generaciones y mutación 0.1: exactamente 20 corridas.
La media y desviación muestral se calculan sobre penalizaciones finales de las
corridas; la generación media incluye todas las corridas. Los tiempos sólo
miden el algoritmo. Listas y desgloses se serializan como JSON dentro de CSV.
`historiales.csv` relaciona cada generación con su ejecución.

El horario CSV incluye software y observaciones de incumplimientos; `OK`
significa sin observaciones. La tabla PNG muestra la ocupación por sala/franja;
ante conflictos se deben consultar las observaciones detalladas del CSV.
Al terminar experimentos, los archivos individuales muestran la mejor corrida
del lote. Una ejecución individual posterior actualiza esos archivos, pero
no los CSV del lote. Un nuevo lote actualiza sus archivos de igual nombre;
para preservar lotes adicionales, pasar otro `directorio` a la función.

En Spyder con Anaconda y Python 3.13: abrir `main.py`, directorio de trabajo
`TALLER_IA`, pulsar F5 y seleccionar **3 → 1**. Enter acepta cada parámetro.
La opción **3** del submenú muestra PNG en el panel Gráficos; **4** imprime
el horario guardado (también después de reiniciar Spyder); **2** ejecuta las
20 corridas; **5** vuelve y **4** del menú principal sale. Las pruebas del menú
usan Python normal y Matplotlib; no se ha abierto la interfaz de Spyder aquí.

Sólo se modificaron el menú principal, README y las pruebas de integración:
las salidas anteriores del menú pasaron de 3 a 4. Los submenús internos de
N-Reinas y TSP permanecen iguales. Las pruebas de integración guardan archivos
temporales para no sobrescribir los resultados de las fases anteriores.

```bash
python -m unittest pruebas_cursos_salas pruebas_n_reinas pruebas_tsp pruebas_integracion -v
python -m compileall main.py cursos_salas pruebas_cursos_salas.py pruebas_integracion.py
```

## FASE 4: problema de la mochila

Se seleccionan objetos maximizando valor sin superar capacidad. Cada uno de
los 15 objetos aparece como un gen: 1 lo selecciona y 0 lo excluye. Esta
decisión sí/no permite un cromosoma binario, cruce de un punto y mutación
bit-flip. No se permiten fracciones ni varias unidades del mismo objeto.

```text
mochila/
├── __init__.py          Exporta el solucionador, peso y valor
├── datos.py             Exactamente 15 objetos fijos, capacidades y factor
├── algoritmo.py         Torneo, cruce, bit-flip, elitismo y ambos métodos
├── experimento.py       40 corridas, CSV, estadísticas y análisis calculado
└── visualizacion.py     Convergencia, comparación y objetos seleccionados
pruebas_mochila.py       14 pruebas de operadores, factibilidad y casos límite
verificacion_preservacion_fase4.json  Huellas de los 226 archivos protegidos
resultados/mochila/
├── ejecucion.csv
├── historial.csv
├── experimentos.csv
├── historiales.csv
├── resumen.csv
├── analisis.md
├── convergencia.png
├── comparacion_metodos.png
└── objetos_seleccionados.png
```

Datos: 15 objetos con ID, nombre, peso y valor, reproducibles y expresados en
unidades académicas. Capacidades experimentales: **30 y 45**, sin ajustes.
La capacidad del menú acepta cualquier entero no negativo. La población
es binaria aleatoria; una posición inicial se sustituye por la mochila vacía,
igual para ambos métodos, garantizando al menos una solución factible.
Los otros individuos pueden superar capacidad.

**Penalización:** `fitness = valor - max(0, peso-capacidad) * 813`.
El factor 813 es la suma de valores (812) más uno. Con pesos y capacidades
enteros, todo exceso es al menos uno; cualquier inválido tiene fitness negativo,
por debajo de cualquier válido. Los valores negativos se conservan, sin truncar.
Los individuos no se reparan en este método. El resultado final se elige sólo
entre los válidos vistos durante toda la ejecución, nunca entre los inválidos.

**Reparación:** antes de evaluar, elimina objetos seleccionados en orden
ascendente de valor/peso hasta cumplir capacidad, con desempate por ID.
Se aplica a la población inicial y después de cruce/mutación. No agrega
objetos ni modifica el padre. Como todos los reparados son válidos, su fitness
coincide con su valor. La estrategia es simple y no garantiza el óptimo.

El torneo maximiza fitness entre tres candidatos aleatorios. El cruce utiliza
un punto entre genes. La tasa de mutación es **por gen**, a diferencia de las
fases que mutan un individuo con cierta probabilidad: 0.1 implica en promedio
1.5 cambios por cromosoma de 15 genes. Elitismo copia los dos mejores por
defecto; admite cero. Guardar el mejor válido histórico no significa volverlo
a insertar cuando se desactiva el elitismo.

`resolver_mochila(capacidad, metodo="penalizacion", poblacion=100,
generaciones=500, tasa_mutacion=0.1, elitismo=2, semilla=42)` devuelve
parámetros, cromosoma, nombres seleccionados, peso, valor, fitness, primera
generación del mejor resultado, tiempo e historial. El historial muestra
el mejor valor válido acumulado, mejor fitness generacional y cantidad de
individuos válidos. Se ejecutan siempre las generaciones solicitadas: 500
reemplazos y 501 evaluaciones con generación 0 como población inicial.
No se usa un óptimo conocido ni parada por un valor concreto.

Experimentos: 30/45 × penalizacion/reparacion × 10 repeticiones = **40**.
Se usan población 100, generaciones 500, mutación 0.1, elitismo 2 y semillas
2026..2035 por combinación. El resumen incluye mejor/peor/media de valor,
desviación estándar muestral (n-1), peso medio, generación media y tiempo medio.
Los tiempos excluyen gráficas y escritura. Las comparaciones entre métodos se
hacen por capacidad; el análisis distingue convergencia en generaciones de
tiempo total. La mayor capacidad cambia el conjunto de soluciones posibles.

Las listas se serializan como JSON dentro de CSV UTF-8 con BOM. El lote
guarda todos los historiales. Al terminar, los archivos individuales muestran
la corrida de mayor valor de todo el lote (no implica superioridad de un método
entre capacidades distintas). Una ejecución individual actualiza esos archivos
sin cambiar los CSV experimentales. Para conservar varios lotes, pasar otro
`directorio` al ejecutar experimentos. No se escribe en resultados anteriores.

En **Spyder + Anaconda + Python 3.13**: abrir `main.py`, elegir `TALLER_IA`
como directorio de trabajo y pulsar F5. En el menú principal seleccionar
**4 → 1**, aceptar capacidad 30 o escribir 45 y elegir `penalizacion` o
`reparacion`. Enter acepta los demás parámetros. En el submenú, **2** ejecuta
las 40 corridas, **3** muestra gráficas guardadas y **4** muestra la selección
guardada incluso tras reiniciar Spyder. **5** vuelve al menú principal;
**5** del menú principal sale. Esta numeración de salida sustituye a la de
las guías históricas anteriores. No se modificaron sus submenús internos.

No hay dependencias nuevas: NumPy, Matplotlib y biblioteca estándar. La
carpeta `.dependencias_pruebas` sigue siendo auxiliar del entorno de desarrollo.
Las pruebas usan Python normal; no se abrió Spyder desde este entorno.

```bash
python -m unittest pruebas_mochila pruebas_n_reinas pruebas_tsp pruebas_cursos_salas pruebas_integracion -v
python -m compileall main.py mochila pruebas_mochila.py pruebas_integracion.py
```

Las pruebas de integración acceden a las cuatro fases, prueban guardado y
visualización con archivos temporales, y no sobrescriben resultados anteriores.
