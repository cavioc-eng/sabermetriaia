import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Sabermetría IA / Winometry", page_icon="🏀", layout="wide")

# Sidebar - Logo & Navigation
logo_path = os.path.join(os.path.dirname(__file__) if "__file__" in locals() else ".", "logo.jpeg")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=220)

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
        "⚙️ Panel de Administración" if lang_code == "es" else "⚙️ Admin Panel"
    ]
)

current_dir = os.path.dirname(__file__) if "__file__" in locals() else "."

# File paths mapping
if sport_prefix == "nba":
    cartelera_path = os.path.join(current_dir, "cartelera_juegos.csv")
    apuestas_path = os.path.join(current_dir, "apuestas_usa.csv")
    efectividad_path = os.path.join(current_dir, "historial_efectividad.csv")
    checklist_path = os.path.join(current_dir, "checklist_ultimo_minuto.csv")
else:
    cartelera_path = os.path.join(current_dir, "nfl_cartelera_juegos.csv")
    apuestas_path = os.path.join(current_dir, "nfl_apuestas_usa.csv")
    efectividad_path = os.path.join(current_dir, "nfl_historial_efectividad.csv")
    checklist_path = os.path.join(current_dir, "nfl_checklist_ultimo_minuto.csv")

# Effectiveness Display in Sidebar or Top
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

# Main content based on menu selection
if "Cartelera" in menu or "Schedule" in menu:
    st.markdown(f"## 📊 Cartelera de Partidos [{sport}]")
    if os.path.exists(cartelera_path):
        df_cart = pd.read_csv(cartelera_path)
        for idx, row in df_cart.iterrows():
            st.markdown(f"### 🏀 {row.get('equipo1', '')} vs {row.get('equipo2', '')}")
            st.markdown(f"⏰ **Hora (VE):** {row.get('hora', '')} | 🏟️ **Sede:** {row.get('sede', '')}")
            st.markdown(f"🎯 **Pick / Pronóstico:** {row.get('ganador', '')} | 📊 **Total Puntos (O/U):** {row.get('total_puntos', '')}")
            st.markdown("---")
    else:
        st.warning("No se encontró el archivo de cartelera.")

elif "Apuestas" in menu or "Betting" in menu:
    st.markdown(f"## 📈 Apuestas USA & Métricas Avanzadas [{sport}]")
    if os.path.exists(apuestas_path):
        df_ap = pd.read_csv(apuestas_path)
        st.dataframe(df_ap, use_container_width=True)
    else:
        st.warning("No se encontró el archivo de apuestas y métricas.")

elif "Checklist" in menu:
    st.markdown(f"## 🧭 Checklist de Último Minuto [{sport}]")
    if os.path.exists(checklist_path):
        df_chk = pd.read_csv(checklist_path)
        for idx, row in df_chk.iterrows():
            st.markdown(f"**Partido:** {row.get('partido', '')}")
            st.markdown(f"• **Estado:** {row.get('estado', '')}")
            st.markdown(f"• **Alerta / Notas:** {row.get('alerta_notas', '')}")
            st.markdown(f"• **Cambio de Perspectiva:** {row.get('cambio_perspectiva', '')}")
            st.markdown("---")
    else:
        st.warning("No se encontró el checklist de último minuto.")

elif "Administración" in menu or "Admin" in menu:
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
