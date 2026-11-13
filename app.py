import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Sabermetría IA / Winometry", page_icon="🏀", layout="wide")

# Sidebar - Sport and Language Selection
logo_path = os.path.join(os.path.dirname(__file__) if "__file__" in locals() else ".", "logo.jpeg")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=220)

st.sidebar.markdown("---")
sport = st.sidebar.selectbox("Deporte / Sport", ["NBA (Básquetbol)", "NFL (Fútbol Americano)"])
sport_prefix = "nba" if "Básquetbol" in sport else "nfl"

lang = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
lang_code = "es" if lang == "Español" else "en"

st.sidebar.markdown("---")

current_dir = os.path.dirname(__file__) if "__file__" in locals() else "."

# Match exact GitHub file naming:
# NBA files: cartelera_juegos.csv, apuestas_usa.csv, historial_efectividad.csv, checklist_ultimo_minuto.csv
# NFL files: nfl_cartelera_juegos.csv, nfl_apuestas_usa.csv, nfl_historial_efectividad.csv, nfl_checklist_ultimo_minuto.csv
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

if os.path.exists(cartelera_path):
    df_cart = pd.read_csv(cartelera_path)
    st.markdown(f"## Cartelera de Partidos [{sport}]")
    for idx, row in df_cart.iterrows():
        st.markdown(f"**{row['equipo1']} vs {row['equipo2']}** | ⏰ {row.get('hora', '')} | 🏟️ {row.get('sede', '')}")
        st.markdown(f"• **Pick:** {row.get('ganador', '')} | **O/U:** {row.get('total_puntos', '')}")
        st.markdown("---")
else:
    st.warning(f"No se encontró el archivo de cartelera para {sport}.")
