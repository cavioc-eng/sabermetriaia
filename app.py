import os
from datetime import datetime
import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo.jpeg")
db_usuarios_path = os.path.join(current_dir, "registros_tiktok.csv")

st.set_page_config(
    page_title="Sabermetría IA - Analítica Avanzada de Deportes",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

def registrar_visita():
    try:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_visita = pd.DataFrame([{"fecha_hora": now_str, "origen": "Acceso Directo / TikTok"}])
        if os.path.exists(db_usuarios_path):
            df_vis = pd.read_csv(db_usuarios_path, encoding="utf-8")
            df_vis = pd.concat([df_vis, nueva_visita], ignore_index=True)
        else:
            df_vis = nueva_visita
        df_vis.to_csv(db_usuarios_path, index=False, encoding="utf-8")
    except Exception:
        pass

if 'visit_registered' not in st.session_state:
    registrar_visita()
    st.session_state['visit_registered'] = True

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #00FF66; color: #000000; font-weight: bold; border-radius: 8px; }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar Sport Selector & Language Selector
st.sidebar.title("🏆 Selección de Deporte" if "es" == "es" else "🏆 Sport Selection")
deporte_seleccionado = st.sidebar.selectbox("Deporte / Sport", ["🏀 NBA (Básquetbol)", "🏈 NFL (Fútbol Americano)"])
sport_prefix = "nba" if "NBA" in deporte_seleccionado else "nfl"

idioma = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
lang = "es" if idioma == "Español" else "en"

st.sidebar.markdown("---")
st.sidebar.title("Menú Principal" if lang == "es" else "Main Menu")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=220)

# Paths specific to selected sport
cartelera_csv_path = os.path.join(current_dir, f"{sport_prefix}_cartelera_juegos.csv")
apuestas_csv_path = os.path.join(current_dir, f"{sport_prefix}_apuestas_usa.csv")
checklist_csv_path = os.path.join(current_dir, f"{sport_prefix}_checklist_ultimo_minuto.csv")
historial_efectividad_path = os.path.join(current_dir, f"{sport_prefix}_historial_efectividad.csv")
noticias_txt_path = os.path.join(current_dir, f"{sport_prefix}_noticias.txt")

LOGOS_NBA = {
    "Atlanta Hawks": "https://cdn.nba.com/logos/nba/1610612737/global/L/logo.svg",
    "Boston Celtics": "https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg",
    "Brooklyn Nets": "https://cdn.nba.com/logos/nba/1610612751/global/L/logo.svg",
    "Charlotte Hornets": "https://cdn.nba.com/logos/nba/1610612766/global/L/logo.svg",
    "Chicago Bulls": "https://cdn.nba.com/logos/nba/1610612741/global/L/logo.svg",
    "Cleveland Cavaliers": "https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
    "Dallas Mavericks": "https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg",
    "Denver Nuggets": "https://cdn.nba.com/logos/nba/1610612743/global/L/logo.svg",
    "Detroit Pistons": "https://cdn.nba.com/logos/nba/1610612765/global/L/logo.svg",
    "Golden State Warriors": "https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg",
    "Houston Rockets": "https://cdn.nba.com/logos/nba/1610612745/global/L/logo.svg",
    "Indiana Pacers": "https://cdn.nba.com/logos/nba/1610612754/global/L/logo.svg",
    "Los Angeles Clippers": "https://cdn.nba.com/logos/nba/1610612746/global/L/logo.svg",
    "Los Angeles Lakers": "https://cdn.nba.com/logos/nba/1610612747/global/L/logo.svg",
    "Memphis Grizzlies": "https://cdn.nba.com/logos/nba/1610612763/global/L/logo.svg",
    "Miami Heat": "https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg",
    "Milwaukee Bucks": "https://cdn.nba.com/logos/nba/1610612749/global/L/logo.svg",
    "Minnesota Timberwolves": "https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg",
    "New Orleans Pelicans": "https://cdn.nba.com/logos/nba/1610612740/global/L/logo.svg",
    "New York Knicks": "https://cdn.nba.com/logos/nba/1610612752/global/L/logo.svg",
    "Oklahoma City Thunder": "https://cdn.nba.com/logos/nba/1610612760/global/L/logo.svg",
    "Orlando Magic": "https://cdn.nba.com/logos/nba/1610612753/global/L/logo.svg",
    "Philadelphia 76ers": "https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg",
    "Phoenix Suns": "https://cdn.nba.com/logos/nba/1610612756/global/L/logo.svg",
    "Portland Trail Blazers": "https://cdn.nba.com/logos/nba/1610612757/global/L/logo.svg",
    "Sacramento Kings": "https://cdn.nba.com/logos/nba/1610612758/global/L/logo.svg",
    "San Antonio Spurs": "https://cdn.nba.com/logos/nba/1610612759/global/L/logo.svg",
    "Toronto Raptors": "https://cdn.nba.com/logos/nba/1610612761/global/L/logo.svg",
    "Utah Jazz": "https://cdn.nba.com/logos/nba/1610612762/global/L/logo.svg",
    "Washington Wizards": "https://cdn.nba.com/logos/nba/1610612764/global/L/logo.svg",
}

LOGOS_NFL = {
    "Kansas City Chiefs": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
    "Buffalo Bills": "https://a.espncdn.com/i/teamlogos/nfl/500/buf.png",
    "San Francisco 49ers": "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png",
    "Dallas Cowboys": "https://a.espncdn.com/i/teamlogos/nfl/500/dal.png",
}

LOGOS_EQUIPOS = LOGOS_NBA if sport_prefix == "nba" else LOGOS_NFL

def cargar_noticias_txt():
    if sport_prefix == "nba":
        default_es = "Una Noche de Pura Maestría Táctica: El Salto de Calidad del Modelo Sabermétrico\n\n• Precisión en la duela y eficiencia de posesión."
        default_en = "A Night of Pure Tactical Mastery: The Sabermetric Model's Leap\n\n• Court precision and possession efficiency."
    else:
        default_es = "Dominio Táctico en la Emparrillada: La Revolución Analítica en la NFL\n\n• Eficiencia EPA por jugada y control de ritmo."
        default_en = "Gridiron Tactical Dominance: The NFL Analytics Revolution\n\n• EPA efficiency per play and tempo control."

    if os.path.exists(noticias_txt_path):
        try:
            with open(noticias_txt_path, "r", encoding="utf-8") as f:
                lines = f.read().split("---SEPARADOR_NOTICIAS---")
                if len(lines) >= 2:
                    return lines[0].strip(), lines[1].strip()
        except Exception:
            pass
    return default_es, default_en

def guardar_noticias_txt(mat_es, mat_en):
    try:
        with open(noticias_txt_path, "w", encoding="utf-8") as f:
            f.write(mat_es + "\n---SEPARADOR_NOTICIAS---\n" + mat_en)
    except Exception:
        pass

def cargar_historial_efectividad():
    if os.path.exists(historial_efectividad_path):
        try:
            df_hist = pd.read_csv(historial_efectividad_path, encoding="utf-8")
            if not df_hist.empty:
                return df_hist
        except Exception:
            pass
    df_default = pd.DataFrame([
        {"fecha": "2026-11-10", "juegos": 10, "aciertos": 8, "efectividad": 80.0},
        {"fecha": "2026-11-11", "juegos": 8, "aciertos": 7, "efectividad": 87.5}
    ])
    guardar_historial_efectividad(df_default)
    return df_default

def guardar_historial_efectividad(df):
    try:
        df.to_csv(historial_efectividad_path, index=False, encoding="utf-8")
    except Exception:
        pass

def calcular_metricas_efectividad():
    df_hist = cargar_historial_efectividad()
    if df_hist.empty:
        return "N/A", "N/A"
    ultima_fila = df_hist.iloc[-1]
    ayer_str = f"{int(ultima_fila['aciertos'])} / {int(ultima_fila['juegos'])} ({ultima_fila['efectividad']:.1f}%)"
    total_juegos = df_hist['juegos'].sum()
    total_aciertos = df_hist['aciertos'].sum()
    acumulado_pct = (total_aciertos / total_juegos * 100) if total_juegos > 0 else 0.0
    acumulado_str = f"{int(total_aciertos)} / {int(total_juegos)} ({acumulado_pct:.1f}%)"
    return ayer_str, acumulado_str

def cargar_cartelera():
    if os.path.exists(cartelera_csv_path):
        try:
            df_saved = pd.read_csv(cartelera_csv_path, encoding="utf-8")
            if not df_saved.empty:
                return df_saved
        except Exception:
            pass
    if sport_prefix == "nba":
        datos_respaldo = [{
            "equipo1": "Orlando Magic", "equipo2": "Boston Celtics", "hora": "16:30 (VE)",
            "sede": "Kia Center, Orlando", "ganador": "Boston Celtics", "total_puntos": "220.5",
            "analisis_es": "**ANÁLISIS SABERMÉTRICO EXPERTO (⭐ JUGADA FIJA):**<br><br>• **Net Rating Superior:** Los Celtics dominan con eficiencia neta.",
            "analisis_en": "**EXPERT SABERMETRIC ANALYSIS (⭐ LOCK OF THE DAY):**<br><br>• **Net Rating:** Celtics lead.",
            "es_jugada_fija": True
        }]
    else:
        datos_respaldo = [{
            "equipo1": "Kansas City Chiefs", "equipo2": "Buffalo Bills", "hora": "20:15 (VE)",
            "sede": "Highmark Stadium, Orchard Park", "ganador": "Kansas City Chiefs", "total_puntos": "48.5",
            "analisis_es": "**ANÁLISIS SABERMÉTRICO EXPERTO (⭐ JUGADA FIJA NFL):**<br><br>• **EPA per Play:** Dominio en eficiencia ofensiva bajo presión.",
            "analisis_en": "**EXPERT SABERMETRIC ANALYSIS (⭐ NFL LOCK OF THE DAY):**<br><br>• **EPA per Play:** Chiefs dominate.",
            "es_jugada_fija": True
        }]
    df_resp = pd.DataFrame(datos_respaldo)
    guardar_cartelera(df_resp)
    return df_resp

def guardar_cartelera(df):
    try:
        df.to_csv(cartelera_csv_path, index=False, encoding="utf-8")
    except Exception:
        pass

def cargar_checklist():
    if os.path.exists(checklist_csv_path):
        try:
            df = pd.read_csv(checklist_csv_path, encoding="utf-8")
            if not df.empty:
                return df
        except Exception:
            pass
    return pd.DataFrame(columns=["partido", "estado", "alerta_notas", "cambio_perspectiva"])

def guardar_checklist(df):
    try:
        df.to_csv(checklist_csv_path, index=False, encoding="utf-8")
    except Exception:
        pass

def cargar_apuestas_usa():
    if os.path.exists(apuestas_csv_path):
        try:
            df_apuestas = pd.read_csv(apuestas_csv_path, encoding="utf-8")
            if not df_apuestas.empty:
                return df_apuestas
        except Exception:
            pass
    return pd.DataFrame(columns=["equipo1", "equipo2", "spread", "total_ou", "proyeccion_usa", "probabilidad"])

menu_options_es = [
    "Cartelera y Partidos",
    "Apuestas y Proyecciones USA (Las Vegas)",
    "🧭 Checklist de Último Minuto",
    "El Pulso de la Duela (Noticias)",
    "La Jugada Fija del Día",
    "Diccionario Sabermétrico",
    "Panel de Administración",
]

menu_options_en = [
    "Matchup Schedule",
    "USA Betting & Projections (Las Vegas)",
    "🧭 Last-Minute Checklist",
    "The Pulse of the Matchup (News)",
    "Lock of the Day",
    "Sabermetric Dictionary",
    "Admin Panel",
]

menu_options = menu_options_es if lang == "es" else menu_options_en
menu = st.sidebar.radio("Selecciona una sección:" if lang == "es" else "Select a section:", menu_options)

is_cartelera = menu in ["Cartelera y Partidos", "Matchup Schedule"]
is_apuestas = menu in ["Apuestas y Proyecciones USA (Las Vegas)", "USA Betting & Projections (Las Vegas)"]
is_checklist = menu in ["🧭 Checklist de Último Minuto", "🧭 Last-Minute Checklist"]
is_pulso = menu in ["El Pulso de la Duela (Noticias)", "The Pulse of the Matchup (News)"]
is_jugada = menu in ["La Jugada Fija del Día", "Lock of the Day"]
is_diccionario = menu in ["Diccionario Sabermétrico", "Sabermetric Dictionary"]
is_admin = menu in ["Panel de Administración", "Admin Panel"]

fecha_hoy = datetime.now().strftime("%d de %B de %Y" if lang == "es" else "%B %d, %Y")
df_cartelera = cargar_cartelera()
df_apuestas = cargar_apuestas_usa()

ayer_auto, acum_auto = calcular_metricas_efectividad()
with st.container():
    sport_label = "NBA (Básquetbol)" if sport_prefix == "nba" else "NFL (Fútbol Americano)"
    if lang == "es":
        st.markdown(f"🎯 **Efectividad Modelo [{sport_label}]:**<br>• Jornada Anterior: **{ayer_auto}**<br>• Acumulado Global: **{acum_auto}**", unsafe_allow_html=True)
    else:
        st.markdown(f"🎯 **Model Effectiveness [{sport_label}]:**<br>• Last Slate: **{ayer_auto}**<br>• Accumulated: **{acum_auto}**", unsafe_allow_html=True)

if is_cartelera:
    st.header(f"Cartelera de Partidos [{sport_label}] - Análisis Profundo (" + fecha_hoy + ")" if lang == "es" else f"Matchup Schedule [{sport_label}] - Deep Analysis (" + fecha_hoy + ")")
    if df_cartelera.empty:
        st.warning("No hay partidos cargados actualmente en la cartelera." if lang == "es" else "No matches currently loaded in the schedule.")
    else:
        st.write("Selecciona un encuentro para ver el desglose científico del modelo:" if lang == "es" else "Select a matchup to view the model's scientific breakdown:")
        opciones_dict = {}
        for _, row in df_cartelera.iterrows():
            e1 = str(row["equipo1"]).strip()
            e2 = str(row["equipo2"]).strip()
            label = e1 + " vs. " + e2
            opciones_dict[label] = row

        partido_seleccionado = st.selectbox("Juegos de hoy:" if lang == "es" else "Today's Games:", list(opciones_dict.keys()))
        if partido_seleccionado:
            fila_juego = opciones_dict[partido_seleccionado]
            equipo1 = str(fila_juego["equipo1"]).strip()
            equipo2 = str(fila_juego["equipo2"]).strip()
            logo1_url = LOGOS_EQUIPOS.get(equipo1, "")
            logo2_url = LOGOS_EQUIPOS.get(equipo2, "")

            col_L, col_VS, col_R = st.columns([2, 1, 2])
            with col_L:
                if logo1_url:
                    st.image(logo1_url, width=80)
                st.subheader(equipo1)
                st.caption("(Visitante)" if lang == "es" else "(Visitor)")
            with col_VS:
                st.markdown("<h2 style='text-align: center; color: #00FF66;'>VS</h2>", unsafe_allow_html=True)
            with col_R:
                if logo2_url:
                    st.image(logo2_url, width=80)
                st.subheader(equipo2)
                st.caption("(Local)" if lang == "es" else "(Home)")

            hora_val = str(fila_juego.get("hora", "19:30 (VE)"))
            sede_val = str(fila_juego.get("sede", "Arena Principal"))
            st.markdown(f"🕒 **{'Hora (VE)' if lang == 'es' else 'Time (VE)'}:** {hora_val} &nbsp;&nbsp;|&nbsp;&nbsp; 🏟️ **{'Sede' if lang == 'es' else 'Venue'}:** {sede_val}")
            st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Ganador Proyectado" if lang == "es" else "Projected Winner", value=str(fila_juego["ganador"]))
            with col2:
                st.metric(label="Total de Puntos (O/U)" if lang == "es" else "Total Points (O/U)", value=str(fila_juego["total_puntos"]))

            st.markdown("### " + ("Razonamiento Táctico y Métricas Avanzadas" if lang == "es" else "Tactical Reasoning & Advanced Metrics"))
            analisis_amplio = str(fila_juego["analisis_es"]) if lang == "es" else str(fila_juego.get("analisis_en", fila_juego["analisis_es"]))
            st.markdown(analisis_amplio, unsafe_allow_html=True)

elif is_apuestas:
    st.header("🇺🇸 Proyecciones y Líneas USA (Las Vegas Lines)" if lang == "es" else "🇺🇸 USA Projections & Lines (Las Vegas)")
    st.write("Análisis de mercado ordenado rigurosamente de mayor a menor probabilidad según nuestro modelo sabermétrico:" if lang == "es" else "Market analysis rigorously sorted by highest to lowest probability according to our sabermetric model:")
    if df_apuestas.empty:
        st.info("No hay datos de apuestas cargados actualmente." if lang == "es" else "No betting data currently loaded.")
    else:
        df_apuestas_ordenado = df_apuestas.sort_values(by="probabilidad", ascending=False) if "probabilidad" in df_apuestas.columns else df_apuestas
        for _, row in df_apuestas_ordenado.iterrows():
            e1 = str(row.get("equipo1", ""))
            e2 = str(row.get("equipo2", ""))
            spread = str(row.get("spread", ""))
            total_ou = str(row.get("total_ou", ""))
            prob = row.get("probabilidad", 0.0)
            proj = str(row.get("proyeccion_usa", ""))
            
            with st.container():
                cols = st.columns([3, 2, 2, 2])
                with cols[0]:
                    st.markdown(f"**{e1} vs {e2}**")
                with cols[1]:
                    st.markdown(f"Spread: `{spread}`")
                with cols[2]:
                    st.markdown(f"Total: `{total_ou}`")
                with cols[3]:
                    st.metric("Confianza" if lang == "es" else "Confidence", f"{prob}%" if prob else "N/A")
                st.markdown(f"*{proj}*")
                st.markdown("---")

elif is_checklist:
    st.header("🧭 Checklist de Último Minuto del Analista" if lang == "es" else "🧭 Analyst Last-Minute Checklist")
    st.markdown("Monitoreo en vivo de lesiones, reportes climáticos/médicos oficiales y factores de última hora." if lang == "es" else "Live monitoring of injuries, official injury/weather reports, and last-minute factors.")
    st.markdown("---")
    df_chk = cargar_checklist()
    if df_chk.empty:
        st.info("No hay alertas registradas para la jornada de hoy." if lang == "es" else "No alerts registered for today's slate.")
    else:
        for _, row in df_chk.iterrows():
            partido = str(row.get("partido", ""))
            estado = str(row.get("estado", "🟢 Normal"))
            notas = str(row.get("alerta_notas", ""))
            cambio = str(row.get("cambio_perspectiva", "Ninguno"))
            
            color_box = "#161b22"
            border_col = "#00FF66" if "🟢" in estado else ("#FFD700" if "🟡" in estado else "#FF4B4B")
            
            st.markdown(f"""
            <div style="background-color: {color_box}; padding: 18px; border-radius: 10px; border-left: 5px solid {border_col}; margin-bottom: 15px;">
                <h4 style="margin: 0; color: #ffffff;">{partido} &nbsp;|&nbsp; Estado: {estado}</h4>
                <p style="margin: 8px 0 0 0; color: #e6edf3;"><b>Notas:</b> {notas}</p>
                <p style="margin: 5px 0 0 0; color: #00FF66;"><b>Sugerencia:</b> {cambio}</p>
            </div>
            """, unsafe_allow_html=True)

elif is_pulso:
    st.header("🎙️ El Pulso de la Duela - Crónicas y Exclusivas (" + fecha_hoy + ")" if lang == "es" else "🎙️ The Pulse of the Matchup - Chronicles & Exclusives (" + fecha_hoy + ")")
    st.markdown("---")
    mat_es, mat_en = cargar_noticias_txt()
    cronica_texto = mat_es if lang == "es" else mat_en
    st.markdown(f"""<div style="background-color: #161b22; padding: 25px; border-radius: 12px; border-left: 5px solid #00FF66;">{cronica_texto.replace(chr(10), '<br>')}</div>""", unsafe_allow_html=True)

elif is_jugada:
    st.header("La Jugada Estelar del Modelo" if lang == "es" else "Model's Star Play (Lock of the Day)")
    if df_cartelera.empty:
        st.warning("No hay partidos cargados actualmente." if lang == "es" else "No matches currently loaded.")
    else:
        juegos_fijos = df_cartelera[df_cartelera["es_jugada_fija"].astype(str).str.lower().isin(["true", "1", "yes", "si"])]
        juego_estelar = juegos_fijos.iloc[0] if not juegos_fijos.empty else df_cartelera.iloc[0]
        st.subheader(f"{juego_estelar['equipo1']} vs {juego_estelar['equipo2']}")
        st.markdown(str(juego_estelar["analisis_es"] if lang == "es" else juego_estelar.get("analisis_en", juego_estelar["analisis_es"])), unsafe_allow_html=True)

elif is_diccionario:
    st.header("Diccionario Sabermétrico Educativo" if lang == "es" else "Educational Sabermetric Dictionary")
    if sport_prefix == "nba":
        st.markdown("### Métricas NBA\n- **Pace (Ritmo):** Posesiones por 48 min.\n- **TS% (True Shooting):** Eficiencia de tiro.\n- **Net Rating:** Diferencial por 100 posesiones.")
    else:
        st.markdown("### Métricas NFL\n- **EPA (Expected Points Added):** Puntos esperados añadidos por jugada.\n- **Success Rate:** Porcentaje de jugadas con rendimiento positivo según situación.\n- **DVOA:** Defensa u ofensiva ajustada al rival y situación.")

elif is_admin:
    st.header(f"🔐 Panel de Administración [{sport_label}]" if lang == "es" else f"🔐 Admin Panel [{sport_label}]")
    clave = st.text_input("Clave de administrador:" if lang == "es" else "Admin password:", type="password")
    if clave == "sabermetria2026":
        st.success("¡Acceso concedido!" if lang == "es" else "Access granted!")
        archivo_subido = st.file_uploader("Cargar Cartelera CSV:" if lang == "es" else "Upload Matchup CSV:", type=["csv"])
        if archivo_subido is not None:
            df_nuevo = pd.read_csv(archivo_subido, encoding="utf-8")
            guardar_cartelera(df_nuevo)
            st.success("¡Cartelera actualizada con éxito!" if lang == "es" else "Schedule updated successfully!")
            st.rerun()
