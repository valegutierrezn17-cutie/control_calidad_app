import streamlit as st
import pandas as pd
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from modules.data_loader import load_data
from modules.fase1.capability import capability_analysis
from modules.fase1.control_charts import control_chart_module
from modules.fase1.estadistica import normality_analysis
from modules.fase2.potencia import ejecutar_potencia
from modules.fase2.arl import arl_analysis
from modules.fase2.simulacion import arl_live_simulation
from planes_muestreo.muestreo_aceptacion import render_muestreo_modulo
from modules.plan_economico.economico import render_modulo_economico

# ── LEER ARCHIVO DE PLANTILLA FÍSICO ──
try:
    with open("PLANTILLA DATOS.xlsx", "rb") as file:
        plantilla_bytes = file.read()
except Exception:
    plantilla_bytes = None

st.set_page_config(layout="wide", page_title="Sistema Control de Calidad")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp { background: linear-gradient(135deg, #f4f7fb 0%, #eef2f7 100%); }
.main .block-container { padding-top: 1.2rem !important; max-width: 98%; }

section[data-testid="stSidebar"] { background: #1f2a38 !important; }

.sidebar-title {
    font-size: 22px; font-weight: 700; text-align: center;
    padding: 10px 0 20px 0; color: white !important;
}

section[data-testid="stSidebar"] .stMarkdown p { color: white !important; line-height: 1.6 !important; }
section[data-testid="stSidebar"] label p { color: white !important; }
div[data-testid="stSelectbox"] div[data-baseweb="select"] div { color: #1B2631 !important; }
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li, div[data-baseweb="popover"] li * {
    background-color: #FFFFFF !important; color: #1B2631 !important;
}
div[data-baseweb="popover"] li:hover, div[data-baseweb="popover"] li:hover * {
    background-color: #F0F4F8 !important; color: #2E86C1 !important;
}

.main-title { font-size: 38px; font-weight: 800; color: #1B2631; margin-bottom: 0.2rem; }
.subtitle { color: #5D6D7E; font-size: 16px; margin-bottom: 2rem; }

.card {
    background: rgba(255,255,255,0.72); border-radius: 22px; padding: 24px;
    border: 1px solid rgba(255,255,255,0.5);
    box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 20px;
}

.stButton>button {
    border-radius: 14px;
    background: linear-gradient(135deg, #3498DB, #2E86C1);
    color: white; font-weight: 600;
}

.modules-section-title {
    font-size: 13px; font-weight: 700; color: #8A9BB0;
    letter-spacing: 0.08em; text-transform: uppercase; margin: 2rem 0 1rem 0;
}

.module-card {
    background: #ffffff; border-radius: 20px; padding: 32px 28px 28px 28px;
    border: 1px solid #E8EEF5; box-shadow: 0 2px 12px rgba(0,0,0,0.045);
    transition: box-shadow 0.2s, transform 0.2s;
    display: flex; flex-direction: column; align-items: flex-start;
    gap: 12px; min-height: 170px;
}
.module-card:hover { box-shadow: 0 6px 24px rgba(52,152,219,0.12); transform: translateY(-2px); }
.module-icon-wrap {
    width: 52px; height: 52px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 6px; flex-shrink: 0;
}
.module-icon-wrap svg { display: block; }
.module-card-title { font-size: 17px; font-weight: 700; color: #1B2631; margin: 0; }
.module-card-desc { font-size: 13.5px; color: #8A9BB0; margin: 0; line-height: 1.55; }

/* ── HERO KPI CARD ── */
.hero-kpi-card {
    background: linear-gradient(135deg, #EAF2FB 0%, #ddeaf8 40%, #e8f0fa 70%, #EDF4FD 100%);
    border-radius: 24px;
    padding: 0;
    border: 1px solid rgba(180,210,240,0.6);
    box-shadow: 0 8px 40px rgba(52,120,200,0.10), 0 2px 8px rgba(52,120,200,0.06);
    margin-bottom: 28px;
    overflow: hidden;
    display: flex;
    align-items: stretch;
    min-height: 200px;
    position: relative;
}
.hero-kpi-content {
    flex: 1;
    padding: 40px 44px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    z-index: 2;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(46,134,193,0.10);
    border: 1px solid rgba(46,134,193,0.22);
    border-radius: 20px; padding: 4px 12px;
    font-size: 11px; font-weight: 700; color: #2471A3;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 16px; width: fit-content;
}
.hero-kpi-title {
    font-size: 32px; font-weight: 800; color: #1B2631;
    line-height: 1.2; margin: 0 0 10px 0;
}
.hero-kpi-title span { color: #2E86C1; }
.hero-kpi-subtitle {
    font-size: 15px; color: #5D7A96;
    margin: 0 0 24px 0; line-height: 1.5; max-width: 420px;
}
.hero-stats { display: flex; gap: 32px; }
.hero-stat-item { display: flex; flex-direction: column; gap: 2px; }
.hero-stat-value { font-size: 22px; font-weight: 800; color: #1B2631; }
.hero-stat-label { font-size: 11px; color: #7F9DB5; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; }
.hero-stat-divider { width: 1px; background: rgba(46,134,193,0.18); margin: 4px 0; }

.hero-glow {
    position: absolute; width: 380px; height: 380px;
    background: radial-gradient(circle, rgba(180,215,255,0.45) 0%, transparent 68%);
    top: -80px; right: 60px; z-index: 1;
    pointer-events: none;
}
.hero-glow-2 {
    position: absolute; width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(147,198,255,0.25) 0%, transparent 70%);
    bottom: -40px; left: 30%; z-index: 1;
    pointer-events: none;
}

/* ── VISUAL DECORATIVO HERO ── */
.hero-kpi-visual {
    width: 320px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 28px 32px 28px 0;
    z-index: 2;
}
.visual-chart-wrap {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(180,210,240,0.55);
    border-radius: 18px;
    padding: 20px 22px 16px 22px;
    width: 100%;
    position: relative;
    box-shadow: 0 4px 20px rgba(52,120,200,0.08);
}
.visual-chart-label {
    font-size: 11px; font-weight: 700;
    color: #7F9DB5;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 12px;
}
.visual-line-svg { width: 100%; height: auto; display: block; }
.visual-badge-bajo-control {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(34,197,94,0.10);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 20px; padding: 5px 12px;
    font-size: 11px; font-weight: 700; color: #16A34A;
    margin-top: 14px; letter-spacing: 0.04em;
}

/* ── UPLOAD SECTION (sutil) ── */
.upload-section {
    background: #ffffff;
    border-radius: 14px;
    padding: 14px 20px;
    border: 1px solid #E8EEF5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 18px;
    flex-wrap: wrap;
}
.upload-info {
    display: flex; align-items: center; gap: 14px;
    flex: 1; min-width: 200px;
}
.upload-icon-wrap {
    width: 44px; height: 44px; background: #EBF5FF;
    border-radius: 12px; display: flex;
    align-items: center; justify-content: center; flex-shrink: 0;
}
.upload-text-block h4 { font-size: 14px; font-weight: 700; color: #1B2631; margin: 0 0 2px 0; }
.upload-text-block p { font-size: 12px; color: #7F8C9A; margin: 0; line-height: 1.4; }
.upload-drop-zone {
    flex: 1; min-width: 200px;
    border: 1.5px dashed #C8D8E8; border-radius: 12px;
    padding: 12px 20px;
    display: flex; align-items: center; gap: 12px;
    background: #F7FAFD;
}
.upload-drop-zone-text p { font-size: 13px; color: #5D6D7E; margin: 0; }
.upload-drop-zone-text a { color: #2E86C1; font-weight: 600; text-decoration: none; }
.upload-drop-zone-text .meta { font-size: 11px; color: #AAB8C5; margin-top: 2px; }
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

menu = None
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

    st.markdown("""
    <div class="hero-kpi-card">
        <div class="hero-glow"></div>
        <div class="hero-glow-2"></div>
        <div class="hero-kpi-content">
            <div class="hero-badge">
                <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24"
                     fill="none" stroke="#2471A3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                </svg>
                Plataforma Activa
            </div>
            <h1 class="hero-kpi-title">Sistema de <span>Control</span><br>de Calidad</h1>
            <p class="hero-kpi-subtitle">
                Monitoreo estadístico en tiempo real, análisis de capacidad,
                planes de muestreo y optimización económica de procesos productivos.
            </p>
            <div class="hero-stats">
                <div class="hero-stat-item">
                    <span class="hero-stat-value">8</span>
                    <span class="hero-stat-label">Módulos</span>
                </div>
                <div class="hero-stat-divider"></div>
                <div class="hero-stat-item">
                    <span class="hero-stat-value">2</span>
                    <span class="hero-stat-label">Fases SPC</span>
                </div>
                <div class="hero-stat-divider"></div>
                <div class="hero-stat-item">
                    <span class="hero-stat-value">CSV · XLSX</span>
                    <span class="hero-stat-label">Formatos</span>
                </div>
            </div>
        </div>
        <div class="hero-kpi-visual">
            <div class="visual-chart-wrap">
                <div class="visual-chart-label">Cp / Cpk</div>
                <svg viewBox="0 0 200 90" xmlns="http://www.w3.org/2000/svg" class="visual-line-svg">
                    <defs>
                        <linearGradient id="lineGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.22"/>
                            <stop offset="100%" stop-color="#3B82F6" stop-opacity="0"/>
                        </linearGradient>
                    </defs>
                    <path d="M0 70 C20 65, 35 50, 50 45 S80 30, 100 28 S140 20, 160 18 S185 15, 200 12 L200 90 L0 90 Z"
                          fill="url(#lineGrad)"/>
                    <path d="M0 70 C20 65, 35 50, 50 45 S80 30, 100 28 S140 20, 160 18 S185 15, 200 12"
                          fill="none" stroke="#2E86C1" stroke-width="2.5" stroke-linecap="round"/>
                    <circle cx="50"  cy="45" r="3.5" fill="#2E86C1"/>
                    <circle cx="100" cy="28" r="3.5" fill="#2E86C1"/>
                    <circle cx="160" cy="18" r="3.5" fill="#2E86C1"/>
                    <line x1="0" y1="18" x2="200" y2="18" stroke="rgba(239,68,68,0.35)" stroke-width="1.2" stroke-dasharray="5,4"/>
                    <line x1="0" y1="76" x2="200" y2="76" stroke="rgba(239,68,68,0.35)" stroke-width="1.2" stroke-dasharray="5,4"/>
                </svg>
                <div class="visual-badge-bajo-control">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"
                         fill="none" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    Proceso Bajo Control
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='modules-section-title'>Módulos disponibles</div>", unsafe_allow_html=True)

    svg_capacidad = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>"""
    svg_graficos = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>"""
    svg_estadistica = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16"/><path d="M4 4l4 8-4 8h16"/></svg>"""
    svg_potencia = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>"""
    svg_monitoreo = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>"""
    svg_arl = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#6366F1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>"""
    svg_muestreo = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>"""
    svg_economico = """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>"""

    modules = [
        {"icon": svg_capacidad,   "bg": "#EBF4FF", "title": "Capacidad",               "desc": "Índices Cp, Cpk y análisis de capacidad del proceso."},
        {"icon": svg_graficos,    "bg": "#ECFDF5", "title": "Gráficos de Control",     "desc": "Cartas de control Shewhart en tiempo real."},
        {"icon": svg_estadistica, "bg": "#F5F3FF", "title": "Estadística",             "desc": "Análisis descriptivo y pruebas de normalidad."},
        {"icon": svg_potencia,    "bg": "#FFFBEB", "title": "Potencia",                "desc": "Análisis de potencia estadística del proceso."},
        {"icon": svg_monitoreo,   "bg": "#FEF2F2", "title": "Monitoreo en Tiempo Real","desc": "Alertas automáticas con datos en vivo."},
        {"icon": svg_arl,         "bg": "#EEF2FF", "title": "ARL y ATS",               "desc": "Average Run Length y análisis de tiempo de señal."},
        {"icon": svg_muestreo,    "bg": "#F0F9FF", "title": "Planes de Muestreo",      "desc": "Diseño de planes de aceptación por atributos y variables."},
        {"icon": svg_economico,   "bg": "#F0FDF4", "title": "Análisis Económico",      "desc": "Optimización de peso seteado y análisis de mermas."},
    ]

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
    svg_upload_cloud = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
        fill="none" stroke="#2E86C1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/>
        <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/>
    </svg>"""

    svg_upload_arrow = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
        fill="none" stroke="#2E86C1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
    </svg>"""

    # Upload solo visible en Capacidad y Monitoreo en Tiempo Real
    mostrar_upload = (
        (fase == "Fase 1" and menu == "Capacidad") or
        (fase == "Fase 2" and menu == "Monitoreo en Tiempo Real")
    )

    if mostrar_upload:
        st.markdown(f"""
        <div class="upload-section">
            <div class="upload-info">
                <div class="upload-icon-wrap">{svg_upload_cloud}</div>
                <div class="upload-text-block">
                    <h4>Carga de datos</h4>
                    <p>Sube tu archivo CSV o Excel para comenzar<br>con el análisis del proceso.</p>
                </div>
            </div>
            <div class="upload-drop-zone">
                <div class="drop-icon">{svg_upload_arrow}</div>
                <div class="upload-drop-zone-text">
                    <p>Arrastra tu archivo aquí o <a href="#">selecciona un archivo</a></p>
                    <p class="meta">CSV, XLSX &bull; Máx. 200MB por archivo</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón de descarga de la plantilla estructurada física justo debajo de la zona de carga
        if plantilla_bytes is not None:
            st.download_button(
                label="Descargar Plantilla Excel (Estructura de Datos)",
                data=plantilla_bytes,
                file_name="PLANTILLA DATOS.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    df = load_data()
    if df is not None:
        df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all')
        cols_seleccionadas = st.multiselect("Selecciona las columnas:", df.select_dtypes(include=['number']).columns)
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