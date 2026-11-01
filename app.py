st.markdown("---")
        st.subheader("🇺🇸 Carga Masiva de Apuestas y Proyecciones USA (CSV)")
        
        # Generar DataFrame en memoria para la plantilla de apuestas de forma segura
        df_plantilla_apuestas = pd.DataFrame([
            {"equipo1": "Orlando Magic", "equipo2": "Boston Celtics", "spread": "-8.5", "total_ou": "220.5", "proyeccion_usa": "Pick: Boston Celtics | Line: -8.5 | Conf: 91.0%", "probabilidad": 91.0},
            {"equipo1": "Indiana Pacers", "equipo2": "Brooklyn Nets", "spread": "-5.5", "total_ou": "234.0", "proyeccion_usa": "Pick: Indiana Pacers | Line: -5.5 | Conf: 87.5%", "probabilidad": 87.5}
        ])
        
        csv_apuestas_bytes = df_plantilla_apuestas.to_csv(index=False, encoding="utf-8").encode("utf-8")
        st.download_button(
            label="📥 Descargar Plantilla CSV de Apuestas USA", 
            data=csv_apuestas_bytes, 
            file_name="plantilla_apuestas_usa.csv", 
            mime="text/csv"
        )

        archivo_apuestas_subido = st.file_uploader("Selecciona el archivo CSV de Apuestas USA:", type=["csv"], key="up_apuestas")
        if archivo_apuestas_subido is not None:
            try:
                df_nuevo_apuestas = pd.read_csv(archivo_apuestas_subido, encoding="utf-8")
                df_nuevo_apuestas.to_csv(apuestas_csv_path, index=False, encoding="utf-8")
                st.success("¡Apuestas USA actualizadas con éxito!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        if st.button("🗑️ Vaciar / Borrar Tabla de Apuestas USA"):
            if os.path.exists(apuestas_csv_path):
                os.remove(apuestas_csv_path)
            pd.DataFrame(columns=["equipo1", "equipo2", "spread", "total_ou", "proyeccion_usa", "probabilidad"]).to_csv(apuestas_csv_path, index=False, encoding="utf-8")
            st.success("¡Tabla de apuestas vaciada!")
            st.rerun()
