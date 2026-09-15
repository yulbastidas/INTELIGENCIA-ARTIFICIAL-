# Taller de Inteligencia Artificial — algoritmos genéticos

Proyecto académico con cuatro soluciones implementadas manualmente: N-Reinas, Agente Viajero (TSP), Asignación de Cursos a Salas y Mochila. Incluye consola compatible con Spyder, experimentos reproducibles, resultados CSV, análisis Markdown, gráficas Matplotlib e interfaz web Streamlit.

Repositorio: https://github.com/yulbastidas/INTELIGENCIA-ARTIFICIAL-

Aplicativo desplegado: [URL DEL APLICATIVO EN RENDER]

El despliegue fue informado por la autora. Falta incorporar aquí la URL pública y las capturas de evidencia. El código de la web está en `app.py` y su presentación en `styles.css`; ambos utilizan los mismos algoritmos que la consola. No se emplean bibliotecas que implementen algoritmos genéticos automáticamente.

## Instalación y ejecución local

Desde la carpeta `TALLER_IA`, con el entorno de Python activado:

```bash
pip install -r requirements.txt
python main.py
```

Para la interfaz web:

```bash
streamlit run app.py
```

El navegador abre la interfaz; la terminal mantiene el servidor en ejecución. Para finalizarlo, Ctrl+C. Las dependencias actuales declaradas en `requirements.txt` son Streamlit, NumPy (>=1.23), Matplotlib (>=3.6) y pandas. NumPy se utiliza en los operadores; Matplotlib en las gráficas; pandas en tablas de la web. Los CSV experimentales se escriben con la biblioteca estándar. No hay PySpark ni configuración exclusiva de VS Code.

## Ejecución en Spyder

Conservar toda la carpeta del proyecto. Abrir primero `main.py`, seleccionar `TALLER_IA` como directorio de trabajo en Spyder y ejecutar con F5. Las cuatro opciones del menú principal corresponden, en orden, a N-Reinas, TSP, Cursos/Salas y Mochila; la opción 5 sale. En cada submenú, 1 ejecuta un caso y 2 los experimentos; las demás opciones muestran resultados y permiten volver. Enter acepta el parámetro predeterminado. Las gráficas se muestran con Matplotlib en el panel Gráficos según la configuración de Spyder.

El entorno de uso informado es Anaconda con Python 3.13. La validación documental se realizó en otro intérprete y queda identificada en `documentacion/regeneracion.json`; no equivale a una nueva prueba manual de Spyder. Las rutas de salida se calculan respecto a los módulos mediante pathlib, sin rutas internas del editor.

## Estructura y responsabilidades

```text
TALLER_IA/
├── main.py                       Menú de consola
├── app.py                        Interfaz Streamlit para los cuatro problemas
├── styles.css                    Estilos de la web
├── requirements.txt              Dependencias actuales
├── README.md                     Guía general
├── nreinas.py                    Referencia original del profesor
├── taller_ia_geneticos.pdf        Guía original
├── n_reinas/                     Algoritmo, experimentos y visualización
├── tsp/                          Datos, algoritmo, experimentos y visualización
├── cursos_salas/                 Datos, algoritmo, experimentos y visualización
├── mochila/                      Datos, algoritmo, experimentos y visualización
├── pruebas_*.py                  Pruebas unitarias y de integración
├── resultados/
│   ├── n_reinas/
│   ├── tsp/
│   ├── cursos_salas/
│   ├── mochila/
│   └── web/                      Salidas de la interfaz cuando se utiliza
└── documentacion/                Informe Word, matriz y trazabilidad
```

Cada paquete contiene `__init__.py`, `algoritmo.py`, `experimento.py` y `visualizacion.py`. TSP, Cursos/Salas y Mochila añaden `datos.py`. La lógica de búsqueda está separada de consola, web y exportación. Los originales del profesor se conservan intactos.

## Conceptos y metodología

Un individuo representa una solución; sus genes forman un cromosoma. Una población reúne candidatos que se evalúan con una función de aptitud. Selección y cruce combinan soluciones; mutación introduce variaciones; elitismo conserva los mejores individuos en la población siguiente. Se registra además el mejor histórico. Guardar ese histórico no equivale a reinsertarlo cuando el elitismo vale cero.

Todos los algoritmos utilizan semillas controladas. La generación 0 corresponde a la población inicial. La generación de la mejor solución es su primera aparición; el tiempo medido corresponde al algoritmo, excluyendo la exportación de CSV y figuras. Una curva estable no certifica el óptimo global.

### N-Reinas

Permutación de filas: índice = columna y valor = fila. Se minimizan ataques por pares mediante fitness = −conflictos. Selección aleatoria desde la mejor mitad, cruce de un punto con reparación de duplicados y mutación swap por individuo. Reemplazo con elitismo configurable. Finaliza al obtener cero conflictos o alcanzar el límite.

La función `n_reinas.algoritmo.resolver` permite configurar N, población, generaciones, mutación, elitismo y semilla. Se comparan N=6/8, poblaciones 50/100/200 y tasas 0.05/0.10/0.20: 18 configuraciones con diez semillas cada una. Los 180 registros activos contienen 170 éxitos; los resultados por grupo están en `resumen.csv`. El script original de experimentación genera también un PNG por corrida si se vuelve a ejecutar; esa colección no es necesaria para la entrega actual, que conserva todos los historiales y una comparación compacta.

### Agente Viajero

Permutaciones válidas de ciudades sobre coordenadas fijas. La distancia euclidiana incluye el retorno al inicio. Existe fitness = 1/(distancia+epsilon), pero la selección por torneo de tres compara directamente la menor distancia. Cruce OX y mutación swap o inversión; no se implementan PMX ni inserción. Ejecuta el máximo de generaciones y guarda la mejor distancia encontrada.

Se realizaron 40 corridas: 10 ciudades, población 100, 500 generaciones, dos élites, tasas 0.05/0.20 y dos mutaciones, diez semillas por grupo. Todos los grupos terminaron con distancia 329.31823027761055. La inversión encontró ese resultado en menor generación media, pero no obtuvo rutas finales más cortas ni certifica optimalidad global.

### Cursos y Salas

Ocho genes (sala, franja), cuatro salas y cinco franjas. Inicialización aleatoria sin reparación. Torneo de tres, cruce de un punto entre genes completos y mutación de sala, franja o ambas en un curso. Se minimiza penalización: 100 por condición dura incumplida y curso (sobrecupo, computadores, software, recurso, bloqueo de curso o sala); 200 por pareja con misma sala/franja. La concentración que supera dos cursos por sala o franja suma un punto por exceso. Cero implica cumplir las restricciones duras y el equilibrio definido. Se detiene en cero o al límite.

Se comparan élites 0 y 2 con población 100, máximo 500 generaciones y tasa 0.1. Las 20 corridas regeneradas conservan las semillas 2026–2035 y reproducen los historiales previos. Ambas variantes alcanzan cero en 10/10; generación media 15.9 sin elitismo y 19.3 con elitismo. Los nuevos tiempos reales constan en los CSV. Esto no prueba superioridad general de una variante.

### Mochila

Quince objetos fijos y cromosoma binario: cada gen decide seleccionar o no un objeto. Se maximiza valor con capacidades 30 y 45. Torneo de tres, cruce de un punto, bit-flip independiente por gen y elitismo. Se ejecuta el máximo de generaciones y siempre se devuelve el mejor individuo válido histórico; una mochila vacía inicial asegura una alternativa factible.

Penalización: fitness = valor − max(0, peso−capacidad) × 813. El factor es la suma de todos los valores más uno; con pesos enteros, todo inválido tiene fitness negativo. No se trunca a cero. Reparación: eliminar seleccionados de menor valor/peso, desempate por ID, hasta respetar capacidad; no agrega objetos. Se repara antes de evaluar población inicial e hijos.

Se conservan 40 corridas, diez por capacidad/método, población 100, 500 generaciones, tasa 0.1 por gen y dos élites. Ambos métodos alcanzan valor 422 con peso 30 y valor 552 con peso 45. Reparación encuentra esos valores en menor generación media, pero consume mayor tiempo total medio en las mediciones almacenadas.

## Resultados y experimentación

En cada subcarpeta de `resultados/`:

- `experimentos.csv`: corridas completas con parámetros, semilla y resultados.
- `resumen.csv`: estadísticas por configuración.
- `historiales.csv`: evolución de todas las corridas.
- `ejecucion.csv` e `historial.csv`: caso representativo o última ejecución individual.
- `convergencia.png`: curva del caso individual.
- `analisis.md`: interpretación y límites de los resultados.

Se añaden `tablero.png` y `comparacion_parametros.png` en N-Reinas; `mejor_ruta.png` y `comparacion_mutaciones.png` en TSP; `horario.csv`, `horario.png` y `comparacion_elitismo.png` en Cursos/Salas; `objetos_seleccionados.png` y `comparacion_metodos.png` en Mochila.

Hay 280 filas experimentales activas: 180 + 40 + 20 + 40. Para completar esta entrega se repitieron únicamente las 20 corridas de Cursos/Salas y dos casos representativos (N-Reinas y Mochila). No deben sumarse los respaldos como experimentos nuevos. Una ejecución individual actualiza sus CSV/PNG sin alterar el lote experimental; ejecutar experimentos vuelve a escribir el lote. Para conservar otros lotes, las funciones admiten un `directorio` de salida diferente.

## Pruebas

```bash
python -m unittest pruebas_n_reinas pruebas_tsp pruebas_cursos_salas pruebas_mochila pruebas_integracion -v
```

Las pruebas cubren operadores, validez, evaluación y acceso desde los cuatro menús. Las de integración utilizan directorios temporales para el guardado. La última verificación y el estado de la importación web constan en `documentacion/pruebas.txt` y `documentacion/verificacion.json`.

## Informe y entrega

`documentacion/Informe_Taller_IA.docx` contiene conceptos, metodología, tablas, figuras, conclusiones específicas y comparación de los algoritmos genéticos como técnica de IA. `documentacion/matriz_cumplimiento.md` vincula la guía con cada evidencia. Los CSV completos acompañan al informe como evidencia digital. Antes de entregar, completar la portada, URL de Render y capturas reales pendientes; no se han inventado imágenes del despliegue.
