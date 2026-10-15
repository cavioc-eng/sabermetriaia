import os
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo.jpeg")
db_usuarios_path = os.path.join(current_dir, "registros_tiktok.csv")
estadisticas_path = os.path.join(current_dir, "historial_aciertos.csv")
noticias_txt_path = os.path.join(current_dir, "noticias.txt")
cartelera_csv_path = os.path.join(current_dir, "cartelera_juegos.csv")

st.set_page_config(
    page_title="Sabermetría IA - Analítica Avanzada de Básquetbol",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def cargar_noticias_txt():
    default_mat_es = "• Radiografía de Eficiencia Ofensiva y eFG%: Los Celtics impulsaron su eFG% con excelente spacing perimetral.\n\n• Impacto del Net Rating: Los diferenciales de eficiencia neta marcaron el ritmo en los cierres ajustados."
    default_vesp_es = "• Reporte Crítico de Lesiones: Monitoreo estricto en las rotaciones perimetrales de Dallas y Phoenix.\n\n• Efecto en el Pace: Gestión rigurosa de la carga física en la pretemporada."
    default_mat_en = "• Offensive Efficiency & eFG%: Boston Celtics fueled perimeter spacing and high-value shot selection.\n\n• Net Rating Impact: Advanced net rating metrics drove game dynamics."
    default_vesp_en = "• Critical Injury Reports: Active backcourt roster monitoring for tonight's matchups.\n\n• Pace Adjustments: Workload management controlling possession velocity."
    
    if os.path.exists(noticias_txt_path):
        try:
            with open(noticias_txt_path, "r", encoding="utf-8") as f:
                lines = f.read().split("---SEPARADOR_NOTICIAS---")
                if len(lines) == 4:
                    return lines[0].strip(), lines[1].strip(), lines[2].strip(), lines[3].strip()
        except Exception:
            pass
    return default_mat_es, default_vesp_es, default_mat_en, default_vesp_en

def guardar_noticias_txt(mat_es, vesp_es, mat_en, vesp_en):
    try:
        with open(noticias_txt_path, "w", encoding="utf-8") as f:
            f.write(mat_es + "\n---SEPARADOR_NOTICIAS---\n" + vesp_es + "\n---SEPARADOR_NOTICIAS---\n" + mat_en + "\n---SEPARADOR_NOTICIAS---\n" + vesp_en)
    except Exception:
        pass

TEXTOS = {
    "es": {
        "titulo_app": "SABERMETRÍA IA",
        "sub_app": "Analítica Avanzada de Básquetbol",
        "paso1_titulo": "Paso 1: Síguenos en TikTok",
        "paso1_desc": "Abre nuestro perfil oficial @sabermetriaia y presiona el botón de Seguir:",
        "btn_tiktok": "📲 Ir a @sabermetriaia",
        "paso2_titulo": "Paso 2: Acceso Directo",
        "paso2_desc": "Haz clic en el botón para entrar al portal exclusivo:",
        "btn_acceso": "🏀 Entrar al Portal Exclusivo",
        "admin_titulo": "🔐 Panel de Control y Publicación - Sabermetría IA",
        "admin_desc": "Control estadístico de visitas, cartelera masiva por CSV y noticias.",
        "admin_clave": "Ingresa la clave de administrador:",
        "admin_exito": "¡Acceso de administrador concedido!",
        "admin_error": "❌ Clave de administrador incorrecta.",
        "total_visitas": "Total de Accesos al Portal"
    },
    "en": {
        "titulo_app": "SABERMETRIA AI",
        "sub_app": "Advanced Basketball Analytics",
        "paso1_titulo": "Step 1: Follow us on TikTok",
        "paso1_desc": "Open our official profile @sabermetriaia and hit Follow:",
        "btn_tiktok": "📲 Go to @sabermetriaia",
        "paso2_titulo": "Step 2: Direct Access",
        "paso2_desc": "Click the button to enter the exclusive portal:",
        "btn_acceso": "🏀 Enter Exclusive Portal",
        "admin_titulo": "🔐 Control & Publishing Panel - Sabermetria AI",
        "admin_desc": "Visit statistical control, CSV slate upload and news.",
        "admin_clave": "Enter admin password:",
        "admin_exito": "Admin access granted!",
        "admin_error": "❌ Incorrect admin password.",
        "total_visitas": "Total Portal Accesses"
    }
}

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #00FF66; color: #000000; font-weight: bold; border-radius: 8px; }
    .matchup-box { display: flex; align-items: center; justify-content: space-around; text-align: center; padding: 15px; background-color: #161b22; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 20px; }
    .team-col { flex: 1; display: flex; flex-direction: column; align-items: center; }
    .vs-col { flex: 0 0 100px; font-size: 32px; font-weight: bold; color: #00FF66; text-align: center; }
    .tiktok-card { background-color: #161b22; padding: 15px 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    .stats-banner { background: linear-gradient(135deg, #161b22 0%, #1f2937 100%); border: 1px solid #00FF66; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

LOGOS_EQUIPOS = {
    "Boston Celtics": "https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg",
    "Charlotte Hornets": "https://cdn.nba.com/logos/nba/1610612766/global/L/logo.svg",
    "Miami Heat": "https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg",
    "Brooklyn Nets": "https://cdn.nba.com/logos/nba/1610612751/global/L/logo.svg",
    "Dallas Mavericks": "https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg",
    "New Orleans Pelicans": "https://cdn.nba.com/logos/nba/1610612740/global/L/logo.svg",
    "Milwaukee Bucks": "https://cdn.nba.com/logos/nba/1610612749/global/L/logo.svg",
    "Chicago Bulls": "https://cdn.nba.com/logos/nba/1610612741/global/L/logo.svg",
    "Minnesota Timberwolves": "https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg",
    "Detroit Pistons": "https://cdn.nba.com/logos/nba/1610612765/global/L/logo.svg",
    "San Antonio Spurs": "https://cdn.nba.com/logos/nba/1610612759/global/L/logo.svg",
    "Phoenix Suns": "https://cdn.nba.com/logos/nba/1610612756/global/L/logo.svg",
    "Los Angeles Clippers": "https://cdn.nba.com/logos/nba/1610612746/global/L/logo.svg",
    "Denver Nuggets": "https://cdn.nba.com/logos/nba/1610612743/global/L/logo.svg"
}

def generar_pdf_analisis(partido, hora, sede, ganador, total_puntos, razonamiento):
    pdf_path = os.path.join(current_dir, "reporte_sabermetria.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#00FF66'), spaceAfter=12)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#333333'), spaceAfter=10, leading=14)
    story.append(Paragraph("SABERMETRÍA IA - REPORTE DE ANALÍTICA AVANZADA", title_style))
    story.append(Paragraph("Encuentro: " + partido, body_style))
    story.append(Paragraph("Hora (VE): " + hora + " | Sede: " + sede, body_style))
    story.append(Paragraph("Fecha del Reporte: " + datetime.now().strftime('%d/%m/%Y'), body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Ganador Proyectado: " + ganador, body_style))
    story.append(Paragraph("Línea de Puntos Totales (O/U): " + total_puntos, body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Desglose Táctico y Métricas del Modelo:", title_style))
    story.append(Paragraph(razonamiento, body_style))
    doc.build(story)
    return pdf_path

def registrar_visita():
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nuevo_reg = pd.DataFrame([["Seguidor TikTok (Acceso Directo)", fecha_hora]], columns=["Usuario", "Fecha_Acceso"])
    if os.path.exists(db_usuarios_path):
        df_ex = pd.read_csv(db_usuarios_path)
        pd.concat([df_ex, nuevo_reg], ignore_index=True).to_csv(db_usuarios_path, index=False, encoding='utf-8')
    else:
        nuevo_reg.to_csv(db_usuarios_path, index=False, encoding='utf-8')

def cargar_estadisticas():
    if os.path.exists(estadisticas_path):
        try:
            return str(pd.read_csv(estadisticas_path, encoding='utf-8').iloc[0]["ayer"])
        except Exception:
            pass
    return "3 / 4 (75% de Aciertos)"

def guardar_estadisticas(ayer):
    pd.DataFrame([[ayer]], columns=["ayer"]).to_csv(estadisticas_path, index=False, encoding='utf-8')

def cargar_cartelera():
    analisis_celtics = (
        "🏀 Análisis Táctico y de Espaciamiento (Spacing):\n\n"
        "Los Boston Celtics llegan a este encuentro exhibiendo una estructura ofensiva fundamentada en la saturación perimetral y la creación de ventajas a partir del pick-and-pop. Con un promedio de conversión superior al 56.2% en eFG% (Effective Field Goal Percentage), el conjunto verde maximiza el valor esperado de cada posesión castigando las ayudas defensivas del rival.\n\n"
        "📊 Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):\n\n"
        "• Net Rating Proyectado: +10.4 a favor de Boston, sustentado en una eficiencia defensiva que limita al oponente a menos de 102 puntos por cada 100 posesiones.\n"
        "• Pace Estimado: 99.2 posesiones por 48 minutos, lo que favorece un ritmo dinámico e incrementa el volumen total de lanzamientos de larga distancia.\n"
        "• Turnover Percentage (TOV%): Boston mantiene una tasa de pérdida de balón controlada (inferior al 11.2%), neutralizando las transiciones defensivas de Charlotte.\n\n"
        "🎯 Conclusión del Modelo: La superioridad en la profundidad de banquillo y el dominio en la captura de rebotes ofensivos (OREB%) inclinan la balanza con solvencia hacia la línea de los Celtics."
    )

    analisis_heat = (
        "🏀 Análisis Táctico y de Espaciamiento (Spacing):\n\n"
        "El sistema de Miami opera bajo una disciplina defensiva inquebrantable, priorizando la defensa de contención en el perímetro y cerrando los espacios en la llave (paint protection). Brooklyn intentará proponer un juego abierto, pero la presión física en la primera línea de pase cortocircuitará su circulación de balón.\n\n"
        "📊 Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):\n\n"
        "• Pace Proyectado: 96.5 posesiones. Al ser un juego de posesiones más pausadas, el ritmo beneficia la tendencia a la baja (Under) en la línea de puntos totales.\n"
        "• Defensive Rating: Miami proyecta frenar la eficiencia ofensiva rival por debajo del 44% en tiros de campo globales.\n"
        "• True Shooting Percentage (TS%): La selección de tiro de Miami en la media distancia ofrece mayor estabilidad en los minutos de cierre.\n\n"
        "🎯 Conclusión del Modelo: Disciplina táctica y control absoluto del reloj de posesión otorgan la ventaja a Miami en un duelo de pocos puntos."
    )

    data_def = [
        {
            "equipo1": "Boston Celtics", "equipo2": "Charlotte Hornets", 
            "hora": "19:30 (VE)", "sede": "Spectrum Center (Charlotte, NC)", 
            "ganador": "Boston Celtics (-8.5 pts)", "total_puntos": "224.5 (Altas / Over)", 
            "analisis_es": analisis_celtics, "analisis_en": analisis_celtics, "es_jugada_fija": True
        },
        {
            "equipo1": "Miami Heat", "equipo2": "Brooklyn Nets", 
            "hora": "19:30 (VE)", "sede": "Barclays Center (Brooklyn, NY)", 
            "ganador": "Miami Heat (-4.5 pts)", "total_puntos": "218.5 (Bajas / Under)", 
            "analisis_es": analisis_heat, "analisis_en": analisis_heat, "es_jugada_fija": False
        }
    ]
    df_default = pd.DataFrame(data_def)

    if os.path.exists(cartelera_csv_path):
        try:
            df_saved = pd.read_csv(cartelera_csv_path, encoding='utf-8')
            if not df_saved.empty and "equipo1" in df_saved.columns:
                return df_saved
        except Exception:
            pass
    
    df_default.to_csv(cartelera_csv_path, index=False, encoding='utf-8')
    return df_default

def guardar_cartelera(df):
    try:
        df.to_csv(cartelera_csv_path, index=False, encoding='utf-8')
    except Exception:
        pass

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
        st.image("https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg", width=140)
    
    st.markdown("---")
    col_paso1, col_paso2 = st.columns(2)
    with col_paso1:
        st.markdown(
            '<div class="tiktok-card">'
            '<h4 style="color: #00FF66; margin-top: 0;">' + t["paso1_titulo"] + '</h4>'
            '<p style="font-size: 14px; margin-bottom: 10px;">' + t["paso1_desc"] + '</p>'
            '<a href="https://www.tiktok.com/@sabermetriaia" target="_blank" style="background-color: #00FF66; color: #000000; padding: 8px 15px; border-radius: 6px; font-weight: bold; text-decoration: none; display: inline-block;">' + t["btn_tiktok"] + '</a>'
            '</div>', unsafe_allow_html=True
        )
    with col_paso2:
        st.markdown(
            '<div class="tiktok-card">'
            '<h4 style="color: #00FF66; margin-top: 0;">' + t["paso2_titulo"] + '</h4>'
            '<p style="font-size: 14px; margin-bottom: 15px;">' + t["paso2_desc"] + '</p>'
            '</div>', unsafe_allow_html=True
        )
        if st.button(t["btn_acceso"]):
            registrar_visita()
            st.session_state.autenticado = True
            st.rerun()
else:
    st.sidebar.title("Menú Principal" if lang == "es" else "Main Menu")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=220)
        
    menu = st.sidebar.radio(
        "Selecciona una sección:" if lang == "es" else "Select a section:", 
        [
            "Cartelera y Partidos", 
            "Noticias (Doble Actualización)", 
            "La Jugada Fija del Día", 
            "Diccionario Sabermétrico",
            "🔐 Panel de Administración"
        ]
    )

    fecha_hoy = datetime.now().strftime("%d de %B de %Y")
    df_cartelera = cargar_cartelera()
    ayer_str = cargar_estadisticas()

    if lang == "es":
        st.markdown(
            '<div class="stats-banner">'
            '<h4 style="color: #00FF66; margin: 0;">🎯 Rendimiento del Modelo Sabermétrico (Evaluación de la Jornada)</h4>'
            '<p style="font-size: 15px; margin: 5px 0 0 0;">Aciertos del Modelo: <b>' + ayer_str + '</b></p>'
            '</div>', unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="stats-banner">'
            '<h4 style="color: #00FF66; margin: 0;">🎯 Sabermetric Model Performance (Slate Evaluation)</h4>'
            '<p style="font-size: 15px; margin: 5px 0 0 0;">Model Hits: <b>' + ayer_str + '</b></p>'
            '</div>', unsafe_allow_html=True
        )

    if menu == "Cartelera y Partidos":
        st.header("📅 Cartelera de Partidos - Análisis Profundo ("
