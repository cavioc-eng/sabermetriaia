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
        "admin_desc": "Control estadístico de visitas, cartelera de juegos y noticias.",
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
        "admin_desc": "Visit statistical control, game slate and news.",
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

    analisis_mavericks = (
        "🏀 Análisis Táctico y de Espaciamiento (Spacing):\n\n"
        "Encuentro caracterizado por un alto volumen de transiciones ofensivas y situaciones de bloqueo directo (pick-and-roll). Dallas explota de manera quirúrgica las debilidades en el cambio de marca defensivo del rival, generando tiros abiertos desde las esquinas.\n\n"
        "📊 Métricas Avanzadas y Modelo Predictivo (Sabermetría IA):\n\n"
        "• True Shooting Percentage (TS%): Proyectado en un formidable 59.8% para los Mavericks, reflejando gran eficacia combinando tiros libres, dobles y triples.\n"
        "• Usage Rate (USG%): Alta concentración de jugadas culminadas por los creadores de juego principales, elevando el potencial de anotación colectiva.\n"
        "• Pace Estimado: 101.4 posesiones, apuntando directamente a superar la línea de altas (Over).\n\n"
        "🎯 Conclusión del Modelo: La capacidad anotadora exterior de Dallas y la velocidad en transición garantizan un partido de alto voltaje ofensivo."
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
        },
        {
            "equipo1": "Dallas Mavericks", "equipo2": "New Orleans Pelicans", 
            "hora": "20:00 (VE)", "sede": "Smoothie King Center (New Orleans, LA)", 
            "ganador": "Dallas Mavericks (-3.0 pts)", "total_puntos": "230.5 (Altas / Over)", 
            "analisis_es": analisis_mavericks, "analisis_en": analisis_mavericks, "es_jugada_fija": False
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
        st.header("📅 Cartelera de Partidos - Análisis Profundo (" + fecha_hoy + ")")
        st.write("Selecciona un encuentro para ver el desglose científico del modelo:")
        
        opciones_dict = {}
        for _, row in df_cartelera.iterrows():
            e1 = str(row['equipo1']).strip()
            e2 = str(row['equipo2']).strip()
            label = e1 + " vs. " + e2
            opciones_dict[label] = row
            
        partido_seleccionado = st.selectbox("Juegos de hoy:", list(opciones_dict.keys()))
        
        if partido_seleccionado:
            fila_juego = opciones_dict[partido_seleccionado]
            equipo1 = str(fila_juego['equipo1']).strip()
            equipo2 = str(fila_juego['equipo2']).strip()
            
            logo1_url = LOGOS_EQUIPOS.get(equipo1, "")
            logo2_url = LOGOS_EQUIPOS.get(equipo2, "")
            
            matchup_html = (
                '<div class="matchup-box">'
                '<div class="team-col"><img src="' + logo1_url + '" width="100" style="margin-bottom: 10px;"><h3 style="margin: 0; color: #ffffff;">' + equipo1 + '</h3><span style="font-size: 12px; color: #8b949e;">(Visitante)</span></div>'
                '<div class="vs-col">VS</div>'
                '<div class="team-col"><img src="' + logo2_url + '" width="100" style="margin-bottom: 10px;"><h3 style="margin: 0; color: #ffffff;">' + equipo2 + '</h3><span style="font-size: 12px; color: #8b949e;">(Local)</span></div>'
                '</div>'
            )
            st.markdown(matchup_html, unsafe_allow_html=True)
            
            hora_val = str(fila_juego.get('hora', '19:30 (VE)'))
            sede_val = str(fila_juego.get('sede', 'Arena Principal'))
            st.markdown("🕒 **Hora (VE):** " + hora_val + " &nbsp;&nbsp;|&nbsp;&nbsp; 🏟️ **Sede:** " + sede_val)
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Ganador Proyectado", value=str(fila_juego["ganador"]))
            with col2:
                st.metric(label="Total de Puntos (O/U)", value=str(fila_juego["total_puntos"]))
            
            st.markdown("### 🧠 Razonamiento Táctico y Métricas Avanzadas")
            analisis_amplio = str(fila_juego["analisis_es"]) if lang == "es" else str(fila_juego["analisis_en"])
            st.text(analisis_amplio)
            
            st.markdown("---")
            if st.button("📄 Descargar Análisis en PDF"):
                archivo_pdf = generar_pdf_analisis(equipo1 + " vs " + equipo2, hora_val, sede_val, str(fila_juego["ganador"]), str(fila_juego["total_puntos"]), analisis_amplio)
                with open(archivo_pdf, "rb") as f:
                    st.download_button("💾 Guardar archivo PDF en tu equipo", data=f, file_name="reporte_sabermetria_nba.pdf", mime="application/pdf")

    elif menu == "Noticias (Doble Actualización)":
        st.header("📰 Centro de Noticias en Tiempo Real — " + fecha_hoy)
        st.write("Bienvenido al centro informativo oficial de Sabermetría IA.")
        
        mat_es, vesp_es, mat_en, vesp_en = cargar_noticias_txt()
        matutina_texto = mat_es if lang == "es" else mat_en
        vespertina_texto = vesp_es if lang == "es" else vesp_en

        tab1, tab2 = st.tabs(["🌅 Actualización Matutina (Cierre Previo)", "🌇 Actualización de la Tarde (5:00 p.m.)"])
        with tab1:
            st.subheader("🌅 Reporte Matutino: Radiografía y Tendencias de la Liga")
            st.text(matutina_texto)
        with tab2:
            st.subheader("🌇 Reporte Vespertino: Última Hora y Ajustes Previo al Salto Inicial")
            st.text(vespertina_texto)

    elif menu == "La Jugada Fija del Día":
        st.header("⭐ La Jugada Estelar del Modelo")
        st.success("Recomendación avalada estrictamente por eficiencia matemática y métricas de posesión.")
        
        juegos_fijos = df_cartelera[df_cartelera['es_jugada_fija'] == True]
        juego_estelar = juegos_fijos.iloc[0] if not juegos_fijos.empty else df_cartelera.iloc[0]
            
        estelar_eq1 = str(juego_estelar["equipo1"]).strip()
        estelar_eq2 = str(juego_estelar["equipo2"]).strip()
        logo_estelar_1 = LOGOS_EQUIPOS.get(estelar_eq1, "")
        logo_estelar_2 = LOGOS_EQUIPOS.get(estelar_eq2, "")
        
        matchup_estelar_html = (
            '<div class="matchup-box">'
            '<div class="team-col"><img src="' + logo_estelar_1 + '" width="100" style="margin-bottom: 10px;"><h3 style="margin: 0; color: #ffffff;">' + estelar_eq1 + '</h3><span style="font-size: 12px; color: #8b949e;">(Visitante)</span></div>'
            '<div class="vs-col">VS</div>'
            '<div class="team-col"><img src="' + logo_estelar_2 + '" width="100" style="margin-bottom: 10px;"><h3 style="margin: 0; color: #ffffff;">' + estelar_eq2 + '</h3><span style="font-size: 12px; color: #8b949e;">(Local)</span></div>'
            '</div>'
        )
        st.markdown(matchup_estelar_html, unsafe_allow_html=True)
        
        hora_est = str(juego_estelar.get('hora', '19:30 (VE)'))
        sede_est = str(juego_estelar.get('sede', 'Arena Principal'))
        st.markdown("🕒 **Hora (VE):** " + hora_est + " &nbsp;&nbsp;|&nbsp;&nbsp; 🏟️ **Sede:** " + sede_est)
        st.markdown("---")
        st.markdown("### 📊 Fundamento Estadístico y Razonamiento del Modelo")
        analisis_jugada = str(juego_estelar["analisis_es"]) if lang == "es" else str(juego_estelar["analisis_en"])
        st.text(analisis_jugada)

    elif menu == "Diccionario Sabermétrico":
        st.header("📖 Diccionario Sabermétrico Educativo (Básico a Avanzado)")
        st.write("Guía completa de referencia para comprender desde los fundamentos tradicionales hasta las métricas de eficiencia más avanzadas:")
        
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

    elif menu == "🔐 Panel de Administración":
        st.header(t["admin_titulo"])
        st.write(t["admin_desc"])
        clave_admin = st.text_input(t["admin_clave"], type="password", key="input_clave_admin")
        
        if clave_admin == "sabermetria2026":
            st.success(t["admin_exito"])
            
            # Contador acumulado y registro de visitas
            if os.path.exists(db_usuarios_path):
                df_visitas = pd.read_csv(db_usuarios_path, encoding='utf-8')
                total_accesos = len(df_visitas)
                st.metric(label="📊 Total de Ingresos Acumulados al Portal", value=total_accesos)
                st.write("---")
                st.subheader("📋 Registro Detallado de Accesos")
                st.dataframe(df_visitas, use_container_width=True)
            else:
                st.metric(label="📊 Total de Ingresos Acumulados al Portal", value=0)

            st.markdown("---")
            st.subheader("🏀 Gestor de Cartelera y Partidos")
            st.write("Agrega, edita o elimina los encuentros programados para las jornadas:")
            
            lista_equipos = list(LOGOS_EQUIPOS.keys())
            
            with st.form("form_agregar_partido"):
                st.markdown("#### ➕ Registrar Nuevo Encuentro")
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    eq1_nuevo = st.selectbox("Equipo Visitante:", lista_equipos, index=0)
                    hora_nuevo = st.text_input("Hora (Ej: 19:30 (VE)):", value="19:30 (VE)")
                    ganador_nuevo = st.text_input("Ganador Proyectado (Ej: Boston Celtics (-8.5 pts)):", value="Boston Celtics (-8.5 pts)")
                with col_g2:
                    eq2_nuevo = st.selectbox("Equipo Local:", lista_equipos, index=1)
                    sede_nuevo = st.text_input("Sede del Encuentro:", value="Arena Principal")
                    total_nuevo = st.text_input("Línea de Puntos O/U (Ej: 224.5 (Altas / Over)):", value="224.5 (Altas / Over)")
                
                analisis_nuevo = st.text_area("Análisis Táctico y Métricas Avanzadas:", value="🏀 Análisis Táctico y de Espaciamiento:\n\n📊 Métricas Avanzadas y Modelo Predictivo:\n\n🎯 Conclusión del Modelo:", height=120)
                es_fija_nuevo = st.checkbox("⭐ Marcar como 'La Jugada Fija del Día'")
                
                if st.form_submit_button("➕ Publicar / Agregar Partido a la Cartelera"):
                    nuevo_juego_df = pd.DataFrame([{
                        "equipo1": eq1_nuevo,
                        "equipo2": eq2_nuevo,
                        "hora": hora_nuevo,
                        "sede": sede_nuevo,
                        "ganador": ganador_nuevo,
                        "total_puntos": total_nuevo,
                        "analisis_es": analisis_nuevo,
                        "analisis_en": analisis_nuevo,
                        "es_jugada_fija": es_fija_nuevo
                    }])
                    df_actualizado = pd.concat([df_cartelera, nuevo_juego_df], ignore_index=True)
                    guardar_cartelera(df_actualizado)
                    st.success("¡Partido agregado y publicado exitosamente en la cartelera!")
                    st.rerun()

            if not df_cartelera.empty:
                st.markdown("---")
                st.subheader("🗑️ Eliminar Partidos de la Cartelera Activa")
                nombres_juegos = [f"{row['equipo1']} vs {row['equipo2']} ({row['hora']})" for _, row in df_cartelera.iterrows()]
                juego_a_borrar = st.selectbox("Selecciona el encuentro a remover:", nombres_juegos)
                if st.button("🗑️ Eliminar Partido Seleccionado"):
                    idx_a_borrar = nombres_juegos.index(juego_a_borrar)
                    df_cartelera = df_cartelera.drop(idx_a_borrar).reset_index(drop=True)
                    guardar_cartelera(df_cartelera)
                    st.success("¡Encuentro eliminado de la cartelera!")
                    st.rerun()

            st.markdown("---")
            st.subheader("🎯 Gestor de Efectividad del Modelo")
            ayer_act = cargar_estadisticas()
            with st.form("form_estadisticas"):
                nuevo_ayer = st.text_input("Aciertos de la Jornada (Ej: 3 / 4 (75%)):", value=ayer_act)
                if st.form_submit_button("💾 Guardar Efectividad"):
                    guardar_estadisticas(nuevo_ayer)
                    st.success("¡Efectividad actualizada!")
                    st.rerun()

            st.markdown("---")
            st.subheader("📰 Gestor de Noticias Bilingües (Archivo Local)")
            st.write("Modifica los textos directamente y guarda para publicarlos de inmediato en la sección de noticias.")
            
            mat_es_act, vesp_es_act, mat_en_act, vesp_en_act = cargar_noticias_txt()
            
            with st.form("form_noticias_txt"):
                st.markdown("#### 🇪🇸 Español")
                txt_mat_es = st.text_area("Noticia Matutina (Español):", value=mat_es_act, height=140)
                txt_vesp_es = st.text_area("Noticia Vespertina (Español):", value=vesp_es_act, height=140)
                st.markdown("#### 🇺🇸 Inglés (English)")
                txt_mat_en = st.text_area("Morning News (English):", value=mat_en_act, height=140)
                txt_vesp_en = st.text_area("Evening News (English):", value=vesp_en_act, height=140)
                
                if st.form_submit_button("💾 Guardar y Publicar Noticias"):
                    guardar_noticias_txt(txt_mat_es, txt_vesp_es, txt_mat_en, txt_vesp_en)
                    st.success("¡Noticias bilingües guardadas y publicadas correctamente!")
                    st.rerun()

        elif clave_admin != "":
            st.error(t["admin_error"])
