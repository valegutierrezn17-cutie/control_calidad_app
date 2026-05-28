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
st.set_page_config(layout="wide", page_title="PRO-STATS | Control Estadístico de Procesos", page_icon="⚙️")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* =====================================================
   RESET Y BASE
   ===================================================== */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background: #F0F4F8 !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* =====================================================
   SIDEBAR - Fondo oscuro degradado
   ===================================================== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
    width: 240px !important;
    min-width: 240px !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}

section[data-testid="stSidebar"] > div {
    padding: 0 !important;
    background: transparent !important;
}

section[data-testid="stSidebar"] .block-container {
    padding: 0 !important;
}

/* Logo del sidebar */
section[data-testid="stSidebar"] img {
    display: block;
    margin: 24px auto 8px auto;
    width: 80px !important;
    height: 80px !important;
    object-fit: contain;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,0.15);
}

/* Título del sidebar */
.sidebar-brand-title {
    color: #FFFFFF !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    text-align: center !important;
    padding: 4px 16px 20px 16px !important;
    letter-spacing: 0.01em;
    line-height: 1.4;
}

/* Separador de sección */
.sidebar-section-label {
    color: #64748B !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 12px 16px 6px 16px !important;
    display: block;
}

/* Textos generales del sidebar */
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label p {
    color: #CBD5E1 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 12px !important;
}

/* Selectbox del sidebar */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] {
    margin: 0 12px 8px 12px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background: rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: transparent !important;
    border: none !important;
    color: #F1F5F9 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 12px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #94A3B8 !important;
}

/* Opciones del dropdown */
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li {
    background: #1E293B !important;
    color: #F1F5F9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
}

div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li:hover * {
    background: #334155 !important;
    color: #FFFFFF !important;
}

/* Nav items del sidebar (módulos) */
.sidebar-nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 16px;
    margin: 2px 8px;
    border-radius: 8px;
    color: #94A3B8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    cursor: pointer;
    transition: all 0.15s ease;
    text-decoration: none;
}

.sidebar-nav-item:hover {
    background: rgba(255,255,255,0.07);
    color: #F1F5F9 !important;
}

.sidebar-nav-item.active {
    background: rgba(37, 99, 235, 0.2);
    color: #60A5FA !important;
    font-weight: 600 !important;
}

.sidebar-nav-item .nav-icon {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
}

/* Box de ayuda al fondo del sidebar */
.sidebar-help-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 16px;
    margin: 16px 12px 8px 12px;
}

.sidebar-help-box .help-title {
    color: #F1F5F9 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin-bottom: 4px;
}

.sidebar-help-box .help-text {
    color: #64748B !important;
    font-size: 11px !important;
    line-height: 1.5;
}

/* Footer del sidebar */
.sidebar-footer {
    color: #475569 !important;
    font-size: 10px !important;
    text-align: center;
    padding: 12px 16px;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: auto;
}

/* =====================================================
   TOPBAR / NAVBAR SUPERIOR
   ===================================================== */
.topbar {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 16px;
    padding: 12px 32px;
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.topbar-icon-btn {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    position: relative;
    font-size: 16px;
}

.topbar-badge {
    position: absolute;
    top: -3px;
    right: -3px;
    background: #2563EB;
    color: white;
    font-size: 9px;
    font-weight: 700;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid white;
}

.topbar-user {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 20px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    cursor: pointer;
}

.topbar-user-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 12px;
    font-weight: 700;
}

.topbar-user-name {
    font-size: 13px;
    font-weight: 600;
    color: #1E293B;
}

/* =====================================================
   HERO SECTION
   ===================================================== */
.hero-section {
    background: #FFFFFF;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    padding: 36px 40px;
    margin: 24px 24px 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 32px;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 40%;
    height: 100%;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    z-index: 0;
    border-radius: 0 16px 16px 0;
}

.hero-content {
    position: relative;
    z-index: 1;
    flex: 1;
}

.hero-title {
    font-size: 32px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    line-height: 1.2 !important;
    margin-bottom: 8px !important;
}

.hero-title span {
    color: #2563EB !important;
}

.hero-subtitle {
    font-size: 15px !important;
    color: #64748B !important;
    line-height: 1.6 !important;
    margin-bottom: 24px !important;
}

.hero-buttons {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: #2563EB;
    color: white !important;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: background 0.2s;
}

.btn-primary:hover { background: #1D4ED8; }

.btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: white;
    color: #1E293B !important;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    border: 1.5px solid #CBD5E1;
    cursor: pointer;
}

.hero-visual {
    position: relative;
    z-index: 1;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: 16px;
}

.hero-chart-mockup {
    width: 200px;
    height: 130px;
    background: white;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    padding: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    display: flex;
    align-items: flex-end;
    gap: 6px;
}

.hero-chart-mockup .bar {
    flex: 1;
    border-radius: 4px 4px 0 0;
    background: linear-gradient(180deg, #3B82F6, #2563EB);
    opacity: 0.8;
}

.hero-status-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    color: #16A34A;
    white-space: nowrap;
}

.hero-status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22C55E;
    animation: pulse-green 2s infinite;
}

@keyframes pulse-green {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(1.3); }
}

/* =====================================================
   ÁREA DE CARGA Y MÓDULOS
   ===================================================== */
.content-area {
    padding: 20px 24px 24px 24px;
}

/* Card genérica */
.card {
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.card-title {
    font-size: 15px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    margin-bottom: 4px !important;
}

.card-subtitle {
    font-size: 13px !important;
    color: #64748B !important;
    margin-bottom: 0 !important;
}

/* Upload card */
.upload-card {
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    padding: 28px 32px;
    margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    display: flex;
    align-items: center;
    gap: 32px;
}

.upload-icon-wrap {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    background: #EFF6FF;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 24px;
}

.upload-dropzone {
    flex: 1;
    border: 2px dashed #CBD5E1;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s;
}

.upload-dropzone:hover { border-color: #2563EB; }

.upload-dropzone .drop-label {
    font-size: 14px;
    font-weight: 600;
    color: #1E293B;
    margin-bottom: 4px;
}

.upload-dropzone .drop-label a {
    color: #2563EB;
    text-decoration: none;
}

.upload-dropzone .drop-hint {
    font-size: 12px;
    color: #94A3B8;
}

/* Recent files panel */
.recent-files-card {
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    padding: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.recent-files-title {
    font-size: 14px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    margin-bottom: 14px !important;
}

.file-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #F1F5F9;
}

.file-item:last-child { border-bottom: none; }

.file-icon {
    width: 32px;
    height: 32px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}

.file-icon.xlsx { background: #F0FDF4; }
.file-icon.csv { background: #EFF6FF; }

.file-info .file-name {
    font-size: 12px;
    font-weight: 600;
    color: #1E293B;
}

.file-info .file-meta {
    font-size: 11px;
    color: #94A3B8;
}

.view-all-link {
    font-size: 12px;
    font-weight: 600;
    color: #2563EB;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 10px;
}

/* =====================================================
   MÓDULOS / QUICK ACCESS CARDS
   ===================================================== */
.section-header {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    margin-bottom: 16px !important;
    margin-top: 4px !important;
}

.modules-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 14px;
    margin-bottom: 20px;
}

@media (max-width: 1400px) {
    .modules-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 900px) {
    .modules-grid { grid-template-columns: repeat(2, 1fr); }
}

.module-card {
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    padding: 18px 16px 14px 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.module-card:hover {
    border-color: #BFDBFE;
    box-shadow: 0 4px 16px rgba(37,99,235,0.08);
    transform: translateY(-2px);
}

.module-card .mod-icon {
    font-size: 28px;
    margin-bottom: 10px;
    display: block;
}

.module-card .mod-name {
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    margin-bottom: 4px !important;
}

.module-card .mod-desc {
    font-size: 11px !important;
    color: #64748B !important;
    line-height: 1.5 !important;
    margin-bottom: 10px !important;
}

.module-card .mod-arrow {
    font-size: 16px;
    color: #CBD5E1;
    display: block;
    transition: color 0.2s, transform 0.2s;
}

.module-card:hover .mod-arrow {
    color: #2563EB;
    transform: translateX(3px);
}

/* =====================================================
   CONSEJO / TIP CARD
   ===================================================== */
.tip-card {
    background: #FFFFFF;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.tip-icon {
    font-size: 22px;
    flex-shrink: 0;
}

.tip-label {
    font-size: 13px;
    font-weight: 700;
    color: #2563EB;
    margin-bottom: 2px;
}

.tip-text {
    font-size: 13px;
    color: #475569;
}

.tip-actions {
    margin-left: auto;
    display: flex;
    gap: 16px;
    flex-shrink: 0;
    font-size: 22px;
}

/* =====================================================
   MULTISELECT MODERNO
   ===================================================== */
div[data-testid="stMultiSelect"] label p {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #374151 !important;
}

div[data-testid="stMultiSelect"] div[data-baseweb="select"] {
    border-radius: 10px !important;
    border: 1.5px solid #E2E8F0 !important;
    background: #FFFFFF !important;
}

/* =====================================================
   INFO / SUCCESS / WARNING / ERROR MESSAGES
   ===================================================== */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 4px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
}

/* =====================================================
   BOTONES STREAMLIT
   ===================================================== */
.stButton > button {
    border-radius: 8px !important;
    background: #2563EB !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border: none !important;
    padding: 8px 18px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: background 0.2s !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.2) !important;
}

.stButton > button:hover {
    background: #1D4ED8 !important;
}

/* =====================================================
   TABS
   ===================================================== */
div[data-testid="stTabs"] button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* =====================================================
   DATAFRAMES / TABLAS
   ===================================================== */
div[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid #E2E8F0 !important;
}

/* =====================================================
   INPUTS Y SLIDERS
   ===================================================== */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    border-radius: 8px !important;
    border: 1.5px solid #E2E8F0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
}

/* =====================================================
   HEADERS DE STREAMLIT (h1, h2, h3)
   ===================================================== */
h1, h2, h3, h4 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* =====================================================
   SCROLLBAR CUSTOM
   ===================================================== */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F1F5F9; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

/* Ocultar el "Made with Streamlit" footer */
footer { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }
header[data-testid="stHeader"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    # Logo
    try:
        st.image("logo2.png", use_container_width=False, width=80)
    except Exception:
        st.markdown("<div style='text-align:center;font-size:40px;padding:20px 0 8px 0'>⚙️</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-brand-title'>Control Estadístico<br>de Procesos</div>", unsafe_allow_html=True)

    # Separador CONFIGURACIÓN
    st.markdown("<span class='sidebar-section-label'>Configuración</span>", unsafe_allow_html=True)

    fase = st.selectbox(
        "Entorno:",
        ["Fase 1", "Fase 2", "Planes de Muestreo", "Análisis Económico (Mermas)"],
        label_visibility="collapsed"
    )

    # Módulos según fase
    MODULOS = {
        "Fase 1": ["Capacidad", "Gráficos de Control", "Estadística"],
        "Fase 2": ["Monitoreo en Tiempo Real", "Potencia", "ARL y ATS"],
        "Planes de Muestreo": ["Diseño y Planes"],
        "Análisis Económico (Mermas)": ["Optimización de Peso Seteado"],
    }

    ICONOS = {
        "Capacidad": "📊",
        "Gráficos de Control": "📈",
        "Estadística": "∑",
        "Monitoreo en Tiempo Real": "🔴",
        "Potencia": "⚡",
        "ARL y ATS": "🕐",
        "Diseño y Planes": "📋",
        "Optimización de Peso Seteado": "💰",
    }

    label_fase = fase.replace("Análisis Económico (Mermas)", "Económico").upper()
    st.markdown(f"<span class='sidebar-section-label'>Módulos {label_fase[:12]}</span>", unsafe_allow_html=True)

    opciones = MODULOS[fase]
    menu = st.selectbox("Módulo:", opciones, label_visibility="collapsed")

    # Nav items decorativos
    for op in opciones:
        active_class = "active" if op == menu else ""
        st.markdown(
            f"<div class='sidebar-nav-item {active_class}'>{ICONOS.get(op, '▸')} {op}</div>",
            unsafe_allow_html=True
        )

    # Caja de ayuda
    st.markdown("""
    <div class="sidebar-help-box">
        <div class="help-title">¿Necesitas ayuda?</div>
        <div class="help-text">Consulta la documentación o contacta soporte técnico.</div>
    </div>
    """, unsafe_allow_html=True)

    # Botón de ayuda
    st.button("🔗  Ir a la ayuda", use_container_width=True)

    # Footer
    st.markdown("<div class='sidebar-footer'>© 2025 PRO-STATS<br>Todos los derechos reservados.</div>", unsafe_allow_html=True)

# =====================================================
# TOPBAR
# =====================================================
st.markdown("""
<div class="topbar">
    <div class="topbar-icon-btn">☀️</div>
    <div class="topbar-icon-btn">
        🔔
        <div class="topbar-badge">2</div>
    </div>
    <div class="topbar-user">
        <div class="topbar-user-avatar">U</div>
        <span class="topbar-user-name">Usuario</span>
        <span style="color:#94A3B8;font-size:12px;">▾</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# HERO SECTION
# =====================================================
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <div class="hero-title">Sistema de <span>Control<br>de Calidad</span></div>
        <div class="hero-subtitle">Monitoreo estadístico, análisis de capacidad<br>y simulación avanzada.</div>
        <div class="hero-buttons">
            <span class="btn-primary">📊 Comenzar análisis</span>
            <span class="btn-secondary">📄 Ver reportes</span>
        </div>
    </div>
    <div class="hero-visual">
        <div class="hero-chart-mockup">
            <div class="bar" style="height:40%"></div>
            <div class="bar" style="height:65%"></div>
            <div class="bar" style="height:50%"></div>
            <div class="bar" style="height:80%"></div>
            <div class="bar" style="height:55%"></div>
            <div class="bar" style="height:70%"></div>
            <div class="bar" style="height:90%"></div>
            <div class="bar" style="height:60%"></div>
        </div>
        <div class="hero-status-badge">
            <div class="hero-status-dot"></div>
            Proceso<br>Bajo Control
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# ÁREA DE CONTENIDO PRINCIPAL
# =====================================================
st.markdown("<div class='content-area'>", unsafe_allow_html=True)

# ─── RUTAS QUE NO NECESITAN DATOS ───
if fase == "Planes de Muestreo":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    render_muestreo_modulo()
    st.markdown("</div>", unsafe_allow_html=True)

elif fase == "Análisis Económico (Mermas)":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    render_modulo_economico()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # ─── CARGA DE DATOS ───
    col_upload, col_recent = st.columns([3, 1.2])

    with col_upload:
        st.markdown("""
        <div class="card">
            <div class="card-title">📁 Carga de datos</div>
            <div class="card-subtitle">Sube tu archivo CSV o Excel para comenzar con el análisis del proceso.</div>
        </div>
        """, unsafe_allow_html=True)

        df = load_data()

    with col_recent:
        st.markdown("""
        <div class="recent-files-card">
            <div class="recent-files-title">📂 Archivos recientes</div>
            <div class="file-item">
                <div class="file-icon xlsx">📗</div>
                <div class="file-info">
                    <div class="file-name">datos_proceso.xlsx</div>
                    <div class="file-meta">28/05/2025 • 3.2 MB</div>
                </div>
            </div>
            <div class="file-item">
                <div class="file-icon csv">📘</div>
                <div class="file-info">
                    <div class="file-name">subgrupos_fase1.csv</div>
                    <div class="file-meta">27/05/2025 • 1.1 MB</div>
                </div>
            </div>
            <div class="file-item">
                <div class="file-icon xlsx">📗</div>
                <div class="file-info">
                    <div class="file-name">mediciones_proceso.xlsx</div>
                    <div class="file-meta">26/05/2025 • 2.4 MB</div>
                </div>
            </div>
            <a class="view-all-link" href="#">Ver todos los archivos →</a>
        </div>
        """, unsafe_allow_html=True)

    if df is not None:
        df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all')

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        cols_seleccionadas = st.multiselect("📌 Selecciona las columnas a analizar:", df.select_dtypes(include=['number']).columns)
        st.markdown("</div>", unsafe_allow_html=True)

        if cols_seleccionadas:
            data_subset = df[cols_seleccionadas].copy()
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            if fase == "Fase 1":
                if menu == "Capacidad":
                    capability_analysis(data_subset)
                elif menu == "Gráficos de Control":
                    control_chart_module(data_subset)
                elif menu == "Estadística":
                    normality_analysis(data_subset)

            elif fase == "Fase 2":
                if menu == "Monitoreo en Tiempo Real":
                    arl_live_simulation()
                elif menu == "Potencia":
                    ejecutar_potencia(data_subset)
                elif menu == "ARL y ATS":
                    arl_analysis(data_subset)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Acceso rápido a módulos
            st.markdown("<div class='section-header'>Acceso rápido a módulos</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="modules-grid">
                <div class="module-card">
                    <span class="mod-icon">📊</span>
                    <div class="mod-name">Capacidad</div>
                    <div class="mod-desc">Analiza la capacidad del proceso con cartas de control Cp, Cpk y otros índices.</div>
                    <span class="mod-arrow">→</span>
                </div>
                <div class="module-card">
                    <span class="mod-icon">📈</span>
                    <div class="mod-name">Gráficos de Control</div>
                    <div class="mod-desc">Monitorea la estabilidad del proceso con cartas de control en tiempo real.</div>
                    <span class="mod-arrow">→</span>
                </div>
                <div class="module-card">
                    <span class="mod-icon">∑</span>
                    <div class="mod-name">Estadística</div>
                    <div class="mod-desc">Realiza análisis descriptivo y pruebas de normalidad de tus datos.</div>
                    <span class="mod-arrow">→</span>
                </div>
                <div class="module-card">
                    <span class="mod-icon">🔴</span>
                    <div class="mod-name">Monitoreo en Tiempo Real</div>
                    <div class="mod-desc">Monitorea el proceso con datos en tiempo real y recibe alertas automáticas.</div>
                    <span class="mod-arrow">→</span>
                </div>
                <div class="module-card">
                    <span class="mod-icon">⚡</span>
                    <div class="mod-name">Potencia</div>
                    <div class="mod-desc">Evalúa la potencia estadística de tu sistema de monitoreo y sensibilidad.</div>
                    <span class="mod-arrow">→</span>
                </div>
                <div class="module-card">
                    <span class="mod-icon">🕐</span>
                    <div class="mod-name">ARL y ATS</div>
                    <div class="mod-desc">Calcula ARL, ATS y evalúa el desempeño temporal del sistema.</div>
                    <span class="mod-arrow">→</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Tip card
            st.markdown("""
            <div class="tip-card">
                <span class="tip-icon">ℹ️</span>
                <div>
                    <div class="tip-label">Consejo</div>
                    <div class="tip-text">Mantén tus procesos bajo control y toma decisiones basadas en datos.</div>
                </div>
                <div class="tip-actions">🔔 📈 🎯</div>
            </div>
            """, unsafe_allow_html=True)

    else:
        # Acceso rápido a módulos (sin datos cargados)
        st.markdown("<div class='section-header'>Acceso rápido a módulos</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="modules-grid">
            <div class="module-card">
                <span class="mod-icon">📊</span>
                <div class="mod-name">Capacidad</div>
                <div class="mod-desc">Analiza la capacidad del proceso con cartas de control Cp, Cpk y otros índices.</div>
                <span class="mod-arrow">→</span>
            </div>
            <div class="module-card">
                <span class="mod-icon">📈</span>
                <div class="mod-name">Gráficos de Control</div>
                <div class="mod-desc">Monitorea la estabilidad del proceso con cartas de control en tiempo real.</div>
                <span class="mod-arrow">→</span>
            </div>
            <div class="module-card">
                <span class="mod-icon">∑</span>
                <div class="mod-name">Estadística</div>
                <div class="mod-desc">Realiza análisis descriptivo y pruebas de normalidad de tus datos.</div>
                <span class="mod-arrow">→</span>
            </div>
            <div class="module-card">
                <span class="mod-icon">🔴</span>
                <div class="mod-name">Monitoreo en Tiempo Real</div>
                <div class="mod-desc">Monitorea el proceso con datos en tiempo real y recibe alertas automáticas.</div>
                <span class="mod-arrow">→</span>
            </div>
            <div class="module-card">
                <span class="mod-icon">⚡</span>
                <div class="mod-name">Potencia</div>
                <div class="mod-desc">Evalúa la potencia estadística de tu sistema de monitoreo y sensibilidad.</div>
                <span class="mod-arrow">→</span>
            </div>
            <div class="module-card">
                <span class="mod-icon">🕐</span>
                <div class="mod-name">ARL y ATS</div>
                <div class="mod-desc">Calcula ARL, ATS y evalúa el desempeño temporal del sistema.</div>
                <span class="mod-arrow">→</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="tip-card">
            <span class="tip-icon">ℹ️</span>
            <div>
                <div class="tip-label">Consejo</div>
                <div class="tip-text">Mantén tus procesos bajo control y toma decisiones basadas en datos.</div>
            </div>
            <div class="tip-actions">🔔 📈 🎯</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # cierre content-area