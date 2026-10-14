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
cartelera_path = os.path.join(current_dir, "cartelera_bilingue.csv")
estadisticas_path = os.path.join(current_dir, "historial_aciertos.csv")
noticias_txt_path = os.path.join(current_dir, "noticias.txt")

st.set_page_config(
    page_title="Sabermetría IA - Analítica Avanzada de Básquetbol",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def cargar_noticias_txt():
    default_noticias = {
        "mat_es": "• **Radiografía de Eficiencia Ofensiva y eFG%:** Los Celtics impulsaron su eFG% con excelente spacing perimetral.\n\n• **Impacto del Net Rating:** Los diferenciales de eficiencia neta marcaron el ritmo en los cierres ajustados.",
        "vesp_es": "• **Reporte Crítico de Lesiones:** Monitoreo estricto en las rotaciones perimetrales de Dallas y Phoenix.\n\n• **Efecto en el Pace:** Gestión rigurosa de la carga física en la pretemporada.",
        "mat_en": "• **Offensive Efficiency & eFG%:** Boston Celtics fueled perimeter spacing and high-value shot selection.\n\n• **Net Rating Impact:** Advanced net rating metrics drove game dynamics.",
        "vesp_en": "• **Critical Injury Reports:** Active backcourt roster monitoring for tonight's matchups.\n\n• **Pace Adjustments:** Workload management controlling possession velocity."
    }
    
    if os.path.exists(noticias_txt_path):
        try:
            with open(noticias_txt_path, "r", encoding="utf-8") as f:
                lines = f.read().split("---SEPARADOR_NOTICIAS---")
                if len(lines) == 4:
                    return lines[0].strip(), lines[1].strip(), lines[2].strip(), lines[3].strip()
        except Exception:
            pass
    
    guardar_noticias_txt(default_noticias["mat_es"], default_noticias["vesp_es"], default_noticias["mat_en"], default_noticias["vesp_en"])
    return default_noticias["mat_es"], default_noticias["vesp_es"], default_noticias["mat_en"], default_noticias["vesp_en"]

def guardar_noticias_txt(mat_es, vesp_es, mat_en, vesp_en):
    try:
        with open(noticias_txt_path, "w", encoding="utf-8") as f:
            f.write(f"{mat_es}\n---SEPARADOR_NOTICIAS---\n{vesp_es}\n---SEPARADOR_NOTICIAS---\n{mat_en}\n---SEPARADOR_NOTICIAS---\n{vesp_en}")
    except Exception:
        pass

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
        "admin_titulo": "🔐 Panel de Control y Publicación - Sabermetría IA",
        "admin_desc": "Control estadístico de visitas, cartelera bilingüe y noticias.",
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
        "admin_titulo": "🔐 Control & Publishing Panel - Sabermetria AI",
        "admin_desc": "Visit statistical control, bilingual schedule, and news.",
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
    "Golden State Warriors": "https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg",
    "New York Knicks": "https://cdn.nba.com/logos/nba/1610612752/global/L/logo.svg",
    "Toronto Raptors": "https://cdn.nba.com/logos/nba/1610612761/global/L/logo.svg",
    "Indiana Pacers": "https://cdn.nba.com/logos/nba/1610612754/global/L/logo.svg",
    "Sacramento Kings": "https://cdn.nba.com/logos/nba/1610612758/global/L/logo.svg",
    "Portland Trail Blazers": "https://cdn.nba.com/logos/nba/1610612757/global/L/logo.svg",
    "Boston Celtics": "https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg",
    "Miami Heat": "https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg",
    "Brooklyn Nets": "https://cdn.nba.com/logos/nba/1610612751/global/L/logo.svg",
    "New Orleans Pelicans": "https://cdn.nba.com/logos/nba/1610612740/global/L/logo.svg",
    "Minnesota Timberwolves": "https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg",
    "Detroit Pistons": "https://cdn.nba.com/logos/nba/1610612765/global/L/logo.svg",
    "San Antonio Spurs": "https://cdn.nba.com/logos/nba/1610612759/global/L/logo.svg",
    "Phoenix Suns": "https://cdn.nba.com/logos/nba/1610612756/global/L/logo.svg",
    "Los Angeles Clippers": "https://cdn.nba.com/logos/nba/1610612746/global/L/logo.svg"
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
    data_def = [
        {
            "equipo1": "Boston Celtics", "equipo2": "Charlotte Hornets", 
            "hora": "19:30 (VE)", "sede": "Spectrum Center (Charlotte, NC)", 
            "ganador": "Boston Celtics (-8.5 pts)", "total_puntos": "224.5 (Altas / Over)", 
            "analisis_es": """
            🏀 **Análisis Táctico y de Espaciamiento (Spacing):**<br>
            Los Boston Celtics llegan a este encuentro exhibiendo una estructura ofensiva fundamentada en la saturación perimetral y la creación de ventajas a partir del <i>pick-and-pop</i>. Con un promedio de conversión superior al 56.2% en eFG% (Effective Field Goal Percentage), el conjunto verde maximiza el valor esperado de cada posesión castigando las ayudas defensivas del rival.<br><br>
            
            📊 **Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):**<br>
            • **Net Rating Proyectado:** +10.4 a favor de Boston, sustentado en una eficiencia defensiva que limita al oponente a menos de 102 puntos por cada 100 posesiones.<br>
            • **Pace Estimado:** 99.2 posesiones por 48 minutos, lo que favorece un ritmo dinámico e incrementa el volumen total de lanzamientos de larga distancia.<br>
            • **Turnover Percentage (TOV%):** Boston mantiene una tasa de pérdida de balón controlada (inferior al 11.2%), neutralizando las transiciones defensivas de Charlotte.<br><br>
            
            🎯 **Conclusión del Modelo:** La superioridad en la profundidad de banquillo y el dominio en la captura de rebotes ofensivos (OREB%) inclinan la balanza con solvencia hacia la línea de los Celtics.
            """,
            "analisis_en": "Advanced tactical breakdown for Boston Celtics vs Charlotte Hornets...", 
            "es_jugada_fija": True
        },
        {
            "equipo1": "Miami Heat", "equipo2": "Brooklyn Nets", 
            "hora": "19:30 (VE)", "sede": "Barclays Center (Brooklyn, NY)", 
            "ganador": "Miami Heat (-4.5 pts)", "total_puntos": "218.5 (Bajas / Under)", 
            "analisis_es": """
            🏀 **Análisis Táctico y de Espaciamiento (Spacing):**<br>
            El sistema de Miami opera bajo una disciplina defensiva inquebrantable, priorizando la defensa de contención en el perímetro y cerrando los espacios en la llave (paint protection). Brooklyn intentará proponer un juego abierto, pero la presión física en la primera línea de pase cortocircuitará su circulación de balón.<br><br>
            
            📊 **Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):**<br>
            • **Pace Proyectado:** 96.5 posesiones. Al ser un juego de posesiones más pausadas, el ritmo beneficia la tendencia a la baja (Under) en la línea de puntos totales.<br>
            • **Defensive Rating:** Miami proyecta frenar la eficiencia ofensiva rival por debajo del 44% en tiros de campo globales.<br>
            • **True Shooting Percentage (TS%):** La selección de tiro de Miami en la media distancia ofrece mayor estabilidad en los minutos de cierre.<br><br>
            
            🎯 **Conclusión del Modelo:** Disciplina táctica y control absoluto del reloj de posesión otorgan la ventaja a Miami en un duelo de pocos puntos.
            """,
            "analisis_en": "Advanced tactical breakdown for Miami Heat vs Brooklyn Nets...", 
            "es_jugada_fija": False
        },
        {
            "equipo1": "Dallas Mavericks", "equipo2": "New Orleans Pelicans", 
            "hora": "20:00 (VE)", "sede": "Smoothie King Center (New Orleans, LA)", 
            "ganador": "Dallas Mavericks (-3.0 pts)", "total_puntos": "230.5 (Altas / Over)", 
            "analisis_es": """
            🏀 **Análisis Táctico y de Espaciamiento (Spacing):**<br>
            Encuentro caracterizado por un alto volumen de transiciones ofensivas y situaciones de bloqueo directo (pick-and-roll). Dallas explota de manera quirúrgica las debilidades en el cambio de marca defensivo del rival, generando tiros abiertos desde las esquinas.<br><br>
            
            📊 **Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):**<br>
            • **True Shooting Percentage (TS%):** Proyectado en un formidable 59.8% para los Mavericks, reflejando gran eficacia combinando tiros libres, dobles y triples.<br>
            • **Usage Rate (USG%):** Alta concentración de jugadas culminadas por los creadores de juego principales, elevando el potencial de anotación colectiva.<br>
            • **Pace Estimado:** 101.4 posesiones, apuntando directamente a superar la línea de altas (Over).<br><br>
            
            🎯 **Conclusión del Modelo:** La capacidad anotadora exterior de Dallas y la velocidad en transición garantizan un partido de alto voltaje ofensivo.
            """,
            "analisis_en": "Advanced tactical breakdown for Dallas vs New Orleans...", 
            "es_jugada_fija": False
        },
        {
            "equipo1": "Milwaukee Bucks", "equipo2": "Chicago Bulls", 
            "hora": "20:00 (VE)", "sede": "United Center (Chicago, IL)", 
            "ganador": "Milwaukee Bucks (-6.0 pts)", "total_puntos": "226.0 (Altas / Over)", 
            "analisis_es": """
            🏀 **Análisis Táctico y de Espaciamiento (Spacing):**<br>
            Milwaukee impone condiciones a través de su dominio físico en la pintura y la gravedad ofensiva que atrae su juego interior, abriendo espacios ideales para los tiradores exteriores. Chicago sufrirá para contener el rebote en ambos costados de la duela.<br><br>
            
            📊 **Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):**<br>
            • **Rebounding Percentage (OREB/DREB):** Clara ventaja para los Bucks, asegurando segundas oportunidades de anotación.<br>
            • **Offensive Rating:** Proyectado en 116.8 puntos por 100 posesiones, aprovechando las flaquezas de la estructura defensiva de los Bulls.<br><br>
            
            🎯 **Conclusión del Modelo:** La jerarquía en la pintura y el control del ritmo ofensivo inclinan el pronóstico claramente hacia Milwaukee.
            """,
            "analisis_en": "Advanced tactical breakdown for Milwaukee vs Chicago...", 
            "es_jugada_fija": False
        },
        {
            "equipo1": "Minnesota Timberwolves", "equipo2": "Detroit Pistons", 
            "hora": "20:00 (VE)", "sede": "Little Caesars Arena (Detroit, MI)", 
            "ganador": "Minnesota Timberwolves (-7.5 pts)", "total_puntos": "215.0 (Bajas / Under)", 
            "anal
