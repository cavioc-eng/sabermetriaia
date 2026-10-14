elif menu == t["menu_diccionario"]:
        st.header(
            "📖 Diccionario Sabermétrico Educativo (Básico a Avanzado)"
            if lang == "es"
            else "📖 Educational Sabermetric Dictionary (Basic to Advanced)"
        )
        st.write(
            "Guía completa de referencia para comprender desde los"
            " fundamentos tradicionales hasta las métricas de eficiencia más"
            " avanzadas:"
            if lang == "es"
            else "Complete reference guide to understand everything from"
            " traditional fundamentals to advanced efficiency metrics:"
        )

        if lang == "es":
            st.markdown("""
                ### 🟢 Indicadores Básicos y Tradicionales (Box Score)
                - **PTS (Points / Puntos):** Total de puntos anotados por un jugador o equipo.
                - **REB (Rebounds / Rebotes):** Balones recuperados tras un lanzamiento fallido.
                - **AST (Assists / Asistencias):** Pases que conducen directamente a una canasta.
                - **STL (Steals / Recuperaciones):** Balones arrebatados al adversario.
                - **BLK (Blocks / Tapones):** Lanzamientos rivales bloqueados en el aire.
                - **TOV (Turnovers / Pérdidas):** Balones entregados al rival por errores.
                - **MIN (Minutes / Minutos):** Tiempo total que un jugador disputa en la duela.

                ### 🟡 Indicadores de Eficiencia Estándar
                - **FG% (Field Goal Percentage):** Porcentaje de tiros de campo encestados.
                - **3P% (Three-Point Percentage):** Eficacia en lanzamientos de larga distancia.
                - **FT% (Free Throw Percentage):** Precisión desde la línea de tiros libres.

                ### 🔴 Indicadores Avanzados y de Profundidad (Sabermetría IA)
                - **Pace (Ritmo):** Cantidad estimada de posesiones por cada 48 minutos.
                - **True Shooting Percentage (TS%):** Eficiencia ofensiva global (dobles, triples y libres).
                - **Net Rating:** Diferencia de puntos anotados y permitidos por 100 posesiones.
                - **Usage Rate (USG%):** Porcentaje de jugadas ofensivas que concluye un jugador en cancha.
                - **PER (Player Efficiency Rating):** Índice global de productividad por minuto.
                """)
        else:
            st.markdown("""
                ### 🟢 Basic & Traditional Indicators (Box Score)
                - **PTS (Points):** Total points scored by a player or team.
                - **REB (Rebounds):** Basketballs recovered after a missed shot.
                - **AST (Assists):** Passes leading directly to a field goal.
                - **STL (Steals):** Balls taken away from the opponent.
                - **BLK (Blocks):** Legal deflections of opponent shots.
                - **TOV (Turnovers):** Possessions lost due to unforced errors.
                - **MIN (Minutes):** Total time a player spends on the court.

                ### 🟡 Standard Efficiency Indicators
                - **FG% (Field Goal Percentage):** Ratio of successful field goals.
                - **3P% (Three-Point Percentage):** Shooting accuracy from beyond the arc.
                - **FT% (Free Throw Percentage):** Accuracy from the charity stripe.

                ### 🔴 Advanced & Deep Analytics (Sabermetria AI)
                - **Pace:** Estimated number of possessions per 48 minutes.
                - **True Shooting Percentage (TS%):** Comprehensive scoring efficiency.
                - **Net Rating:** Point differential per 100 possessions.
                - **Usage Rate (USG%):** Estimate of team plays used by a player.
                - **PER (Player Efficiency Rating):** Per-minute productivity rating.
                """)
