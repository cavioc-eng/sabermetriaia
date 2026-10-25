import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Sabermetría IA",
    page_icon="🏀",
    layout="wide"
)

def mostrar_centro_de_noticias():
    st.markdown("---")
    st.markdown("## 🧠 El Pulso de la Duela")
    st.markdown("*Crónicas de élite, análisis con lupa y las historias ocultas de cada jornada en la NBA.*")
    st.markdown("---")

    # Contenido de la Edición Matutina Única (Actualizada)
    st.markdown("### 🏀 Épica en la Altura y Corazón de Perdedor: Las Historias Ocultas de una Noche de Ocho Batallas")
    st.markdown("*Fecha: Edición Principal / Matutina*")
    
    st.markdown("""
    #### 1. La remontada de película en Denver y el show de los 42 puntos
    Anoche la liga entera contuvo la respiración en el Ball Arena. Los Denver Nuggets gesticularon una obra maestra de carácter al levantarse de una desventaja de 23 puntos ante unos rebeldes New Orleans Pelicans, forzar la prórroga y sentenciar un **141-135** inolvidable. 
    
    Mientras **Nikola Jokic** firmaba un triple-doble titánico de 35 puntos, 15 rebotes y 10 asistencias (anotando 8 de sus unidades vitales en el tiempo extra) y **Jamal Murray** explotaba con **42 puntos**, el verdadero drama estuvo en el margen milimétrico de la estrategia: los Pelicans rozaron la hazaña a domicilio, pero la profundidad física de Denver en los minutos de máxima presión quebró la resistencia de Luisiana.
    """)

    st.markdown("""
    #### 2. La hazaña silenciosa del novato que hizo temblar a los Wizards
    En el baloncesto moderno solemos aplaudir únicamente al que levanta los brazos al final, ignorando gestas monumentales de quienes se quedan en la orilla. Anoche, en la dura caída de los Chicago Bulls por **124-120** ante Washington, el joven novato **Caleb Wilson** escribió su nombre con letras de oro al despacharse una noche colosal de **30 puntos y 14 rebotes**. 
    
    Soportar esa carga en la pintura frente a veteranía y galones es una hazaña individual de alcances históricos que ningún titular principal quiso destacar, pero que nuestra lupa analítica consagra como el destello de una futura superestrella.
    """)

    st.markdown("""
    #### 3. La maestría invisible de Devin Booker en el desierto
    En Phoenix, los Suns doblegaron **131-122 en prórroga** a unos Golden State Warriors que sufren un inicio de temporada agónico (0-3 por primera vez desde 2007). 
    
    Más allá de los **43 puntos** magistrales de Booker (con una eficiencia escandalosa de 17 de 25 en tiros de campo), la clave silenciosa del partido radicó en cómo los aleros de Phoenix cerraron las líneas de pase perimetral en el suplementario, asfixiando por completo el circuito de rotación visitante. El verdadero baloncesto se gana en los centímetros que nadie ve.
    """)

    st.markdown("---")
    st.markdown("### 🇺🇸 The Pulse of the Hardwood (English Edition)")
    st.markdown("""
    #### High-Altitude Epic and Underdog Grit: The Untold Stories Behind an Eight-Game Slate
    * **Denver's Cinematic Comeback:** Erasing a 23-deficit, Nikola Jokic's masterclass (35 PTS, 15 REB, 10 AST) and Jamal Murray's 41-point explosion secured an unforgettable 141-135 OT thriller against New Orleans.
    * **Caleb Wilson's Silent Masterpiece:** In Chicago's razor-thin 124-120 loss to Washington, rookie Caleb Wilson carved his name with a colossal 30-point, 14-rebound performance under immense paint pressure.
    * **Devin Booker's Desert Mastery:** Outlasting Golden State 131-122 in overtime, Booker's 43-point night and stellar wing defense plunged the Warriors into an unaccustomed 0-3 start.
    """)

def main():
    st.title("🏀 Sabermetría IA - Analítica Avanzada de Básquetbol")
    # Ejecutamos la función de noticias directamente en la vista principal
    mostrar_centro_de_noticias()

if __name__ == "__main__":
    main()
