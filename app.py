import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Sabermetría IA / Winometry", page_icon="🏀", layout="wide")

# Sidebar - Logo & Navigation
logo_path = os.path.join(os.path.dirname(__file__) if "__file__" in locals() else ".", "logo.jpeg")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=220)

st.sidebar.markdown("---")
st.sidebar.subheader("🏆 Selección de Deporte")

sport = st.sidebar.selectbox("Deporte / Sport", ["NBA (Básquetbol)", "NFL (Fútbol Americano)"])
sport_prefix = "nba" if "Básquetbol" in sport else "nfl"

lang = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
lang_code = "es" if lang == "Español" else "en"

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Menú Principal")

menu = st.sidebar.radio(
    "Navegación",
    [
        "📊 Cartelera de Partidos",
        "📈 Apuestas USA & Métricas",
        "🧭 Checklist de Último Minuto",
        "📰 Noticias & Análisis",
        "📖 Diccionario Sabermétrico",
        "⚙️ Panel de Administración"
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
st.markdown(f"• **Jornada Anterior / Last Slate:** {jornada_txt}")
st.markdown(f"• **Acumulado Global / Global Accumulator:** {global_txt}")
st.markdown("---")

# Section 1: Cartelera de Partidos
if "Cartelera" in menu:
    st.markdown(f"## 📊 Cartelera de Partidos [{sport}] - Análisis Profundo")
    if os.path.exists(cartelera_path):
        df_cart = pd.read_csv(cartelera_path)
        match_options = [f"{row.get('equipo1', '')} vs {row.get('equipo2', '')}" for idx, row in df_cart.iterrows()]
        selected_match = st.selectbox("Selecciona un encuentro para ver el desglose científico del modelo:" if lang_code == "es" else "Select a matchup:", match_options)
        
        for idx, row in df_cart.iterrows():
            match_title = f"{row.get('equipo1', '')} vs {row.get('equipo2', '')}"
            if match_title == selected_match:
                st.markdown(f"### {row.get('equipo1', '')} vs {row.get('equipo2', '')}")
                st.markdown(f"⏰ **Hora (VE):** {row.get('hora', '')} | 🏟️ **Sede:** {row.get('sede', '')}")
                st.markdown(f"🎯 **Pick / Pronóstico:** {row.get('ganador', '')} | 📊 **Total Puntos (O/U):** {row.get('total_puntos', '')}")
                st.markdown(f"💬 **Análisis:** {row.get('analisis', row.get('resumen', 'Análisis estadístico avanzado disponible.'))}")
                st.markdown("---")
    else:
        st.warning("No se encontró el archivo de cartelera de partidos.")

# Section 2: Apuestas USA & Métricas
elif "Apuestas" in menu:
    st.markdown(f"## 📈 Apuestas USA & Métricas Avanzadas [{sport}]")
    if os.path.exists(apuestas_path):
        df_ap = pd.read_csv(apuestas_path)
        st.dataframe(df_ap, use_container_width=True)
    else:
        st.warning("No se encontró el archivo de apuestas de USA.")

# Section 3: Checklist de Último Minuto
elif "Checklist" in menu:
    st.markdown(f"## 🧭 Checklist de Último Minuto [{sport}]")
    if os.path.exists(checklist_path):
        df_chk = pd.read_csv(checklist_path)
        for idx, row in df_chk.iterrows():
            st.markdown(f"### 🏀 Partido: {row.get('partido', '')}")
            st.markdown(f"• **Estado / Status:** {row.get('estado', '')}")
            st.markdown(f"• **Alerta / Notes:** {row.get('alerta_notas', '')}")
            st.markdown(f"• **Cambio de Perspectiva:** {row.get('cambio_perspectiva', '')}")
            st.markdown("---")
    else:
        st.warning("No se encontró el archivo de checklist de último minuto.")

# Section 4: Noticias & Análisis
elif "Noticias" in menu:
    st.markdown(f"## 📰 Noticias & Análisis Avanzado [{sport}]")
    if os.path.exists(noticias_path):
        with open(noticias_path, 'r', encoding='utf-8') as f:
            noticias_text = f.read()
        st.markdown(noticias_text)
    else:
        st.info(f"Reportes y boletines analíticos actualizados para {sport} en desarrollo.")

# Section 5: Diccionario Sabermétrico
elif "Diccionario" in menu:
    st.markdown(f"## 📖 Diccionario Sabermétrico & Glosario Analítico [{sport}]")
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
elif "Administración" in menu:
    st.markdown(f"## ⚙️ Panel de Administración [{sport}]")
    password = st.text_input("Clave de administrador:" if lang_code == "es" else "Admin Password:", type="password")
    if password == "coseinca2026":
        st.success("¡Acceso concedido!" if lang_code == "es" else "Access granted!")
        uploaded_file = st.file_uploader("Cargar Cartelera CSV" if lang_code == "es" else "Upload Schedule CSV", type=["csv"])
        if uploaded_file is not None:
            df_up = pd.read_csv(uploaded_file)
            df_up.to_csv(cartelera_path, index=False, encoding="utf-8")
            st.success("¡Archivo actualizado exitosamente!" if lang_code == "es" else "File successfully updated!")
    elif password != "":
        st.error("Contraseña incorrecta." if lang_code == "es" else "Incorrect password.")
