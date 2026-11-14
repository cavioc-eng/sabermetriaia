import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Sabermetría IA / Winometry", page_icon="🏀", layout="wide")

# Sidebar - Logo & Navigation
logo_path = os.path.join(os.path.dirname(__file__) if "__file__" in locals() else ".", "logo.jpeg")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=220)

# Visitor Counter
visitor_file = "visitas.txt"
if not os.path.exists(visitor_file):
    with open(visitor_file, "w") as f:
        f.write("0")

if 'visited' not in st.session_state:
    st.session_state.visited = True
    try:
        with open(visitor_file, "r") as f:
            count = int(f.read().strip() or "0")
    except:
        count = 0
    count += 1
    try:
        with open(visitor_file, "w") as f:
            f.write(str(count))
    except:
        pass
else:
    try:
        with open(visitor_file, "r") as f:
            count = int(f.read().strip() or "0")
    except:
        count = 0

st.sidebar.markdown("---")
st.sidebar.markdown(f"👁️ **Visitas Totales / Total Visits:** `{count:,}`")


st.sidebar.markdown("---")
st.sidebar.subheader("🏆 Selección de Deporte" if "es" else "🏆 Sport Selection")

sport = st.sidebar.selectbox("Deporte / Sport", ["NBA (Básquetbol)", "NFL (Fútbol Americano)"])
sport_prefix = "nba" if "Básquetbol" in sport else "nfl"

lang = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
lang_code = "es" if lang == "Español" else "en"

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Menú Principal" if lang_code == "es" else "📌 Main Menu")

menu = st.sidebar.radio(
    "Navegación",
    [
        "📊 Cartelera de Partidos" if lang_code == "es" else "📊 Match Schedule",
        "📈 Apuestas USA & Métricas" if lang_code == "es" else "📈 USA Betting & Metrics",
        "🧭 Checklist de Último Minuto" if lang_code == "es" else "🧭 Last-Minute Checklist",
        "📰 Noticias & Análisis" if lang_code == "es" else "📰 News & Analysis",
        "📖 Diccionario Sabermétrico" if lang_code == "es" else "📖 Sabermetric Dictionary",
        "⚙️ Panel de Administración" if lang_code == "es" else "⚙️ Admin Panel"
    ]
)

current_dir = os.path.dirname(__file__) if "__file__" in locals() else "."

# File paths mapping based on sport
if sport_prefix == "nba":
    cartelera_path = os.path.join(current_dir, "cartelera_juegos.csv")
    apuestas_path = os.path.join(current_dir, "apuestas_usa.csv")
    efectividad_path = os.path.join(current_dir, "historial_efectividad.csv")
    checklist_path = os.path.join(current_dir, "checklist_ultimo_minuto.csv")
    noticias_path = os.path.join(current_dir, "noticias.txt")
else:
    cartelera_path = os.path.join(current_dir, "nfl_cartelera_juegos.csv")
    apuestas_path = os.path.join(current_dir, "nfl_apuestas_usa.csv")
    efectividad_path = os.path.join(current_dir, "nfl_historial_efectividad.csv")
    checklist_path = os.path.join(current_dir, "nfl_checklist_ultimo_minuto.csv")
    noticias_path = os.path.join(current_dir, "nfl_noticias.txt")

# Effectiveness Display
if os.path.exists(efectividad_path):
    df_ef = pd.read_csv(efectividad_path)
    if not df_ef.empty:
        last_row = df_ef.iloc[-1]
        jornada_txt = f"{last_row['aciertos']} / {last_row['juegos']} ({last_row['efectividad']}%)"
        total_juegos = df_ef['juegos'].sum()
        total_aciertos = df_ef['aciertos'].sum()
        total_efec = round((total_aciertos / total_juegos * 100), 1) if total_juegos > 0 else 0.0
        global_txt = f"{total_aciertos} / {total_juegos} ({total_efec}%)"
    else:
        jornada_txt = "0 / 0 (0.0%)"
        global_txt = "0 / 0 (0.0%)"
else:
    jornada_txt = "0 / 0 (0.0%)"
    global_txt = "0 / 0 (0.0%)"

st.markdown(f"### 🎯 Efectividad Modelo [{sport}]:")
st.markdown(f"• **{'Jornada Anterior' if lang_code == 'es' else 'Last Slate'}:** {jornada_txt}")
st.markdown(f"• **{'Acumulado Global' if lang_code == 'es' else 'Global Accumulator'}:** {global_txt}")
st.markdown("---")

# Section 1: Cartelera de Partidos
if "Cartelera" in menu or "Schedule" in menu:
    st.markdown(f"## 📊 {'Cartelera de Partidos' if lang_code == 'es' else 'Match Schedule'} [{sport}]")
    if os.path.exists(cartelera_path):
        df_cart = pd.read_csv(cartelera_path)
        match_options = [f"{row.get('equipo1', '')} vs {row.get('equipo2', '')}" for idx, row in df_cart.iterrows()]
        selected_match = st.selectbox("Selecciona un encuentro para ver el desglose científico del modelo:" if lang_code == "es" else "Select a matchup for model breakdown:", match_options)
        
        for idx, row in df_cart.iterrows():
            match_title = f"{row.get('equipo1', '')} vs {row.get('equipo2', '')}"
            if match_title == selected_match:
                st.markdown(f"### {match_title}")
                st.markdown(f"⏰ **{'Hora (VE)' if lang_code == 'es' else 'Time (VE)'}:** {row.get('hora', '')} | 🏟️ **{'Sede' if lang_code == 'es' else 'Venue'}:** {row.get('sede', '')}")
                st.markdown(f"🎯 **{'Pick / Pronóstico' if lang_code == 'es' else 'Model Pick'}:** {row.get('ganador', '')} | 📊 **Total Puntos (O/U):** {row.get('total_puntos', '')}")
                
                analisis_content = row.get('analisis_es', row.get('analisis', 'Análisis estadístico avanzado disponible.'))
                if lang_code == 'en':
                    analisis_content = row.get('analisis_en', analisis_content)
                st.markdown(f"💬 **{'Análisis' if lang_code == 'es' else 'Analysis'}:** {analisis_content}", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.warning("No se encontró el archivo de cartelera." if lang_code == "es" else "Schedule file not found.")

# Section 2: Apuestas USA & Métricas
elif "Apuestas" in menu or "Betting" in menu:
    st.markdown(f"## 📈 {'Apuestas USA & Métricas Avanzadas' if lang_code == 'es' else 'USA Betting & Advanced Metrics'} [{sport}]")
    if os.path.exists(apuestas_path):
        df_ap = pd.read_csv(apuestas_path)
        st.dataframe(df_ap, use_container_width=True)
    else:
        st.warning("No se encontró el archivo de apuestas." if lang_code == "es" else "Betting file not found.")

# Section 3: Checklist de Último Minuto
elif "Checklist" in menu:
    st.markdown(f"## 🧭 {'Checklist de Último Minuto' if lang_code == 'es' else 'Last-Minute Checklist'} [{sport}]")
    if os.path.exists(checklist_path):
        df_chk = pd.read_csv(checklist_path)
        for idx, row in df_chk.iterrows():
            st.markdown(f"### 🏀 {'Partido' if lang_code == 'es' else 'Match'}: {row.get('partido', '')}")
            st.markdown(f"• **{'Estado' if lang_code == 'es' else 'Status'}:** {row.get('estado', '')}")
            st.markdown(f"• **{'Alerta / Notas' if lang_code == 'es' else 'Alert / Notes'}:** {row.get('alerta_notas', '')}")
            st.markdown(f"• **{'Cambio de Perspectiva' if lang_code == 'es' else 'Perspective Shift'}:** {row.get('cambio_perspectiva', '')}")
            st.markdown("---")
    else:
        st.warning("No se encontró el checklist." if lang_code == "es" else "Checklist file not found.")

# Section 4: Noticias & Análisis
elif "Noticias" in menu or "News" in menu:
    st.markdown(f"## 📰 {'Noticias & Análisis Avanzado' if lang_code == 'es' else 'News & Advanced Analysis'} [{sport}]")
    if os.path.exists(noticias_path):
        with open(noticias_path, 'r', encoding='utf-8') as f:
            noticias_text = f.read()
        st.markdown(noticias_text)
    else:
        st.info("Boletines analíticos en desarrollo." if lang_code == "es" else "Analytical bulletins in development.")

# Section 5: Diccionario Sabermétrico
elif "Diccionario" in menu or "Dictionary" in menu:
    st.markdown(f"## 📖 {'Diccionario Sabermétrico & Glosario' if lang_code == 'es' else 'Sabermetric Dictionary & Glossary'} [{sport}]")
    if sport_prefix == "nba":
        st.markdown("### 🏀 Métricas Clave NBA:")
        st.markdown("• **Net Rating:** Diferencial de puntos por 100 posesiones (Ofensiva vs Defensiva).")
        st.markdown("• **Effective Field Goal Percentage (eFG%):** Porcentaje de tiro efectivo ajustado por el valor superior de los triples.")
        st.markdown("• **True Shooting Percentage (TS%):** Eficiencia de anotación considerando tiros de campo, triples y tiros libres.")
        st.markdown("• **Win Probability Model:** Modelo predictivo basado en posesiones, ventaja en la pintura y fatiga del back-to-back.")
    else:
        st.markdown("### 🏈 Métricas Clave NFL:")
        st.markdown("• **EPA per Play (Expected Points Added):** Valor esperado de puntos añadidos por cada jugada ofensiva o defensiva.")
        st.markdown("• **Success Rate (% de Éxito):** Porcentaje de jugadas que cumplen con el umbral de yardas necesarias según el down.")
        st.markdown("• **DVOA (Defense-adjusted Value Over Average):** Eficiencia de un equipo comparada con el promedio de la liga, ajustada por la calidad del oponente.")
        st.markdown("• **Pressure Rate:** Porcentaje de jugadas de pase donde la defensiva presiona al mariscal de campo.")

# Section 6: Panel de Administración
elif "Administración" in menu or "Admin" in menu:
    st.markdown(f"## ⚙️ {'Panel de Administración' if lang_code == 'es' else 'Admin Panel'} [{sport}]")
    password = st.text_input("Clave de administrador:" if lang_code == "es" else "Admin Password:", type="password")
    valid_passwords = ["sabermetria2026", "coseinca2026", "sabermetria"]
    
    if password in valid_passwords:
        st.success("¡Acceso concedido!" if lang_code == "es" else "Access granted!")
        
        st.markdown("---")
        st.subheader("📥 1. Descargar Plantillas / Modelos CSV" if lang_code == "es" else "📥 1. Download CSV Templates")
        st.write("Descarga los modelos oficiales para llenarlos y cargarlos de vuelta:" if lang_code == "es" else "Download official templates to fill and upload back:")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if os.path.exists(cartelera_path):
                with open(cartelera_path, "rb") as f:
                    st.download_button("📥 Cartelera CSV", f, file_name=os.path.basename(cartelera_path), mime="text/csv")
        with col2:
            if os.path.exists(apuestas_path):
                with open(apuestas_path, "rb") as f:
                    st.download_button("📥 Apuestas CSV", f, file_name=os.path.basename(apuestas_path), mime="text/csv")
        with col3:
            if os.path.exists(checklist_path):
                with open(checklist_path, "rb") as f:
                    st.download_button("📥 Checklist CSV", f, file_name=os.path.basename(checklist_path), mime="text/csv")
        with col4:
            if os.path.exists(efectividad_path):
                with open(efectividad_path, "rb") as f:
                    st.download_button("📥 Historial CSV", f, file_name=os.path.basename(efectividad_path), mime="text/csv")
        
        st.markdown("---")
        st.subheader("📤 2. Cargar / Actualizar Archivos CSV" if lang_code == "es" else "📤 2. Upload / Update CSV Files")
        
        up_cartelera = st.file_uploader("Actualizar Cartelera de Partidos (CSV)" if lang_code == "es" else "Update Match Schedule (CSV)", type=["csv"], key="up_cart")
        if up_cartelera is not None:
            df_up = pd.read_csv(up_cartelera)
            df_up.to_csv(cartelera_path, index=False, encoding="utf-8")
            st.success("¡Cartelera actualizada exitosamente!" if lang_code == "es" else "Schedule successfully updated!")
            
        up_apuestas = st.file_uploader("Actualizar Apuestas USA (CSV)" if lang_code == "es" else "Update USA Betting (CSV)", type=["csv"], key="up_ap")
        if up_apuestas is not None:
            df_up = pd.read_csv(up_apuestas)
            df_up.to_csv(apuestas_path, index=False, encoding="utf-8")
            st.success("¡Apuestas actualizadas exitosamente!" if lang_code == "es" else "Betting data successfully updated!")

        up_checklist = st.file_uploader("Actualizar Checklist de Último Minuto (CSV)" if lang_code == "es" else "Update Last-Minute Checklist (CSV)", type=["csv"], key="up_chk")
        if up_checklist is not None:
            df_up = pd.read_csv(up_checklist)
            df_up.to_csv(checklist_path, index=False, encoding="utf-8")
            st.success("¡Checklist actualizado exitosamente!" if lang_code == "es" else "Checklist successfully updated!")

        up_efectividad = st.file_uploader("Actualizar Historial de Efectividad (CSV)" if lang_code == "es" else "Update Effectiveness History (CSV)", type=["csv"], key="up_ef")
        if up_efectividad is not None:
            df_up = pd.read_csv(up_efectividad)
            df_up.to_csv(efectividad_path, index=False, encoding="utf-8")
            st.success("¡Historial de efectividad actualizado exitosamente!" if lang_code == "es" else "Effectiveness history successfully updated!")

        st.markdown("---")
        st.subheader("📰 3. Editor de Noticias & Análisis (Español / English)" if lang_code == "es" else "📰 3. News & Analysis Editor (Spanish / English)")
        
        current_news = ""
        if os.path.exists(noticias_path):
            with open(noticias_path, "r", encoding="utf-8") as f:
                current_news = f.read()
                
        news_input = st.text_area("Edita el boletín de noticias en formato Markdown (Soporta Español e Inglés):" if lang_code == "es" else "Edit news bulletin in Markdown:", value=current_news, height=250)
        if st.button("Guardar Noticias" if lang_code == "es" else "Save News"):
            with open(noticias_path, "w", encoding="utf-8") as f:
                f.write(news_input)
            st.success("¡Noticias guardadas y publicadas exitosamente!" if lang_code == "es" else "News successfully saved and published!")

    elif password != "":
        st.error("Contraseña incorrecta." if lang_code == "es" else "Incorrect password.")
