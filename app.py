import os
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Sabermetría IA | NBA Analytics",
    page_icon="🏀",
    layout="wide",
)

# Archivos de respaldo local
cartelera_csv_path = "cartelera_hoy.csv"
efectividad_txt_path = "efectividad_modelo.txt"


# Funciones auxiliares de persistencia
def guardar_cartelera(df):
  try:
    df.to_csv(cartelera_csv_path, index=False, encoding="utf-8")
  except Exception:
    pass


def cargar_efectividad():
  if os.path.exists(efectividad_txt_path):
    try:
      with open(efectividad_txt_path, "r", encoding="utf-8") as f:
        return f.read().strip()
    except Exception:
      pass
  return "5 de 7 (71.4% de efectividad)"


def guardar_efectividad(texto):
  try:
    with open(efectividad_txt_path, "w", encoding="utf-8") as f:
      f.write(texto)
  except Exception:
    pass


# ==========================================
# GESTIÓN DE DATOS Y CARGA AUTOMÁTICA
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
    # Respaldo automático con los 9 partidos de hoy
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
                " su alto PER quiebran la defensa física di Miami."
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
# MENÚ DE NAVEGACIÓN LATERAL (SIDEBAR)
# ==========================================
st.sidebar.image(
    "https://img.icons8.com/color/96/basketball.png", width=80
)  # Ícono decorativo
st.sidebar.title("🏀 Sabermetría IA")
st.sidebar.markdown(
    "*Plataforma de Analítica Avanzada y Pronósticos Milimétricos.*"
)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Seleccionar Sección:",
    [
        "📊 Cartelera y Pronósticos",
        "📰 Noticias y Crónica",
        "📖 Diccionario Sabermétrico",
        "⚙️ Panel de Administración",
    ],
)

# ==========================================
# SECCIÓN 1: CARTELERA Y PRONÓSTICOS (Con descarga PDF por juego)
# ==========================================
if menu == "📊 Cartelera y Pronósticos":
  st.title("🏀 SABERMETRÍA IA — Análisis Avanzado NBA")
  st.markdown(
      "### *La ciencia de los datos, las métricas y los pronósticos"
      " milimétricos.*"
  )
  st.markdown("---")
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
            f"🔍 Ver Análisis Científico y Descargar PDF — {row['equipo1']} vs"
            f" {row['equipo2']}"
        ):
          st.markdown(f"**Español:**\n\n{row['analisis_es']}")
          st.markdown(f"**English:**\n\n{row['analisis_en']}")

          # Botón de descarga de reporte del juego individual
          texto_pdf = (
              f"SABERMETRÍA IA - REPORTE DE ENCUENTRO\n"
              f"=====================================\n"
              f"Encuentro: {row['equipo1']} vs {row['equipo2']}\n"
              f"Hora: {row['hora']} | Sede: {row['sede']}\n"
              f"Pronóstico Ganador: {row['ganador']}\n"
              f"Puntos Totales (O/U): {row['total_puntos']}\n\n"
              f"ANÁLISIS EN ESPAÑOL:\n{row['analisis_es']}\n\n"
              f"EXPERT ANALYSIS (ENGLISH):\n{row['analisis_en']}\n"
          )
          st.download_button(
              label=(
                  f"📥 Descargar Análisis en PDF / TXT — {row['equipo1']} vs"
                  f" {row['equipo2']}"
              ),
              data=texto_pdf,
              file_name=(
                  f"Analisis_{row['equipo1'].replace(' ', '_')}_vs_{row['equipo2'].replace(' ', '_')}.txt"
              ),
              mime="text/plain",
              key=f"pdf_btn_{idx}",
          )

        st.markdown("---")

# ==========================================
# SECCIÓN 2: NOTICIAS Y CRÓNICA DEL DÍA
# ==========================================
elif menu == "📰 Noticias y Crónica":
  st.title("🏀 SABERMETRÍA IA — Análisis Avanzado NBA")
  st.markdown(
      "### *La ciencia de los datos, las métricas y los pronósticos"
      " milimétricos.*"
  )
  st.markdown("---")
  st.subheader("📰 El Pulso de la Duela — Crónica Editorial de Élite")
  st.markdown(
      "*Lectura profunda de rendimiento, métricas de eficiencia y lecciones"
      " tácticas de la jornada.*"
  )
  st.markdown("---")

  idioma_noticia = st.radio(
      "Seleccionar Idioma / Language:", ["Español", "English"]
  )

  if idioma_noticia == "Español":
    st.markdown("""
        ### 🏀🏹 Eficiencia Asesina y Dominio en la Pintura: Las Lecciones Tácticas de una Jornada de Alto Voltaje
        
        La jornada anterior nos dejó lecciones tácticas fascinantes que van mucho más allá del marcador final. El modelo sabermétrico de la liga demostró que la eficiencia ofensiva y el control del *Pace* son los verdaderos reyes de la duela.
        
        **1. La "Jugada Fija" Se Cumple con Autoridad en Toronto 🐺**
        Nuestra recomendación estelar de la jornada, los **Minnesota Timberwolves**, no decepcionaron. En un partido controlado de principio a fin (117-94), los Wolves dictaron un ritmo pausado (*Pace* bajo) que asfixió el ataque de los Raptors. La clave fue la **eficiencia global real (*TS%*)** de sus piezas estelares.
        
        **2. El Espectáculo de Curry y la Lección de Eficiencia de los Lakers 🔥**
        Los **Angeles Lakers** protagonizaron una victoria de alto octanaje frente al Jazz (132-123), en un encuentro donde el *Pace* fue vertiginoso. Lo sorprendente no fueron los 30 puntos de LeBron James, sino su **eficiencia real (*TS%*)** en la media distancia.
        
        **3. La Profundidad de Banquillo de los Pacers Sorprende a Brooklyn 🤝**
        En el duelo más sorpresivo de la noche, los **Indiana Pacers** superaron a los Brooklyn Nets (136-109). La estadística no miente: el **Net Rating de la segunda unidad** de Indiana fue abismalmente superior.
        
        **En resumen:** La jornada confirmó que los equipos que controlan el ritmo, maximizan la eficiencia por posesión y confían en la profundidad de su rotación son los que dominan el escenario de la NBA.
        """)
  else:
    st.markdown("""
        ### 🏀🏹 Lethal Efficiency and Paint Dominance: High-Voltage Tactical Lessons
        
        Yesterday’s slate offered fascinating tactical lessons that extend far beyond the final score. The league's sabermetric model proved that offensive efficiency and Pace control are the true kings of the court.
        
        **1. The "Lock of the Day" Delivers with Authority in Toronto 🐺**
        Our featured recommendation of the day, the **Minnesota Timberwolves**, did not disappoint. In a controlled game from start to finish (117-94), the Wolves dictated a slow tempo (*low Pace*) that suffocated Toronto's attack.
        
        **2. Curry’s Showcase and the Lakers’ Efficiency Lesson 🔥**
        The **Los Angeles Lakers** secured a high-octane victory against the Jazz (132-123), in a game where the *Pace* was breakneck. LeBron James delivered stellar mid-range efficiency.
        
        **3. Pacers’ Bench Depth Stuns Brooklyn 🤝**
        In the most surprising matchup of the night, the **Indiana Pacers** overpowered the Brooklyn Nets (136-109). The bench Net Rating for Indiana was astronomically higher.
        
        **In Summary:** Yesterday’s games confirmed that teams that control the tempo, maximize efficiency per possession, and trust the depth of their rotation are the ones dominating the NBA stage.
        """)

# ==========================================
# SECCIÓN 3: DICCIONARIO SABERMÉTRICO
# ==========================================
elif menu == "📖 Diccionario Sabermétrico":
  st.title("🏀 SABERMETRÍA IA — Análisis Avanzado NBA")
  st.markdown(
      "### *La ciencia de los datos, las métricas y los pronósticos"
      " milimétricos.*"
  )
  st.markdown("---")
  st.subheader("📖 Diccionario Sabermétrico y Guía de Métricas")
  st.markdown(
      "*Guía completa para comprender los indicadores científicos utilizados en"
      " nuestros modelos de predicción.*"
  )
  st.markdown("---")

  st.markdown("🟢 **Indicadores Básicos y Tradicionales (Box Score)**")
  st.markdown(
      "- **PTS (Points / Puntos):** Total de puntos anotados por un jugador o"
      " equipo."
  )
  st.markdown(
      "- **REB (Rebounds / Rebotes):** Balones recuperados tras un lanzamiento"
      " fallido."
  )
  st.markdown(
      "- **AST (Assists / Asistencias):** Pases que conducen directamente a una"
      " canasta."
  )
  st.markdown(
      "- **STL (Steals / Recuperaciones):** Balones arrebatados al adversario."
  )
  st.markdown(
      "- **BLK (Blocks / Tapones):** Lanzamientos rivales bloqueados en el aire."
  )
  st.markdown(
      "- **TOV (Turnovers / Pérdidas):** Balones entregados al rival por"
      " errores."
  )
  st.markdown(
      "- **MIN (Minutes / Minutos):** Tiempo total que un jugador disputa en la"
      " duela."
  )

  st.markdown("---")
  st.markdown("🟡 **Indicadores de Eficiencia Estándar**")
  st.markdown(
      "- **FG% (Field Goal Percentage):** Porcentaje de tiros de campo"
      " encestados."
  )
  st.markdown(
      "- **3P% (Three-Point Percentage):** Eficacia en lanzamientos de larga"
      " distancia."
  )
  st.markdown(
      "- **FT% (Free Throw Percentage):** Precisión desde la línea de tiros"
      " libres."
  )

  st.markdown("---")
  st.markdown("🔴 **Indicadores Avanzados y de Profundidad (Sabermetría IA)**")
  st.markdown(
      "- **Pace (Ritmo):** Cantidad estimada de posesiones por cada 48 minutos."
  )
  st.markdown(
      "- **True Shooting Percentage (TS%):** Eficiencia ofensiva global (dobles,"
      " triples y libres)."
  )
  st.markdown(
      "- **Net Rating:** Diferencia de puntos anotados y permitidos por 100"
      " posesiones."
  )
  st.markdown(
      "- **Usage Rate (USG%):** Porcentaje de jugadas ofensivas que concluye"
      " un jugador en cancha."
  )
  st.markdown(
      "- **PER (Player Efficiency Rating):** Índice global de productividad por"
      " minuto."
  )

# ==========================================
# SECCIÓN 4: PANEL DE ADMINISTRACIÓN
# ==========================================
elif menu == "⚙️ Panel de Administración":
  st.title("🏀 SABERMETRÍA IA — Análisis Avanzado NBA")
  st.markdown(
      "### *La ciencia de los datos, las métricas y los pronósticos"
      " milimétricos.*"
  )
  st.markdown("---")
  st.subheader("🔐 Panel de Administración Protegido")
  password = st.text_input("Ingrese la clave de administrador:", type="password")

  if password == "sabermetria2026":
    st.success("¡Acceso autorizado!")

    st.markdown("---")
    st.subheader("🎯 Gestor de Efectividad del Modelo")
    efectividad_actual = cargar_efectividad()
    nuevo_efectividad = st.text_input(
        "Aciertos de la Jornada (Ej: 5 de 7 aciertos (71.4%)):",
        value=efectividad_actual,
    )
    if st.button("💾 Guardar Efectividad"):
      guardar_efectividad(nuevo_efectividad)
      st.success("¡Efectividad actualizada con éxito!")

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
