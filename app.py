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
      "Epica en la Altura y Corazon de Perdedor: Las Historias Ocultas de"
      " una Noche de Ocho Batallas\n\n• La remontada de película en Denver:"
      " Nikola Jokic y Jamal Murray guiaron a los Nuggets en un infartante"
      " 141-135 en prórroga frente a unos aguerridos Pelicans.\n\n• La hazaña del"
      " novato: Caleb Wilson brilló con 30 puntos y 14 rebotes en la dura caída"
      " de los Bulls ante Washington."
  )
  default_mat_en = (
      "High-Altitude Epic and Underdog Grit: The Untold Stories Behind an"
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


st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #00FF66; color: #000000; font-weight: bold; border-radius: 8px; }
    .matchup-box { display: flex; align-items: center; justify-content: space-around; text-align: center; padding: 15px; background-color: #161b22; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 20px; }
    .team-col { flex: 1; display: flex; flex-direction: column; align-items: center; }
    .vs-col { flex: 0 0 100px; font-size: 32px; font-weight: bold; color: #00FF66; text-align: center; }
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
  ]
  df_resp = pd.DataFrame(datos_respaldo)
  guardar_cartelera(df_resp)
  return df_resp


def guardar_cartelera(df):
  try:
    df.to_csv(cartelera_csv_path, index=False, encoding="utf-8")
  except Exception:
    pass


idioma = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
lang = "es" if idioma == "Español" else "en"

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
        "Panel de Administración",
    ],
)

fecha_hoy = datetime.now().strftime("%d de %B de %Y")
df_cartelera = cargar_cartelera()
ayer_str = cargar_estadisticas()

if lang == "es":
  st.markdown(
      f"""
    <div class="stats-banner">
        <h4 style="color: #00FF66; margin: 0;">Rendimiento del Modelo Sabermétrico (Evaluación de la Jornada)</h4>
        <p style="font-size: 15px; margin: 5px 0 0 0;">Aciertos del Modelo: <b>{ayer_str}</b></p>
    </div>
    """,
      unsafe_allow_html=True,
  )
else:
  st.markdown(
      f"""
