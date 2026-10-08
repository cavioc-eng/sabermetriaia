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

# Configuración de la página con estética oscura y futurista
st.set_page_config(
    page_title="Sabermetría IA - Analítica Avanzada de Básquetbol",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# URLs oficiales de los logos de la NBA
LOGOS_EQUIPOS = {
    "Dallas Mavericks": "https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg",
    "Oklahoma City Thunder": "https://cdn.nba.com/logos/nba/1610612760/global/L/logo.svg",
    "Philadelphia 76ers": "https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg",
    "Cleveland Cavaliers": "https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
    "Minnesota Timberwolves": "https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg",
    "Memphis Grizzlies": "https://cdn.nba.com/logos/nba/1610612763/global/L/logo.svg"
}

# Función corregida para generar reporte en PDF sin errores de estilo
def generar_pdf_analisis(partido, ganador, total_puntos, razonamiento):
    pdf_path = os.path.join(current_dir, "reporte_sabermetria.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#00FF66'),
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=10,
        leading=14
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

# Función para registrar el usuario de TikTok
def registrar_usuario_tiktok(usuario):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nuevo_registro = pd.DataFrame([[usuario.strip(), fecha_hora]], columns=["Usuario_TikTok", "Fecha_Acceso"])
    
    if os.path.exists(db_usuarios_path):
        df_existente = pd.read_csv(db_usuarios_path)
        # Evitar duplicados seguidos del mismo usuario en la misma sesión
        if usuario.strip() not in df_existente["Usuario_TikTok"].values:
            df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True)
            df_actualizado.to_csv(db_usuarios_path, index=False)
    else:
        nuevo_registro.to_csv(db_usuarios_path, index=False)

# 1. Control de Acceso (Social Gating y Registro)
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    
    st.title("🏀 SABERMETRÍA IA")
    st.subheader("Analítica Avanzada de Básquetbol")
    st.write("Para desbloquear el portal exclusivo, las proyecciones científicas y la jugada fija del día, sigue estos dos simples pasos:")
    
    st.markdown("""
    <div class="tiktok-card">
        <h3 style="color: #00FF66; margin-top: 0;">Paso 1: Síguenos en TikTok</h3>
        <p>Haz clic en el siguiente botón para abrir nuestro perfil oficial <b>@sabermetriaia</b> en una pestaña nueva y presiona el botón de <b>Seguir</b>:</p>
        <a href="https://www.tiktok.com/@sabermetriaia" target="_blank" style="background-color: #00FF66; color: #000000; padding: 10px 20px; border-radius: 8px; font-weight: bold; text-decoration: none; display: inline-block; margin-top: 5px;">📲 Ir a Seguir @sabermetriaia en TikTok</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Paso 2: Valida tu acceso")
    tiktok_user = st.text_input("Ingresa tu usuario de TikTok (ej. @tu_usuario)")
    
    if st.button("🔗 Verificar y Acceder al Portal"):
        if tiktok_user.strip() != "":
            registrar_usuario_tiktok(tiktok_user)
            st.session_state.autenticado = True
            st.success(f"¡Bienvenido a bordo, {tiktok_user}! Acceso concedido al sistema.")
            st.rerun()
        else:
            st.warning("⚠️ Por favor ingresa tu usuario de TikTok para continuar.")
else:
    # 2. Barra Lateral con Menú Principal
    st.sidebar.title("Menú Principal")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
        
    menu = st.sidebar.radio("Selecciona una sección:", [
        "Cartelera y Partidos", 
        "Noticias (Doble Actualización)", 
        "La Jugada Fija del Día", 
        "Diccionario Sabermétrico",
        "🔐 Panel de Administración"
    ])

    fecha_hoy = datetime.now().strftime("%d de %B de %Y")

    if menu == "Cartelera y Partidos":
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

    elif menu == "Noticias (Doble Actualización)":
        st.header(f"📰 Centro de Noticias en Tiempo Real — {fecha_hoy}")
        tab1, tab2 = st.tabs(["🌅 Actualización Matutina (Cierre Previo)", "🌇 Actualización de la Tarde (5:00 p.m.)"])
        
        with tab1:
            st.write("**Resumen de la jornada anterior:** Análisis automatizado del rendimiento global, eficiencia en la pintura y métricas clave de los compromisos cerrados en la madrugada.")
        with tab2:
            st.write("**Reporte previo al salto inicial:** Evaluación táctica de última hora, reporte oficial de lesiones de la liga y variaciones en las líneas de apuestas en tiempo real.")

    elif menu == "La Jugada Fija del Día":
        st.header("⭐ La Jugada Estelar del Modelo")
        st.success("Recomendación avalada estrictamente por eficiencia matemática y métricas de posesión.")
        st.markdown("""
        * **Selección Recomendada:** Oklahoma City Thunder - Spread / Altas
        * **Nivel de Confianza del Modelo:** 88.4%
        * **Fundamento Estadístico:** Ventaja clara en eFG% (Effective Field Goal Percentage) y menor índice de desgaste físico en back-to-back.
        """)

    elif menu == "Diccionario Sabermétrico":
        st.header("📖 Diccionario de Indicadores Avanzados")
        st.write("Guía de referencia rápida para comprender las métricas utilizadas en los modelos de análisis profundo de Sabermetría IA:")
        
        st.markdown("""
        * **Pace (Ritmo):** Mide la cantidad estimada de posesiones que un equipo disputa por cada 48 minutos de juego. Un ritmo alto indica un juego vertiginoso de transiciones rápidas; un ritmo bajo refleja control de posesión y media cancha.
        * **True Shooting Percentage - TS% (Porcentaje de Tiro Verdadero):** Una métrica de eficiencia ofensiva mucho más precisa que el porcentaje de campo tradicional, ya que toma en cuenta los tiros de dos puntos, los triples y los tiros libres.
        * **Effective Field Goal Percentage - eFG% (Porcentaje de Tiro Efectivo):** Evalúa la eficacia en los lanzamientos de campo otorgando un valor adicional del 50% a los triples encestados en comparación con los dobles.
        * **Turnover Percentage - TOV% (Tasa de Pérdidas):** Estima el porcentaje de posesiones de un equipo que terminan en pérdida de balón. Un número bajo denota orden táctico y cuidado de la posesión.
        * **Net Rating (Rating Neto):** Representa la diferencia entre los puntos anotados y los puntos permitidos por cada 100 posesiones. Es el indicador definitivo de la superioridad real de un equipo.
        * **Pick-and-Roll Efficiency:** Mide el rendimiento ofensivo y defensivo cuando se ejecuta la jugada clásica de bloqueo y continuación, clave para descifrar defensas en el perímetro.
        """)

    elif menu == "🔐 Panel de Administración":
        st.header("🔐 Panel de Control de Usuarios - Sabermetría IA")
        st.write("Visualiza el control de seguidores de TikTok que han ingresado y validado su acceso a la plataforma.")
        
        clave_admin = st.text_input("Ingresa la clave de administrador:", type="password")
        
        if clave_admin == "sabermetria2026": # Clave de acceso interna para ti
            st.success("¡Acceso de administrador concedido!")
            
            if os.path.exists(db_usuarios_path):
                df_usuarios = pd.read_csv(db_usuarios_path)
                st.metric(label="Total de Usuarios Registrados", value=len(df_usuarios))
                st.dataframe(df_usuarios, use_container_width=True)
                
                with open(db_usuarios_path, "rb") as f:
                    st.download_button(
                        label="📥 Descargar Base de Registros en CSV",
                        data=f,
                        file_name="registros_tiktok_sabermetria.csv",
                        mime="text/csv"
                    )
            else:
                st.info("Aún no hay usuarios registrados en el sistema.")
        elif clave_admin != "":
            st.error("❌ Clave de administrador incorrecta.")
