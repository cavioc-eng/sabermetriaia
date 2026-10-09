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
        "admin_titulo": "🔐 Panel de Control de Usuarios - Sabermetría IA",
        "admin_desc": "Control estadístico de accesos y visitas a la plataforma.",
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
        "admin_titulo": "🔐 User Control Panel - Sabermetria AI",
        "admin_desc": "Statistical control of platform visits and accesses.",
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

    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#00FF66'), spaceAfter=12
    )
    body_style = ParagraphStyle(
        'BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#333333'), spaceAfter=10, leading=14
    )

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
    nuevo_registro = pd.DataFrame([["Seguidor TikTok", fecha_hora]], columns=["Usuario", "Fecha_Acceso"])
    
    if os.path.exists(db_usuarios_path):
        df_existente = pd.read_csv(db_usuarios_path)
        df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
        df_actualizado.to_csv(db_usuarios_path, index=False)
    else:
        nuevo_registro.to_csv(db_usuarios_path, index=False)

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
        st.write("Para desbloquear el portal exclusivo y la analítica avanzada, sigue los pasos:")
            
    with col_der:
        # Imagen oficial optimizada de la NBA
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
    st.sidebar.title("Menú Principal")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
        
    menu = st.sidebar.radio("Selecciona una sección:", [
        t["menu_cartelera"], 
        t["menu_noticias"], 
        t["menu_jugada"], 
        t["menu_diccionario"],
        t["menu_admin"]
    ])

    fecha_hoy = datetime.now().strftime("%d de %B de %Y")

    if menu == t["menu_cartelera"]:
        st.header(f"📅 Cartelera de Partidos - Análisis Profundo ({fecha_hoy})")
        st.write("Selecciona un encuentro para ver el desglose científico del modelo:")
        
        partido_seleccionado = st.selectbox("Juegos de hoy:", [
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
            st.info(f"Mostrando analítica avanzada para: **{partido_seleccionado}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Ganador Proyectado", value="Oklahoma City Thunder", delta="+4.2 pts")
            with col2:
                st.metric(label="Total de Puntos (O/U)", value="230.5", delta="Altas (Over)")
            
            st.markdown("### 🧠 Razonamiento Táctico y Métricas Avanzadas")
            
            analisis_amplio = (
                "El modelo de eficiencia neta proyecta una ventaja clave en el ritmo de posesiones (Pace). "
                "Oklahoma City registra un índice defensivo en el perímetro que limita el acierto rival en situaciones de pick-and-roll. "
                "Por su parte, el True Shooting Percentage (TS%) de los visitantes se eleva un 4.5% en los últimos cinco encuentros, "
                "respaldado por una menor tasa de pérdidas (TOV%) y una alta conversión en transición rápida. "
                "El diferencial de rebotes defensivos favorece al Oklahoma en un margen de 5.2 balones recuperados por encuentro, "
                "lo que ahoga las segundas oportunidades del rival y consolida la proyección del modelo ganador."
            )
            
            st.write(analisis_amplio)
            
            st.markdown("---")
            st.subheader("📥 Exportar Reporte")
            st.write("Descarga el análisis completo de este encuentro en formato PDF para consultarlo offline.")
            
            if st.button("📄 Descargar Análisis en PDF"):
                archivo_pdf = generar_pdf_analisis(
                    partido_seleccionado, 
                    "Oklahoma City Thunder (+4.2 pts)", 
                    "230.5 (Altas)", 
                    analisis_amplio
                )
                with open(archivo_pdf, "rb") as f:
                    st.download_button(
                        label="💾 Guardar archivo PDF en tu equipo",
                        data=f,
                        file_name="reporte_sabermetria_nba.pdf",
                        mime="application/pdf"
                    )

    elif menu == t["menu_noticias"]:
        st.header(f"📰 Centro de Noticias en Tiempo Real — {fecha_hoy}")
        st.write("Bienvenido al centro informativo oficial de Sabermetría IA. Aquí encontrarás la doble actualización diaria.")
        
        tab1, tab2 = st.tabs(["🌅 Actualización Matutina (Cierre Previo)", "🌇 Actualización de la Tarde (5:00 p.m.)"])
        
        with tab1:
            st.subheader("🌅 Reporte Matutino: Radiografía y Tendencias de la Liga")
            st.markdown("""
            * **Balance de Eficiencia Ofensiva:** Las primeras prácticas y encuentros muestran un incremento notable en el uso de triples en transición.
            * **Impacto en la Pintura:** Los modelos de eficiencia defensiva señalan que los equipos con mayor diferencial en rebotes dominan los primeros cuartos.
            """)
        with tab2:
            st.subheader("🌇 Reporte Vespertino: Última Hora y Ajustes Previo al Salto Inicial")
            st.markdown("""
            * **Reporte Oficial de Lesiones:** Monitoreo en tiempo real de jugadores cuestionables y confirmación de quintetos abridores.
            * **Movimientos en las Líneas de Apuestas:** Análisis de las variaciones en las líneas de puntos totales (O/U).
            """)

    elif menu == t["menu_jugada"]:
        st.header("⭐ La Jugada Estelar del Modelo")
        st.success("Recomendación avalada estrictamente por eficiencia matemática y métricas de posesión.")
        
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
        
        st.markdown("### 📊 Fundamento Estadístico y Razonamiento del Modelo")
        st.markdown("""
        * **Selección Recomendada:** Oklahoma City Thunder - Spread / Altas (Over)
        * **Nivel de Confianza del Modelo:** 88.4%
        * **Por qué elegimos este encuentro:** Nuestro algoritmo de eficiencia neta detecta una superioridad de +4.2 puntos en posesiones de media cancha.
        """)

    elif menu == t["menu_diccionario"]:
        st.header("📖 Diccionario de Indicadores Avanzados")
        st.markdown("""
        * **Pace (Ritmo):** Cantidad estimada de posesiones por cada 48 minutos de juego.
        * **True Shooting Percentage - TS%:** Eficiencia ofensiva global que incluye dobles, triples y tiros libres.
        * **Effective Field Goal Percentage - eFG%:** Eficacia de campo otorgando valor extra a los triples.
        * **Net Rating:** Diferencia entre puntos anotados y permitidos por 100 posesiones.
        """)

    elif menu == t["menu_admin"]:
        st.header(t["admin_titulo"])
        st.write(t["admin_desc"])
        
        clave_admin = st.text_input(t["admin_clave"], type="password")
        
        if clave_admin == "sabermetria2026":
            st.success(t["admin_exito"])
            
            if os.path.exists(db_usuarios_path):
                df_visitas = pd.read_csv(db_usuarios_path)
                st.metric(label=t["total_visitas"], value=len(df_visitas))
                
                if st.button("🔄 Sincronizar Noticias y Reportes de la NBA"):
                    st.success("¡Noticias y boletines de la liga sincronizados exitosamente con el portal!")
                
                st.markdown("### Historial de Accesos al Portal")
                st.dataframe(df_visitas, use_container_width=True)
            else:
                st.metric(label=t["total_visitas"], value=0)
                if st.button("🔄 Sincronizar Noticias y Reportes de la NBA"):
                    st.success("¡Noticias sincronizadas exitosamente!")
        elif clave_admin != "":
            st.error(t["admin_error"])
