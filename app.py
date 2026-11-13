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
estadisticas_path = os.path.join(current_dir, "historial_aciertos.csv")
historial_efectividad_path = os.path.join(current_dir, "historial_efectividad.csv")
noticias_txt_path = os.path.join(current_dir, "noticias.txt")
cartelera_csv_path = os.path.join(current_dir, "cartelera_juegos.csv")
apuestas_csv_path = os.path.join(current_dir, "apuestas_usa.csv")
checklist_csv_path = os.path.join(current_dir, "checklist_ultimo_minuto.csv")

st.set_page_config(
    page_title="Sabermetría IA - Analítica Avanzada de Básquetbol",
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

def cargar_noticias_txt():
    default_mat_es = (
        "Una Noche de Pura Maestría Táctica: El Salto de Calidad del Modelo Sabermétrico\n\n"
        "• Precisión en la duela: Evaluando los marcadores recientes para ajustar nuestro rendimiento con absoluta transparencia.\n\n"
        "• Duelos de alto voltaje: La analítica avanzada sigue marcando la pauta en cada posesión."
    )
    default_mat_en = (
        "A Night of Pure Tactical Mastery: The Sabermetric Model's Leap\n\n"
        "• Court Precision: Reviewing recent scores to adjust our performance with absolute transparency.\n\n"
        "• High-Voltage Showdowns: Advanced analytics setting the pace."
    )
    if os.path.exists(noticias_txt_path):
        try:
            with open(noticias_txt_path, "r", encoding="utf-8") as f:
                lines = f.read().split("---SEPARADOR_NOTICIAS---")
                if len(lines) >= 2:
                    return lines[0].strip(), lines[1].strip()
        except Exception:
            pass
    return default_mat_es, default_mat_en

def guardar_noticias_txt(mat_es, mat_en):
    try:
        with open(noticias_txt_path, "w", encoding="utf-8") as f:
            f.write(mat_es + "\n---SEPARADOR_NOTICIAS---\n" + mat_en)
    except Exception:
        pass

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #00FF66; color: #000000; font-weight: bold; border-radius: 8px; }
    </style>
""",
    unsafe_allow_html=True,
)

LOGOS_EQUIPOS = {
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

def generar_pdf_analisis(partido, hora, sede, ganador, total_puntos, razonamiento):
    pdf_path = os.path.join(current_dir, "reporte_sabermetria.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    title_style = ParagraphStyle("TitleStyle", parent=styles["Heading1"], fontSize=16, textColor=colors.HexColor("#00FF66"), spaceAfter=12)
    body_style = ParagraphStyle("BodyStyle", parent=styles["Normal"], fontSize=10, textColor=colors.HexColor("#333333"), spaceAfter=10, leading=14)
    story.append(Paragraph("SABERMETRÍA IA - REPORTE DE ANALÍTICA AVANZADA", title_style))
    story.append(Paragraph("Encuentro: " + partido, body_style))
    story.append(Paragraph("Hora (VE): " + hora + " | Sede: " + sede, body_style))
    story.append(Paragraph("Fecha del Reporte: " + datetime.now().strftime("%d/%m/%Y"), body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Ganador Proyectado: " + ganador, body_style))
    story.append(Paragraph("Línea de Puntos Totales (O/U): " + total_puntos, body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Desglose Táctico y Métricas del Modelo:", title_style))
    story.append(Paragraph(razonamiento, body_style))
    doc.build(story)
    return pdf_path

def cargar_historial_efectividad():
    if os.path.exists(historial_efectividad_path):
        try:
            df_hist = pd.read_csv(historial_efectividad_path, encoding="utf-8")
            if not df_hist.empty:
                return df_hist
        except Exception:
            pass
    df_default = pd.DataFrame([
        {"fecha": "2026-11-01", "juegos": 4, "aciertos": 3, "efectividad": 75.0},
        {"fecha": "2026-11-02", "juegos": 15, "aciertos": 7, "efectividad": 46.7},
        {"fecha": "2026-11-04", "juegos": 14, "aciertos": 12, "efectividad": 85.7},
        {"fecha": "2026-11-05", "juegos": 2, "aciertos": 2, "efectividad": 100.0},
        {"fecha": "2026-11-06", "juegos": 9, "aciertos": 8, "efectividad": 88.9},
        {"fecha": "2026-11-07", "juegos": 7, "aciertos": 7, "efectividad": 100.0},
        {"fecha": "2026-11-08", "juegos": 7, "aciertos": 6, "efectividad": 85.7},
        {"fecha": "2026-11-09", "juegos": 8, "aciertos": 4, "efectividad": 50.0},
        {"fecha": "2026-11-10", "juegos": 6, "aciertos": 3, "efectividad": 50.0},
        {"fecha": "2026-11-11", "juegos": 10, "aciertos": 7, "efectividad": 70.0},
        {"fecha": "2026-11-12", "juegos": 4, "aciertos": 4, "efectividad": 100.0}
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

def cargar_estadisticas():
    ayer_str, _ = calcular_metricas_efectividad()
    return ayer_str

def guardar_estadisticas(ayer):
    pass

def cargar_cartelera():
    if os.path.exists(cartelera_csv_path):
        try:
            df_saved = pd.read_csv(cartelera_csv_path, encoding="utf-8")
            if not df_saved.empty:
                return df_saved
        except Exception:
            pass
    datos_respaldo = [
        {
            "equipo1": "Orlando Magic",
            "equipo2": "Boston Celtics",
            "hora": "16:30 (VE)",
            "sede": "Kia Center, Orlando",
            "ganador": "Boston Celtics",
            "total_puntos": "220.5",
            "analisis_es": "**ANÁLISIS SABERMÉTRICO EXPERTO (⭐ JUGADA FIJA):**<br><br>• **Net Rating Superior:** Los Celtics dominan con una eficiencia neta abrumadora.",
            "analisis_en": "**EXPERT SABERMETRIC ANALYSIS (⭐ LOCK OF THE DAY):**<br><br>• **Net Rating:** Celtics lead in efficiency.",
            "es_jugada_fija": True,
        }
    ]
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

idioma = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
lang = "es" if idioma == "Español" else "en"

st.sidebar.title("Menú Principal" if lang == "es" else "Main Menu")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=220)

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

menu = st.sidebar.radio(
    "Selecciona una sección:" if lang == "es" else "Select a section:",
    menu_options,
)

# Normalize menu routing regardless of language
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
    if lang == "es":
        st.markdown(f"🎯 **Efectividad Modelo:**<br>• Jornada Anterior: **{ayer_auto}**<br>• Acumulado Global: **{acum_auto}**", unsafe_allow_html=True)
    else:
        st.markdown(f"🎯 **Model Effectiveness:**<br>• Last Slate: **{ayer_auto}**<br>• Accumulated: **{acum_auto}**", unsafe_allow_html=True)

if is_cartelera:
    st.header("Cartelera de Partidos - Análisis Profundo (" + fecha_hoy + ")" if lang == "es" else "Matchup Schedule - Deep Analysis (" + fecha_hoy + ")")
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

            st.markdown("---")
            if st.button("📄 " + ("Descargar Análisis en PDF" if lang == "es" else "Download Analysis PDF")):
                archivo_pdf = generar_pdf_analisis(
                    equipo1 + " vs " + equipo2, hora_val, sede_val, str(fila_juego["ganador"]), str(fila_juego["total_puntos"]), analisis_amplio.replace("<br>", "\n").replace("<b>", "")
                )
                with open(archivo_pdf, "rb") as f:
                    st.download_button("💾 " + ("Guardar archivo PDF en tu equipo" if lang == "es" else "Save PDF file to your device"), data=f, file_name="reporte_sabermetria_nba.pdf", mime="application/pdf")

elif is_apuestas:
    st.header("🇺🇸 Proyecciones y Líneas USA (Las Vegas Lines)" if lang == "es" else "🇺🇸 USA Projections & Lines (Las Vegas)")
    st.write("Análisis de mercado ordenado rigurosamente de mayor a menor probabilidad según nuestro modelo sabermétrico:" if lang == "es" else "Market analysis rigorously sorted by highest to lowest probability according to our sabermetric model:")
    if df_apuestas.empty:
        st.info("No hay datos de apuestas cargados actualmente. Utilice el panel de administración para incorporar las líneas." if lang == "es" else "No betting data currently loaded. Use the admin panel to upload lines.")
    else:
        if "probabilidad" in df_apuestas.columns:
            df_apuestas_ordenado = df_apuestas.sort_values(by="probabilidad", ascending=False)
        else:
            df_apuestas_ordenado = df_apuestas
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
    st.markdown("Monitoreo en vivo de lesiones, reportes médicos oficiales (Rotowire / NBA Injury Report), fatiga *back-to-back* y factores de última hora que complementan nuestras métricas sabermétricas." if lang == "es" else "Live monitoring of injuries, official medical reports (Rotowire / NBA Injury Report), back-to-back fatigue, and last-minute factors complementing our sabermetric metrics.")
    st.markdown("---")
    df_chk = cargar_checklist()
    if df_chk.empty:
        st.info("No hay alertas registradas para la jornada de hoy. Las métricas operan con normalidad." if lang == "es" else "No alerts registered for today's slate. Metrics operating normally.")
    else:
        for _, row in df_chk.iterrows():
            partido = str(row.get("partido", ""))
            estado = str(row.get("estado", "🟢 Normal"))
            notas = str(row.get("alerta_notas", ""))
            cambio = str(row.get("cambio_perspectiva", "Ninguno"))
            
            color_box = "#161b22"
            if "🟢" in estado:
                border_col = "#00FF66"
            elif "🟡" in estado:
                border_col = "#FFD700"
            else:
                border_col = "#FF4B4B"
            
            estado_label = "Estado" if lang == "es" else "Status"
            notas_label = "Notas del Analista (Rotowire / Lesiones / B2B):" if lang == "es" else "Analyst Notes (Rotowire / Injuries / B2B):"
            sug_label = "Sugerencia / Perspectiva:" if lang == "es" else "Suggestion / Perspective:"
            
            st.markdown(f"""
            <div style="background-color: {color_box}; padding: 18px; border-radius: 10px; border-left: 5px solid {border_col}; margin-bottom: 15px;">
                <h4 style="margin: 0; color: #ffffff;">{partido} &nbsp;|&nbsp; {estado_label}: {estado}</h4>
                <p style="margin: 8px 0 0 0; color: #e6edf3;"><b>{notas_label}</b> {notas}</p>
                <p style="margin: 5px 0 0 0; color: #00FF66;"><b>{sug_label}</b> {cambio}</p>
            </div>
            """, unsafe_allow_html=True)

elif is_pulso:
    st.header("🎙️ El Pulso de la Duela - Crónicas y Exclusivas (" + fecha_hoy + ")" if lang == "es" else "🎙️ The Pulse of the Matchup - Chronicles & Exclusives (" + fecha_hoy + ")")
    st.markdown("<p style='color: #00FF66; font-size: 1.1em; font-weight: bold;'>" + ("El análisis más ardiente y sin censura de las duelas de la NBA." if lang == "es" else "The hottest, uncensored analysis of NBA courts.") + "</p>", unsafe_allow_html=True)
    st.markdown("---")
    mat_es, mat_en = cargar_noticias_txt()
    cronica_texto = mat_es if lang == "es" else mat_en
    st.markdown(
        f"""
        <div style="background-color: #161b22; padding: 25px; border-radius: 12px; border-left: 5px solid #00FF66; box-shadow: 0 4px 12px rgba(0,255,102,0.15);">
            <div style="font-size: 1.05em; line-height: 1.6; color: #e6edf3;">
                {cronica_texto.replace(chr(10), '<br>')}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

elif is_jugada:
    st.header("La Jugada Estelar del Modelo" if lang == "es" else "Model's Star Play (Lock of the Day)")
    if df_cartelera.empty:
        st.warning("No hay partidos cargados actualmente." if lang == "es" else "No matches currently loaded.")
    else:
        juegos_fijos = df_cartelera[df_cartelera["es_jugada_fija"].astype(str).str.lower().isin(["true", "1", "yes", "si"])]
        juego_estelar = juegos_fijos.iloc[0] if not juegos_fijos.empty else df_cartelera.iloc[0]
        estelar_eq1 = str(juego_estelar["equipo1"]).strip()
        estelar_eq2 = str(juego_estelar["equipo2"]).strip()
        logo_estelar_1 = LOGOS_EQUIPOS.get(estelar_eq1, "")
        logo_estelar_2 = LOGOS_EQUIPOS.get(estelar_eq2, "")

        col_L, col_VS, col_R = st.columns([2, 1, 2])
        with col_L:
            if logo_estelar_1:
                st.image(logo_estelar_1, width=80)
            st.subheader(estelar_eq1)
            st.caption("(Visitante)" if lang == "es" else "(Visitor)")
        with col_VS:
            st.markdown("<h2 style='text-align: center; color: #00FF66;'>VS</h2>", unsafe_allow_html=True)
        with col_R:
            if logo_estelar_2:
                st.image(logo_estelar_2, width=80)
            st.subheader(estelar_eq2)
            st.caption("(Local)" if lang == "es" else "(Home)")

        analisis_jugada = str(juego_estelar["analisis_es"]) if lang == "es" else str(juego_estelar.get("analisis_en", juego_estelar["analisis_es"]))
        st.markdown(analisis_jugada, unsafe_allow_html=True)

elif is_diccionario:
    st.header("Diccionario Sabermétrico Educativo" if lang == "es" else "Educational Sabermetric Dictionary")
    st.write("Guía completa de referencia para comprender desde los fundamentos tradicionales hasta las métricas de eficiencia:" if lang == "es" else "Complete reference guide covering everything from traditional fundamentals to efficiency metrics:")
    if lang == "es":
        st.markdown(
            "### Indicadores Básicos y Tradicionales\n"
            "- **PTS (Points):** Total de puntos anotados.\n"
            "- **REB (Rebounds):** Rebotes totales.\n"
            "- **AST (Assists):** Asistencias de canasta.\n\n"
            "### Indicadores Avanzados (Sabermetría IA)\n"
            "- **Pace (Ritmo):** Posesiones estimadas por 48 minutos.\n"
            "- **TS% (True Shooting):** Eficiencia de tiro global.\n"
            "- **Net Rating:** Diferencial de puntos por 100 posesiones."
        )
    else:
        st.markdown(
            "### Basic & Traditional Indicators\n"
            "- **PTS (Points):** Total points scored.\n"
            "- **REB (Rebounds):** Total rebounds.\n"
            "- **AST (Assists):** Total assists.\n\n"
            "### Advanced Indicators (Sabermetrics IA)\n"
            "- **Pace:** Estimated possessions per 48 minutes.\n"
            "- **TS% (True Shooting):** Overall scoring efficiency.\n"
            "- **Net Rating:** Point differential per 100 possessions."
        )

elif is_admin:
    st.header("🔐 Panel de Control y Publicación - Sabermetría IA" if lang == "es" else "🔐 Control & Publishing Panel - Sabermetría IA")
    st.write("Control estadístico, cartelera, apuestas y crónicas editoriales." if lang == "es" else "Statistical control, schedule, betting lines, and editorial chronicles.")

    clave_admin = st.text_input("Ingresa la clave de administrador:" if lang == "es" else "Enter admin password:", type="password", key="input_clave_admin")

    if clave_admin == "sabermetria2026":
        st.success("¡Acceso de administrador concedido!" if lang == "es" else "Admin access granted!")

        if os.path.exists(db_usuarios_path):
            df_visitas = pd.read_csv(db_usuarios_path, encoding="utf-8")
            st.metric(label="Total de Ingresos Acumulados al Portal" if lang == "es" else "Total Portal Visits", value=len(df_visitas))
            st.dataframe(df_visitas, use_container_width=True)
        else:
            st.metric(label="Total de Ingresos Acumulados al Portal" if lang == "es" else "Total Portal Visits", value=0)

        st.markdown("---")
        st.subheader("🧭 Gestor del Checklist de Último Minuto" if lang == "es" else "🧭 Last-Minute Checklist Manager")
        df_chk_admin = cargar_checklist()
        with st.form("form_checklist_admin"):
            partido_chk = st.selectbox("Selecciona el Partido:" if lang == "es" else "Select Matchup:", [f"{r['equipo1']} vs {r['equipo2']}" for _, r in df_cartelera.iterrows()] if not df_cartelera.empty else ["Ninguno" if lang == "es" else "None"])
            estado_chk = st.selectbox("Nivel de Alerta:" if lang == "es" else "Alert Level:", ["🟢 Normal (Métrica Pura)" if lang == "es" else "🟢 Normal (Pure Metric)", "🟡 Precaución (Baja / Back-to-back)" if lang == "es" else "🟡 Caution (Injury / B2B)", "🔴 Alerta Roja (Cambio de Perspectiva / Voltear Pronóstico)" if lang == "es" else "🔴 Red Alert (Perspective Shift / Flip Prediction)"])
            notas_chk = st.text_area("Notas del Analista (Rotowire / Lesiones / Descanso):" if lang == "es" else "Analyst Notes (Rotowire / Injuries / Rest):", value="Sin novedades reportadas en el parte médico oficial." if lang == "es" else "No news reported in official injury report.")
            cambio_chk = st.text_input("Sugerencia de Ajuste / Cambio de Perspectiva:" if lang == "es" else "Adjustment Suggestion / Perspective Shift:", value="Mantener pronóstico base del modelo." if lang == "es" else "Maintain base model prediction.")
            
            if st.form_submit_button("💾 " + ("Guardar / Actualizar Alerta de Partido" if lang == "es" else "Save / Update Matchup Alert")):
                nuevo_item = pd.DataFrame([{"partido": partido_chk, "estado": estado_chk, "alerta_notas": notas_chk, "cambio_perspectiva": cambio_chk}])
                if not df_chk_admin.empty:
                    df_chk_admin = df_chk_admin[df_chk_admin["partido"] != partido_chk]
                    df_chk_admin = pd.concat([df_chk_admin, nuevo_item], ignore_index=True)
                else:
                    df_chk_admin = nuevo_item
                guardar_checklist(df_chk_admin)
                st.success(f"¡Alerta actualizada para {partido_chk}!" if lang == "es" else f"Alert updated for {partido_chk}!")
                st.rerun()

        st.subheader("📤 Carga Masiva de Cartelera de Partidos (CSV)" if lang == "es" else "📤 Schedule Mass Upload (CSV)")
        csv_ejemplo = df_cartelera.to_csv(index=False).encode("utf-8")
        st.download_button(label="📥 " + ("Descargar Plantilla CSV de Partidos" if lang == "es" else "Download Matchup CSV Template"), data=csv_ejemplo, file_name="plantilla_cartelera_ejemplo.csv", mime="text/csv")

        archivo_subido = st.file_uploader("Selecciona el archivo CSV de partidos:" if lang == "es" else "Select matchups CSV file:", type=["csv"], key="up_cartelera")
        if archivo_subido is not None:
            try:
                df_nuevo_csv = pd.read_csv(archivo_subido, encoding="utf-8")
                guardar_cartelera(df_nuevo_csv)
                st.success("¡Cartelera actualizada con éxito!" if lang == "es" else "Schedule updated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        if st.button("🗑️ " + ("Vaciar / Borrar Toda la Cartelera" if lang == "es" else "Clear / Delete All Schedule")):
            if os.path.exists(cartelera_csv_path):
                os.remove(cartelera_csv_path)
            guardar_cartelera(pd.DataFrame(columns=["equipo1", "equipo2", "hora", "sede", "ganador", "total_puntos", "analisis_es", "analisis_en", "es_jugada_fija"]))
            st.success("¡Cartelera vaciada!" if lang == "es" else "Schedule cleared!")
            st.rerun()

        st.markdown("---")
        st.subheader("🇺🇸 Carga Masiva de Apuestas y Proyecciones USA (CSV)" if lang == "es" else "🇺🇸 USA Betting Projections Mass Upload (CSV)")
        
        df_plantilla_apuestas = pd.DataFrame([
            {"equipo1": "Orlando Magic", "equipo2": "Boston Celtics", "spread": "-8.5", "total_ou": "220.5", "proyeccion_usa": "Pick: Boston Celtics | Line: -8.5 | Conf: 91.0%", "probabilidad": 91.0},
            {"equipo1": "Indiana Pacers", "equipo2": "Brooklyn Nets", "spread": "-5.5", "total_ou": "234.0", "proyeccion_usa": "Pick: Indiana Pacers | Line: -5.5 | Conf: 87.5%", "probabilidad": 87.5}
        ])
        csv_apuestas_bytes = df_plantilla_apuestas.to_csv(index=False, encoding="utf-8").encode("utf-8")
        st.download_button(
            label="📥 " + ("Descargar Plantilla CSV de Apuestas USA" if lang == "es" else "Download USA Betting CSV Template"), 
            data=csv_apuestas_bytes, 
            file_name="plantilla_apuestas_usa.csv", 
            mime="text/csv"
        )

        archivo_apuestas_subido = st.file_uploader("Selecciona el archivo CSV de Apuestas USA:" if lang == "es" else "Select USA Betting CSV file:", type=["csv"], key="up_apuestas")
        if archivo_apuestas_subido is not None:
            try:
                df_nuevo_apuestas = pd.read_csv(archivo_apuestas_subido, encoding="utf-8")
                df_nuevo_apuestas.to_csv(apuestas_csv_path, index=False, encoding="utf-8")
                st.success("¡Apuestas USA actualizadas con éxito!" if lang == "es" else "USA Betting updated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        if st.button("🗑️ " + ("Vaciar / Borrar Tabla de Apuestas USA" if lang == "es" else "Clear / Delete USA Betting Table")):
            if os.path.exists(apuestas_csv_path):
                os.remove(apuestas_csv_path)
            pd.DataFrame(columns=["equipo1", "equipo2", "spread", "total_ou", "proyeccion_usa", "probabilidad"]).to_csv(apuestas_csv_path, index=False, encoding="utf-8")
            st.success("¡Tabla de apuestas vaciada!" if lang == "es" else "Betting table cleared!")
            st.rerun()

        st.markdown("---")
        st.subheader("📊 Control Automático de Efectividad e Historial" if lang == "es" else "📊 Automatic Effectiveness & History Control")
        ayer_str, acumulado_str = calcular_metricas_efectividad()
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Efectividad Jornada Anterior" if lang == "es" else "Last Slate Effectiveness", ayer_str)
        with col_m2:
            st.metric("Efectividad Acumulada Temporada" if lang == "es" else "Accumulated Season Effectiveness", acumulado_str)
            
        st.write("Registra los resultados de la nueva jornada para actualizar automáticamente el acumulado:" if lang == "es" else "Record new slate results to automatically update the cumulative record:")
        df_hist_actual = cargar_historial_efectividad()
        st.dataframe(df_hist_actual, use_container_width=True)
        
        with st.form("form_nuevo_registro_efectividad"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                fecha_reg = st.text_input("Fecha (YYYY-MM-DD):" if lang == "es" else "Date (YYYY-MM-DD):", value=datetime.now().strftime("%Y-%m-%d"))
                juegos_reg = st.number_input("Total de Partidos Pronosticados:" if lang == "es" else "Total Games Predicted:", min_value=1, max_value=30, value=15)
            with col_f2:
                aciertos_reg = st.number_input("Partidos Acertados:" if lang == "es" else "Correct Predictions:", min_value=0, max_value=30, value=8)
            
            if st.form_submit_button("➕ " + ("Registrar Jornada y Recalcular Automáticamente" if lang == "es" else "Register Slate & Recalculate Automatically")):
                pct = (aciertos_reg / juegos_reg * 100) if juegos_reg > 0 else 0.0
                nueva_fila = pd.DataFrame([{"fecha": fecha_reg, "juegos": int(juegos_reg), "aciertos": int(aciertos_reg), "efectividad": round(pct, 1)}])
                df_actualizado = pd.concat([df_hist_actual, nueva_fila], ignore_index=True)
                guardar_historial_efectividad(df_actualizado)
                st.success(f"¡Jornada registrada con éxito! Efectividad del día: {{pct:.1f}}%" if lang == "es" else f"Slate successfully registered! Daily effectiveness: {{pct:.1f}}%")
                st.rerun()

        mat_es_act, mat_en_act = cargar_noticias_txt()
        with st.form("form_noticias_txt"):
            txt_mat_es = st.text_area("Crónica (Español):" if lang == "es" else "Chronicle (Spanish):", value=mat_es_act, height=180)
            txt_mat_en = st.text_area("Editorial (English):" if lang == "es" else "Editorial (English):", value=mat_en_act, height=180)
            if st.form_submit_button("💾 " + ("Guardar y Publicar Crónica" if lang == "es" else "Save & Publish Chronicle")):
                guardar_noticias_txt(txt_mat_es, txt_mat_en)
                st.success("¡Crónica publicada con éxito!" if lang == "es" else "Chronicle published successfully!")
                st.rerun()

    elif clave_admin != "":
        st.error("❌ Clave de administrador incorrecta." if lang == "es" else "❌ Incorrect admin password.")
