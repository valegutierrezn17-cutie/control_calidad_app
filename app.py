import streamlit as st
import pandas as pd
import sys
import os

# Configuración de ruta robusta para encontrar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# =========================
# IMPORTS
# =========================
from modules.data_loader import load_data

# FASE 1
from modules.fase1.capability import capability_analysis
from modules.fase1.control_charts import control_chart_module
from modules.fase1.estadistica import normality_analysis

# FASE 2
from modules.fase2.potencia import ejecutar_potencia
from modules.fase2.arl import arl_analysis
from modules.fase2.simulacion import arl_live_simulation

# PLANES DE MUESTREO
from planes_muestreo.muestreo_aceptacion import render_muestreo_modulo

# OPTIMIZACIÓN ECONÓMICA
from modules.plan_economico.economico import render_modulo_economico

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(layout="wide", page_title="Sistema Control de Calidad")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }

/* Fondo de la aplicación */
.stApp { background: linear-gradient(135deg, #f4f7fb 0%, #eef2f7 100%); }
.main .block-container { padding-top: 1.2rem !important; max-width: 98%; }

/* Fondo oscuro para la Barra Lateral */
section[data-testid="stSidebar"] {
    background: #1f2a38 !important;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    text-align: center;
    padding: 10px 0 20px 0;
    color: white !important;
}

section[data-testid="stSidebar"] .stMarkdown p {
    color: white !important;
    line-height: 1.6 !important;
}

section[data-testid="stSidebar"] label p {
    color: white !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
    color: #1B2631 !important;
}

div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] li * {
    background-color: #FFFFFF !important;
    color: #1B2631 !important;
}

div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li:hover * {
    background-color: #F0F4F8 !important;
    color: #2E86C1 !important;
}

/* Panel principal */
.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #1B2631;
    margin-bottom: 0.2rem;
}

.subtitle {
    color: #5D6D7E;
    font-size: 16px;
    margin-bottom: 2rem;
}

.card {
    background: rgba(255,255,255,0.72);
    border-radius: 22px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.5);
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.stButton>button {
    border-radius: 14px;
    background: linear-gradient(135deg, #3498DB, #2E86C1);
    color: white;
    font-weight: 600;
}

/* =====================
   TARJETAS DE MÓDULOS
   ===================== */
.modules-section-title {
    font-size: 13px;
    font-weight: 700;
    color: #8A9BB0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 2rem 0 1rem 0;
}

.modules-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 2rem;
}

.module-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 32px 28px 28px 28px;
    border: 1px solid #E8EEF5;
    box-shadow: 0 2px 12px rgba(0,0,0,0.045);
    transition: box-shadow 0.2s, transform 0.2s;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    min-height: 170px;
}

.module-card:hover {
    box-shadow: 0 6px 24px rgba(52,152,219,0.12);
    transform: translateY(-2px);
}

.module-icon-wrap {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 6px;
    flex-shrink: 0;
}

.module-icon-wrap svg {
    display: block;
}

.module-card-title {
    font-size: 17px;
    font-weight: 700;
    color: #1B2631;
    margin: 0;
}

.module-card-desc {
    font-size: 13.5px;
    color: #8A9BB0;
    margin: 0;
    line-height: 1.55;
}

/* =====================
   UPLOAD ESTILIZADO
   ===================== */
.upload-section {
    background: #ffffff;
    border-radius: 18px;
    padding: 22px 26px;
    border: 1px solid #E8EEF5;
    box-shadow: 0 4px 18px rgba(0,0,0,0.055);
    display: flex;
    align-items: center;
    gap: 28px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}

.upload-info {
    display: flex;
    align-items: center;
    gap: 18px;
    flex: 1;
    min-width: 220px;
}

.upload-icon-wrap {
    width: 54px;
    height: 54px;
    background: #EBF5FF;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    flex-shrink: 0;
}

.upload-text-block h4 {
    font-size: 16px;
    font-weight: 700;
    color: #1B2631;
    margin: 0 0 4px 0;
}

.upload-text-block p {
    font-size: 13px;
    color: #7F8C9A;
    margin: 0;
    line-height: 1.5;
}

.upload-drop-zone {
    flex: 1;
    min-width: 220px;
    border: 2px dashed #C8D8E8;
    border-radius: 14px;
    padding: 18px 24px;
    text-align: center;
    background: #F7FAFD;
}

.upload-drop-zone span.drop-icon {
    font-size: 26px;
    display: block;
    margin-bottom: 6px;
}

.upload-drop-zone p {
    font-size: 13px;
    color: #7F8C9A;
    margin: 0;
}

.upload-drop-zone a {
    color: #2E86C1;
    font-weight: 600;
    text-decoration: none;
}

.upload-drop-zone .meta {
    font-size: 11px;
    color: #AAB8C5;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR Y ENRUTAMIENTO
# =========================
st.sidebar.image("logo2.png", use_container_width=True)
st.sidebar.markdown("<div class='sidebar-title'>Control Estadístico de Procesos</div>", unsafe_allow_html=True)

fase = st.sidebar.selectbox(
    "Selecciona el Entorno:",
    ["Inicio", "Fase 1", "Fase 2", "Planes de Muestreo", "Análisis Económico (Mermas)"]
)

if fase == "Fase 1":
    menu = st.sidebar.selectbox("Módulos Fase 1:", ["Capacidad", "Gráficos", "Estadística"])
elif fase == "Fase 2":
    menu = st.sidebar.selectbox("Módulos Fase 2:", ["Monitoreo en Tiempo Real", "Potencia", "ARL"])
elif fase == "Planes de Muestreo":
    menu = st.sidebar.selectbox("Herramientas de Muestreo:", ["Diseño y Planes"])
elif fase == "Análisis Económico (Mermas)":
    menu = st.sidebar.selectbox("Simulación Financiera:", ["Optimización de Peso Seteado"])

# =========================
# HEADER
# =========================
st.markdown("""
<div class="main-title">Sistema de Control de Calidad</div>
<div class="subtitle">Monitoreo estadístico, análisis de capacidad y simulación avanzada</div>
""", unsafe_allow_html=True)

# =========================
# PORTADA (INICIO)
# =========================
if fase == "Inicio":

    # --- Sección de módulos ---
    st.markdown("<div class='modules-section-title'>Módulos disponibles</div>", unsafe_allow_html=True)

    # SVG icons matching reference image style (Lucide-style, stroke-based)
    svg_capacidad = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>"""
    svg_graficos = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>"""
    svg_estadistica = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16"/><path d="M4 4l4 8-4 8h16"/></svg>"""
    svg_potencia = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>"""
    svg_monitoreo = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>"""
    svg_arl = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#6366F1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>"""
    svg_muestreo = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>"""
    svg_economico = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>"""

    modules = [
        {"icon": svg_capacidad,  "bg": "#EBF4FF", "color": "#3B82F6", "title": "Capacidad",             "desc": "Índices Cp, Cpk y análisis de capacidad del proceso."},
        {"icon": svg_graficos,   "bg": "#ECFDF5", "color": "#10B981", "title": "Gráficos de Control",   "desc": "Cartas de control Shewhart en tiempo real."},
        {"icon": svg_estadistica,"bg": "#F5F3FF", "color": "#8B5CF6", "title": "Estadística",           "desc": "Análisis descriptivo y pruebas de normalidad."},
        {"icon": svg_potencia,   "bg": "#FFFBEB", "color": "#F59E0B", "title": "Potencia",              "desc": "Análisis de potencia estadística del proceso."},
        {"icon": svg_monitoreo,  "bg": "#FEF2F2", "color": "#EF4444", "title": "Monitoreo en Tiempo Real","desc": "Alertas automáticas con datos en vivo."},
        {"icon": svg_arl,        "bg": "#EEF2FF", "color": "#6366F1", "title": "ARL y ATS",             "desc": "Average Run Length y análisis de tiempo de señal."},
        {"icon": svg_muestreo,   "bg": "#F0F9FF", "color": "#0EA5E9", "title": "Planes de Muestreo",    "desc": "Diseño de planes de aceptación por atributos y variables."},
        {"icon": svg_economico,  "bg": "#F0FDF4", "color": "#22C55E", "title": "Análisis Económico",    "desc": "Optimización de peso seteado y análisis de mermas."},
    ]

    # Renderizar en grid de 2 columnas
    num_cols = 2
    rows = [modules[i:i+num_cols] for i in range(0, len(modules), num_cols)]

    for row in rows:
        cols = st.columns(num_cols, gap="large")
        for col, mod in zip(cols, row):
            with col:
                st.markdown(f"""
                <div class="module-card">
                    <div class="module-icon-wrap" style="background:{mod['bg']};">{mod['icon']}</div>
                    <p class="module-card-title">{mod['title']}</p>
                    <p class="module-card-desc">{mod['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <p style="text-align:center; color:#AAB8C5; font-size:13px; margin-top:0.5rem;">
        Usa la barra lateral para navegar entre módulos.
    </p>
    """, unsafe_allow_html=True)

# =========================
# MÓDULOS FUNCIONALES
# =========================
elif fase == "Planes de Muestreo":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    render_muestreo_modulo()
    st.markdown("</div>", unsafe_allow_html=True)

elif fase == "Análisis Económico (Mermas)":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    render_modulo_economico()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- Zona de carga de datos estilizada ---
    st.markdown("""
    <div class="upload-section">
        <div class="upload-info">
            <div class="upload-icon-wrap">☁️</div>
            <div class="upload-text-block">
                <h4>Carga de datos</h4>
                <p>Sube tu archivo CSV o Excel para comenzar<br>con el análisis del proceso.</p>
            </div>
        </div>
        <div class="upload-drop-zone">
            <span class="drop-icon">⬆️</span>
            <p>Arrastra tu archivo aquí<br>o <a href="#">selecciona un archivo</a></p>
            <p class="meta">CSV, XLSX &bull; Máx. 200MB por archivo</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    df = load_data()
    if df is not None:
        df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all')
        cols_seleccionadas = st.multiselect("📌 Selecciona las columnas:", df.select_dtypes(include=['number']).columns)
        if cols_seleccionadas:
            data_subset = df[cols_seleccionadas].copy()
            if fase == "Fase 1":
                if menu == "Capacidad":
                    capability_analysis(data_subset)
                elif menu == "Gráficos":
                    control_chart_module(data_subset)
                elif menu == "Estadística":
                    normality_analysis(data_subset)
            elif fase == "Fase 2":
                if menu == "Monitoreo en Tiempo Real":
                    arl_live_simulation()
                elif menu == "Potencia":
                    ejecutar_potencia(data_subset)
                elif menu == "ARL":
                    arl_analysis(data_subset)
        else:
            st.info("Selecciona columnas para continuar.")
    else:
        st.info("Carga un archivo CSV o Excel para comenzar.")

    st.markdown("</div>", unsafe_allow_html=True)