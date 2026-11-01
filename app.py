from datetime import datetime
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
import streamlit as st
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo.jpeg")
db_usuarios_path = os.path.join(current_dir, "registros_tiktok.csv")
estadisticas_path = os.path.join(current_dir, "historial_aciertos.csv")
noticias_txt_path = os.path.join(current_dir, "noticias.txt")
cartelera_csv_path = os.path.join(current_dir, "cartelera_juegos.csv")
apuestas_csv_path = os.path.join(current_dir, "apuestas_usa.csv")

st.set_page_config(
    page_title="Sabermetría IA - Analítica Avanzada de Básquetbol",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

def cargar_estadisticas():
    if os.path.exists(estadisticas_path):
        try:
            return str(pd.read_csv(estadisticas_path, encoding="utf-8").iloc[0]["ayer"])
        except Exception:
            pass
    return "Actualizando rendimiento..."

def guardar_estadisticas(ayer):
    pd.DataFrame([[ayer]], columns=["ayer"]).to_csv(estadisticas_path, index=False, encoding="utf-8")

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
            "analisis_es": "**ANÁLISIS SABERMÉTRICO EXPERTO (⭐ JUGADA FIJA):**<br><br>• **Net Rating Superior:** Los Celtics dominan en eficiencia neta y control de ritmo.",
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

menu = st.sidebar.radio(
    "Selecciona una sección:" if lang == "es" else "Select a section:",
    [
        "Cartelera y Partidos",
        "Apuestas y Proyecciones USA (Las Vegas)",
        "El Pulso de la Duela (Noticias)",
        "La Jugada Fija del Día",
        "Diccionario Sabermétrico",
        "Panel de Administración",
    ],
)

fecha_hoy = datetime.now().strftime("%d de %B de %Y")
df_cartelera = cargar_cartelera()
df_apuestas = cargar_apuestas_usa()
ayer_str = cargar_estadisticas()

with st.container():
    st.info(
        f"🎯 **Rendimiento del Modelo Sabermétrico:** Aciertos Recientes: **{ayer_str}**"
        if lang == "es"
        else f"🎯 **Sabermetric Model Performance:** Recent Hits: **{ayer_str}**"
    )

if menu == "Cartelera y Partidos":
    st.header("Cartelera de Partidos - Análisis Profundo (" + fecha_hoy + ")")
    if df_cartelera.empty:
        st.warning("No hay partidos cargados actualmente en la cartelera.")
    else:
        st.write("Selecciona un encuentro para ver el desglose científico del modelo:")
        opciones_dict = {}
        for _, row in df_cartelera.iterrows():
            e1 = str(row["equipo1"]).strip()
            e2 = str(row["equipo2"]).strip()
            label = e1 + " vs. " + e2
            opciones_dict[label] = row

        partido_seleccionado = st.selectbox("Juegos de hoy:", list(opciones_dict.keys()))
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
                st.caption("(Visitante)")
            with col_VS:
                st.markdown("<h2 style='text-align: center; color: #00FF66;'>VS</h2>", unsafe_allow_html=True)
            with col_R:
                if logo2_url:
                    st.image(logo2_url, width=80)
                st.subheader(equipo2)
                st.caption("(Local)")

            hora_val = str(fila_juego.get("hora", "19:30 (VE)"))
            sede_val = str(fila_juego.get("sede", "Arena Principal"))
            st.markdown(f"🕒 **Hora (VE):** {hora_val} &nbsp;&nbsp;|&nbsp;&nbsp; 🏟️ **Sede:** {sede_val}")
            st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Ganador Proyectado", value=str(fila_juego["ganador"]))
            with col2:
                st.metric(label="Total de Puntos (O/U)", value=str(fila_juego["total_puntos"]))

            st.markdown("### Razonamiento Táctico y Métricas Avanzadas")
            analisis_amplio = str(fila_juego["analisis_es"]) if lang == "es" else str(fila_juego["analisis_en"])
            st.markdown(analisis_amplio, unsafe_allow_html=True)

            st.markdown("---")
            if st.button("📄 Descargar Análisis en PDF"):
                archivo_pdf = generar_pdf_analisis(
                    equipo1 + " vs " + equipo2, hora_val, sede_val, str(fila_juego["ganador"]), str(fila_juego["total_puntos"]), analisis_amplio.replace("<br>", "\n").replace("<b>", "")
                )
                with open(archivo_pdf, "rb") as f:
                    st.download_button("💾 Guardar archivo PDF en tu equipo", data=f, file_name="reporte_sabermetria_nba.pdf", mime="application/pdf")

elif menu == "Apuestas y Proyecciones USA (Las Vegas)":
    st.header("🇺🇸 Proyecciones y Líneas USA (Las Vegas Lines)")
    st.write("Análisis de mercado ordenado rigurosamente de mayor a menor probabilidad según nuestro modelo sabermétrico:")
    if df_apuestas.empty:
        st.info("No hay datos de apuestas cargados actualmente. Utilice el panel de administración para incorporar las líneas.")
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
                    st.metric("Confianza", f"{prob}%" if prob else "N/A")
                st.markdown(f"*{proj}*")
                st.markdown("---")

elif menu == "El Pulso de la Duela (Noticias)":
    st.header("El Pulso de la Duela - Crónicas de Élite (" + fecha_hoy + ")")
    st.markdown("---")
    mat_es, mat_en = cargar_noticias_txt()
    cronica_texto = mat_es if lang == "es" else mat_en
    st.markdown(cronica_texto)

elif menu == "La Jugada Fija del Día":
    st.header("La Jugada Estelar del Modelo")
    if df_cartelera.empty:
        st.warning("No hay partidos cargados actualmente.")
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
            st.caption("(Visitante)")
        with col_VS:
            st.markdown("<h2 style='text-align: center; color: #00FF66;'>VS</h2>", unsafe_allow_html=True)
        with col_R:
            if logo_estelar_2:
                st.image(logo_estelar_2, width=80)
            st.subheader(estelar_eq2)
            st.caption("(Local)")

        analisis_jugada = str(juego_estelar["analisis_es"]) if lang == "es" else str(juego_estelar["analisis_en"])
        st.markdown(analisis_jugada, unsafe_allow_html=True)

elif menu == "Diccionario Sabermétrico":
    st.header("Diccionario Sabermétrico Educativo (Básico a Avanzado)")
    st.write("Guía completa de referencia para comprender desde los fundamentos tradicionales hasta las métricas de eficiencia más avanzadas:")
    if lang == "es":
        st.markdown(
            "### Indicadores Básicos y Tradicionales (Box Score)\n"
            "- **PTS (Points / Puntos):** Total de puntos anotados por un jugador o equipo.\n"
            "- **REB (Rebounds / Rebotes):** Balones recuperados tras un lanzamiento fallido.\n"
            "- **AST (Assists / Asistencias):** Pases que conducen directamente a una canasta.\n\n"
            "### Indicadores Avanzados y de Profundidad (Sabermetría IA)\n"
            "- **Pace (Ritmo):** Cantidad estimada de posesiones por cada 48 minutos.\n"
            "- **True Shooting Percentage (TS%):** Eficiencia ofensiva global (dobles, triples y libres).\n"
            "- **Net Rating:** Diferencia de puntos anotados y permitidos por 100 posesiones."
        )
    else:
        st.markdown(
            "### Basic & Traditional Indicators (Box Score)\n"
            "- **PTS (Points):** Total points scored.\n"
            "- **REB (Rebounds):** Basketballs recovered.\n"
            "- **AST (Assists):** Passes leading to field goals.\n\n"
            "### Advanced Analytics (Sabermetria AI)\n"
            "- **Pace:** Estimated possessions per 48 minutes.\n"
            "- **True Shooting Percentage (TS%):** Scoring efficiency.\n"
            "- **Net Rating:** Point differential per 100 possessions."
        )

elif menu == "Panel de Administración":
    st.header("🔐 Panel de Control y Publicación - Sabermetría IA")
    st.write("Control estadístico, cartelera, apuestas y crónicas editoriales.")

    clave_admin = st.text_input("Ingresa la clave de administrador:", type="password", key="input_clave_admin")

    if clave_admin == "sabermetria2026":
        st.success("¡Acceso de administrador concedido!")

        if os.path.exists(db_usuarios_path):
            df_visitas = pd.read_csv(db_usuarios_path, encoding="utf-8")
            st.metric(label="Total de Ingresos Acumulados al Portal", value=len(df_visitas))
            st.dataframe(df_visitas, use_container_width=True)
        else:
            st.metric(label="Total de Ingresos Acumulados al Portal", value=0)

        st.markdown("---")
        st.subheader("📤 Carga Masiva de Cartelera por Archivo CSV")
        csv_ejemplo = df_cartelera.to_csv(index=False).encode("utf-8")
        st.download_button(label="📥 Descargar Plantilla CSV de Ejemplo", data=csv_ejemplo, file_name="plantilla_cartelera_ejemplo.csv", mime="text/csv")

        archivo_subido = st.file_uploader("Selecciona el archivo CSV de partidos:", type=["csv"])
        if archivo_subido is not None:
            try:
                df_nuevo_csv = pd.read_csv(archivo_subido, encoding="utf-8")
                guardar_cartelera(df_nuevo_csv)
                st.success("¡Cartelera actualizada con éxito!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        st.markdown("---")
        if st.button("🗑️ Vaciar / Borrar Toda la Cartelera"):
            if os.path.exists(cartelera_csv_path):
                os.remove(cartelera_csv_path)
            guardar_cartelera(pd.DataFrame(columns=["equipo1", "equipo2", "hora", "sede", "ganador", "total_puntos", "analisis_es", "analisis_en", "es_jugada_fija"]))
            st.success("¡Cartelera vaciada!")
            st.rerun()

        st.markdown("---")
        ayer_act = cargar_estadisticas()
        with st.form("form_estadisticas"):
            nuevo_ayer = st.text_input("Aciertos de la Jornada (Ej: 6 / 10 (60.0%)):", value=ayer_act)
            if st.form_submit_button("💾 Guardar Efectividad"):
                guardar_estadisticas(nuevo_ayer)
                st.success("¡Efectividad actualizada con transparencia!")
                st.rerun()

        mat_es_act, mat_en_act = cargar_noticias_txt()
        with st.form("form_noticias_txt"):
            txt_mat_es = st.text_area("Crónica (Español):", value=mat_es_act, height=180)
            txt_mat_en = st.text_area("Editorial (English):", value=mat_en_act, height=180)
            if st.form_submit_button("💾 Guardar y Publicar Crónica"):
                guardar_noticias_txt(txt_mat_es, txt_mat_en)
                st.success("¡Crónica publicada con éxito!")
                st.rerun()

    elif clave_admin != "":
        st.error("❌ Clave de administrador incorrecta.")
