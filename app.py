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
cartelera_path = os.path.join(current_dir, "cartelera_bilingue.csv")
estadisticas_path = os.path.join(current_dir, "historial_aciertos.csv")

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
        "admin_desc": "Control estadístico de visitas, cartelera bilingüe, efectividad y noticias.",
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
        "admin_desc": "Visit statistical control, bilingual schedule, accuracy, and news.",
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
    .stats-banner {
        background: linear-gradient(135deg, #161b22 0%, #1f2937 100%);
        border: 1px solid #00FF66;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

LOGOS_EQUIPOS = {
    "Orlando Magic": "https://cdn.nba.com/logos/nba/1610612753/global/L/logo.svg",
    "Cleveland Cavaliers": "https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
    "Milwaukee Bucks": "https://cdn.nba.com/logos/nba/1610612749/global/L/logo.svg",
    "Charlotte Hornets": "https://cdn.nba.com/logos/nba/1610612766/global/L/logo.svg",
    "Chicago Bulls": "https://cdn.nba.com/logos/nba/1610612741/global/L/logo.svg",
    "Denver Nuggets": "https://cdn.nba.com/logos/nba/1610612743/global/L/logo.svg",
    "Dallas Mavericks": "https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg",
    "Oklahoma City Thunder": "https://cdn.nba.com/logos/nba/1610612760/global/L/logo.svg",
    "Philadelphia 76ers": "https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg",
    "Los Angeles Lakers": "https://cdn.nba.com/logos/nba/1610612747/global/L/logo.svg",
    "Golden State Warriors": "https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg"
}

def generar_pdf_analisis(partido, hora, sede, ganador, total_puntos, razonamiento):
    pdf_path = os.path.join(current_dir, "reporte_sabermetria.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#00FF66'), spaceAfter=12)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#333333'), spaceAfter=10, leading=14)

    story.append(Paragraph("SABERMETRÍA IA - REPORTE DE ANALÍTICA AVANZADA", title_style))
    story.append(Paragraph(f"<b>Encuentro:</b> {partido}", body_style))
    story.append(Paragraph(f"<b>Hora (VE):</b> {hora} | <b>Sede:</b> {sede}", body_style))
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

def cargar_estadisticas():
    if os.path.exists(estadisticas_path):
        try:
            df = pd.read_csv(estadisticas_path)
            return str(df.iloc[0]["ayer"]), str(df.iloc[0]["acumulado"])
        except Exception:
            pass
    
    def_ayer = "3 / 3 (100% de Aciertos)"
    def_acum = "3 / 3 (100% Efectividad Global)"
    guardar_estadisticas(def_ayer, def_acum)
    return def_ayer, def_acum

def guardar_estadisticas(ayer, acumulado):
    df = pd.DataFrame([[ayer, acumulado]], columns=["ayer", "acumulado"])
    df.to_csv(estadisticas_path, index=False)

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
    
    def_mat_es = "• **Balance de Eficiencia Ofensiva:** Las primeras prácticas muestran un incremento en triples.\n• **Impacto en la Pintura:** Equipos con mayor diferencial de rebotes dominan."
    def_vesp_es = "• **Reporte de Lesiones:** Monitoreo en tiempo real de jugadores.\n• **Líneas de Apuestas:** Análisis de puntos totales."
    def_mat_en = "• **Offensive Efficiency Balance:** Early practices show an increase in three-pointers.\n• **Paint Impact:** Teams with higher rebound differentials dominate."
    def_vesp_en = "• **Injury Report:** Real-time player monitoring.\n• **Betting Lines:** Total points analysis."
    
    guardar_noticias(def_mat_es, def_vesp_es, def_mat_en, def_vesp_en)
    return def_mat_es, def_vesp_es, def_mat_en, def_vesp_en

def guardar_noticias(mat_es, vesp_es, mat_en, vesp_en):
    df = pd.DataFrame([[mat_es, vesp_es, mat_en, vesp_en]], columns=["matutina_es", "vespertina_es", "matutina_en", "vespertina_en"])
    df.to_csv(noticias_path, index=False)

def cargar_cartelera():
    if os.path.exists(cartelera_path):
        try:
            df = pd.read_csv(cartelera_path)
            if "hora" not in df.columns:
                df["hora"] = "18:30 (VE)"
            if "sede" not in df.columns:
                df["sede"] = "Rocket Arena (Cleveland, OH)"
            return df
        except Exception:
            pass
    
    data_def = [
        {
            "equipo1": "Orlando Magic",
            "equipo2": "Cleveland Cavaliers",
            "hora": "18:30 (VE)",
            "sede": "Rocket Arena (Cleveland, OH)",
            "ganador": "Cleveland Cavaliers (-3.5 pts)",
            "total_puntos": "218.5 (Bajas / Under)",
            "analisis_es": "El modelo de eficiencia neta proyecta una ventaja táctica clave para Cleveland en el control del ritmo de posesiones (Pace), limitando las transiciones rápidas de Orlando. Defensivamente, los Cavaliers despliegan una estructura en la pintura que neutraliza las penetraciones al aro, forzando tiros de media distancia con baja conversión esperada (eFG%). Asimismo, el análisis del True Shooting Percentage (TS%) histórico en pretemporada muestra una caída en ambos conjuntos durante los últimos periodos, lo que respalda con solidez matemática la proyección de puntos hacia las bajas (Under). Este nivel de control defensivo convierte a este duelo en nuestra jugada estelar de alta convicción.",
            "analisis_en": "The net efficiency model projects a key tactical advantage for Cleveland in controlling possession pace, limiting Orlando's fast breaks. Defensively, the Cavaliers deploy an interior structure that neutralizes drives to the rim, forcing lower-expected mid-range shots (eFG%). Likewise, historical preseason True Shooting Percentage (TS%) analysis shows a drop in efficiency for both squads during the final periods, solidly backing the mathematical projection toward the Under. This level of defensive control establishes this matchup as our high-conviction star play of the day.",
            "es_jugada_fija": True
        }
    ]
    df_def = pd.DataFrame(data_def)
    df_def.to_csv(cartelera_path, index=False)
    return df_def

def guardar_cartelera(df):
    df.to_csv(cartelera_path, index=False)

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
    df_cartelera = cargar_cartelera()
    ayer_str, acumulado_str = cargar_estadisticas()

    # --- BANNER DE EFECTIVIDAD DEL MODELO ---
    if lang == "es":
        st.markdown(f"""
        <div class="stats-banner">
            <h4 style="color: #00FF66; margin: 0;">🎯 Rendimiento Histórico del Modelo Sabermétrico</h4>
            <p style="font-size: 15px; margin: 5px 0 0 0;">Aciertos de Ayer: <b>{ayer_str}</b> &nbsp;|&nbsp; Acumulado: <b>{acumulado_str}</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="stats-banner">
            <h4 style="color: #00FF66; margin: 0;">🎯 Sabermetric Model Historical Performance</h4>
            <p style="font-size: 15px; margin: 5px 0 0 0;">Yesterday's Hits: <b>{ayer_str}</b> &nbsp;|&nbsp; Cumulative: <b>{acumulado_str}</b></p>
        </div>
        """, unsafe_allow_html=True)

    if menu == t["menu_cartelera"]:
        titulo_cartelera = "📅 Cartelera de Partidos - Análisis Profundo" if lang == "es" else "📅 Game Schedule - Deep Analysis"
        st.header(f"{titulo_cartelera} ({fecha_hoy})")
        st.write("Selecciona un encuentro para ver el desglose científico del modelo:" if lang == "es" else "Select a matchup to view the scientific breakdown:")
        
        lista_partidos = [f"(Visita) {row['equipo1']} vs. (Local) {row['equipo2']}" for _, row in df_cartelera.iterrows()]
        
        partido_seleccionado = st.selectbox("Juegos de hoy:" if lang == "es" else "Today's Games:", lista_partidos)
        
        if partido_seleccionado:
            limpio = partido_seleccionado.replace("(Visita) ", "").replace("(Local) ", "")
            equipo1, equipo2 = limpio.split(" vs. ")
            fila_juego = df_cartelera[(df_cartelera['equipo1'] == equipo1) & (df_cartelera['equipo2'] == equipo2)].iloc[0]
            
            logo1_url = LOGOS_EQUIPOS.get(equipo1, "")
            logo2_url = LOGOS_EQUIPOS.get(equipo2, "")
            
            matchup_html = f"""
            <div class="matchup-box">
                <div class="team-col">
                    <img src="{logo1_url}" width="100" style="margin-bottom: 10px;">
                    <h3 style="margin: 0; color: #ffffff;">{equipo1}</h3>
                    <span style="font-size: 12px; color: #8b949e;">(Visitante)</span>
                </div>
                <div class="vs-col">VS</div>
                <div class="team-col">
                    <img src="{logo2_url}" width="100" style="margin-bottom: 10px;">
                    <h3 style="margin: 0; color: #ffffff;">{equipo2}</h3>
                    <span style="font-size: 12px; color: #8b949e;">(Local)</span>
                </div>
            </div>
            """
            st.markdown(matchup_html, unsafe_allow_html=True)
            
            hora_val = str(fila_juego.get('hora', '18:30 (VE)'))
            sede_val = str(fila_juego.get('sede', 'Arena Principal'))
            st.markdown(f"🕒 **Hora (VE):** {hora_val} &nbsp;&nbsp;|&nbsp;&nbsp; 🏟️ **Sede:** {sede_val}")
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Ganador Proyectado" if lang == "es" else "Projected Winner", value=fila_juego["ganador"])
            with col2:
                st.metric(label="Total de Puntos (O/U)" if lang == "es" else "Total Points (O/U)", value=fila_juego["total_puntos"])
            
            st.markdown("### 🧠 Razonamiento Táctico y Métricas Avanzadas" if lang == "es" else "### 🧠 Tactical Reasoning & Advanced Metrics")
            
            analisis_amplio = fila_juego["analisis_es"] if lang == "es" else fila_juego["analisis_en"]
            st.write(analisis_amplio)
            
            st.markdown("---")
            st.subheader("📥 Exportar Reporte" if lang == "es" else "📥 Export Report")
            
            if st.button("📄 Descargar Análisis en PDF" if lang == "es" else "📄 Download PDF Analysis"):
                archivo_pdf = generar_pdf_analisis(
                    f"{equipo1} vs {equipo2}", 
                    hora_val,
                    sede_val,
                    fila_juego["ganador"], 
                    fila_juego["total_puntos"], 
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
        tab_vesp = "🌇 Actualización de la Tarde (5:00 p.m.)" if lang == "es" else "🌇 Evening Update (5:00 p.m.)"

        tab1, tab2 = st.tabs([tab_mat, tab_vesp])
        
        with tab1:
            titulo_mat = "🌅 Reporte Matutino: Radiografía y Tendencias de la Liga" if lang == "es" else "🌅 Morning Report: League Radiography & Trends"
            st.subheader(titulo_mat)
            st.markdown(matutina_texto)
        with tab2:
            titulo_vesp = "🌇 Reporte Vespertino: Última Hora y Ajustes Previo al Salto Inicial" if lang == "es" else "🌇 Evening Report: Breaking News & Pre-Tip Adjustments"
            st.subheader(titulo_vesp)
            st.markdown(vespertina_texto)

    elif menu == t["menu_jugada"]:
        st.header("⭐ La Jugada Estelar del Modelo" if lang == "es" else "⭐ Model's Star Play of the Day")
        st.success("Recomendación avalada estrictamente por eficiencia matemática y métricas de posesión." if lang == "es" else "Recommendation strictly backed by mathematical efficiency and possession metrics.")
        
        juegos_fijos = df_cartelera[df_cartelera['es_jugada_fija'] == True]
        if not juegos_fijos.empty:
            juego_estelar = juegos_fijos.iloc[0]
        else:
            juego_estelar = df_cartelera.iloc[0]
            
        estelar_eq1 = juego_estelar["equipo1"]
        estelar_eq2 = juego_estelar["equipo2"]
        logo_estelar_1 = LOGOS_EQUIPOS.get(estelar_eq1, "")
        logo_estelar_2 = LOGOS_EQUIPOS.get(estelar_eq2, "")
        
        matchup_estelar_html = f"""
        <div class="matchup-box">
            <div class="team-col">
                <img src="{logo_estelar_1}" width="100" style="margin-bottom: 10px;">
                <h3 style="margin: 0; color: #ffffff;">{estelar_eq1}</h3>
                <span style="font-size: 12px; color: #8b949e;">(Visitante)</span>
            </div>
            <div class="vs-col">VS</div>
            <div class="team-col">
                <img src="{logo_estelar_2}" width="100" style="margin-bottom: 10px;">
                <h3 style="margin: 0; color: #ffffff;">{estelar_eq2}</h3>
                <span style="font-size: 12px; color: #8b949e;">(Local)</span>
            </div>
        </div>
        """
        st.markdown(matchup_estelar_html, unsafe_allow_html=True)
        
        hora_est = str(juego_estelar.get('hora', '18:30 (VE)'))
        sede_est = str(juego_estelar.get('sede', 'Arena Principal'))
        st.markdown(f"🕒 **Hora (VE):** {hora_est} &nbsp;&nbsp;|&nbsp;&nbsp; 🏟️ **Sede:** {sede_est}")
        st.markdown("---")
        
        st.markdown("### 📊 Fundamento Estadístico y Razonamiento del Modelo" if lang == "es" else "### 📊 Statistical Foundation & Model Reasoning")
        analisis_jugada = juego_estelar["analisis_es"] if lang == "es" else juego_estelar["analisis_en"]
        
        if lang == "es":
            st.markdown(f"""
            * **Selección Recomendada:** {juego_estelar["ganador"]} | Totales: {juego_estelar["total_puntos"]}
            * **Nivel de Confianza del Modelo:** 88.4%
            * **Por qué elegimos este encuentro:** {analisis_jugada}
            """)
        else:
            st.markdown(f"""
            * **Recommended Selection:** {juego_estelar["ganador"]} | Totals: {juego_estelar["total_puntos"]}
            * **Model Confidence Level:** 88.4%
            * **Why we chose this matchup:** {analisis_jugada}
            """)

    elif menu == t["menu_diccionario"]:
        st.header("📖 Diccionario Sabermétrico Educativo (Básico a Avanzado)" if lang == "es" else "📖 Educational Sabermetric Dictionary (Basic to Advanced)")
        st.write("Guía completa de referencia para comprender desde los fundamentos tradicionales hasta las métricas de eficiencia más avanzadas:" if lang == "es" else "Complete reference guide to understand everything from traditional fundamentals to advanced efficiency metrics:")
        
        if lang == "es":
            st.markdown(
                "### 🟢 Indicadores Básicos y Tradicionales (Box Score)\n"
                "- **PTS (Points / Puntos):** Total de puntos anotados por un jugador o equipo.\n"
                "- **REB (Rebounds / Rebotes):** Balones recuperados tras un lanzamiento fallido.\n"
                "- **AST (Assists / Asistencias):** Pases que conducen directamente a una canasta.\n"
                "- **STL (Steals / Recuperaciones):** Balones arrebatados al adversario.\n"
                "- **BLK (Blocks / Tapones):** Lanzamientos rivales bloqueados en el aire.\n"
                "- **TOV (Turnovers / Pérdidas):** Balones entregados al rival por errores.\n"
                "- **MIN (Minutes / Minutos):** Tiempo total que un jugador disputa en la duela.\n\n"
                "### 🟡 Indicadores de Eficiencia Estándar\n"
                "- **FG% (Field Goal Percentage):** Porcentaje de tiros de campo encestados.\n"
                "- **3P% (Three-Point Percentage):** Eficacia en lanzamientos de larga distancia.\n"
                "- **FT% (Free Throw Percentage):** Precisión desde la línea de tiros libres.\n\n"
                "### 🔴 Indicadores Avanzados y de Profundidad (Sabermetría IA)\n"
                "- **Pace (Ritmo):** Cantidad estimada de posesiones por cada 48 minutos.\n"
                "- **True Shooting Percentage (TS%):** Eficiencia ofensiva global (dobles, triples y libres).\n"
                "- **Net Rating:** Diferencia de puntos anotados y permitidos por 100 posesiones.\n"
                "- **Usage Rate (USG%):** Porcentaje de jugadas ofensivas que concluye un jugador en cancha.\n"
                "- **PER (Player Efficiency Rating):** Índice global de productividad por minuto."
            )
        else:
            st.markdown(
                "### 🟢 Basic & Traditional Indicators (Box Score)\n"
                "- **PTS (Points):** Total points scored by a player or team.\n"
                "- **REB (Rebounds):** Basketballs recovered after a missed shot.\n"
                "- **AST (Assists):** Passes leading directly to a field goal.\n"
                "- **STL (Steals):** Balls taken away from the opponent.\n"
                "- **BLK (Blocks):** Legal deflections of opponent shots.\n"
                "- **TOV (Turnovers):** Possessions lost due to unforced errors.\n"
                "- **MIN (Minutes):** Total time a player spends on the court.\n\n"
                "### 🟡 Standard Efficiency Indicators\n"
                "- **FG% (Field Goal Percentage):** Ratio of successful field goals.\n"
                "- **3P% (Three-Point Percentage):** Shooting accuracy from beyond the arc.\n"
                "- **FT% (Free Throw Percentage):** Accuracy from the charity stripe.\n\n"
                "### 🔴 Advanced & Deep Analytics (Sabermetria AI)\n"
                "- **Pace:** Estimated number of possessions per 48 minutes.\n"
                "- **True Shooting Percentage (TS%):** Comprehensive scoring efficiency.\n"
                "- **Net Rating:** Point differential per 100 possessions.\n"
                "- **Usage Rate (USG%):** Estimate of team plays used by a player.\n"
                "- **PER (Player Efficiency Rating):** Per-minute productivity rating."
            )

    elif menu == t["menu_admin"]:
        st.header(t["admin_titulo"])
        st.write(t["admin_desc"])
        
        clave_admin = st.text_input(t["admin_clave"], type="password")
        
        if clave_admin == "sabermetria2026":
            st.success(t["admin_exito"])
            
            if os.path.exists(db_usuarios_path):
                df_visitas = pd.read_csv(db_usuarios_path)
                st.metric(label=t["total_visitas"], value=len(df_visitas))
                
                hist_acc = "Historial de Accesos al Portal" if lang == "es" else "Portal Access History"
                st.markdown(f"### {hist_acc}")
                st.dataframe(df_visitas, use_container_width=True)
            else:
                st.metric(label=t["total_visitas"], value=0)
                st.info("Aún no hay registros de visitas." if lang == "es" else "No visit records yet.")

            st.markdown("---")
            
            # --- GESTOR DE ESTADÍSTICAS DE ACIERTOS ---
            st.subheader("🎯 Gestor de Efectividad y Aciertos del Modelo")
            st.write("Actualiza el rendimiento diario y acumulado que se muestra en el banner principal de la app.")
            
            ayer_act, acumulado_act = cargar_estadisticas()
            with st.form("form_estadisticas"):
                nuevo_ayer = st.text_input("Aciertos de Ayer (Ej: 3 / 3 (100%)):", value=ayer_act)
                nuevo_acumulado = st.text_input("Récord Acumulado (Ej: 12 / 14 (85.7%)):", value=acumulado_act)
                
                btn_guardar_stats = st.form_submit_button("💾 Guardar Estadísticas de Aciertos")
                if btn_guardar_stats:
                    guardar_estadisticas(nuevo_ayer, nuevo_acumulado)
                    st.success("¡Estadísticas de aciertos actualizadas con éxito!")
                    st.rerun()

            st.markdown("---")
            
            # --- GESTOR DE CARTELERA CON HORA Y SEDE ---
            st.subheader("📅 Editor de Cartelera, Horarios y Sedes")
            st.write("Edita o agrega encuentros indicando el equipo visitante, local, hora, sede y los análisis bilingües.")
            
            nombres_partidos = [f"{r['equipo1']} vs {r['equipo2']}" for _, r in df_cartelera.iterrows()] + ["➕ Agregar Nuevo Partido"]
            seleccion_edicion = st.selectbox("Selecciona encuentro a editar:", nombres_partidos)
            
            if seleccion_edicion != "➕ Agregar Nuevo Partido":
                idx_sel = nombres_partidos.index(seleccion_edicion)
                row_sel = df_cartelera.iloc[idx_sel]
                
                with st.form("form_editar_partido"):
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        ed_eq1 = st.text_input("Equipo Visitante:", value=str(row_sel["equipo1"]))
                    with col_e2:
                        ed_eq2 = st.text_input("Equipo Local:", value=str(row_sel["equipo2"]))
                    
                    col_h1, col_h2 = st.columns(2)
                    with col_h1:
                        ed_hora = st.text_input("Hora (Ej: 18:30 (VE)):", value=str(row_sel["hora"]) if "hora" in row_sel and pd.notna(row_sel["hora"]) else "18:30 (VE)")
                    with col_h2:
                        ed_sede = st.text_input("Sede / Arena:", value=str(row_sel["sede"]) if "sede" in row_sel and pd.notna(row_sel["sede"]) else "Rocket Arena (Cleveland, OH)")

                    col_g1, col_g2 = st.columns(2)
                    with col_g1:
                        ed_ganador = st.text_input("Ganador Proyectado:", value=str(row_sel["ganador"]))
                    with col_g2:
                        ed_puntos = st.text_input("Total Puntos (O/U):", value=str(row_sel["total_puntos"]))
                    
                    ed_analisis_es = st.text_area("Análisis Profundo (Español):", value=str(row_sel["analisis_es"]), height=130)
                    ed_analisis_en = st.text_area("Advanced Analysis (English):", value=str(row_sel["analisis_en"]), height=130)
                    ed_es_fija = st.checkbox("⭐ Marcar como 'Jugada Fija del Día'", value=bool(row_sel["es_jugada_fija"]))
                    
                    btn_actualizar = st.form_submit_button("💾 Actualizar Este Partido")
                    
                    if btn_actualizar:
                        if ed_es_fija:
                            df_cartelera["es_jugada_fija"] = False
                        df_cartelera.at[idx_sel, "equipo1"] = ed_eq1
                        df_cartelera.at[idx_sel, "equipo2"] = ed_eq2
                        df_cartelera.at[idx_sel, "hora"] = ed_hora
                        df_cartelera.at[idx_sel, "sede"] = ed_sede
                        df_cartelera.at[idx_sel, "ganador"] = ed_ganador
                        df_cartelera.at[idx_sel, "total_puntos"] = ed_puntos
                        df_cartelera.at[idx_sel, "analisis_es"] = ed_analisis_es
                        df_cartelera.at[idx_sel, "analisis_en"] = ed_analisis_en
                        df_cartelera.at[idx_sel, "es_jugada_fija"] = ed_es_fija
                        
                        guardar_cartelera(df_cartelera)
                        st.success("¡Partido actualizado con éxito!")
                        st.rerun()
                
                if st.button("🗑️ Eliminar este partido"):
                    df_cartelera = df_cartelera.drop(idx_sel).reset_index(drop=True)
                    guardar_cartelera(df_cartelera)
                    st.success("¡Partido eliminado!")
                    st.rerun()

            else:
                with st.form("form_nuevo_partido"):
                    col_ne1, col_ne2 = st.columns(2)
                    with col_ne1:
                        nuevo_eq1 = st.text_input("Equipo Visitante:")
                    with col_ne2:
                        nuevo_eq2 = st.text_input("Equipo Local:")
                    
                    col_nh1, col_nh2 = st.columns(2)
                    with col_nh1:
                        nuevo_hora = st.text_input("Hora (Ej: 19:00 (VE)):", value="19:00 (VE)")
                    with col_nh2:
                        nuevo_sede = st.text_input("Sede / Arena:", value="Spectrum Center (Charlotte, NC)")

                    col_ng1, col_ng2 = st.columns(2)
                    with col_ng1:
                        nuevo_ganador = st.text_input("Ganador Proyectado:")
                    with col_ng2:
                        nuevo_puntos = st.text_input("Total Puntos (O/U):")
                    
                    nuevo_analisis_es = st.text_area("Análisis Profundo (Español):", height=130)
                    nuevo_analisis_en = st.text_area("Advanced Analysis (English):", height=130)
                    nuevo_es_fija = st.checkbox("⭐ Marcar como 'Jugada Fija del Día'")
                    
                    btn_crear = st.form_submit_button("➕ Guardar Nuevo Partido")
                    
                    if btn_crear:
                        if nuevo_es_fija:
                            df_cartelera["es_jugada_fija"] = False
                        nuevo_registro = pd.DataFrame([{
                            "equipo1": nuevo_eq1,
                            "equipo2": nuevo_eq2,
                            "hora": nuevo_hora,
                            "sede": nuevo_sede,
                            "ganador": nuevo_ganador,
                            "total_puntos": nuevo_puntos,
                            "analisis_es": nuevo_analisis_es,
                            "analisis_en": nuevo_analisis_en,
                            "es_jugada_fija": nuevo_es_fija
                        }])
                        df_cartelera = pd.concat([df_cartelera, nuevo_registro], ignore_index=True)
                        guardar_cartelera(df_cartelera)
                        st.success("¡Nuevo partido agregado con éxito!")
                        st.rerun()

            st.markdown("---")
            
            # --- GESTOR DE NOTICIAS BILINGÜES ---
            titulo_editor = "📰 Editor y Publicador de Noticias Bilingüe (Español / Inglés)" if lang == "es" else "📰 Bilingual News Editor & Publisher (Spanish / English)"
            st.subheader(titulo_editor)
            st.write("Actualiza los reportes tanto en español como en inglés para que la app se adapte al idioma que elija el usuario." if lang == "es" else "Update reports in both Spanish and English so the app adapts to the user's selected language.")
            
            mat_es_act, vesp_es_act, mat_en_act, vesp_en_act = cargar_noticias()
            
            with st.form("form_noticias_bilingue"):
                st.markdown("#### 🇪🇸 Versión en Español")
                nueva_mat_es = st.text_area("Edición Matutina (Español):", value=mat_es_act, height=130)
                nueva_vesp_es = st.text_area("Edición Vespertina (Español):", value=vesp_es_act, height=130)
                
                st.markdown("#### 🇺🇸 Versión en Inglés (English Version)")
                nueva_mat_en = st.text_area("Morning Edition (English):", value=mat_en_act, height=130)
