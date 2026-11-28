from fpdf import FPDF
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Sabermetría IA / Winometry AI",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

current_dir = os.path.dirname(__file__) if "__file__" in locals() else "."

# --- Sidebar: Logo, Language, Sport & Navigation ---
logo_path = os.path.join(current_dir, "logo.jpeg")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)

lang = st.sidebar.selectbox("Idioma / Language", ["Español", "English"])
lang_code = "es" if lang == "Español" else "en"

sport = st.sidebar.selectbox(
    "Deporte / Sport",
    ["NBA (Básquetbol)", "NFL (Fútbol Americano)"],
)
sport_prefix = "nba" if "Básquetbol" in sport else "nfl"

import threading

@st.cache_resource
def _get_visitor_store(file_path: str):
    lock = threading.Lock()
    initial = 0
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                initial = int(f.read().strip() or "0")
        except Exception:
            initial = 0
    return {"lock": lock, "count": initial}

visitor_file = os.path.join(current_dir, "visitas.txt")
_vstore = _get_visitor_store(visitor_file)

if "visited" not in st.session_state:
    st.session_state.visited = True
    with _vstore["lock"]:
        _vstore["count"] += 1
        count = _vstore["count"]
        try:
            with open(visitor_file, "w", encoding="utf-8") as f:
                f.write(str(count))
        except Exception:
            pass
else:
    with _vstore["lock"]:
        count = _vstore["count"]

st.sidebar.markdown("---")
st.sidebar.markdown(f"👁️ **{'Visitas Totales' if lang_code == 'es' else 'Total Visits'}:** `{count:,}`")

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Menú Principal" if lang_code == "es" else "📌 Main Menu")

menu = st.sidebar.radio(
    "Navegación" if lang_code == "es" else "Navigation",
    [
        "📊 Cartelera de Partidos" if lang_code == "es" else "📊 Match Schedule",
        "📈 Apuestas USA & Métricas" if lang_code == "es" else "📈 USA Betting & Metrics",
        "🧭 Checklist de Último Minuto" if lang_code == "es" else "🧭 Last-Minute Checklist",
        "📰 Noticias & Análisis" if lang_code == "es" else "📰 News & Analysis",
        "📖 Diccionario Sabermétrico" if lang_code == "es" else "📖 Sabermetric Dictionary",
        "⚙️ Panel de Administración" if lang_code == "es" else "⚙️ Admin Panel",
    ],
)

# --- Custom Visual Theme (Dark Slate + Court Emerald + Gold/Cyan Accents) ---
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #0b1320 0%, #0f1c2e 55%, #0c1824 100%);
            color: #f8fafc;
        }
        .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        .stApp p, .stApp li, .stApp label,
        [data-testid="stMetricLabel"] *, [data-testid="stMetricValue"] * {
            color: #f8fafc !important;
        }
        .stApp [data-baseweb="select"] * {
            color: #0f172a !important;
        }
        .stApp input, .stApp textarea {
            color: #0f172a !important;
        }
        .stApp button, .stApp button * {
            color: #0f172a !important;
        }
        [data-testid="stSidebar"] {
            background-color: #09101c;
            border-right: 1px solid rgba(16, 185, 129, 0.25);
        }
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] div[role="radiogroup"] * {
            color: #f8fafc !important;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] * {
            color: #0f172a !important;
        }
        [data-testid="stSidebar"] code {
            color: #fbbf24 !important;
            background-color: rgba(245, 158, 11, 0.18) !important;
            border: 1px solid rgba(245, 158, 11, 0.45) !important;
        }
        .hero-banner {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(15, 23, 42, 0.95) 60%, rgba(245, 158, 11, 0.14) 100%);
            border: 1px solid rgba(245, 158, 11, 0.35);
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 18px;
        }
        .hero-title {
            font-size: 1.55rem;
            font-weight: 800;
            color: #ffffff !important;
            margin: 0 0 6px 0;
        }
        .hero-sub {
            color: #cbd5e1 !important;
            font-size: 0.95rem;
            margin: 0;
        }
        .kpi-card {
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid rgba(56, 189, 248, 0.28);
            border-left: 4px solid #f59e0b;
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 10px;
        }
        .kpi-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #94a3b8 !important;
            margin-bottom: 4px;
        }
        .kpi-val {
            font-size: 1.35rem;
            font-weight: 700;
            color: #fbbf24 !important;
        }
        .lock-card {
            background: linear-gradient(145deg, rgba(16, 185, 129, 0.14), rgba(15, 23, 42, 0.96));
            border: 1px solid rgba(245, 158, 11, 0.55);
            border-left: 6px solid #f59e0b;
            border-radius: 14px;
            padding: 18px 20px;
            margin: 12px 0 18px 0;
        }
        .game-card {
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-left: 5px solid #10b981;
            border-radius: 12px;
            padding: 16px 18px;
            margin: 12px 0;
        }
        .badge-pill {
            display: inline-block;
            background: rgba(245, 158, 11, 0.18);
            color: #fbbf24 !important;
            border: 1px solid rgba(245, 158, 11, 0.45);
            border-radius: 999px;
            padding: 3px 10px;
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- File Paths Based on Sport ---
if sport_prefix == "nba":
    cartelera_path = os.path.join(current_dir, "cartelera_juegos.csv")
    apuestas_path = os.path.join(current_dir, "apuestas_usa.csv")
    efectividad_path = os.path.join(current_dir, "historial_efectividad.csv")
    checklist_path = os.path.join(current_dir, "checklist_ultimo_minuto.csv")
    noticias_path = os.path.join(current_dir, "noticias.txt")
else:
    cartelera_path = os.path.join(current_dir, "nfl_cartelera_juegos.csv")
    apuestas_path = os.path.join(current_dir, "nfl_apuestas_usa.csv")
    efectividad_path = os.path.join(current_dir, "nfl_historial_efectividad.csv")
    checklist_path = os.path.join(current_dir, "nfl_checklist_ultimo_minuto.csv")
    noticias_path = os.path.join(current_dir, "nfl_noticias.txt")

# --- Effectiveness Calculation ---
if os.path.exists(efectividad_path):
    df_ef = pd.read_csv(efectividad_path)
    if not df_ef.empty:
        last_row = df_ef.iloc[-1]
        jornada_txt = f"{int(last_row['aciertos'])} / {int(last_row['juegos'])} ({last_row['efectividad']}%)"
        total_juegos = int(df_ef["juegos"].sum())
        total_aciertos = int(df_ef["aciertos"].sum())
        total_efec = round((total_aciertos / total_juegos * 100), 1) if total_juegos > 0 else 0.0
        global_txt = f"{total_aciertos} / {total_juegos} ({total_efec}%)"
    else:
        jornada_txt = "0 / 0 (0.0%)"
        global_txt = "0 / 0 (0.0%)"
else:
    jornada_txt = "0 / 0 (0.0%)"
    global_txt = "0 / 0 (0.0%)"

brand_name = "Sabermetría IA" if lang_code == "es" else "Winometry AI"
st.markdown(
    f"""
    <div class="hero-banner">
        <div class="badge-pill">{brand_name} • {sport}</div>
        <div class="hero-title">{"Análisis Deportivo & Modelo Estadístico de 4 Capas" if lang_code == "es" else "Sports Analytics & 4-Layer Statistical Model"}</div>
        <div class="hero-sub">{"Lectura métrica, contexto situacional y seguimiento diario de efectividad." if lang_code == "es" else "Metric breakdown, situational context, and daily accuracy tracking."}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(
        f"""<div class="kpi-card"><div class="kpi-label">{"Jornada Anterior" if lang_code == "es" else "Last Slate"}</div><div class="kpi-val">{jornada_txt}</div></div>""",
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f"""<div class="kpi-card"><div class="kpi-label">{"Acumulado Global" if lang_code == "es" else "Global Accumulator"}</div><div class="kpi-val">{global_txt}</div></div>""",
        unsafe_allow_html=True,
    )
with k3:
    games_today_count = len(pd.read_csv(cartelera_path)) if os.path.exists(cartelera_path) else 0
    st.markdown(
        f"""<div class="kpi-card"><div class="kpi-label">{"Partidos en Cartelera" if lang_code == "es" else "Scheduled Games"}</div><div class="kpi-val">{games_today_count}</div></div>""",
        unsafe_allow_html=True,
    )


class PDFReport(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.set_text_color(15, 118, 110)
        self.cell(0, 10, "Sabermetria IA / Winometry AI - Reporte Analitico", 0, 1, "C")
        self.set_font("helvetica", "I", 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 5, "Rigor Metrico Deportivo & Analisis Situacional", 0, 1, "C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f"Pagina {self.page_no()} | Generado por Sabermetria IA / Winometry AI", 0, 0, "C")


def get_match_pdf_bytes(match_title, hora, sede, pick, total_ou, analisis, sport_name):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    def clean_str(s):
        if not s:
            return ""
        return "".join(c for c in str(s) if ord(c) < 256).encode("latin1", errors="ignore").decode("latin1")

    match_title = clean_str(match_title)
    sport_name = clean_str(sport_name)
    hora = clean_str(hora)
    sede = clean_str(sede)
    pick = clean_str(pick)
    total_ou = clean_str(total_ou)

    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, f"Encuentro: {match_title}", 0, 1, "L")

    pdf.set_font("helvetica", "B", 9)
    pdf.set_fill_color(240, 253, 250)
    pdf.cell(0, 7, f" Deporte: {sport_name}", 0, 1, "L", fill=True)
    pdf.cell(0, 7, f" Hora (VE): {hora}", 0, 1, "L", fill=True)
    pdf.cell(0, 7, f" Sede: {sede}", 0, 1, "L", fill=True)
    pdf.cell(0, 7, f" Ganador Proyectado: {pick}", 0, 1, "L", fill=True)
    pdf.cell(0, 7, f" Referencia Total: {total_ou}", 0, 1, "L", fill=True)
    pdf.ln(4)

    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 7, "Analisis Sabermetrico Avanzado", 0, 1, "L")

    clean_text = (
        str(analisis)
        .replace("<br>", "\n")
        .replace("<br/>", "\n")
        .replace("<b>", "")
        .replace("</b>", "")
        .replace("<strong>", "")
        .replace("</strong>", "")
        .replace("<em>", "")
        .replace("</em>", "")
        .replace("&bull;", "-")
    )
    clean_text = clean_str(clean_text)

    pdf.set_font("helvetica", "", 9.5)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 5.5, clean_text)

    res = pdf.output(dest="S")
    if isinstance(res, str):
        return res.encode("latin1", errors="ignore")
    return bytes(res)


# --- Section 1: Cartelera de Partidos ---
if "Cartelera" in menu or "Schedule" in menu:
    st.markdown(f"## 📊 {'Cartelera de Partidos' if lang_code == 'es' else 'Match Schedule'}")
    if os.path.exists(cartelera_path):
        df_cart = pd.read_csv(cartelera_path)
        if not df_cart.empty:
            if "es_jugada_fija" in df_cart.columns:
                df_fija = df_cart[df_cart["es_jugada_fija"] == True]
                if not df_fija.empty:
                    row_fija = df_fija.iloc[0]
                    match_name = f"{row_fija.get('equipo1', '')} vs {row_fija.get('equipo2', '')}"
                    hora_v = row_fija.get("hora", "")
                    sede_v = row_fija.get("sede", "")
                    ganador_v = row_fija.get("ganador", "")
                    total_v = row_fija.get("total_puntos", "")
                    analisis_v = row_fija.get("analisis_es", row_fija.get("analisis", ""))
                    if lang_code == "en" and "analisis_en" in row_fija and pd.notna(row_fija["analisis_en"]):
                        analisis_v = row_fija["analisis_en"]

                    html_analisis = str(analisis_v).replace("\n", "<br>")
                    st.markdown(
                        f"""
                        <div class="lock-card">
                            <div class="badge-pill">⭐ {"PROYECCIÓN PRINCIPAL DEL DÍA" if lang_code == "es" else "TOP PROJECTION OF THE DAY"}</div>
                            <h4 style="color:#ffffff !important; margin:0 0 6px 0; font-size:1.25rem;">{match_name}</h4>
                            <p style="color:#cbd5e1 !important; margin:0 0 6px 0;">⏰ <b>{"Hora (VE)" if lang_code == "es" else "Time (VE)"}:</b> {hora_v} &nbsp;|&nbsp; 🏟️ <b>{"Sede" if lang_code == "es" else "Venue"}:</b> {sede_v}</p>
                            <p style="color:#fbbf24 !important; margin:0 0 10px 0;">🎯 <b>{"Ganador Proyectado" if lang_code == "es" else "Projected Winner"}:</b> {ganador_v} &nbsp;|&nbsp; 📊 <b>{"Referencia Total" if lang_code == "es" else "Total Ref"}:</b> {total_v}</p>
                            <div style="color:#e2e8f0 !important; font-size:0.93rem; line-height:1.55;">{html_analisis}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    pdf_bytes_fija = get_match_pdf_bytes(match_name, hora_v, sede_v, ganador_v, str(total_v), analisis_v, sport)
                    st.download_button(
                        label="📥 Descargar Análisis en PDF" if lang_code == "es" else "📥 Download PDF Analysis",
                        data=pdf_bytes_fija,
                        file_name=f"Proyeccion_Principal_{match_name.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key="download_fija_pdf",
                    )

            st.markdown(f"### 📋 {'Detalle por Encuentro' if lang_code == 'es' else 'Match Breakdown'}")
            match_options = [f"{row.get('equipo1', '')} vs {row.get('equipo2', '')}" for _, row in df_cart.iterrows()]
            selected_match = st.selectbox(
                "Selecciona un encuentro:" if lang_code == "es" else "Select a matchup:",
                match_options,
            )

            for idx, row in df_cart.iterrows():
                match_title = f"{row.get('equipo1', '')} vs {row.get('equipo2', '')}"
                if match_title == selected_match:
                    analisis_content = row.get("analisis_es", row.get("analisis", ""))
                    if lang_code == "en" and "analisis_en" in row and pd.notna(row["analisis_en"]):
                        analisis_content = row["analisis_en"]
                    html_item = str(analisis_content).replace("\n", "<br>")
                    st.markdown(
                        f"""
                        <div class="game-card">
                            <h4 style="color:#ffffff !important; margin:0 0 6px 0;">{match_title}</h4>
                            <p style="color:#cbd5e1 !important; margin:0 0 6px 0;">⏰ <b>{"Hora (VE)" if lang_code == "es" else "Time (VE)"}:</b> {row.get("hora", "")} &nbsp;|&nbsp; 🏟️ <b>{"Sede" if lang_code == "es" else "Venue"}:</b> {row.get("sede", "")}</p>
                            <p style="color:#34d399 !important; margin:0 0 10px 0;">🎯 <b>{"Ganador Proyectado" if lang_code == "es" else "Projected Winner"}:</b> {row.get("ganador", "")} &nbsp;|&nbsp; 📊 <b>{"Referencia Total" if lang_code == "es" else "Total Ref"}:</b> {row.get("total_puntos", "")}</p>
                            <div style="color:#e2e8f0 !important; font-size:0.93rem; line-height:1.55;">{html_item}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    pdf_bytes_match = get_match_pdf_bytes(
                        match_title,
                        row.get("hora", ""),
                        row.get("sede", ""),
                        row.get("ganador", ""),
                        str(row.get("total_puntos", "")),
                        analisis_content,
                        sport,
                    )
                    st.download_button(
                        label="📥 Descargar Ficha en PDF" if lang_code == "es" else "📥 Download Match PDF",
                        data=pdf_bytes_match,
                        file_name=f"Analisis_{match_title.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key=f"download_pdf_{idx}",
                    )
        else:
            st.info("No hay partidos cargados en la cartelera actual." if lang_code == "es" else "No games loaded in the current schedule.")
    else:
        st.warning("No se encontró el archivo de cartelera." if lang_code == "es" else "Schedule file not found.")

# --- Section 2: Apuestas USA & Métricas ---
elif "Apuestas" in menu or "Betting" in menu:
    st.markdown(f"## 📈 {'Métricas Avanzadas & Proyecciones' if lang_code == 'es' else 'Advanced Metrics & Projections'}")
    if os.path.exists(apuestas_path):
        df_ap = pd.read_csv(apuestas_path)
        if not df_ap.empty:
            if "probabilidad" in df_ap.columns:
                df_ap = df_ap.sort_values(by="probabilidad", ascending=False).reset_index(drop=True)
            for _, row in df_ap.iterrows():
                equipo1 = row.get("equipo1", row.get("partido", "Partido"))
                equipo2 = row.get("equipo2", "")
                spread = row.get("spread", "N/A")
                total_ou = row.get("total_ou", "N/A")
                proyeccion = row.get("proyeccion_usa", row.get("analisis_apuesta", ""))
                prob = row.get("probabilidad", 0.0)
                match_str = f"{equipo1} vs {equipo2}" if equipo2 else f"{equipo1}"

                c1, c2, c3 = st.columns([3, 1.5, 1.5])
                with c1:
                    st.markdown(f"#### 🏀 {match_str}")
                    st.markdown(f"{proyeccion}")
                with c2:
                    st.markdown(f"**Margen Ref:** `{spread}`")
                    st.markdown(f"**Total Ref:** `{total_ou}`")
                with c3:
                    st.metric(label="Confianza / Conf" if lang_code == "es" else "Confidence", value=f"{prob}%")
                st.markdown("---")
        else:
            st.info("Sin registros de métricas cargados para hoy." if lang_code == "es" else "No metric records loaded for today.")
    else:
        st.warning("No se encontró el archivo de métricas." if lang_code == "es" else "Metrics file not found.")

# --- Section 3: Checklist de Último Minuto ---
elif "Checklist" in menu:
    st.markdown(f"## 🧭 {'Checklist de Último Minuto' if lang_code == 'es' else 'Last-Minute Checklist'}")
    if os.path.exists(checklist_path):
        df_chk = pd.read_csv(checklist_path)
        for _, row in df_chk.iterrows():
            st.markdown(
                f"""
                <div class="game-card">
                    <h4 style="color:#ffffff !important; margin:0 0 6px 0;">{row.get("partido", "")}</h4>
                    <p style="color:#fbbf24 !important; margin:0 0 4px 0;"><b>{"Estado" if lang_code == "es" else "Status"}:</b> {row.get("estado", "")}</p>
                    <p style="color:#e2e8f0 !important; margin:0 0 4px 0;"><b>{"Notas / Filtro" if lang_code == "es" else "Notes / Filter"}:</b> {row.get("alerta_notas", "")}</p>
                    <p style="color:#94a3b8 !important; margin:0;"><b>{"Ajuste" if lang_code == "es" else "Adjustment"}:</b> {row.get("cambio_perspectiva", "")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.warning("No se encontró el checklist." if lang_code == "es" else "Checklist file not found.")

# --- Section 4: Noticias & Análisis ---
elif "Noticias" in menu or "News" in menu:
    st.markdown(f"## 📰 {'Noticias & Análisis Avanzado' if lang_code == 'es' else 'News & Advanced Analysis'}")
    if os.path.exists(noticias_path):
        with open(noticias_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.info("Boletines analíticos en desarrollo." if lang_code == "es" else "Analytical bulletins in development.")

# --- Section 5: Diccionario Sabermétrico ---
elif "Diccionario" in menu or "Dictionary" in menu:
    st.markdown(f"## 📖 {'Diccionario Sabermétrico & Glosario' if lang_code == 'es' else 'Sabermetric Dictionary & Glossary'}")
    if sport_prefix == "nba":
        st.markdown("• **Net Rating:** Diferencial de puntos por 100 posesiones (Ofensiva vs. Defensiva).")
        st.markdown("• **Effective Field Goal Percentage (eFG%):** Eficiencia de tiro ajustada por el valor del triple.")
        st.markdown("• **True Shooting Percentage (TS%):** Eficiencia integral de anotación (tiros de campo, triples y libres).")
        st.markdown("• **Turnover & Rebound Control (TOV% / ORB%):** Control de pérdidas y recuperación de posesiones extra.")
    else:
        st.markdown("• **EPA per Play:** Valor esperado de puntos añadidos por jugada ofensiva o defensiva.")
        st.markdown("• **Success Rate:** Porcentaje de jugadas que cumplen el objetivo de yardas según el *down*.")
        st.markdown("• **DVOA:** Eficiencia ajustada por calidad del rival frente al promedio de la liga.")
        st.markdown("• **Pressure Rate:** Porcentaje de jugadas de pase con presión defensiva sobre el *quarterback*.")

# --- Section 6: Panel de Administración ---
elif "Administración" in menu or "Admin" in menu:
    st.markdown(f"## ⚙️ {'Panel de Administración' if lang_code == 'es' else 'Admin Panel'}")
    password = st.text_input("Clave de administrador:" if lang_code == "es" else "Admin Password:", type="password")
    valid_passwords = ["sabermetria2026", "coseinca2026", "sabermetria"]

    if password in valid_passwords:
        st.success("¡Acceso concedido!" if lang_code == "es" else "Access granted!")

        st.subheader("📥 1. Descargar Archivos Actuales" if lang_code == "es" else "📥 1. Download Current Files")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if os.path.exists(cartelera_path):
                with open(cartelera_path, "rb") as f:
                    st.download_button("📥 Cartelera CSV", f, file_name=os.path.basename(cartelera_path), mime="text/csv")
        with col2:
            if os.path.exists(apuestas_path):
                with open(apuestas_path, "rb") as f:
                    st.download_button("📥 Métricas CSV", f, file_name=os.path.basename(apuestas_path), mime="text/csv")
        with col3:
            if os.path.exists(checklist_path):
                with open(checklist_path, "rb") as f:
                    st.download_button("📥 Checklist CSV", f, file_name=os.path.basename(checklist_path), mime="text/csv")
        with col4:
            if os.path.exists(efectividad_path):
                with open(efectividad_path, "rb") as f:
                    st.download_button("📥 Historial CSV", f, file_name=os.path.basename(efectividad_path), mime="text/csv")

        st.markdown("---")
        st.subheader("📤 2. Cargar / Actualizar CSV" if lang_code == "es" else "📤 2. Upload / Update CSV")

        up_cartelera = st.file_uploader("Cartelera (CSV)", type=["csv"], key="up_cart")
        if up_cartelera is not None:
            pd.read_csv(up_cartelera).to_csv(cartelera_path, index=False, encoding="utf-8")
            st.success("Cartelera actualizada." if lang_code == "es" else "Schedule updated.")

        up_apuestas = st.file_uploader("Métricas (CSV)", type=["csv"], key="up_ap")
        if up_apuestas is not None:
            pd.read_csv(up_apuestas).to_csv(apuestas_path, index=False, encoding="utf-8")
            st.success("Métricas actualizadas." if lang_code == "es" else "Metrics updated.")

        up_checklist = st.file_uploader("Checklist (CSV)", type=["csv"], key="up_chk")
        if up_checklist is not None:
            pd.read_csv(up_checklist).to_csv(checklist_path, index=False, encoding="utf-8")
            st.success("Checklist actualizado." if lang_code == "es" else "Checklist updated.")

        up_efectividad = st.file_uploader("Historial de Efectividad (CSV)", type=["csv"], key="up_ef")
        if up_efectividad is not None:
            pd.read_csv(up_efectividad).to_csv(efectividad_path, index=False, encoding="utf-8")
            st.success("Historial actualizado." if lang_code == "es" else "History updated.")

        st.markdown("---")
        st.subheader("📰 3. Editor de Noticias & Análisis" if lang_code == "es" else "📰 3. News & Analysis Editor")
        current_news = ""
        if os.path.exists(noticias_path):
            with open(noticias_path, "r", encoding="utf-8") as f:
                current_news = f.read()

        news_input = st.text_area("Boletín (Markdown):", value=current_news, height=220)
        if st.button("Guardar Noticias" if lang_code == "es" else "Save News"):
            with open(noticias_path, "w", encoding="utf-8") as f:
                f.write(news_input)
            st.success("Noticias guardadas." if lang_code == "es" else "News saved.")

    elif password != "":
        st.error("Contraseña incorrecta." if lang_code == "es" else "Incorrect password.")
