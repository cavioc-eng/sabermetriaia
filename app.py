import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import leaguegamelog

# Configuración de la página
st.set_page_config(page_title="Sabermetría IA - Pretemporada NBA", page_icon="🏀", layout="wide")

@st.cache_data(ttl=3600)
def cargar_pretemporada_nba(season="2026-27"):
    try:
        game_log = leaguegamelog.LeagueGameLog(
            season=season, 
            season_type_all_star="Pre Season"
        )
        df = game_log.get_data_frames()[0]
        
        if df.empty:
            return None

        df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
        df['PTS'] = pd.to_numeric(df['PTS'])
        
        columnas_clave = [
            'GAME_ID', 'GAME_DATE', 'TEAM_ABBREVIATION', 
            'MATCHUP', 'WL', 'PTS', 'FGM', 'FGA', 'FG_PCT', 
            'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 
            'AST', 'REB', 'TOV', 'PLUS_MINUS'
        ]
        
        df_limpio = df[columnas_clave].copy()
        df_limpio = df_limpio.sort_values('GAME_DATE', ascending=False)
        return df_limpio
        
    except Exception as e:
        st.error(f"Error al conectar con la API de la NBA: {e}")
        return None

# Panel de Administrador en la barra lateral
with st.sidebar:
    st.subheader("⚙️ Panel de Administrador")
    if st.button("🔄 Actualizar Datos de Pretemporada"):
        st.cache_data.clear()
        st.success("¡Caché limpiada con éxito!")
        st.rerun()

# Interfaz principal
st.title("🏀 Sabermetría IA - Monitoreo de Pretemporada")
st.write("Seguimiento automatizado y análisis de eficiencia en tiempo real para la pretemporada de la NBA.")

with st.spinner("Sincronizando registros de pretemporada..."):
    df_stats = cargar_pretemporada_nba()

if df_stats is not None and not df_stats.empty:
    st.metric("Total de Registros Analizados", len(df_stats))
    
    # Filtro interactivo por franquicia
    equipos = sorted(df_stats['TEAM_ABBREVIATION'].unique())
    equipo_seleccionado = st.selectbox("Filtrar por Equipo:", ["Todos los equipos"] + equipos)
    
    if equipo_seleccionado != "Todos los equipos":
        df_mostrar = df_stats[df_stats['TEAM_ABBREVIATION'] == equipo_seleccionado]
    else:
        df_mostrar = df_stats

    st.subheader("Últimos Partidos Registrados")
    st.dataframe(df_mostrar[['GAME_DATE', 'TEAM_ABBREVIATION', 'MATCHUP', 'WL', 'PTS', 'PLUS_MINUS']], use_container_width=True)
else:
    st.warning("No se encontraron registros de pretemporada disponibles en este momento.")
