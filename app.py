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
  # Respaldo automático con los partidos de la jornada
  datos_respaldo = [
      {
          "equipo1": "Charlotte Hornets",
          "equipo2": "Washington Wizards",
          "hora": "19:00 (VE)",
          "sede": "Capital One Arena, Washington",
          "ganador": "Charlotte Hornets",
          "total_puntos": "231.5",
          "analisis_es": (
              "ANÁLISIS SABERMÉTRICO EXPERTO: Ritmo rápido y debilidad"
              " defensiva en la pintura de Washington. Charlotte asegura la"
              " victoria por mejor TS%."
          ),
          "analisis_en": (
              "EXPERT ANALYSIS: High pace and defensive weaknesses allow"
              " Charlotte to edge it."
          ),
          "es_jugada_fija": False,
      },
      {
          "equipo1": "Cleveland Cavaliers",
          "equipo2": "Minnesota Timberwolves",
          "hora": "19:00 (VE)",
          "sede": "Rocket Mortgage FieldHouse, Cleveland",
          "ganador": "Minnesota Timberwolves",
          "total_puntos": "221.0",
          "analisis_es": (
              "ANÁLISIS SABERMÉTRICO EXPERTO (⭐ JUGADA FIJA): Muralla"
              " defensiva de élite y Net Rating superior de los Wolves a"
              " domicilio."
          ),
          "analisis_en": (
              "EXPERT ANALYSIS (LOCK OF THE DAY): Wolves' elite defensive"
              " Net Rating secures the road win."
          ),
          "es_jugada_fija": True,
      },
      {
          "equipo1": "Boston Celtics",
          "equipo2": "Chicago Bulls",
          "hora": "19:30 (VE)",
          "sede": "TD Garden, Boston",
          "ganador": "Boston Celtics",
          "total_puntos": "228.5",
          "analisis_es": (
              "ANÁLISIS SABERMÉTRICO EXPERTO: Eficiencia perimetral"
              " estratosférica y control absoluto de pérdidas (TOV)."
          ),
          "analisis_en": (
              "EXPERT ANALYSIS: Absolute perimeter efficiency and superior"
              " ball security."
          ),
          "es_jugada_fija": False,
      },
      {
          "equipo1": "Miami Heat",
          "equipo2": "Dallas Mavericks",
          "hora": "19:30 (VE)",
          "sede": "Kaseya Center, Miami",
          "ganador": "Dallas Mavericks",
          "total_puntos": "225.0",
          "analisis_es": (
              "ANÁLISIS SABERMÉTRICO EXPERTO: El talento exterior de Dallas y"
              " su alto PER quiebran la defensa física de Miami."
          ),
          "analisis_en": (
              "EXPERT ANALYSIS: Dallas star efficiency breaks through Miami's"
              " gritty defense."
          ),
          "es_jugada_fija": False,
      },
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

# Menú lateral fijo y siempre disponible
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

# Banner superior de rendimiento
if lang == "es":
  st.markdown(
      f
