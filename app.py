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
      df_cartelera = pd.DataFrame(
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
  else:
    df_cartelera = pd.DataFrame(
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
    st.info(
        "ℹ️ La cartelera se encuentra actualmente vacía. Por favor, ve al"
        " Panel de Administración para cargar los encuentros."
    )
  else:
    for idx, row in df_cartelera.iterrows():
      # Destacar si es la Jugada Fija
      es_fija = (
          str(row.get("es_jugada_fija", False)).strip().lower()
          in ["true", "1", "yes", "si"]
      )

      with st.container():
        if es_fija:
          st.markdown(
              f"### ⭐ **JUGADA FIJA DEL DÍA** ⭐"
          )

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
