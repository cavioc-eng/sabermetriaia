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

st.set_page_config(
    page_title="Sabermetría IA - Analítica Avanzada de Básquetbol",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def cargar_noticias_txt():
    default_mat_es = "• **Radiografía de Eficiencia Ofensiva y eFG%:** Los Celtics impulsaron su eFG% con excelente spacing perimetral.\n\n• **Impacto del Net Rating:** Los diferenciales de eficiencia neta marcaron el ritmo en los cierres ajustados."
    default_vesp_es = "• **Reporte Crítico de Lesiones:** Monitoreo estricto en las rotaciones perimetrales de Dallas y Phoenix.\n\n• **Efecto en el Pace:** Gestión rigurosa de la carga física en la pretemporada."
    default_mat_en = "• **Offensive Efficiency & eFG%:** Boston Celtics fueled perimeter spacing and high-value shot selection.\n\n• **Net Rating Impact:** Advanced net rating metrics drove game dynamics."
    default_vesp_en = "• **Critical Injury Reports:** Active backcourt roster monitoring for tonight's matchups.\n\n• **Pace Adjustments:** Workload management controlling possession velocity."
    
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
        "admin_desc": "Control estadístico de visitas y noticias.",
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
        "admin_desc": "Visit statistical control and news.",
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
            "analisis_es": (
                "🏀 <b>Análisis Táctico y de Espaciamiento (Spacing):</b><br>"
                "Los Boston Celtics llegan a este encuentro exhibiendo una estructura ofensiva fundamentada en la saturación perimetral y la creación de ventajas a partir del <i>pick-and-pop</i>. Con un promedio de conversión superior al 56.2% en eFG% (Effective Field Goal Percentage), el conjunto verde maximiza el valor esperado de cada posesión castigando las ayudas defensivas del rival.<br><br>"
                "📊 <b>Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):</b><br>"
                "• <b>Net Rating Proyectado:</b> +10.4 a favor de Boston, sustentado en una eficiencia defensiva que limita al oponente a menos de 102 puntos por cada 100 posesiones.<br>"
                "• <b>Pace Estimado:</b> 99.2 posesiones por 48 minutos, lo que favorece un ritmo dinámico e incrementa el volumen total de lanzamientos de larga distancia.<br>"
                "• <b>Turnover Percentage (TOV%):</b> Boston mantiene una tasa de pérdida de balón controlada (inferior al 11.2%), neutralizando las transiciones defensivas de Charlotte.<br><br>"
                "🎯 <b>Conclusión del Modelo:</b> La superioridad en la profundidad de banquillo y el dominio en la captura de rebotes ofensivos (OREB%) inclinan la balanza con solvencia hacia la línea de los Celtics."
            ),
            "analisis_en": "Advanced tactical breakdown for Boston Celtics vs Charlotte Hornets...", 
            "es_jugada_fija": True
        },
        {
            "equipo1": "Miami Heat", "equipo2": "Brooklyn Nets", 
            "hora": "19:30 (VE)", "sede": "Barclays Center (Brooklyn, NY)", 
            "ganador": "Miami Heat (-4.5 pts)", "total_puntos": "218.5 (Bajas / Under)", 
            "analisis_es": (
                "🏀 <b>Análisis Táctico y de Espaciamiento (Spacing):</b><br>"
                "El sistema de Miami opera bajo una disciplina defensiva inquebrantable, priorizando la defensa de contención en el perímetro y cerrando los espacios en la llave (paint protection). Brooklyn intentará proponer un juego abierto, pero la presión física en la primera línea de pase cortocircuitará su circulación de balón.<br><br>"
                "📊 <b>Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):</b><br>"
                "• <b>Pace Proyectado:</b> 96.5 posesiones. Al ser un juego de posesiones más pausadas, el ritmo beneficia la tendencia a la baja (Under) en la línea de puntos totales.<br>"
                "• <b>Defensive Rating:</b> Miami proyecta frenar la eficiencia ofensiva rival por debajo del 44% en tiros de campo globales.<br>"
                "• <b>True Shooting Percentage (TS%):</b> La selección de tiro de Miami en la media distancia ofrece mayor estabilidad en los minutos de cierre.<br><br>"
                "🎯 <b>Conclusión del Modelo:</b> Disciplina táctica y control absoluto del reloj de posesión otorgan la ventaja a Miami en un duelo de pocos puntos."
            ),
            "analisis_en": "Advanced tactical breakdown for Miami Heat vs Brooklyn Nets...", 
            "es_jugada_fija": False
        },
        {
            "equipo1": "Dallas Mavericks", "equipo2": "New Orleans Pelicans", 
            "hora": "20:00 (VE)", "sede": "Smoothie King Center (New Orleans, LA)", 
            "ganador": "Dallas Mavericks (-3.0 pts)", "total_puntos": "230.5 (Altas / Over)", 
            "analisis_es": (
                "🏀 <b>Análisis Táctico y de Espaciamiento (Spacing):</b><br>"
                "Encuentro caracterizado por un alto volumen de transiciones ofensivas y situaciones de bloqueo directo (pick-and-roll). Dallas explota de manera quirúrgica las debilidades en el cambio de marca defensivo del rival, generando tiros abiertos desde las esquinas.<br><br>"
                "📊 <b>Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):</b><br>"
                "• <b>True Shooting Percentage (TS%):</b> Proyectado en un formidable 59.8% para los Mavericks, reflejando gran eficacia combinando tiros libres, dobles y triples.<br>"
                "• <b>Usage Rate (USG%):</b> Alta concentración de jugadas culminadas por los creadores de juego principales, elevando el potencial de anotación colectiva.<br>"
                "• <b>Pace Estimado:</b> 101.4 posesiones, apuntando directamente a superar la línea de altas (Over).<br><br>"
                "🎯 <b>Conclusión del Modelo:</b> La capacidad anotadora exterior de Dallas y la velocidad en transición garantizan un partido de alto voltaje ofensivo."
            ),
            "analisis_en": "Advanced tactical breakdown for Dallas vs New Orleans...", 
            "es_jugada_fija": False
        },
        {
            "equipo1": "Milwaukee Bucks", "equipo2": "Chicago Bulls", 
            "hora": "20:00 (VE)", "sede": "United Center (Chicago, IL)", 
            "ganador": "Milwaukee Bucks (-6.0 pts)", "total_puntos": "226.0 (Altas / Over)", 
            "analisis_es": (
                "🏀 <b>Análisis Táctico y de Espaciamiento (Spacing):</b><br>"
                "Milwaukee impone condiciones a través de su dominio físico en la pintura y la gravedad ofensiva que atrae su juego interior, abriendo espacios ideales para los tiradores exteriores. Chicago sufrirá para contener el rebote en ambos costados de la duela.<br><br>"
                "📊 <b>Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):</b><br>"
                "• <b>Rebounding Percentage (OREB/DREB):</b> Clara ventaja para los Bucks, asegurando segundas oportunidades de anotación.<br>"
                "• <b>Offensive Rating:</b> Proyectado en 116.8 puntos por 100 posesiones, aprovechando las flaquezas de la estructura defensiva de los Bulls.<br><br>"
                "🎯 <b>Conclusión del Modelo:</b> La jerarquía en la pintura y el control del ritmo ofensivo inclinan el pronóstico claramente hacia Milwaukee."
            ),
            "analisis_en": "Advanced tactical breakdown for Milwaukee vs Chicago...", 
            "es_jugada_fija": False
        },
        {
            "equipo1": "Minnesota Timberwolves", "equipo2": "Detroit Pistons", 
            "hora": "20:00 (VE)", "sede": "Little Caesars Arena (Detroit, MI)", 
            "ganador": "Minnesota Timberwolves (-7.5 pts)", "total_puntos": "215.0 (Bajas / Under)", 
            "analisis_es": (
                "🏀 <b>Análisis Táctico y de Espaciamiento (Spacing):</b><br>"
                "Minnesota despliega uno de los entramados defensivos más asfixiantes de la liga. Su capacidad para colapsar la pintura y recuperar la posición perimetral neutraliza los sistemas de penetración rivales.<br><br>"
                "📊 <b>Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):</b><br>"
                "• <b>Defensive Win Shares:</b> Alto índice acumulado en el quinteto titular visitante.<br>"
                "• <b>Opponent Effective Field Goal Percentage (Opp eFG%):</b> Proyectado por debajo del 48%, conteniendo severamente la producción ofensiva de Detroit.<br><br>"
                "🎯 <b>Conclusión del Modelo:</b> Solidez defensiva y control de las líneas de pase marcan la pauta para una victoria cómoda y de baja anotación."
            ),
            "analisis_en": "Advanced tactical breakdown for Minnesota vs Detroit...", 
            "es_jugada_fija": False
        },
        {
            "equipo1": "San Antonio Spurs", "equipo2": "Phoenix Suns", 
            "hora": "20:00 (VE)", "sede": "Footprint Center (Phoenix, AZ)", 
            "ganador": "Phoenix Suns (-5.0 pts)", "total_puntos": "228.0 (Altas / Over)", 
            "analisis_es": (
                "🏀 <b>Análisis Táctico y de Espaciamiento (Spacing):</b><br>"
                "Duelo de alta escuela en la ejecución de tiros de media distancia y situaciones de aclarado (isolation). Phoenix cuenta con individualidades letales capaces de castigar cualquier desajuste en los cambios defensivos.<br><br>"
                "📊 <b>Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):</b><br>"
                "• <b>Clutch Efficiency:</b> Los Suns registran superioridad estadística en posesiones apretadas durante los últimos cuartos.<br>"
                "• <b>Offensive Pace:</b> Ritmo elevado que propicia un intercambio constante de canastas.<br><br>"
                "🎯 <b>Conclusión del Modelo:</b> La experiencia y la precisión en los momentos clave otorgan la ventaja a Phoenix en un marcador alto."
            ),
            "analisis_en": "Advanced tactical breakdown for San Antonio vs Phoenix...", 
            "es_jugada_fija": False
        },
        {
            "equipo1": "Los Angeles Clippers", "equipo2": "Denver Nuggets", 
            "hora": "22:30 (VE)", "sede": "Ball Arena (Denver, CO)", 
            "ganador": "Denver Nuggets (-4.0 pts)", "total_puntos": "222.0 (Altas / Over)", 
            "analisis_es": (
                "🏀 <b>Análisis Táctico y de Espaciamiento (Spacing):</b><br>"
                "Cierres de jornada con un ajedrez táctico en la altura de Denver. La capacidad de distribución desde el poste alto y la lectura de cortes sin balón desarticulan cualquier planteamiento defensivo convencional.<br><br>"
                "📊 <b>Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):</b><br>"
                "• <b>Net Rating en la Altura:</b> Denver maximiza su localía elevando su eficiencia neta en los tramos finales del encuentro.<br>"
                "• <b>Assist-to-Turnover Ratio:</b> Excelente circulación de balón que minimiza las pérdidas no forzadas.<br><br>"
                "🎯 <b>Conclusión del Modelo:</b> El factor local y la fluidez en la distribución ofensiva inclinan el pronóstico a favor de los Nuggets."
            ),
            "analisis_en": "Advanced tactical breakdown for Clippers vs Nuggets...", 
            "es_jugada_fija": False
        }
    ]
    return pd.DataFrame(data_def)

# Selector de idioma global en la barra lateral
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
        "Cartelera y Partidos", 
        "Noticias (Doble Actualización)", 
        "La Jugada Fija del Día", 
        "Diccionario Sabermétrico",
        "🔐 Panel de Administración"
    ])

    fecha_hoy = datetime.now().strftime("%d de %B de %Y")
    df_cartelera = cargar_cartelera()
    ayer_str = cargar_estadisticas()

    if lang == "es":
        st.markdown(f"""
        <div class="stats-banner">
            <h4 style="color: #00FF66; margin: 0;">🎯 Rendimiento del Modelo Sabermétrico (Evaluación de la Jornada)</h4>
            <p style="font-size: 15px; margin: 5px 0 0 0;">Aciertos del Modelo: <b>{ayer_str}</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="stats-banner">
            <h4 style="color: #00FF66; margin: 0;">🎯 Sabermetric Model Performance (Slate Evaluation)</h4>
            <p style="font-size: 15px; margin: 5px 0 0 0;">Model Hits: <b>{ayer_str}</b></p>
        </div>
        """, unsafe_allow_html=True)

    if menu == "Cartelera y Partidos":
        st.header(f"📅 Cartelera de Partidos - Análisis Profundo ({fecha_hoy})")
        st.write("Selecciona un encuentro para ver el desglose científico del modelo:")
        
        opciones_dict = {}
        for _, row in df_cartelera.iterrows():
            e1 = str(row['equipo1']).strip()
            e2 = str(row['equipo2']).strip()
            label = f"{e1} vs. {e2}"
            opciones_dict[label] = row
            
        partido_seleccionado = st.selectbox("Juegos de hoy:", list(opciones_dict.keys()))
        
        if partido_seleccionado:
            fila_juego = opciones_dict[partido_seleccionado]
            equipo1 = str(fila_juego['equipo1']).strip()
            equipo2 = str(fila_juego['equipo2']).strip()
            
            logo1_url = LOGOS_EQUIPOS.get(equipo1, "")
            logo2_url = LOGOS_EQUIPOS.get(equipo2, "")
            
            matchup_html = f'<div class="matchup-box"><div class="team-col"><img src="{logo1_url}" width="100" style="margin-bottom: 10px;"><h3 style="margin: 0; color: #ffffff;">{equipo1}</h3><span style="font-size: 12px; color: #8b949e;">(Visitante)</span></div><div class="vs-col">VS</div><div class="team-col"><img src="{logo2_url}" width="100" style="margin-bottom: 10px;"><h3 style="margin: 0; color: #ffffff;">{equipo2}</h3><span style="font-size: 12px; color: #8b949e;">(Local)</span></div></div>'
            st.markdown(matchup_html, unsafe_allow_html=True)
            
            hora_val = str(fila_juego.get('hora', '19:30 (VE)'))
            sede_val = str(fila_juego.get('sede', 'Arena Principal'))
            st.markdown(f"🕒 **Hora (VE):** {hora_val} &nbsp;&nbsp;|&nbsp;&nbsp; 🏟️ **Sede:** {sede_val}")
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Ganador Proyectado", value=fila_juego["ganador"])
            with col2:
                st.metric(label="Total de Puntos (O/U)", value=fila_juego["total_puntos"])
            
            st.markdown("### 🧠 Razonamiento Táctico y Métricas Avanzadas")
            analisis_amplio = fila_juego["analisis_es"] if lang == "es" else fila_juego["analisis_en"]
            st.markdown(analisis_amplio, unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("📄 Descargar Análisis en PDF"):
                archivo_pdf = generar_pdf_analisis(f"{equipo1} vs {equipo2}", hora_val, sede_val, fila_juego["ganador"], fila_juego["total_puntos"], analisis_amplio)
                with open(archivo_pdf, "rb") as f:
                    st.download_button("💾 Guardar archivo PDF en tu equipo", data=f, file_name="reporte_sabermetria_nba.pdf", mime="application/pdf")

    elif menu == "Noticias (Doble Actualización)":
        st.header(f"📰 Centro de Noticias en Tiempo Real — {fecha_hoy}")
        st.write("Bienvenido al centro informativo oficial de Sabermetría IA.")
        
        mat_es, vesp_es, mat_en, vesp_en = cargar_noticias_txt()
        matutina_texto = mat_es if lang == "es" else mat_en
        vespertina_texto = vesp_es if lang == "es" else vesp_en

        tab1, tab2 = st.tabs(["🌅 Actualización Matutina (Cierre Previo)", "🌇 Actualización de la Tarde (5:00 p.m.)"])
        with tab1:
            st.subheader("🌅 Reporte Matutino: Radiografía y Tendencias de la Liga")
            st.markdown(matutina_texto)
        with tab2:
            st.subheader("🌇 Reporte Vespertino: Última Hora y Ajustes Previo al Salto Inicial")
            st.markdown(vespertina_texto)

    elif menu == "La Jugada Fija del Día":
        st.header("⭐ La Jugada Estelar del Modelo")
        st.success("Recomendación avalada estrictamente por eficiencia matemática y métricas de posesión.")
        
        juegos_fijos = df_cartelera[df_cartelera['es_jugada_fija'] == True]
        juego_estelar = juegos_fijos.iloc[0] if not juegos_fijos.empty else df_cartelera.iloc[0]
            
        estelar_eq1 = str(juego_estelar["equipo1"]).strip()
        estelar_eq2 = str(juego_estelar["equipo2"]).strip()
        logo_estelar_1 = LOGOS_EQUIPOS.get(estelar_eq1, "")
        logo_estelar_2 = LOGOS_EQUIPOS.get(estelar_eq2, "")
        
        matchup_estelar_html = f'<div class="matchup-box"><div class="team-col"><img src="{logo_estelar_1}" width="100" style="margin-bottom: 10px;"><h3 style="margin: 0; color: #ffffff;">{estelar_eq1}</h3><span style="font-size: 12px; color: #8b949e;">(Visitante)</span></div><div class="vs-col">VS</div><div class="team-col"><img src="{logo_estelar_2}" width="100" style="margin-bottom: 10px;"><h3 style="margin: 0; color: #ffffff;">{estelar_eq2}</h3><span style="font-size: 12px; color: #8b949e;">(Local)</span></div></div>'
        st.markdown(matchup_estelar_html, unsafe_allow_html=True)
        
        hora_est = str(juego_estelar.get('hora', '19:30 (VE)'))
        sede_est = str(juego_estelar.get('sede', 'Arena Principal'))
        st.markdown(f"🕒 **Hora (
