from pathlib import Path
from textwrap import dedent

import pandas as pd
import streamlit as st

from n_reinas.algoritmo import resolver as resolver_n_reinas
from n_reinas.visualizacion import (
    graficar_convergencia as convergencia_n_reinas,
    graficar_tablero as tablero_n_reinas,
)

from tsp.algoritmo import resolver_tsp
from tsp.visualizacion import (
    graficar_convergencia as convergencia_tsp,
    graficar_ruta as ruta_tsp,
)

from cursos_salas.algoritmo import (
    resolver_cursos_salas,
    construir_horario,
)
from cursos_salas.visualizacion import (
    graficar_convergencia as convergencia_cursos,
    graficar_horario as horario_cursos,
)

from mochila.algoritmo import resolver_mochila
from mochila.visualizacion import (
    graficar_convergencia as convergencia_mochila,
    graficar_objetos as objetos_mochila,
)


BASE_DIR = Path(__file__).resolve().parent
WEB_RESULTADOS = BASE_DIR / "resultados" / "web"
WEB_RESULTADOS.mkdir(parents=True, exist_ok=True)


st.set_page_config(
    page_title="Algoritmos Genéticos | IA",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)


def cargar_css():
    ruta = BASE_DIR / "styles.css"

    if ruta.exists():
        with open(ruta, "r", encoding="utf-8") as archivo:
            st.markdown(
                f"<style>{archivo.read()}</style>",
                unsafe_allow_html=True,
            )


def hero(etiqueta, icono, titulo, descripcion):
    st.markdown(
        dedent(
            f"""
            <div class="hero">
                <div class="badge">{etiqueta}</div>
                <div class="hero-title">{icono} {titulo}</div>
                <div class="hero-subtitle">
                    {descripcion}
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def metrica(titulo, valor):
    st.markdown(
        dedent(
            f"""
            <div class="result-card">
                <div class="result-title">{titulo}</div>
                <div class="result-value">{valor}</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def mostrar_inicio():
    hero(
        "INTELIGENCIA ARTIFICIAL",
        "🧬",
        "Algoritmos Genéticos",
        """
        Plataforma interactiva para experimentar con técnicas evolutivas
        aplicadas a problemas clásicos de búsqueda y optimización.
        """,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">4</div>
                <div class="metric-label">Problemas implementados</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">280</div>
                <div class="metric-label">Experimentos realizados</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">39</div>
                <div class="metric-label">Pruebas automatizadas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">100%</div>
                <div class="metric-label">Integración completada</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="custom-divider"></div>',
        unsafe_allow_html=True,
    )

    st.markdown("## Explora los algoritmos")

    izquierda, derecha = st.columns(2)

    with izquierda:
        st.markdown(
            dedent(
                """
                <div class="algorithm-card">
                    <div class="card-icon">♛</div>
                    <div class="card-title">N-Reinas</div>
                    <div class="card-description">
                        Encuentra una distribución de N reinas evitando
                        ataques entre ellas mediante selección,
                        cruzamiento y mutación.
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with derecha:
        st.markdown(
            dedent(
                """
                <div class="algorithm-card">
                    <div class="card-icon">🗺️</div>
                    <div class="card-title">Agente Viajero</div>
                    <div class="card-description">
                        Busca una ruta que visite todas las ciudades
                        exactamente una vez y regrese al punto inicial.
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    st.write("")

    izquierda, derecha = st.columns(2)

    with izquierda:
        st.markdown(
            dedent(
                """
                <div class="algorithm-card">
                    <div class="card-icon">🏫</div>
                    <div class="card-title">Cursos y Salas</div>
                    <div class="card-description">
                        Optimiza la asignación de cursos, salas y franjas
                        minimizando conflictos y penalizaciones.
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with derecha:
        st.markdown(
            dedent(
                """
                <div class="algorithm-card">
                    <div class="card-icon">🎒</div>
                    <div class="card-title">Problema de la Mochila</div>
                    <div class="card-description">
                        Maximiza el valor de los objetos seleccionados
                        sin superar la capacidad de la mochila.
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )


def pagina_n_reinas():
    hero(
        "PROBLEMA 01",
        "♛",
        "N-Reinas",
        """
        Encuentra posiciones para N reinas evitando que se ataquen
        entre filas, columnas y diagonales.
        """,
    )

    st.markdown("## ⚙️ Configuración")

    c1, c2, c3 = st.columns(3)

    with c1:
        n = st.number_input(
            "Número de reinas",
            min_value=4,
            max_value=20,
            value=8,
        )

    with c2:
        poblacion = st.number_input(
            "Tamaño de población",
            min_value=4,
            max_value=1000,
            value=100,
            step=10,
            key="nr_poblacion",
        )

    with c3:
        generaciones = st.number_input(
            "Máximo de generaciones",
            min_value=0,
            max_value=5000,
            value=500,
            step=10,
            key="nr_generaciones",
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        tasa = st.slider(
            "Tasa de mutación",
            0.0,
            1.0,
            0.10,
            0.01,
            key="nr_tasa",
        )

    with c5:
        elitismo = st.number_input(
            "Cantidad de élites",
            min_value=0,
            max_value=20,
            value=2,
            key="nr_elitismo",
        )

    with c6:
        semilla = st.number_input(
            "Semilla",
            min_value=0,
            value=42,
            key="nr_semilla",
        )

    if st.button(
        "🚀 Ejecutar N-Reinas",
        use_container_width=True,
    ):
        try:
            with st.spinner("Evolucionando población..."):
                resultado = resolver_n_reinas(
                    n=int(n),
                    poblacion=int(poblacion),
                    generaciones=int(generaciones),
                    tasa_mutacion=float(tasa),
                    elitismo=int(elitismo),
                    semilla=int(semilla),
                )

                ruta_tablero = WEB_RESULTADOS / "n_reinas_tablero.png"
                ruta_convergencia = WEB_RESULTADOS / "n_reinas_convergencia.png"

                tablero_n_reinas(
                    resultado,
                    destino=ruta_tablero,
                    mostrar=False,
                )

                convergencia_n_reinas(
                    resultado,
                    destino=ruta_convergencia,
                    mostrar=False,
                )

                st.session_state["n_reinas"] = resultado

        except Exception as error:
            st.error(f"Error al ejecutar N-Reinas: {error}")

    resultado = st.session_state.get("n_reinas")

    if resultado:
        st.markdown("---")
        st.markdown("## 🧬 Resultado")

        if resultado["exito"]:
            st.success("Solución válida encontrada: 0 conflictos.")
        else:
            st.warning(
                "No se encontró una solución perfecta con los parámetros indicados."
            )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metrica("Conflictos", resultado["conflictos"])

        with c2:
            metrica("Generación", resultado["generacion_mejor"])

        with c3:
            metrica("Población", resultado["poblacion"])

        with c4:
            metrica(
                "Tiempo",
                f"{resultado['tiempo_segundos']:.4f} s",
            )

        st.markdown("### 🧬 Cromosoma")

        st.code(
            str(resultado["mejor_solucion"]),
            language="text",
        )

        izquierda, derecha = st.columns(2)

        with izquierda:
            st.markdown("### ♛ Tablero solución")

            st.image(
                str(WEB_RESULTADOS / "n_reinas_tablero.png"),
                use_container_width=True,
            )

        with derecha:
            st.markdown("### 📈 Convergencia")

            st.image(
                str(WEB_RESULTADOS / "n_reinas_convergencia.png"),
                use_container_width=True,
            )


def pagina_tsp():
    hero(
        "PROBLEMA 02",
        "🗺️",
        "Agente Viajero",
        """
        Busca una ruta de mínima distancia que visite todas las
        ciudades exactamente una vez y regrese al punto inicial.
        """,
    )

    st.markdown("## ⚙️ Configuración")

    c1, c2, c3 = st.columns(3)

    with c1:
        ciudades = st.number_input(
            "Número de ciudades",
            min_value=3,
            max_value=15,
            value=10,
        )

    with c2:
        poblacion = st.number_input(
            "Tamaño de población",
            min_value=3,
            value=100,
            step=10,
            key="tsp_poblacion",
        )

    with c3:
        generaciones = st.number_input(
            "Máximo de generaciones",
            min_value=0,
            value=500,
            step=10,
            key="tsp_generaciones",
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        tasa = st.slider(
            "Tasa de mutación",
            0.0,
            1.0,
            0.10,
            0.01,
            key="tsp_tasa",
        )

    with c5:
        tipo = st.selectbox(
            "Tipo de mutación",
            ["swap", "inversion"],
        )

    with c6:
        elitismo = st.number_input(
            "Cantidad de élites",
            min_value=0,
            max_value=20,
            value=2,
            key="tsp_elitismo",
        )

    semilla = st.number_input(
        "Semilla",
        min_value=0,
        value=42,
        key="tsp_semilla",
    )

    if st.button(
        "🚀 Ejecutar Agente Viajero",
        use_container_width=True,
    ):
        try:
            with st.spinner("Buscando la mejor ruta..."):
                resultado = resolver_tsp(
                    numero_ciudades=int(ciudades),
                    poblacion=int(poblacion),
                    generaciones=int(generaciones),
                    tasa_mutacion=float(tasa),
                    tipo_mutacion=tipo,
                    elitismo=int(elitismo),
                    semilla=int(semilla),
                )

                ruta_grafica = WEB_RESULTADOS / "tsp_ruta.png"
                ruta_convergencia = WEB_RESULTADOS / "tsp_convergencia.png"

                ruta_tsp(
                    resultado,
                    destino=ruta_grafica,
                    mostrar=False,
                )

                convergencia_tsp(
                    resultado,
                    destino=ruta_convergencia,
                    mostrar=False,
                )

                st.session_state["tsp"] = resultado

        except Exception as error:
            st.error(f"Error al ejecutar TSP: {error}")

    resultado = st.session_state.get("tsp")

    if resultado:
        st.markdown("---")
        st.markdown("## 🗺️ Resultado")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metrica(
                "Distancia",
                f"{resultado['mejor_distancia']:.3f}",
            )

        with c2:
            metrica(
                "Generación",
                resultado["generacion_mejor"],
            )

        with c3:
            metrica(
                "Ciudades",
                resultado["numero_ciudades"],
            )

        with c4:
            metrica(
                "Tiempo",
                f"{resultado['tiempo_segundos']:.3f} s",
            )

        ruta = list(resultado["mejor_ruta"])

        if ruta:
            ruta.append(ruta[0])

        st.markdown("### 🧭 Mejor ruta")

        st.code(
            " → ".join(map(str, ruta)),
            language="text",
        )

        izquierda, derecha = st.columns(2)

        with izquierda:
            st.markdown("### 🗺️ Ruta encontrada")

            st.image(
                str(WEB_RESULTADOS / "tsp_ruta.png"),
                use_container_width=True,
            )

        with derecha:
            st.markdown("### 📈 Convergencia")

            st.image(
                str(WEB_RESULTADOS / "tsp_convergencia.png"),
                use_container_width=True,
            )


def pagina_cursos():
    hero(
        "PROBLEMA 03",
        "🏫",
        "Cursos y Salas",
        """
        Busca una programación académica válida minimizando
        sobrecupos, choques, bloqueos y recursos faltantes.
        """,
    )

    st.markdown("## ⚙️ Configuración")

    c1, c2, c3 = st.columns(3)

    with c1:
        poblacion = st.number_input(
            "Tamaño de población",
            min_value=3,
            value=100,
            step=10,
            key="cs_poblacion",
        )

    with c2:
        generaciones = st.number_input(
            "Máximo de generaciones",
            min_value=0,
            value=500,
            step=10,
            key="cs_generaciones",
        )

    with c3:
        tasa = st.slider(
            "Tasa de mutación",
            0.0,
            1.0,
            0.10,
            0.01,
            key="cs_tasa",
        )

    c4, c5 = st.columns(2)

    with c4:
        elitismo = st.number_input(
            "Cantidad de élites",
            min_value=0,
            max_value=20,
            value=2,
            key="cs_elitismo",
        )

    with c5:
        semilla = st.number_input(
            "Semilla",
            min_value=0,
            value=42,
            key="cs_semilla",
        )

    if st.button(
        "🚀 Generar horario",
        use_container_width=True,
    ):
        try:
            with st.spinner("Optimizando asignaciones..."):
                resultado = resolver_cursos_salas(
                    poblacion=int(poblacion),
                    generaciones=int(generaciones),
                    tasa_mutacion=float(tasa),
                    elitismo=int(elitismo),
                    semilla=int(semilla),
                )

                ruta_horario = WEB_RESULTADOS / "cursos_horario.png"
                ruta_convergencia = WEB_RESULTADOS / "cursos_convergencia.png"

                horario_cursos(
                    resultado,
                    destino=ruta_horario,
                    mostrar=False,
                )

                convergencia_cursos(
                    resultado,
                    destino=ruta_convergencia,
                    mostrar=False,
                )

                st.session_state["cursos"] = resultado

        except Exception as error:
            st.error(
                f"Error al ejecutar Cursos y Salas: {error}"
            )

    resultado = st.session_state.get("cursos")

    if resultado:
        st.markdown("---")
        st.markdown("## 🏫 Resultado")

        if resultado["penalizacion"] == 0:
            st.success(
                "Horario válido encontrado sin penalizaciones."
            )
        else:
            st.warning(
                f"Penalización total: {resultado['penalizacion']}"
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            metrica(
                "Penalización",
                resultado["penalizacion"],
            )

        with c2:
            metrica(
                "Generación",
                resultado["generacion_mejor"],
            )

        with c3:
            metrica(
                "Tiempo",
                f"{resultado['tiempo_segundos']:.3f} s",
            )

        st.markdown("### 📋 Desglose de penalizaciones")

        st.json(
            resultado["detalles_penalizacion"]
        )

        st.markdown("### 📅 Horario generado")

        filas = construir_horario(
            resultado["mejor_individuo"]
        )

        dataframe = pd.DataFrame(filas)

        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True,
        )

        izquierda, derecha = st.columns(2)

        with izquierda:
            st.markdown("### 🖼️ Horario")

            st.image(
                str(WEB_RESULTADOS / "cursos_horario.png"),
                use_container_width=True,
            )

        with derecha:
            st.markdown("### 📈 Convergencia")

            st.image(
                str(WEB_RESULTADOS / "cursos_convergencia.png"),
                use_container_width=True,
            )


def pagina_mochila():
    hero(
        "PROBLEMA 04",
        "🎒",
        "Problema de la Mochila",
        """
        Maximiza el valor total de los objetos seleccionados
        sin superar la capacidad establecida.
        """,
    )

    st.markdown("## ⚙️ Configuración")

    c1, c2, c3 = st.columns(3)

    with c1:
        capacidad = st.selectbox(
            "Capacidad",
            [30, 45],
        )

    with c2:
        metodo = st.selectbox(
            "Método",
            [
                "penalizacion",
                "reparacion",
            ],
        )

    with c3:
        poblacion = st.number_input(
            "Tamaño de población",
            min_value=3,
            value=100,
            step=10,
            key="m_poblacion",
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        generaciones = st.number_input(
            "Máximo de generaciones",
            min_value=0,
            value=500,
            step=10,
            key="m_generaciones",
        )

    with c5:
        tasa = st.slider(
            "Tasa de mutación",
            0.0,
            1.0,
            0.10,
            0.01,
            key="m_tasa",
        )

    with c6:
        elitismo = st.number_input(
            "Cantidad de élites",
            min_value=0,
            max_value=20,
            value=2,
            key="m_elitismo",
        )

    semilla = st.number_input(
        "Semilla",
        min_value=0,
        value=42,
        key="m_semilla",
    )

    if st.button(
        "🚀 Resolver mochila",
        use_container_width=True,
    ):
        try:
            with st.spinner(
                "Buscando la mejor combinación..."
            ):
                resultado = resolver_mochila(
                    capacidad=int(capacidad),
                    metodo=metodo,
                    poblacion=int(poblacion),
                    generaciones=int(generaciones),
                    tasa_mutacion=float(tasa),
                    elitismo=int(elitismo),
                    semilla=int(semilla),
                )

                ruta_objetos = WEB_RESULTADOS / "mochila_objetos.png"
                ruta_convergencia = WEB_RESULTADOS / "mochila_convergencia.png"

                objetos_mochila(
                    resultado,
                    destino=ruta_objetos,
                    mostrar=False,
                )

                convergencia_mochila(
                    resultado,
                    destino=ruta_convergencia,
                    mostrar=False,
                )

                st.session_state["mochila"] = resultado

        except Exception as error:
            st.error(
                f"Error al ejecutar Mochila: {error}"
            )

    resultado = st.session_state.get("mochila")

    if resultado:
        st.markdown("---")
        st.markdown("## 🎒 Resultado")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metrica(
                "Valor total",
                resultado["valor_total"],
            )

        with c2:
            metrica(
                "Peso total",
                resultado["peso_total"],
            )

        with c3:
            metrica(
                "Capacidad",
                resultado["capacidad"],
            )

        with c4:
            metrica(
                "Generación",
                resultado["generacion_mejor"],
            )

        if resultado["peso_total"] <= resultado["capacidad"]:
            st.success(
                "La solución respeta la capacidad de la mochila."
            )

        st.markdown("### 🧬 Cromosoma")

        st.code(
            str(resultado["mejor_individuo"]),
            language="text",
        )

        st.markdown("### 📦 Objetos seleccionados")

        for objeto in resultado["objetos_seleccionados"]:
            st.write(f"• {objeto}")

        izquierda, derecha = st.columns(2)

        with izquierda:
            st.markdown("### 📊 Objetos seleccionados")

            st.image(
                str(WEB_RESULTADOS / "mochila_objetos.png"),
                use_container_width=True,
            )

        with derecha:
            st.markdown("### 📈 Convergencia")

            st.image(
                str(WEB_RESULTADOS / "mochila_convergencia.png"),
                use_container_width=True,
            )


cargar_css()


with st.sidebar:
    st.markdown("## 🧬 Genetic AI")
    st.caption("Taller de Inteligencia Artificial")

    st.markdown("---")

    pagina = st.radio(
        "Selecciona el algoritmo",
        [
            "🏠 Inicio",
            "♛ N-Reinas",
            "🗺️ Agente Viajero",
            "🏫 Cursos y Salas",
            "🎒 Mochila",
        ],
    )

    st.markdown("---")

    st.markdown("### 📚 Proyecto")
    st.write("**Asignatura:** Inteligencia Artificial")
    st.write("**Tema:** Algoritmos Genéticos")

    st.markdown("---")

    st.caption(
        "Python · Streamlit · Algoritmos Evolutivos"
    )


if pagina == "🏠 Inicio":
    mostrar_inicio()

elif pagina == "♛ N-Reinas":
    pagina_n_reinas()

elif pagina == "🗺️ Agente Viajero":
    pagina_tsp()

elif pagina == "🏫 Cursos y Salas":
    pagina_cursos()

elif pagina == "🎒 Mochila":
    pagina_mochila()


st.markdown(
    dedent(
        """
        <div class="footer">
            Taller de Inteligencia Artificial ·
            Algoritmos Genéticos ·
            Python + Streamlit
        </div>
        """
    ),
    unsafe_allow_html=True,
)