elif menu == "Panel de Administración":
    st.header("🔐 Panel de Control y Publicación - Sabermetría IA")
    st.write("Control estadístico, cartelera, apuestas y crónicas editoriales.")

    clave_admin = st.text_input("Ingresa la clave de administrador:", type="password", key="input_clave_admin")

    if clave_admin == "sabermetria2026":
        st.success("¡Acceso de administrador concedido!")

        if os.path.exists(db_usuarios_path):
            df_visitas = pd.read_csv(db_usuarios_path, encoding="utf-8")
            st.metric(label="Total de Ingresos Acumulados al Portal", value=len(df_visitas))
            st.dataframe(df_visitas, use_container_width=True)
        else:
            st.metric(label="Total de Ingresos Acumulados al Portal", value=0)

        st.markdown("---")
        st.subheader("📤 Carga Masiva de Cartelera de Partidos (CSV)")
        csv_ejemplo = df_cartelera.to_csv(index=False).encode("utf-8")
        st.download_button(label="📥 Descargar Plantilla CSV de Partidos", data=csv_ejemplo, file_name="plantilla_cartelera_ejemplo.csv", mime="text/csv")

        archivo_subido = st.file_uploader("Selecciona el archivo CSV de partidos:", type=["csv"], key="up_cartelera")
        if archivo_subido is not None:
            try:
                df_nuevo_csv = pd.read_csv(archivo_subido, encoding="utf-8")
                guardar_cartelera(df_nuevo_csv)
                st.success("¡Cartelera actualizada con éxito!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        if st.button("🗑️ Vaciar / Borrar Toda la Cartelera"):
            if os.path.exists(cartelera_csv_path):
                os.remove(cartelera_csv_path)
            guardar_cartelera(pd.DataFrame(columns=["equipo1", "equipo2", "hora", "sede", "ganador", "total_puntos", "analisis_es", "analisis_en", "es_jugada_fija"]))
            st.success("¡Cartelera vaciada!")
            st.rerun()

        st.markdown("---")
        st.subheader("🇺🇸 Carga Masiva de Apuestas y Proyecciones USA (CSV)")
        csv_apuestas_ejemplo = df_apuestas.to_csv(index=False).encode("utf-8") if not df_apuestas.empty else "equipo1,equipo2,spread,total_ou,proyeccion_usa,probabilidad\nOrlando Magic,Boston Celtics,-8.5,220.5,Pick: Boston Celtics | Line: -8.5 | Conf: 91.0%,91.0".encode("utf-8")
        st.download_button(label="📥 Descargar Plantilla CSV de Apuestas USA", data=csv_apuestas_ejemplo, file_name="plantilla_apuestas_usa.csv", mime="text/csv")

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

        st.markdown("---")
        ayer_act = cargar_estadisticas()
        with st.form("form_estadisticas"):
            nuevo_ayer = st.text_input("Aciertos de la Jornada (Ej: 6 / 10 (60.0%)):", value=ayer_act)
            if st.form_submit_button("💾 Guardar Efectividad"):
                guardar_estadisticas(nuevo_ayer)
                st.success("¡Efectividad actualizada con transparencia!")
                st.rerun()

        mat_es_act, mat_en_act = cargar_noticias_txt()
        with st.form("form_noticias_txt"):
            txt_mat_es = st.text_area("Crónica (Español):", value=mat_es_act, height=180)
            txt_mat_en = st.text_area("Editorial (English):", value=mat_en_act, height=180)
            if st.form_submit_button("💾 Guardar y Publicar Crónica"):
                guardar_noticias_txt(txt_mat_es, txt_mat_en)
                st.success("¡Crónica publicada con éxito!")
                st.rerun()

    elif clave_admin != "":
        st.error("❌ Clave de administrador incorrecta.")
