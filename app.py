def cargar_noticias():
  if os.path.exists(noticias_path):
    try:
      df = pd.read_csv(noticias_path)
      return (
          str(df.iloc[0]["matutina_es"]),
          str(df.iloc[0]["vespertina_es"]),
          str(df.iloc[0]["matutina_en"]),
          str(df.iloc[0]["vespertina_en"]),
      )
    except Exception:
      pass

  def_mat_es = (
      "• **Balance de Eficiencia Ofensiva:** Las primeras prácticas muestran un"
      " incremento en triples.\n• **Impacto en la Pintura:** Equipos con mayor"
      " diferencial de rebotes dominan."
  )
  def_vesp_es = (
      "• **Reporte de Lesiones:** Monitoreo en tiempo real de jugadores.\n•"
      " **Líneas de Apuestas:** Análisis de puntos totales."
  )
  def_mat_en = (
      "• **Offensive Efficiency Balance:** Early practices show an increase in"
      " three-pointers.\n• **Paint Impact:** Teams with higher rebound"
      " differentials dominate."
  )
  def_vesp_en = (
      "• **Injury Report:** Real-time player monitoring.\n• **Betting Lines:**"
      " Total points analysis."
  )

  guardar_noticias(def_mat_es, def_vesp_es, def_mat_en, def_vesp_en)
  return def_mat_es, def_vesp_es, def_mat_en, def_vesp_en
