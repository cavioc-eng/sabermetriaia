import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Sabermetría IA - Analítica y Proyecciones NBA", 
    page_icon="🏀", 
    layout="wide"
)

# Estilo y cabecera principal
st.title("🏀 Sabermetría IA")
st.subheader("La ciencia de convertir datos en estrategia y conocimiento deportivo")

st.markdown("""
Bienvenido al centro de análisis avanzado de la NBA. Aquí transformamos las estadísticas tradicionales en métricas de alto valor (eficiencia neta, eFG%, Usage Rate, Box Plus/Minus y True Shooting Percentage) para entender el juego con absoluta precisión.
""")

# Barra lateral informativa
with st.sidebar:
    st.image("logo.jpeg", use_container_width=True) if "logo.jpeg" in [f for f in []] else None
    st.header("Navegación")
    seccion = st.radio(
        "Selecciona una sección:",
        ["📰 Reportes y Actualidad", "📊 Modelos y Métricas Avanzadas", "🎯 Proyecciones de Temporada"]
    )
    
    st.markdown("---")
    st.info("💡 **Próximo gran hito:** Inicio de la temporada regular de la NBA el 20 de octubre de 2026.")

# Contenido según la sección seleccionada
if seccion == "📰 Reportes y Actualidad":
    st.header("Reportes y Análisis de la Jornada")
    st.write("Mantente al día con los resúmenes tácticos, notas de pretemporada y el seguimiento detallado de las franquicias rumbo al inicio de campaña.")
    
    # Ejemplo de tarjeta de reporte editorial
    with st.expander("📌 Reporte Especial: El pulso táctico previo al 20 de octubre", expanded=True):
        st.markdown("""
        * **Evaluación de Plantillas:** Los cuerpos técnicos afinan rotaciones y esquemas defensivos en esta recta final de preparación.
        * **Enfoque Sabermétrico:** Analizamos el impacto de las nuevas piezas y el rendimiento por posesión para anticipar los favoritos de la conferencia.
        * **Próxima Actualización:** Cobertura especial con el inicio oficial de la fase regular.
        """)

elif seccion == "📊 Modelos y Métricas Avanzadas":
    st.header("Laboratorio de Sabermetría")
    st.write("Explora las fórmulas y conceptos estadísticos que rigen el baloncesto moderno.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Eficiencia Ofensiva Promedio", value="114.2", delta="+1.5")
        st.markdown("**eFG% (Effective Field Goal Percentage):** Mide la efectividad en tiros de campo ponderando el valor extra del triple.")
    with col2:
        st.metric(label="Ritmo de Juego (Pace)", value="99.8", delta="-0.3")
        st.markdown("**True Shooting % (TS%):** Considera tiros de dos, triples y tiros libres para evaluar la verdadera capacidad anotadora.")

elif seccion == "🎯 Proyecciones de Temporada":
    st.header("Proyecciones y Modelos Predictivos")
    st.write("Nuestros algoritmos están listos y calibrándose para ofrecerte pronósticos fundamentados desde el primer salto entre dos de la temporada regular.")
    st.info("Los modelos predictivos interactivos se activarán automáticamente con el inicio de la jornada inaugural.")

# Pie de página
st.markdown("---")
st.caption("© 2026 Sabermetría IA — Todos los derechos reservados. Análisis basado en datos y rigor científico.")
