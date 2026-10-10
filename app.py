import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Sabermetría IA - Pretemporada NBA", page_icon="🏀", layout="wide")

@st.cache_data
def cargar_pretemporada_local():
    try:
        # Lee el archivo CSV sincronizado en el repositorio de GitHub
        df = pd.read_csv("pretemporada_nba_2026_limpio.csv")
        df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
        return df
    except Exception as e:
        st.error(f"No se pudo cargar el archivo de datos: {e}")
        return None

# Panel de Administrador en la barra lateral
with st.sidebar:
    st.subheader("⚙️ Panel de Administrador")
    st.info("💡 **Estado:** Conectado a la base de datos local optimizada para la nube.")
    if st.button("🔄 Recargar Datos"):
        st.cache_data.clear()
        st.success("¡Caché actualizada!")
        st.rerun()

# Interfaz principal
st.title("🏀 Sabermetría IA - Monitoreo de Pretemporada")
st.write("Seguimiento automatizado y análisis de eficiencia en tiempo real para la pretemporada de la NBA.")

# Carga de datos
df_stats = cargar_pretemporada_local()

if df_stats is not None and not df_stats.empty:
    st.metric("Total de Registros Analizados", len(df_stats))
    
    # Filtro interactivo por equipo
    equipos = sorted(df_stats['TEAM_ABBREVIATION'].unique())
    equipo_seleccionado = st.selectbox("Filtrar por Equipo:", ["Todos los equipos"] + equipos)
    
    if equipo_seleccionado != "Todos los equipos":
        df_mostrar = df_stats[df_stats['TEAM_ABBREVIATION'] == equipo_seleccionado]
    else:
        df_mostrar = df_stats

    st.subheader("Últimos Partidos Registrados")
    st.dataframe(df_mostrar[['GAME_DATE', 'TEAM_ABBREVIATION', 'MATCHUP', 'WL', 'PTS', 'PLUS_MINUS']], use_container_width=True)
else:
    st.warning("Asegúrate de haber subido el archivo 'pretemporada_nba_2026_limpio.csv' al repositorio principal de GitHub.")
