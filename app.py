import streamlit as st
import os
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Obtener ruta absoluta del directorio
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo.jpeg")
db_usuarios_path = os.path.join(current_dir, "registros_tiktok.csv")
noticias_path = os.path.join(current_dir, "noticias_bilingue_v2.csv")

# Configuración de la página
st.set_page_config(
    page_title="Sabermetría IA - Analítica Avanzada de Básquetbol",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Diccionario de Idiomas (Español / Inglés)
TEXTOS = {
    "es": {
        "titulo_app": "SABERMETRÍA IA",
        "sub_app": "Analítica Avanzada de Básquetbol",
        "paso1_titulo": "Paso 1: Síguenos en TikTok",
        "paso1_desc": "Abre nuestro perfil oficial <b>@sabermetriaia</b> y presiona el botón de Seguir:",
        "btn_tiktok": "📲 Ir a @sabermetriaia",
        "paso2_titulo": "Paso 2: Acceso Directo",
        "paso2_desc": "Haz clic en el botón para entrar al portal exclusivo:",
        "btn_acceso": "🏀 Entrar al Portal Exclusivo",
        "menu_cartelera": "Cartelera y Partidos",
        "menu_noticias": "Noticias (Doble Actualización)",
        "menu_jugada": "La Jugada Fija del Día",
        "menu_diccionario": "Diccionario Sabermétrico",
        "menu_admin": "🔐 Panel de Administración",
        "admin_titulo": "🔐 Panel de Control y Publicación - Sabermetría IA",
        "admin_desc": "Control estadístico de visitas y editor de noticias bilingüe.",
        "admin_clave": "Ingresa la clave de administrador:",
        "admin_exito": "¡Acceso de administrador concedido!",
        "admin_error": "❌ Clave de administrador incorrecta.",
        "total_visitas": "Total de Accesos al Portal"
    },
    "en": {
        "titulo_app": "SABERMETRIA AI",
        "sub_app": "Advanced Basketball Analytics",
        "paso1_titulo": "Step 1: Follow us on TikTok",
        "paso1_desc": "Open our official profile <b>@sabermetriaia</b> and hit Follow:",
        "btn_tiktok": "📲 Go to @sabermetriaia",
        "paso2_titulo": "Step 2: Direct Access",
        "paso2_desc": "Click the button to enter the exclusive portal:",
        "btn_acceso": "🏀 Enter Exclusive Portal",
        "menu_cartelera": "Schedule & Games",
        "menu_noticias": "News (Double Update)",
        "menu_jugada": "Play of the Day",
        "menu_diccionario": "Sabermetric Dictionary",
        "menu_admin": "🔐 Admin Panel",
        "admin_titulo": "🔐 Control & Publishing Panel - Sabermetria AI",
        "admin_desc": "Visit statistical control and bilingual news editor.",
        "admin_clave": "Enter admin password:",
        "admin_exito": "Admin access granted!",
        "admin_error": "❌ Incorrect admin password.",
        "total_visitas": "Total Portal Accesses"
    }
}

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #00FF66;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
    }
    .matchup-box {
        display: flex;
        align-items: center;
        justify-content: space-around;
        text-align: center;
        padding: 15px;
        background-color: #161b22;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    .team-col {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .vs-col {
        flex: 0 0 100px;
        font-size: 32px;
        font-weight: bold;
        color: #00FF66;
        text-align: center;
    }
    .tiktok-card {
        background-color: #161b22;
        padding: 15px 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

LOGOS_EQUIPOS = {
    "Dallas Mavericks": "https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg",
    "Oklahoma City Thunder": "https://cdn.nba.com/logos/nba/1610612760/global/L/logo.svg",
    "Philadelphia 76ers": "https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg",
    "Cleveland Cavaliers": "https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
    "Minnesota Timberwolves": "https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg",
    "Memphis Grizzlies": "https://cdn.nba.com/logos/nba/1610612763/global/L/logo.svg"
}

def generar_pdf_analisis(partido, ganador, total_puntos, razonamiento):
    pdf_path = os.path.join(current_dir, "reporte_sabermetria.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#00FF66'), spaceAfter=12)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#333333'), spaceAfter=10, leading=14)

    story.append(Paragraph("SABERMETRÍA IA - REPORTE DE ANALÍTICA AVANZADA", title_style))
    story.append(Paragraph(f"<b>Encuentro:</b> {partido}", body_style))
    story.append(Paragraph(f"<b>Fecha del Reporte:</b> {datetime.now().strftime('%d/%m/%Y')}", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Ganador Proyectado:</b> {ganador}", body_style))
    story.append(Paragraph(f"<b>Línea de Puntos Totales (O/U):</b> {total_puntos}", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Desglose Táctico y Métricas del Modelo:</b>", title_style))
    story.append(Paragraph(razonamiento, body_style))

    doc.build(story)
    return pdf_path

def registrar_visita():
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nuevo_registro = pd.DataFrame([["Seguidor TikTok (Acceso Directo)", fecha_hora]], columns=["Usuario", "Fecha_Acceso"])
    
    if os.path.exists(db_usuarios_path):
        df_existente = pd.read_csv(db_usuarios_path)
        df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
        df_actualizado.to_csv(db_usuarios_path, index=False)
    else:
        nuevo_registro.to_csv(db_usuarios_path, index=False)

def cargar_noticias():
    if os.path.exists(noticias_path):
        try:
            df = pd.read_csv(noticias_path)
            return (
                str(df.iloc[0]["matutina_es"]), 
                str(df.iloc[0]["vespertina_es"]),
                str(df.iloc[0]["matutina_en"]),
                str(df.iloc[0]["vespertina_en"])
            )
        except Exception:
            pass
    
    # Valores por defecto si no existe o hay error
    def_mat_es = "• **Balance de Eficiencia Ofensiva:** Las primeras prácticas muestran un incremento en triples.\n• **Impacto en la Pintura:** Equipos con mayor diferencial de rebotes dominan."
    def_vesp_es = "• **Reporte de Lesiones:** Monitoreo en tiempo real de jugadores.\n• **Líneas de Apuestas:** Análisis de puntos totales."
    def_mat_en = "• **Offensive Efficiency Balance:** Early practices show an increase in three-pointers.\n• **Paint Impact:** Teams with higher rebound differentials dominate."
    def_vesp_en = "• **Injury Report:** Real-time player monitoring.\n• **Betting Lines:** Total points analysis."
    
    guardar_noticias(def_mat_es, def_vesp_es, def_mat_en, def_vesp_en)
    return def_mat_es, def_vesp_es, def_mat_en, def_vesp_en

def guardar_noticias(mat_es, vesp_es, mat_en, vesp_en):
    df = pd.DataFrame([[mat_es, vesp_es, mat_en, vesp_en]], columns=["matutina_es", "vespertina_es", "matutina_en", "vespertina_en"])
    df.to_csv(noticias_path, index=False)

# Selector de Idioma
idioma = st.sidebar.selectbox("🌐 Idioma / Language", ["Español", "English"])
lang = "es" if idioma == "Español" else "en"
t = TEXTOS[lang]

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    col_izq, col_centro, col_der = st.columns([1.2, 1.8, 1])
    
    with col_izq:
        if os.path.exists(logo_path):
            st.image(logo_path, width=220)
            
    with col_centro:
        st.markdown("<br>", unsafe_allow_html=True)
        st.title(t["titulo_app"])
        st.subheader(t["sub_app"])
        if lang == "es":
            st.write("Para desbloquear el portal exclusivo y la analítica avanzada, sigue los pasos:")
        else:
            st.write("To unlock the exclusive portal and advanced analytics, follow the steps:")
            
    with col_der:
        st.image("https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg", width=140)
    
    st.markdown("---")
    
    col_paso1, col_paso2 = st.columns(2)
    
    with col_paso1:
        st.markdown(f"""
        <div class="tiktok-card">
            <h4 style="color: #00FF66; margin-top: 0;">{t["paso1_titulo"]}</h4>
            <p style="font-size: 14px; margin-bottom: 10px;">{t["paso1_desc"]}</p>
            <a href="https://www.tiktok.com/@sabermetriaia" target="_blank" style="background-color: #00FF66; color: #000000; padding: 8px 15px; border-radius: 6px; font-weight: bold; text-decoration: none; display: inline-block;">{t["btn_tiktok"]}</a>
        </div>
        """, unsafe_allow_html=True)
        
    with col_paso2:
        st.markdown(f"""
        <div class="tiktok-card">
            <h4 style="color: #00FF66; margin-top: 0;">{t["paso2_titulo"]}</h4>
            <p style="font-size: 14px; margin-bottom: 15px;">{t["paso2_desc"]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(t["btn_acceso"]):
            registrar_visita()
            st.session_state.autenticado = True
            st.rerun()
else:
    st.sidebar.title("Menú Principal" if lang == "es" else "Main Menu")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=220)
        
    menu = st.sidebar.radio("Selecciona una sección:" if lang == "es" else "Select a section:", [
        t["menu_cartelera"], 
        t["menu_noticias"], 
        t["menu_jugada"], 
        t["menu_diccionario"],
        t["menu_admin"]
    ])

    fecha_hoy = datetime.now().strftime("%d de %B de %Y")

    if menu == t["menu_cartelera"]:
        titulo_cartelera = "📅 Cartelera de Partidos - Análisis Profundo" if lang == "es" else "📅 Game Schedule - Deep Analysis"
        st.header(f"{titulo_cartelera} ({fecha_hoy})")
        st.write("Selecciona un encuentro para ver el desglose científico del modelo:" if lang == "es" else "Select a matchup to view the scientific breakdown:")
        
        partido_seleccionado = st.selectbox("Juegos de hoy:" if lang == "es" else "Today's Games:", [
            "Dallas Mavericks vs. Oklahoma City Thunder",
            "Philadelphia 76ers vs. Cleveland Cavaliers",
            "Minnesota Timberwolves vs. Memphis Grizzlies"
        ])
        
        if partido_seleccionado:
            equipo1, equipo2 = partido_seleccionado.split(" vs. ")
            logo1_url = LOGOS_EQUIPOS.get(equipo1, "")
            logo2_url = LOGOS_EQUIPOS.get(equipo2, "")
            
            matchup_html = f"""
            <div class="matchup-box">
                <div class="team-col">
                    <img src="{logo1_url}" width="100" style="margin-bottom: 10px;">
                    <h3 style="margin: 0; color: #ffffff;">{equipo1}</h3>
                </div>
                <div class="vs-col">VS</div>
                <div class="team-col">
                    <img src="{logo2_url}" width="100" style="margin-bottom: 10px;">
                    <h3 style="margin: 0; color: #ffffff;">{equipo2}</h3>
                </div>
            </div>
            """
            st.markdown(matchup_html, unsafe_allow_html=True)
            
            st.markdown("---")
            st.info(f"Mostrando analítica avanzada para: **{partido_seleccionado}**" if lang == "es" else f"Showing advanced analytics for: **{partido_seleccionado}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Ganador Proyectado" if lang == "es" else "Projected Winner", value="Oklahoma City Thunder", delta="+4.2 pts")
            with col2:
                st.metric(label="Total de Puntos (O/U)" if lang == "es" else "Total Points (O/U)", value="230.5", delta="Altas (Over)" if lang == "es" else "Over")
            
            st.markdown("### 🧠 Razonamiento Táctico y Métricas Avanzadas" if lang == "es" else "### 🧠 Tactical Reasoning & Advanced Metrics")
            
            if lang == "es":
                analisis_amplio = (
                    "El modelo de eficiencia neta proyecta una ventaja clave en el ritmo de posesiones (Pace). "
                    "Oklahoma City registra un índice defensivo en el perímetro que limita el acierto rival en situaciones de pick-and-roll. "
                    "Por su parte, el True Shooting Percentage (TS%) de los visitantes se eleva un 4.5% en los últimos cinco encuentros, "
                    "respaldado por una menor tasa de pérdidas (TOV%) y una alta conversión en transición rápida. "
                    "El diferencial de rebotes defensivos favorece al Oklahoma en un margen de 5.2 balones recuperados por encuentro, "
                    "lo que ahoga las segundas oportunidades del rival y consolida la proyección del modelo ganador."
                )
            else:
                analisis_amplio = (
                    "The net efficiency model projects a key advantage in possession pace. "
                    "Oklahoma City registers a perimeter defensive rating that limits opponent shooting in pick-and-roll situations. "
                    "Meanwhile, the visitors' True Shooting Percentage (TS%) rises 4.5% over the last five games, "
                    "supported by a lower turnover rate (TOV%) and high fast-break conversion. "
                    "The defensive rebound differential favors Oklahoma by a margin of 5.2 recovered balls per game, "
                    "suppressing second-chance opportunities and solidifying the winning model's projection."
                )
            
            st.write(analisis_amplio)
            
            st.markdown("---")
            st.subheader("📥 Exportar Reporte" if lang == "es" else "📥 Export Report")
            st.write("Descarga el análisis completo de este encuentro en formato PDF para consultarlo offline." if lang == "es" else "Download the complete analysis of this matchup in PDF format for offline consultation.")
            
            if st.button("📄 Descargar Análisis en PDF" if lang == "es" else "📄 Download PDF Analysis"):
                archivo_pdf = generar_pdf_analisis(
                    partido_seleccionado, 
                    "Oklahoma City Thunder (+4.2 pts)", 
                    "230.5 (Altas)", 
                    analisis_amplio
                )
                with open(archivo_pdf, "rb") as f:
                    st.download_button(
                        label="💾 Guardar archivo PDF en tu equipo" if lang == "es" else "💾 Save PDF file to your device",
                        data=f,
                        file_name="reporte_sabermetria_nba.pdf",
                        mime="application/pdf"
                    )

    elif menu == t["menu_noticias"]:
        titulo_noticias = f"📰 Centro de Noticias en Tiempo Real — {fecha_hoy}" if lang == "es" else f"📰 Real-Time News Center — {fecha_hoy}"
        st.header(titulo_noticias)
        st.write("Bienvenido al centro informativo oficial de Sabermetría IA. Aquí encontrarás la doble actualización diaria." if lang == "es" else "Welcome to Sabermetria AI's official news center. Here you will find the double daily update.")
        
        mat_es, vesp_es, mat_en, vesp_en = cargar_noticias()
        
        matutina_texto = mat_es if lang == "es" else mat_en
        vespertina_texto = vesp_es if lang == "es" else vesp_en

        tab_mat = "🌅 Actualización Matutina (Cierre Previo)" if lang == "es" else "🌅 Morning Update (Previous Close)"
        tab_vesp = "🌇 Actualización de la Tarde (5:00 p.m.)" if
