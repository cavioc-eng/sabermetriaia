import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Sabermetría IA - Analítica y Proyecciones NBA", 
    page_icon="🏀", 
    layout="wide"
)

# Inicializar el estado de sesión para las noticias bilingües si no existen
if 'noticia_matutina_es' not in st.session_state:
    st.session_state.noticia_matutina_es = (
        "• **Radiografía de Eficiencia Ofensiva y eFG%:** Franquicias como los **Boston Celtics** e **Indiana Pacers** están dictando cátedra sobre cómo elevar el eFG% con excelente spacing.\n\n"
        "• **Impacto del Net Rating:** Los diferenciales de eficiencia neta en contendientes como los **Denver Nuggets** explican los cierres de partido bajo presión.\n\n"
        "• **Tendencias Defensivas:** Minimizar pérdidas de balón (**TOV%**) es clave para controlar el ritmo (*Pace*)."
    )

if 'noticia_vespertina_es' not in st.session_state:
    st.session_state.noticia_vespertina_es = (
        "• **Usage Rate y Rotaciones:** Ante el descanso de figuras como **Stephen Curry**, la carga ofensiva recae sobre la segunda unidad.\n\n"
        "• **Impacto del Pace en la Carga de Minutos:** Las restricciones de minutos en pretemporada reducen temporalmente la velocidad de posesiones.\n\n"
        "• **Líneas O/U y Eficiencia Defensiva:** El control del rebote defensivo (**DRB%**) define las diferencias en las proyecciones de hoy."
    )

if 'noticia_matutina_en' not in st.session_state:
    st.session_state.noticia_matutina_en = (
        "• **Offensive Efficiency & eFG% Breakdown:** Elite squads like the **Boston Celtics** and **Indiana Pacers** demonstrate the power of optimized eFG% via superior spacing.\n\n"
        "• **Net Rating Dynamics:** Advanced differentials in contenders like the **Denver Nuggets** explain clutch execution under pressure.\n\n"
        "• **Pace Velocity & Turnovers:** Minimizing live-ball turnovers (**TOV%**) dictates overall game tempo control."
    )

if 'noticia_vespertina_en' not in st.session_state:
    st.session_state.noticia_vespertina_en = (
        "• **Usage Rate Shifts:** With load management for icons like **Stephen Curry**, the offensive burden shifts to secondary units.\n\n"
        "• **Pace Adjustments:** Camp restrictions temporarily suppress overall possession velocity.\n\n"
        "• **O/U Betting Lines & Defense:** Defensive rebounding percentages (**DRB%**) remain key to covering projected spreads."
    )

if 'idioma_app' not in st.session_state:
    st.session_state.idioma_app = "Español"

# Barra lateral para navegación e idioma
with st.sidebar:
    st.header("⚙️ Navegación")
    seccion = st.radio(
        "Selecciona una sección:",
        ["📰 Centro de Noticias", "📊 Laboratorio Sabermétrico", "🎯 Modelos Predictivos", "🛠️ Panel de Administrador"]
    )
    
    st.markdown("---")
    st.session_state.idioma_app = st.selectbox("🌐 Idioma / Language:", ["Español", "English"])
    
    st.markdown("---")
    st.info("💡 **Próximo gran hito:** Inicio de la temporada regular de la NBA el 20 de octubre de 2026.")

# Encabezado principal dinámico según el idioma
if st.session_state.idioma_app == "Español":
    st.title("🏀 Sabermetría IA")
    st.subheader("La ciencia de convertir datos en estrategia y conocimiento deportivo")
else:
    st.title("🏀 Sabermetría AI")
    st.subheader("The science of turning data into sports strategy and insight")

# 1. SECCIÓN: CENTRO DE NOTICIAS
if seccion == "📰 Centro de Noticias":
    if st.session_state.idioma_app == "Español":
        st.markdown("### 📰 Centro de Noticias en Tiempo Real — 14 de Octubre de 2026")
        st.write("Bienvenido al centro informativo oficial de Sabermetría IA.")
        
        # Pestañas para Edición Matutina y Vespertina
        tab1, tab2 = st.tabs(["🌅 Actualización Matutina (Cierre Previo)", "🌇 Actualización de la Tarde (5:00 p.m.)"])
        
        with tab1:
            st.markdown("### 🌅 Reporte Matutino: Radiografía y Tendencias de la Liga")
            st.markdown(st.session_state.noticia_matutina_es)
            
        with tab2:
            st.markdown("### 🌇 Reporte Vespertino: Análisis Previo al Salto Inicial")
            st.markdown(st.session_state.noticia_vespertina_es)
            
    else:
        st.markdown("### 📰 Real-Time News Center — October 14, 2026")
        st.write("Welcome to the official Sabermetry AI news hub.")
        
        tab1, tab2 = st.tabs(["🌅 Morning Edition (Pre-Game Wrap-Up)", "🌇 Evening Edition (Pre-Tip-Off Analysis)"])
        
        with tab1:
            st.markdown("### 🌅 Morning Edition: League Radiography & Trends")
            st.markdown(st.session_state.noticia_matutina_en)
            
        with tab2:
            st.markdown("### 🌇 Evening Edition: Pre-Tip-Off Strategic Preview")
            st.markdown(st.session_state.noticia_vespertina_en)

# 2. SECCIÓN: LABORATORIO SABERMÉTRICO
elif seccion == "📊 Laboratorio Sabermétrico":
    if st.session_state.idioma_app == "Español":
        st.header("Laboratorio de Sabermetría Avanzada")
        st.write("Explora las métricas de eficiencia que rigen el baloncesto moderno.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Eficiencia Ofensiva Promedio", value="114.2", delta="+1.5")
            st.markdown("**eFG% (Effective Field Goal Percentage):** Mide la efectividad ponderando el valor extra del triple.")
        with col2:
            st.metric(label="Ritmo de Juego (Pace)", value="99.8", delta="-0.3")
            st.markdown("**True Shooting % (TS%):** Considera tiros de campo y libres para evaluar la verdadera capacidad anotadora.")
    else:
        st.header("Advanced Sabermetrics Laboratory")
        st.write("Explore the efficiency metrics driving modern basketball.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Average Offensive Rating", value="114.2", delta="+1.5")
            st.markdown("**eFG% (Effective Field Goal Percentage):** Measures shooting effectiveness weighting the extra value of 3s.")
        with col2:
            st.metric(label="Possession Pace", value="99.8", delta="-0.3")
            st.markdown("**True Shooting % (TS%):** Evaluates true scoring capability across all shot types.")

# 3. SECCIÓN: MODELOS PREDICTIVOS
elif seccion == "🎯 Modelos Predictivos":
    if st.session_state.idioma_app == "Español":
        st.header("Modelos Predictivos y Proyecciones")
        st.write("Nuestros algoritmos están calibrándose para la jornada inaugural del 20 de octubre.")
        
        # Aquí se ubica de forma limpia y exclusiva el indicador de rendimiento del modelo
        st.info("🎯 **Rendimiento del Modelo Sabermétrico (Jornada Anterior):** Aciertos de Ayer: 2/5 (40% de Aciertos)")
    else:
        st.header("Predictive Models & Projections")
        st.write("Our algorithms are calibrating for opening night on October 20th.")
        st.info("🎯 **Sabermetric Model Performance (Previous Slate):** Yesterday's Accuracy: 2/5 (40% Correct)")

# 4. SECCIÓN: PANEL DE ADMINISTRADOR
elif seccion == "🛠️ Panel de Administrador":
    st.subheader("🛠️ Editor y Publicador de Noticias Bilingüe")
    st.write("Modifica los reportes en tiempo real. Los cambios se actualizarán instantáneamente para toda la fanaticada.")
    
    st.markdown("### 🇪🇸 Edición en Español")
    input_mat_es = st.text_area("Editar Edición Matutina (Español):", value=st.session_state.noticia_matutina_es, height=150)
    input_ves_es = st.text_area("Editar Edición Vespertina (Español):", value=st.session_state.noticia_vespertina_es, height=150)
    
    st.markdown("### 🇺🇸 English Edition")
    input_mat_en = st.text_area("Edit Morning Edition (English):", value=st.session_state.noticia_matutina_en, height=150)
    input_ves_en = st.text_area("Edit Evening Edition (English):", value=st.session_state.noticia_vespertina_en, height=150)
    
    if st.button("💾 Guardar y Publicar Noticias", type="primary"):
        st.session_state.noticia_matutina_es = input_mat_es
        st.session_state.noticia_vespertina_es = input_ves_es
        st.session_state.noticia_matutina_en = input_mat_en
        st.session_state.noticia_vespertina_en = input_ves_en
        st.success("¡Noticias publicadas con éxito en tiempo real!")
        st.balloons()

# Pie de página
st.markdown("---")
st.caption("© 2026 Sabermetría IA — Todos los derechos reservados. Análisis basado en datos y rigor científico.")
