import json
import streamlit as st

st.subheader("⚡ Carga Masiva de Cartelera (Modo Avanzado)")
st.info(
    "Pega aquí abajo el bloque completo de partidos en formato JSON para"
    " actualizar toda la cartelera de golpe de forma segura."
)

# Ejemplo de estructura esperada para guiar al administrador
ejemplo_json = [
    {
        "visitante": "Orlando Magic",
        "local": "Cleveland Cavaliers",
        "hora": "19:00 (VE)",
        "sede": "Rocket Arena (Cleveland, OH)",
        "ganador": "Cleveland Cavaliers (-4.5 pts)",
        "ou": "217.5 (Bajas / Under)",
        "jugada_fija": True,
        "analisis_es": (
            "El modelo sabermétrico de eficiencia neta..."
        ),
        "analisis_en": "The sabermetric net efficiency...",
    }
]

# Campo de texto grande para pegar todo el bloque
bloque_texto_masivo = st.text_area(
    "Pegar Cartelera Completa (Formato JSON)",
    value=json.dumps(ejemplo_json, indent=4, ensure_ascii=False),
    height=250,
)

if st.button("🚀 Procesar y Cargar Cartelera Masiva"):
  try:
    # Convertir el texto pegado en objetos de datos legibles por la app
    nueva_cartelera = json.loads(bloque_texto_masivo)

    # Aquí puedes integrar la lógica para guardar en tu base de datos o estado actual de la app
    # Ejemplo: st.session_state['cartelera_activa'] = nueva_cartelera

    st.success(
        f"¡Éxito! Se han procesado {len(nueva_cartelera)} partidos correctamente"
        " sin alterar la estructura general."
    )
  except json.JSONDecodeError as e:
    st.error(
        "Error en el formato JSON. Por favor verifica las comillas, llaves y"
        f" comas. Detalle: {e}"
    )
