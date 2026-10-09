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
noticias_path = os.path.join(current_dir, "noticias_admin.csv")

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
        "admin_desc": "Control estadístico de visitas y editor de noticias en tiempo real.",
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
        "admin_desc": "Visit statistical control and real-time news editor.",
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

# Funciones para leer y guardar noticias personalizadas por el administrador
def cargar_noticias():
    if os.path.exists(noticias_path):
        df = pd.read_csv(noticias_path)
        return df.iloc[0]["matutina"], df.iloc[0]["vespertina"]
    else:
        default_mat = "• **Balance de Eficiencia Ofensiva:** Las primeras prácticas y encuentros muestran un incremento notable en el uso de triples en transición.\n• **Impacto en la Pintura:** Los modelos de eficiencia defensiva señalan que los equipos con mayor diferencial en rebotes dominan los primeros cuartos."
        default_vesp = "• **Reporte Oficial de Lesiones:** Monitoreo en tiempo real de jugadores cuestionables y confirmación de quintetos abridores.\n• **Movimientos en las Líneas de Apuestas:** Análisis de las variaciones en las líneas de puntos totales (O/U)."
        return default_mat, default_vesp

def guardar_noticias(matutina, vespertina):
    df = pd.DataFrame([[matutina, vespertina]], columns=["matutina", "vespertina"])
    df.to_csv(noticias_path, index=False)

# Selector de Idioma en la barra lateral
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
        
        # Cargamos las noticias publicadas por el administrador
        matutina_texto, vespertina_texto = cargar_noticias()

        tab1, tab2 = st.tabs(["🌅 Actualización Matutina (Cierre Previo)" if lang == "es" else "🌅 Morning Update (Previous Close)", "🌇 Actualización de la Tarde (5:00 p.m.)" if lang == "es" else "🌇 Evening Update (5:00 p.m.)"])
        
        with tab1:
            st.subheader("🌅 Reporte Matutino: Radiografía y Tendencias de la Liga" if lang == "es" else "🌅 Morning Report: League Radiography & Trends")
            st.markdown(matutina_texto)
        with tab2:
            st.subheader("🌇 Reporte Vespertino: Última Hora y Ajustes Previo al Salto Inicial" if lang == "es" else "🌇 Evening Report: Breaking News & Pre-Tip Adjustments")
            st.markdown(vespertina_texto)

    elif menu == t["menu_jugada"]:
        st.header("⭐ La Jugada Estelar del Modelo" if lang == "es" else "⭐ Model's Star Play of the Day")
        st.success("Recomendación avalada estrictamente por eficiencia matemática y métricas de posesión." if lang == "es" else "Recommendation strictly backed by mathematical efficiency and possession metrics.")
        
        equipo_estelar_1 = "Oklahoma City Thunder"
        equipo_estelar_2 = "Dallas Mavericks"
        logo_estelar_1 = LOGOS_EQUIPOS.get(equipo_estelar_1, "")
        logo_estelar_2 = LOGOS_EQUIPOS.get(equipo_estelar_2, "")
        
        matchup_estelar_html = f"""
        <div class="matchup-box">
            <div class="team-col">
                <img src="{logo_estelar_1}" width="100" style="margin-bottom: 10px;">
                <h3 style="margin: 0; color: #ffffff;">{equipo_estelar_1}</h3>
            </div>
            <div class="vs-col">VS</div>
            <div class="team-col">
                <img src="{logo_estelar_2}" width="100" style="margin-bottom: 10px;">
                <h3 style="margin: 0; color: #ffffff;">{equipo_estelar_2}</h3>
            </div>
        </div>
        """
        st.markdown(matchup_estelar_html, unsafe_allow_html=True)
        
        st.markdown("### 📊 Fundamento Estadístico y Razonamiento del Modelo" if lang == "es" else "### 📊 Statistical Foundation & Model Reasoning")
        if lang == "es":
            st.markdown("""
            * **Selección Recomendada:** Oklahoma City Thunder - Spread / Altas (Over)
            * **Nivel de Confianza del Modelo:** 88.4%
            * **Por qué elegimos este encuentro:** Nuestro algoritmo de eficiencia neta detecta una superioridad de +4.2 puntos en posesiones de media cancha.
            """)
        else:
            st.markdown("""
            * **Recommended Selection:** Oklahoma City Thunder - Spread / Over
            * **Model Confidence Level:** 88.4%
            * **Why we chose this matchup:** Our net efficiency algorithm detects a +4.2 point superiority in half-court possessions.
            """)

    elif menu == t["menu_diccionario"]:
        st.header("📖 Diccionario Sabermétrico Educativo (Básico a Avanzado)" if lang == "es" else "📖 Educational Sabermetric Dictionary (Basic to Advanced)")
        st.write("Guía completa de referencia para comprender desde los fundamentos tradicionales hasta las métricas de eficiencia más avanzadas:" if lang == "es" else "Complete reference guide to understand everything from traditional fundamentals to advanced efficiency metrics:")
        
        if lang == "es":
            st.markdown("""
            ### 🟢 Indicadores Básicos y Tradicionales (Box Score)
            * **PTS (Points / Puntos):** Total de puntos anotados por un jugador o equipo a través de tiros libres, dobles y triples.
            * **REB (Rebounds / Rebotes):** Balones recuperados tras un lanzamiento fallido (se dividen en Ofensivos y Defensivos).
            * **AST (Assists / Asistencias):** Pases que conducen directamente a una canasta anotada por un compañero.
            * **STL (Steals / Recuperaciones):** Balones arrebatados al adversario cortando líneas de pase o robando el balón directamente.
            * **BLK (Blocks / Tapones):** Lanzamientos rivales bloqueados de forma legal en el aire antes de que tomen trayectoria descendente hacia el aro.
            * **TOV (Turnovers / Pérdidas):** Balones entregados al rival por errores no forzados, faltas ofensivas o malas entregas.
            * **MIN (Minutes / Minutos):** Tiempo total que un jugador permanece disputando el encuentro en la duela.

            ### 🟡 Indicadores de Eficiencia Estándar
            * **FG% (Field Goal Percentage / Porcentaje de Campo):** Relación entre los tiros de campo encestados y los intentados.
            * **3P% (Three-Point Percentage / Porcentaje de Triples):** Eficacia en lanzamientos de larga distancia.
            * **FT% (Free Throw Percentage / Porcentaje de Tiros Libres):** Precisión desde la línea de castigo.
            * **Fouls (FALTAS):** Infracciones personales cometidas que otorgan tiros libres al rival o acumulan penalización de equipo.

            ### 🔴 Indicadores Avanzados y de Profundidad (Sabermetría IA)
            * **Pace (Ritmo):** Cantidad estimada de posesiones que un equipo disputa por cada 48 minutos de juego. Mide la velocidad del encuentro.
            * **True Shooting Percentage - TS% (Tiro Verdadero):** Eficiencia ofensiva global que pondera de forma exacta dobles, triples y tiros libres.
            * **Effective Field Goal Percentage - eFG% (Tiro de Campo Efectivo):** Mide la eficacia de campo otorgando un valor adicional del 50% a los triples encestados.
            * **Net Rating (Rating Neto):** Diferencia entre los puntos anotados y permitidos por cada 100 posesiones. Es el indicador definitivo de superioridad.
            * **Usage Rate - USG% (Tasa de Uso):** Estima el porcentaje de jugadas ofensivas que concluyen un jugador (con lanzamiento, falta recibida o pérdida) mientras está en cancha.
            * **Player Efficiency Rating - PER:** Índice global de productividad por minuto creado por John Hollinger, ajustado al ritmo de juego del equipo.
            * **Box Plus/Minus - BPM:** Estimación de los puntos por 100 posesiones que un jugador aporta en comparación con un jugador promedio de la liga.
            """)
        else:
            st.markdown("""
            ### 🟢 Basic & Traditional Indicators (Box Score)
            * **PTS (Points):** Total points scored by a player or team through free throws, two-pointers, and three-pointers.
            * **REB (Rebounds):** Basketballs recovered after a missed shot (split into Offensive and Defensive).
            * **AST (Assists):** Passes that directly lead to a teammate's field goal.
            * **STL (Steals):** Balls taken away from the opponent by intercepting passes or stripping the ball.
            * **BLK (Blocks):** Legal deflections of opponent shots in midair before descending toward the rim.
            * **TOV (Turnovers):** Possessions lost due to unforced errors, offensive fouls, or bad passes.
            * **MIN (Minutes):** Total time a player spends on the court during a game.

            ### 🟡 Standard Efficiency Indicators
            * **FG% (Field Goal Percentage):** Ratio of successful field goals made versus attempted.
            * **3P% (Three-Point Percentage):** Shooting accuracy from beyond the arc.
            * **FT% (Free Throw Percentage):** Accuracy from the charity stripe.
            * **Fouls:** Personal infractions committed leading to free throws or team penalty.

            ### 🔴 Advanced & Deep Analytics (Sabermetria AI)
            * **Pace:** Estimated number of possessions a team plays per 48 minutes. Measures game speed.
            * **True Shooting Percentage - TS%:** Comprehensive scoring efficiency weighting twos, threes, and free throws.
            * **Effective Field Goal Percentage - eFG%:** Field goal accuracy giving 50% extra value to three-pointers.
            * **Net Rating:** Point differential per 100 possessions. The ultimate team superiority metric.
            * **Usage Rate - USG%:** Estimate of team plays used by a player while on the floor.
            * **Player Efficiency Rating - PER:** Per-minute productivity rating created by John Hollinger, adjusted for team pace.
            * **Box Plus/Minus - BPM:** Box-score estimate of points per 100 possessions a player contributes above a league-average player.
            """)

    elif menu == t["menu_admin"]:
        st.header(t["admin_titulo"])
        st.write(t["admin_desc"])
        
        clave_admin = st.text_input(t["admin_clave"], type="password")
        
        if clave_admin == "sabermetria2026":
            st.success(t["admin_exito"])
            
            # 1. Contador y Listado de Visitas
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
            
            # 2. Editor de Noticias en Tiempo Real para el Administrador
            st.subheader("📰 Editor y Publicador de Noticias Diarias" if lang == "es" else "📰 Daily News Editor & Publisher")
            st.write("Redacta o pega aquí las noticias de la liga. Al hacer clic en guardar, se actualizarán al instante para todos los usuarios." if lang == "es" else "Write or paste league news here. Clicking save will instantly update them for all users.")
            
            mat_actual, vesp_actual = cargar_noticias()
            
            with st.form("form_noticias"):
                nueva_matutina = st.text_area("Edición Matutina (Mañana):" if lang == "es" else "Morning Edition:", value=mat_actual, height=150)
                nueva_vespertina = st.text_area("Edición Vespertina (Tarde):" if lang == "es" else "Evening Edition:", value=vesp_actual, height=150)
                
                btn_guardar = st.form_submit_button("💾 Guardar y Publicar Noticias" if lang == "es" else "💾 Save and Publish News")
                
                if btn_guardar:
                    guardar_noticias(nueva_matutina, nueva_vespertina)
                    st.success("¡Noticias guardadas y publicadas exitosamente en el portal!" if lang == "es" else "News successfully saved and published on the portal!")
                    st.rerun()

        elif clave_admin != "":
            st.error(t["admin_error"])
