import os
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Sabermetría IA | NBA Analytics",
    page_icon="🏀",
    layout="wide",
)

# Título principal de la aplicación
st.title("🏀 SABERMETRÍA IA — Análisis Avanzado NBA")
st.markdown(
    "### *La ciencia de los datos, las métricas y los pronósticos milimétricos.*"
)
st.markdown("---")

# Archivo CSV de respaldo por defecto
cartelera_csv_path = "cartelera_hoy.csv"


# Función auxiliar para guardar cartelera localmente
def guardar_cartelera(df):
  try:
    df.to_csv(cartelera_csv_path, index=False, encoding="utf-8")
  except Exception:
    pass


# ==========================================
# GESTIÓN DE DATOS Y CARGA AUTOMÁTICA BLINDADA
# ==========================================
if (
    "df_cartelera" not in st.session_state
    or st.session_state["df_cartelera"] is None
    or st.session_state["df_cartelera"].empty
):
  if os.path.exists(cartelera_csv_path):
    try:
      df_cartelera = pd.read_csv(cartelera_csv_path, encoding="utf-8")
      st.session_state["df_cartelera"] = df_cartelera
    except Exception as e:
      st.error(f"Error al leer el archivo de respaldo: {e}")
      df_cartelera = pd.DataFrame()
  else:
    # 🛡️ RESPALDO AUTOMÁTICO INTERNO (Por si falta el archivo físico en GitHub)
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
        {
            "equipo1": "Milwaukee Bucks",
            "equipo2": "Indiana Pacers",
            "hora": "20:00 (VE)",
            "sede": "Fiserv Forum, Milwaukee",
            "ganador": "Milwaukee Bucks",
            "total_puntos": "239.5",
            "analisis_es": (
                "ANÁLISIS SABERMÉTRICO EXPERTO: Torbellino ofensivo con"
                " superioridad física en la pintura bajo los tableros (REB)."
            ),
            "analisis_en": (
                "EXPERT ANALYSIS: Bucks leverage interior muscle to win a"
                " high-scoring track meet."
            ),
            "es_jugada_fija": False,
        },
        {
            "equipo1": "Oklahoma City Thunder",
            "equipo2": "Phoenix Suns",
            "hora": "20:00 (VE)",
            "sede": "Paycom Center, Oklahoma City",
            "ganador": "Oklahoma City Thunder",
            "total_puntos": "230.0",
            "analisis_es": (
                "ANÁLISIS SABERMÉTRICO EXPERTO: Dinamismo en velocidad y presión"
                " constante al aro para castigar en la línea de libres."
            ),
            "analisis_en": (
                "EXPERT ANALYSIS: Thunder's athletic depth wears down Phoenix"
                " in the fourth."
            ),
            "es_jugada_fija": False,
        },
        {
            "equipo1": "Houston Rockets",
            "equipo2": "Atlanta Hawks",
            "hora": "20:30 (VE)",
            "sede": "Toyota Center, Houston",
            "ganador": "Houston Rockets",
            "total_puntos": "233.0",
            "analisis_es": (
                "ANÁLISIS SABERMÉTRICO EXPERTO: Dominio absoluto en rebotes"
                " ofensivos y mayor efectividad efectiva de tiro (eFG%)."
            ),
            "analisis_en": (
                "EXPERT ANALYSIS: Houston dominates second-chance points on the"
                " glass."
            ),
            "es_jugada_fija": False,
        },
        {
            "equipo1": "Utah Jazz",
            "equipo2": "Memphis Grizzlies",
            "hora": "21:00 (VE)",
            "sede": "Delta Center, Salt Lake City",
            "ganador": "Memphis Grizzlies",
            "total_puntos": "234.0",
            "analisis_es": (
                "ANÁLISIS SABERMÉTRICO EXPERTO: Memphis capitaliza los errores y"
                " pérdidas de balón (TOV) de Utah para correr el contraataque."
            ),
            "analisis_en": (
                "EXPERT ANALYSIS: Grizzlies punish sloppy ball handling with"
                " fast-break efficiency."
            ),
            "es_jugada_fija": False,
        },
        {
            "equipo1": "Denver Nuggets",
            "equipo2": "Golden State Warriors",
            "hora": "22:00 (VE)",
            "sede": "Ball Arena, Denver",
            "ganador": "Denver Nuggets",
            "total_puntos": "232.5",
            "analisis_es": (
                "ANÁLISIS SABERMÉTRICO EXPERTO: Inteligencia colectiva de pases"
                " (AST) y el factor de desgaste por la altitud en Denver."
            ),
            "analisis_en": (
                "EXPERT ANALYSIS: Altitude fatigue and home paint dominance secure"
                " Denver's win."
            ),
            "es_jugada_fija": False,
        },
    ]
    df_cartelera = pd.DataFrame(datos_respaldo)
    guardar_cartelera(df_cartelera)
    st.session_state["df_cartelera"] = df_cartelera
else:
  df_cartelera = st.session_state["df_cartelera"]

# ==========================================
# PESTAÑAS PRINCIPALES DE NAVEGACIÓN
# ==========================================
tab_cartelera, tab_admin = st.tabs(
    ["📊 Cartelera y Pronósticos", "⚙️ Panel de Administración"]
)

with tab_cartelera:
  st.subheader("🔥 Partidos y Análisis Sabermétrico de la Jornada")

  if df_cartelera.empty:
    st.info("ℹ️ La cartelera se encuentra actualmente vacía.")
  else:
    for idx, row in df_cartelera.iterrows():
      es_fija = (
          str(row.get("es_jugada_fija", False)).strip().lower()
          in ["true", "1", "yes", "si"]
      )

      with st.container():
        if es_fija:
          st.markdown("### ⭐ **JUGADA FIJA DEL DÍA** ⭐")

        col1, col2, col3 = st.columns([3, 2, 3])
        with col1:
          st.markdown(f"**🏠 Local:** {row['equipo1']}")
        with col2:
          st.markdown(
              f"🕒 **{row['hora']}**<br>📍 _{row['sede']}_", unsafe_allow_html=True
          )
        with col3:
          st.markdown(f"**✈️ Visitante:** {row['equipo2']}")

        st.markdown(
            f"🎯 **Pronóstico Ganador:** `{row['ganador']}` &nbsp;&nbsp;|&nbsp;&nbsp;"
            f" 📈 **Puntos Totales (O/U):** `{row['total_puntos']}`"
        )

        with st.expander(
            f"🔍 Ver Análisis Científico Detallado — {row['equipo1']} vs"
            f" {row['equipo2']}"
        ):
          st.markdown(f"**Español:**\n\n{row['analisis_es']}")
          st.markdown(f"**English:**\n\n{row['analisis_en']}")

        st.markdown("---")

with tab_admin:
  st.subheader("🔐 Panel de Administración Protegido")
  password = st.text_input("Ingrese la clave de administrador:", type="password")

  if password == "sabermetria2026":
    st.success("¡Acceso autorizado!")

    st.markdown("---")
    st.subheader("📁 Carga Masiva de Cartelera por Archivo CSV")
    archivo_subido = st.file_uploader(
        "Sube tu archivo .csv con la programación:", type=["csv"]
    )

    if archivo_subido is not None:
      try:
        df_nuevo = pd.read_csv(archivo_subido, encoding="utf-8")
        st.session_state["df_cartelera"] = df_nuevo
        guardar_cartelera(df_nuevo)
        st.success(
            "¡Cartelera actualizada masivamente y guardada en el respaldo"
            " local con éxito!"
        )
        st.rerun()
      except Exception as e:
        st.error(f"Error al procesar el archivo CSV: {e}")

    st.markdown("---")
    st.subheader("📁 Cartelera Actual Cargada en el Sistema")

    if df_cartelera.empty:
      st.info("ℹ️ La cartelera se encuentra actualmente vacía.")
    else:
      st.dataframe(df_cartelera, use_container_width=True)

    # Botón para vaciar / borrar toda la cartelera
    if st.button("🗑️ Vaciar / Borrar Toda la Cartelera"):
      if os.path.exists(cartelera_csv_path):
        try:
          os.remove(cartelera_csv_path)
        except Exception:
          pass

      df_vacio = pd.DataFrame(
          columns=[
              "equipo1",
              "equipo2",
              "hora",
              "sede",
              "ganador",
              "total_puntos",
              "analisis_es",
              "analisis_en",
              "es_jugada_fija",
          ]
      )
      st.session_state["df_cartelera"] = df_vacio
      st.success(
          "¡Se ha vaciado la cartelera y borrado el archivo local exitosamente!"
      )
      st.rerun()

  elif password != "":
    st.error("Clave incorrecta. Acceso denegado.")
