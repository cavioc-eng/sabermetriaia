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

# Barra lateral informativa y navegación
with st.sidebar:
    st.header("Navegación")
    seccion = st.radio(
        "Selecciona una sección:",
        ["📰 Reportes y Actualidad", "📊 Modelos y Métricas Avanzadas", "🎯 Proyecciones de Temporada", "⚙️ Panel de Administrador"]
    )
    
    st.markdown("---")
    st.info("💡 **Próximo gran hito:** Inicio de la temporada regular de la NBA el 20 de octubre de 2026.")

# Contenido según la sección seleccionada
if seccion == "📰 Reportes y Actualidad":
    st.header("Reportes y Análisis de la Jornada")
    st.write("Mantente al día con los resúmenes tácticos, notas de pretemporada y el seguimiento detallado de las franquicias rumbo al inicio de campaña.")
    
    with st.expander("📌 Reporte Especial: El pulso táctico previo al 20 de octubre", expanded=True):
        st.markdown("""
        * **Balance de Eficiencia Ofensiva:** Las primeras prácticas muestran un incremento en triples.
        * **Impacto en la Pintura:** Equipos con mayor diferencial de rebotes dominan.
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

elif seccion == "⚙️ Panel de Administrador":
    st.subheader("📰 Editor y Publicador de Noticias Bilingüe (Español / Inglés)")
    st.write("Actualiza los reportes tanto en español como en inglés para que la app se adapte al idioma que elija el usuario.")

    # Campos de texto para Español
    st.markdown("### 🇪🇸 Versión en Español")
    edicion_matutina_es = st.text_area("Edición Matutina (Español):", value="* **Balance de Eficiencia Ofensiva:** Las primeras prácticas muestran un incremento en triples.\n* **Impacto en la Pintura:** Equipos con mayor diferencial de rebotes dominan.")
    edicion_vespertina_es = st.text_area("Edición Vespertina (Español):", value="* **Reporte de Lesiones y Rotaciones:** Cuidado físico clave en los jugadores.\n* **Líneas de Apuesta:** Análisis preliminar de favoritos.")

    # Campos de texto para Inglés
    st.markdown("### 🇺🇸 English Version")
    morning_edition_en = st.text_area("Morning Edition (English):", value="* **Offensive Efficiency Balance:** Early practices show an increase in three-pointers.\n* **Paint Impact:** Teams with higher rebound differentials dominate.")
    evening_edition_en = st.text_area("Evening Edition (English):", value="* **Injury and Rotation Report:** Key physical care for players.\n* **Betting Lines:** Preliminary analysis of favorites.")

    # Botón de guardar y publicar
    if st.button("💾 Guardar y Publicar Noticias", type="primary"):
        st.success("¡Noticias guardadas y publicadas exitosamente para toda la comunidad de seguidores!")

# Pie de página
st.markdown("---")
st.caption("© 2026 Sabermetría IA — Todos los derechos reservados. Análisis basado en datos y rigor científico.")
