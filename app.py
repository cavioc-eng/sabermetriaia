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

st.set_page_config(
    page_title="Sabermetría IA - Analítica Avanzada de Básquetbol",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)


def cargar_noticias_txt():
  default_mat_es = (
      "🏀 Épica en la Altura y Corazón de Perdedor: Las Historias Ocultas de"
      " una Noche de Ocho Batallas\n\n• La remontada de película en Denver:"
      " Nikola Jokic y Jamal Murray guiaron a los Nuggets en un infartante"
      " 141-135 en prórroga frente a unos aguerridos Pelicans.\n\n• La hazaña del"
      " novato: Caleb Wilson brilló con 30 puntos y 14 rebotes en la dura caída"
      " de los Bulls ante Washington."
  )
  default_mat_en = (
      "🏀 High-Altitude Epic and Underdog Grit: The Untold Stories Behind an"
      " Eight-Game Slate\n\n• Denver's Cinematic Comeback: Nikola Jokic and"
      " Jamal Murray secured a thrilling 141-135 OT victory against New"
      " Orleans.\n\n• The Rookie's Silent Masterpiece: Caleb Wilson shined with"
      " 30 points and 14 rebounds in Chicago's razor-thin defeat."
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


TEXTOS = {
    "es": {
        "titulo_app": "SABERMETRÍA IA",
        "sub_app": "Analítica Avanzada de Básquetbol",
        "paso1_titulo": "Paso 1: Síguenos en TikTok",
        "paso1_desc": (
            "Abre nuestro perfil oficial @sabermetriaia y presiona el botón de"
            " Seguir:"
        ),
        "btn_tiktok": "📲 Ir a @sabermetriaia",
        "paso2_titulo": "Paso 2: Acceso Directo",
        "paso2_desc": "Haz clic en el botón para entrar al portal exclusivo:",
        "btn_acceso": "🏀 Entrar al Portal Exclusivo",
        "admin_titulo": "🔐 Panel de Control y Publicación - Sabermetría IA",
        "admin_desc": (
            "Control estadístico de visitas, cartelera masiva por CSV y noticias"
            " editoriales."
        ),
        "admin_clave": "Ingresa la clave de administrador:",
        "admin_exito": "¡Acceso de administrador concedido!",
        "admin_error": "❌ Clave de administrador incorrecta.",
        "total_visitas": "Total de Accesos al Portal",
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
        "admin_desc": (
            "Visit statistical control, CSV slate upload and editorial news."
        ),
        "admin_clave": "Enter admin password:",
        "admin_exito": "Admin access granted!",
        "admin_error": "❌ Incorrect admin password.",
        "total_visitas": "Total Portal Accesses",
    },
}

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #00FF66; color: #000000; font-weight: bold; border-radius: 8px; }
    .matchup-box { display: flex; align-items: center; justify-content: space-around; text-align: center; padding: 15px; background-color: #161b22; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 20px; }
    .team-col { flex: 1; display: flex; flex-direction: column; align-items: center; }
    .vs-col { flex: 0 0 100px; font-size: 32px; font-weight: bold; color: #00FF66; text-align: center; }
    .tiktok-card { background-color: #161b22; padding: 15px 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px; }
    .stats-banner { background: linear-gradient(135deg, #161b22 0%, #1f2937 100%); border: 1px solid #00FF66; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    </style>
""",
    unsafe_allow_html=True,
)

LOGOS_EQUIPOS = {
    "Atlanta Hawks": (
        "https://cdn.nba.com/logos/nba/1610612737/global/L/logo.svg"
    ),
    "Boston Celtics": (
        "https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg"
    ),
    "Brooklyn Nets": "https://cdn.nba.com/logos/nba/1610612751/global/L/logo.svg",
    "Charlotte Hornets": (
        "https://cdn.nba.com/logos/nba/1610612766/global/L/logo.svg"
    ),
    "Chicago Bulls": "https://cdn.nba.com/logos/nba/1610612741/global/L/logo.svg",
    "Cleveland Cavaliers": (
        "https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg"
    ),
    "Dallas Mavericks": (
        "https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg"
    ),
    "Denver Nuggets": "https://cdn.nba.com/logos/nba/1610612743/global/L/logo.svg",
    "Detroit Pistons": (
        "https://cdn.nba.com/logos/nba/1610612765/global/L/logo.svg"
    ),
    "Golden State Warriors": (
        "https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg"
    ),
    "Houston Rockets": (
        "https://cdn.nba.com/logos/nba/1610612745/global/L/logo.svg"
    ),
    "Indiana Pacers": "https://cdn.nba.com/logos/nba/1610612754/global/L/logo.svg",
    "Los Angeles Clippers": (
        "https://cdn.nba.com/logos/nba/1610612746/global/L/logo.svg"
    ),
    "Los Angeles Lakers": (
        "https://cdn.nba.com/logos/nba/1610612747/global/L/logo.svg"
    ),
    "Memphis Grizzlies": (
        "https://cdn.nba.com/logos/nba/1610612763/global/L/logo.svg"
    ),
    "Miami Heat": "https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg",
    "Milwaukee Bucks": (
        "https://cdn.nba.com/logos/nba/1610612749/global/L/logo.svg"
    ),
    "Minnesota Timberwolves": (
        "https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg"
    ),
    "New Orleans Pelicans": (
        "https://cdn.nba.com/logos/nba/1610612740/global/L/logo.svg"
    ),
    "New York Knicks": "https://cdn.nba.com/logos/nba/1610612752/global/L/logo.svg",
    "Oklahoma City Thunder": (
        "https://cdn.nba.com/logos/nba/1610612760/global/L/logo.svg"
    ),
    "Orlando Magic": "https://cdn.nba.com/logos/nba/1610612753/global/L/logo.svg",
    "Philadelphia 76ers": (
        "https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg"
    ),
    "Phoenix Suns": "https://cdn.nba.com/logos/nba/1610612756/global/L/logo.svg",
    "Portland Trail Blazers": (
        "https://cdn.nba.com/logos/nba/1610612757/global/L/logo.svg"
    ),
    "Sacramento Kings": (
        "https://cdn.nba.com/logos/nba/1610612758/global/L/logo.svg"
    ),
    "San Antonio Spurs": (
        "https://cdn.nba.com/logos/nba/1610612759/global/L/logo.svg"
    ),
    "Toronto Raptors": (
        "https://cdn.nba.com/logos/nba/1610612761/global/L/logo.svg"
    ),
    "Utah Jazz": "https://cdn.nba.com/logos/nba/1610612762/global/L/logo.svg",
    "Washington Wizards": (
        "https://cdn.nba.com/logos/nba/1610612764/global/L/logo.svg"
    ),
}


def generar_pdf_analisis(
    partido, hora, sede, ganador, total_puntos, razonamiento
):
  pdf_path = os.path.join(current_dir, "reporte_sabermetria.pdf")
  doc = SimpleDocTemplate(pdf_path, pagesize=letter)
  styles = getSampleStyleSheet()
  story = []
  title_style = ParagraphStyle(
      "TitleStyle",
      parent=styles["Heading1"],
      fontSize=16,
      textColor=colors.HexColor("#00FF66"),
      spaceAfter=12,
  )
  body_style = ParagraphStyle(
      "BodyStyle",
      parent=styles["Normal"],
      fontSize=10,
      textColor=colors.HexColor("#333333"),
      spaceAfter=10,
      leading=14,
  )
  story.append(
      Paragraph(
          "SABERMETRÍA IA - REPORTE DE ANALÍTICA AVANZADA", title_style
      )
  )
  story.append(Paragraph("Encuentro: " + partido, body_style))
  story.append(Paragraph("Hora (VE): " + hora + " | Sede: " + sede, body_style))
  story.append(
      Paragraph(
          "Fecha del Reporte: " + datetime.now().strftime("%d/%m/%Y"), body_style
      )
  )
  story.append(Spacer(1, 10))
  story.append(Paragraph("Ganador Proyectado: " + ganador, body_style))
  story.append(
      Paragraph("Línea de Puntos Totales (O/U): " + total_puntos, body_style)
  )
  story.append(Spacer(1, 10))
  story.append(
      Paragraph("Desglose Táctico y Métricas del Modelo:", title_style)
  )
  story.append(Paragraph(razonamiento, body_style))
  doc.build(story)
  return pdf_path


def registrar_visita():
  fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  nuevo_reg = pd.DataFrame(
      [["Seguidor TikTok (Acceso Directo)", fecha_hora]],
      columns=["Usuario", "Fecha_Acceso"],
  )
  if os.path.exists(db_usuarios_path):
    df_ex = pd.read_csv(db_usuarios_path)
    pd.concat([df_ex, nuevo_reg], ignore_index=True).to_csv(
        db_usuarios_path, index=False, encoding="utf-8"
    )
  else:
    nuevo_reg.to_csv(db_usuarios_path, index=False, encoding="utf-8")


def cargar_estadisticas():
  if os.path.exists(estadisticas_path):
    try:
      return str(
          pd.read_csv(estadisticas_path, encoding="utf-8").iloc[0]["ayer"]
      )
    except Exception:
      pass
  return "3 / 4 (75% de Aciertos)"


def guardar_estadisticas(ayer):
  pd.DataFrame([[ayer]], columns=["ayer"]).to_csv(
      estadisticas_path, index=False, encoding="utf-8"
  )


def cargar_cartelera():
  if os.path.exists(cartelera_csv_path):
    try:
      df_saved = pd.read_csv(cartelera_csv_path, encoding="utf-8")
      if not df_saved.empty:
        return df_saved
    except Exception:
      pass
  # Respaldo automático por defecto
  datos_respaldo = [
      {
          "equipo1": "Cleveland Cavaliers",
          "equipo2": "Minnesota Timberwolves",
          "hora": "19:00 (VE)",
          "sede": "Rocket Mortgage FieldHouse, Cleveland",
          "ganador": "Minnesota Timberwolves",
          "total_puntos": "221.0",
          "analisis_es": (
              "ANÁLISIS SABERMÉTRICO EXPERTO (⭐ JUGADA FIJA): Muralla defensiva"
              " de élite y Net Rating superior de los Wolves a domicilio."
          ),
          "analisis_en": (
              "EXPERT ANALYSIS (LOCK OF THE DAY): Wolves' elite defensive"
              " Net Rating secures the road win."
          ),
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


idioma = st.sidebar.selectbox("🌐 Idioma / Language", ["Español", "English"])
lang = "es" if idioma == "Español" else "en"
t = TEXTOS[lang]

if "autenticado" not in st.session_state:
  st.session_state.autenticado = False

# Selector global de secciones en el menú lateral para que SIEMPRE esté disponible
st.sidebar.title("Menú Principal" if lang == "es" else "Main Menu")
if os.path.exists(logo_path):
  st.sidebar.image(logo_path, width=220)

menu = st.sidebar.radio(
    "Selecciona una sección:" if lang == "es" else "Select a section:",
    [
        "Cartelera y Partidos",
        "El Pulso de la Duela (Noticias)",
        "La Jugada Fija del Día",
        "Diccionario Sabermétrico",
        "🔐 Panel de Administración",
    ],
)

fecha_hoy = datetime.now().strftime("%d de %B de %Y")
df_cartelera = cargar_cartelera()
ayer_str = cargar_estadisticas()

if not st.session_state.autenticado:
  col_izq, col_centro, col_der = st.columns([1.2, 1.8, 1])
  with col_izq:
    if os.path.exists(logo_path):
      st.image(logo_path, width=220)
  with col_centro:
    st.markdown("<br>", unsafe_allow_html=True)
    st.title(t["titulo_app"])
    st.subheader(t["sub_app"])
    st.write(
        "Para desbloquear el portal exclusivo y la analítica avanzada, sigue los"
        " pasos:"
    )
  with col_der:
    st.image(
        "https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg",
        width=140,
    )

  st.markdown("---")
  col_paso1, col_paso2 = st.columns(2)
  with col_paso1:
    st.markdown(
        f"""
        <div class="tiktok-card">
            <h4 style="color: #00FF66; margin-top: 0;">{t["paso1_titulo"]}</h4>
            <p style="font-size: 14px; margin-bottom: 10px;">{t["paso1_desc"]}</p>
            <a href="https://www.tiktok.com/@sabermetriaia" target="_blank" style="background-color: #00FF66; color: #000000; padding: 8px 15px; border-radius: 6px; font-weight: bold; text-decoration: none; display: inline-block;">{t["btn_tiktok"]}</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col_paso2:
    st.markdown(
        f"""
        <div class="tiktok-card">
            <h4 style="color: #00FF66; margin-top: 0;">{t["paso2_titulo"]}</h4>
            <p style="font-size: 14px; margin-bottom: 15px;">{t["paso2_desc"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(t["btn_acceso"]):
      registrar_visita()
      st.session_state.autenticado = True
      st.rerun()
else:
  if lang == "es":
    st.markdown(
        f"""
        <div class="stats-banner">
            <h4 style="color: #00FF66; margin: 0;">🎯 Rendimiento del Modelo Sabermétrico (Evaluación de la Jornada)</h4>
            <p style="font-size: 15px; margin: 5px 0 0 0;">Aciertos del Modelo: <b>{ayer_str}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        f"""
        <div class="stats-banner">
            <h4 style="color: #00FF66; margin: 0;">🎯 Sabermetric Model Performance (Slate Evaluation)</h4>
            <p style="font-size: 15px; margin: 5px 0 0 0;">Model Hits: <b>{ayer_str}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  if menu == "Cartelera y Partidos":
    st.header(
        "📅 Cartelera de Partidos - Análisis Profundo (" + fecha_hoy + ")"
    )
    if df_cartelera.empty:
      st.warning(
          "⚠️ No hay partidos cargados en este momento en la cartelera. Por"
          " favor, sube un archivo CSV desde el Panel de Administración."
      )
    else:
      st.write(
          "Selecciona un encuentro para ver el desglose científico del modelo:"
      )

      opciones_dict = {}
      for _, row in df_cartelera.iterrows():
        e1 = str(row["equipo1"]).strip()
        e2 = str(row["equipo2"]).strip()
        label = e1 + " vs. " + e2
        opciones_dict[label] = row

      partido_seleccionado = st.selectbox(
          "Juegos de hoy:", list(opciones_dict.keys())
      )

      if partido_seleccionado:
        fila_juego = opciones_dict[partido_seleccionado]
        equipo1 = str(fila_juego["equipo1"]).strip()
        equipo2 = str(fila_juego["equipo2"]).strip()

        logo1_url = LOGOS_EQUIPOS.get(equipo1, "")
        logo2_url = LOGOS_EQUIPOS.get(equipo2, "")

        matchup_html = f"""
                <div class="matchup-box">
                    <div class="team-col"><img src="{logo1_url}" width="100" style="margin-bottom: 10px;"><h3 style="margin: 0; color: #ffffff;">{equipo1}</h3><span style="font-size: 12px; color: #8b949e;">(Visitante)</span></div>
                    <div class="vs-col">VS</div>
                    <div class="team-col"><img src="{logo2_url}" width="100" style="margin-bottom: 10px;"><h3 style="margin: 0; color: #ffffff;">{equipo2}</h3><span style="font-size: 12px; color: #8b949e;">(Local)</span></div>
                </div>
                """
        st.markdown(matchup_html, unsafe_allow_html=True)

        hora_val = str(fila_juego.get("hora", "19:30 (VE)"))
        sede_val = str(fila_juego.get("sede", "Arena Principal"))
        st.markdown(
            "🕒 **Hora (VE):** "
            + hora_val
            + " &nbsp;&nbsp;|&nbsp;&nbsp; 🏟️ **Sede:** "
            + sede_val
        )
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
          st.metric(
              label="Ganador Proyectado", value=str(fila_juego["ganador"])
          )
        with col2:
          st.metric(
              label="Total de Puntos (O/U)",
              value=str(fila_juego["total_puntos"]),
          )

        st.markdown("### 🧠 Razonamiento Táctico y Métricas Avanzadas")
        analisis_amplio = (
            str(fila_juego["analisis_es"])
            if lang == "es"
            else str(fila_juego["analisis_en"])
        )
        st.text(analisis_amplio)

        st.markdown("---")
        if st.button("📄 Descargar Análisis en PDF"):
          archivo_pdf = generar_pdf_analisis(
              equipo1 + " vs " + equipo2,
              hora_val,
              sede_val,
              str(fila_juego["ganador"]),
              str(fila_juego["total_puntos"]),
              analisis_amplio,
          )
          with open(archivo_pdf, "rb") as f:
            st.download_button(
                "💾 Guardar archivo PDF en tu equipo",
                data=f,
                file_name="reporte_sabermetria_nba.pdf",
                mime="application/pdf",
            )

  elif menu == "El Pulso de la Duela (Noticias)":
    st.header(
        "🧠 El Pulso de la Duela — Crónicas de Élite (" + fecha_hoy + ")"
    )
    st.markdown(
        "*Análisis con lupa, historias ocultas y periodismo deportivo de altura"
        " sobre la jornada anterior en la NBA.*"
    )
    st.markdown("---")

    mat_es, mat_en = cargar_noticias_txt()
    cronica_texto = mat_es if lang == "es" else mat_en

    st.markdown(cronica_texto)

  elif menu == "La Jugada Fija del Día":
    st.header("⭐ La Jugada Estelar del Modelo")
    if df_cartelera.empty:
      st.warning(
          "⚠️ No hay partidos cargados actualmente para mostrar la jugada fija."
      )
    else:
      st.success(
          "Recomendación avalada estrictamente por eficiencia matemática y"
          " métricas de posesión."
      )

      # Filtro robusto que busca booleano o string 'True'/'true'
      juegos_fijos = df_cartelera[
          df_cartelera["es_jugada_fija"].astype(str).str.lower().isin(["true", "1", "yes", "si"])
      ]
      juego_estelar = (
          juegos_fijos.iloc[0] if not juegos_fijos.empty else df_cartelera.iloc[0]
      )

      estelar_eq1 = str(juego_estelar["equipo1"]).strip()
      estelar_eq2 = str(juego_estelar["equipo2"]).strip()
      logo_estelar_1 = LOGOS_EQUIPOS.get(estelar_eq1, "")
