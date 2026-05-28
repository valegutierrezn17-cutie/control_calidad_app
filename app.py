import streamlit as st
import pandas as pd
import sys
import os
import json
from datetime import datetime

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
st.set_page_config(
    layout="wide",
    page_title="PRO-STATS | Control Estadístico de Procesos",
    page_icon="⚙️"
)

# =========================
# SESSION STATE: historial de archivos
# =========================
if "file_history" not in st.session_state:
    st.session_state.file_history = []

if "active_module" not in st.session_state:
    st.session_state.active_module = None

# =========================
# CSS PRINCIPAL
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');

/* =====================================================
   RESET Y VARIABLES
   ===================================================== */
:root {
  --bg-page:       #F4F6FA;
  --bg-card:       #FFFFFF;
  --bg-sidebar:    #0D1117;
  --bg-sidebar-2:  #161B22;
  --border:        #E4E8EF;
  --border-soft:   #F0F2F7;
  --text-primary:  #0D1117;
  --text-secondary:#5C6880;
  --text-muted:    #9AA3B2;
  --text-sidebar:  #8B949E;
  --text-sidebar-active: #F0F6FF;
  --accent:        #1A6CF6;
  --accent-2:      #0EA5E9;
  --accent-hover:  #1558D6;
  --accent-glow:   rgba(26,108,246,0.15);
  --accent-bg:     #EEF4FF;
  --success:       #16A34A;
  --success-bg:    #F0FDF4;
  --success-border:#BBF7D0;
  --warning:       #D97706;
  --warning-bg:    #FFFBEB;
  --danger:        #DC2626;
  --radius-sm:     6px;
  --radius-md:     10px;
  --radius-lg:     14px;
  --radius-xl:     18px;
  --shadow-xs:     0 1px 3px rgba(0,0,0,0.06);
  --shadow-sm:     0 2px 8px rgba(0,0,0,0.07);
  --shadow-md:     0 4px 20px rgba(0,0,0,0.08);
  --shadow-lg:     0 8px 32px rgba(0,0,0,0.1);
  --font:          'DM Sans', sans-serif;
  --font-mono:     'DM Mono', monospace;
  --sidebar-w:     248px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
  font-family: var(--font) !important;
  background: var(--bg-page) !important;
  color: var(--text-primary) !important;
}

.main .block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

/* Ocultar chrome de Streamlit */
footer { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }
header[data-testid="stHeader"] { display: none !important; }
.stDeployButton { display: none !important; }

/* =====================================================
   SIDEBAR
   ===================================================== */
section[data-testid="stSidebar"] {
  background: var(--bg-sidebar) !important;
  width: var(--sidebar-w) !important;
  min-width: var(--sidebar-w) !important;
  border-right: 1px solid rgba(255,255,255,0.04) !important;
}

section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] .block-container {
  padding: 0 !important;
  background: transparent !important;
}

/* Logo */
section[data-testid="stSidebar"] img {
  display: block !important;
  margin: 28px auto 0 auto !important;
  width: 52px !important;
  height: 52px !important;
  object-fit: contain !important;
  border-radius: 12px !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
}

/* Textos sidebar */
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label p {
  color: var(--text-sidebar) !important;
  font-family: var(--font) !important;
  font-size: 12px !important;
}

/* Selectbox sidebar */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] {
  margin: 0 12px 4px 12px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] {
  background: rgba(255,255,255,0.05) !important;
  border-radius: var(--radius-md) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  transition: border-color 0.2s;
}

section[data-testid="stSidebar"] div[data-baseweb="select"]:hover {
  border-color: rgba(255,255,255,0.14) !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
  background: transparent !important;
  border: none !important;
  color: #E6EDF3 !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  font-family: var(--font) !important;
  padding: 9px 12px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
  fill: #8B949E !important;
}

/* Dropdown options */
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li {
  background: #1C2128 !important;
  color: #E6EDF3 !important;
  font-family: var(--font) !important;
  font-size: 13px !important;
}

div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li:hover * {
  background: #2D333B !important;
  color: #FFFFFF !important;
}

/* Sidebar button */
section[data-testid="stSidebar"] .stButton > button {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  color: #8B949E !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  border-radius: var(--radius-md) !important;
  padding: 7px 14px !important;
  box-shadow: none !important;
  transition: all 0.2s !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,255,255,0.1) !important;
  color: #E6EDF3 !important;
  border-color: rgba(255,255,255,0.14) !important;
}

/* Nav items */
.sb-nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 14px;
  margin: 1px 10px;
  border-radius: var(--radius-md);
  color: var(--text-sidebar) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  cursor: pointer;
  transition: all 0.18s ease;
  user-select: none;
}

.sb-nav-item:hover {
  background: rgba(255,255,255,0.06);
  color: #C9D1D9 !important;
}

.sb-nav-item.active {
  background: rgba(26,108,246,0.18);
  color: #79B8FF !important;
  font-weight: 600 !important;
}

.sb-nav-item.active .sb-icon svg { stroke: #79B8FF !important; }

.sb-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  opacity: 0.7;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sb-nav-item.active .sb-icon { opacity: 1; }

/* Sidebar divider */
.sb-divider {
  height: 1px;
  background: rgba(255,255,255,0.05);
  margin: 10px 14px;
}

/* Sidebar section label */
.sb-label {
  color: #484F58 !important;
  font-size: 10px !important;
  font-weight: 600 !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  padding: 12px 14px 5px 14px !important;
  display: block;
}

/* Sidebar brand */
.sb-brand {
  text-align: center;
  padding: 10px 16px 20px 16px;
}

.sb-brand-name {
  color: #E6EDF3 !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  line-height: 1.3;
  margin-bottom: 2px;
}

.sb-brand-tagline {
  color: #484F58 !important;
  font-size: 10px !important;
  font-weight: 500 !important;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* Sidebar footer */
.sb-footer {
  color: #30363D !important;
  font-size: 10px !important;
  text-align: center;
  padding: 12px 16px;
  border-top: 1px solid rgba(255,255,255,0.04);
  line-height: 1.6;
}

/* Sidebar help box */
.sb-help {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: var(--radius-lg);
  padding: 14px;
  margin: 12px 12px 8px 12px;
}

.sb-help-title {
  color: #8B949E !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  margin-bottom: 3px;
}

.sb-help-text {
  color: #484F58 !important;
  font-size: 11px !important;
  line-height: 1.5;
}

/* =====================================================
   TOPBAR
   ===================================================== */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  height: 58px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.topbar-breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-muted);
}

.topbar-breadcrumb .crumb-active {
  color: var(--text-primary);
  font-weight: 600;
}

.topbar-breadcrumb svg { opacity: 0.4; }

.topbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.topbar-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--bg-page);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  transition: all 0.18s;
  color: var(--text-secondary);
}

.topbar-btn:hover {
  background: var(--border-soft);
  border-color: var(--border);
  color: var(--text-primary);
}

.topbar-badge {
  position: absolute;
  top: -2px; right: -2px;
  background: var(--accent);
  color: white;
  font-size: 8px;
  font-weight: 700;
  width: 14px; height: 14px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  border: 2px solid white;
  font-family: var(--font);
}

.topbar-user {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 10px 5px 5px;
  border-radius: 20px;
  background: var(--bg-page);
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.18s;
}

.topbar-user:hover { border-color: var(--accent); }

.topbar-avatar {
  width: 26px; height: 26px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent) 0%, #7C3AED 100%);
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 11px; font-weight: 700;
}

.topbar-username { font-size: 12px; font-weight: 600; color: var(--text-primary); }
.topbar-role { font-size: 10px; color: var(--text-muted); }

.topbar-separator {
  width: 1px; height: 20px;
  background: var(--border);
  margin: 0 4px;
}

/* =====================================================
   HERO / PAGE HEADER
   ===================================================== */
.page-header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  padding: 24px 32px 20px 32px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
}

.page-header-left {}

.page-eyebrow {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.eyebrow-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  background: var(--accent-bg);
  border: 1px solid rgba(26,108,246,0.15);
  border-radius: 4px;
  font-size: 10px;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.page-title {
  font-size: 22px !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  line-height: 1.2 !important;
  margin-bottom: 4px !important;
}

.page-desc {
  font-size: 13px !important;
  color: var(--text-secondary) !important;
  line-height: 1.5 !important;
  margin: 0 !important;
}

.page-header-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: var(--success-bg);
  border: 1px solid var(--success-border);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: var(--success);
}

.status-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #22C55E;
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.4); }
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--accent);
  color: white !important;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 600;
  font-family: var(--font);
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(26,108,246,0.25);
}

.btn-primary:hover {
  background: var(--accent-hover);
  box-shadow: 0 4px 16px rgba(26,108,246,0.3);
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: white;
  color: var(--text-primary) !important;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 600;
  font-family: var(--font);
  text-decoration: none;
  border: 1.5px solid var(--border);
  cursor: pointer;
  transition: all 0.18s;
}

.btn-outline:hover { border-color: var(--accent); color: var(--accent) !important; }

/* =====================================================
   CONTENT AREA
   ===================================================== */
.content-area {
  padding: 24px 32px 32px 32px;
}

/* =====================================================
   CARDS
   ===================================================== */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  padding: 22px 24px;
  margin-bottom: 18px;
  box-shadow: var(--shadow-xs);
}

.card-sm {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  padding: 16px 20px;
  box-shadow: var(--shadow-xs);
}

.card-title {
  font-size: 14px !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  margin-bottom: 3px !important;
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
}

.card-subtitle {
  font-size: 12px !important;
  color: var(--text-secondary) !important;
  margin: 0 !important;
  line-height: 1.5 !important;
}

/* Upload card */
.upload-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.upload-icon {
  width: 40px; height: 40px;
  border-radius: var(--radius-md);
  background: var(--accent-bg);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

/* =====================================================
   ARCHIVOS RECIENTES
   ===================================================== */
.files-list {}

.file-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 0;
  border-bottom: 1px solid var(--border-soft);
  transition: background 0.15s;
}

.file-row:last-child { border-bottom: none; }

.file-type-badge {
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px;
  font-weight: 700;
  flex-shrink: 0;
  font-family: var(--font-mono);
  letter-spacing: 0;
}

.badge-xlsx { background: #F0FDF4; color: #16A34A; border: 1px solid #BBF7D0; }
.badge-csv  { background: var(--accent-bg); color: var(--accent); border: 1px solid rgba(26,108,246,0.18); }
.badge-other { background: #FFF7ED; color: #D97706; border: 1px solid #FED7AA; }

.file-info { flex: 1; min-width: 0; }
.file-name { font-size: 12px; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.file-meta { font-size: 10px; color: var(--text-muted); margin-top: 1px; }

.file-action {
  width: 26px; height: 26px;
  border-radius: 6px;
  background: transparent;
  border: 1px solid transparent;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  color: var(--text-muted);
  transition: all 0.15s;
  font-size: 12px;
}

.file-action:hover { background: var(--bg-page); border-color: var(--border); color: var(--danger); }

/* =====================================================
   MODULE CARDS GRID
   ===================================================== */
.section-header {
  font-size: 15px !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  margin-bottom: 14px !important;
  margin-top: 0 !important;
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin-bottom: 20px;
}

@media (min-width: 1600px) {
  .modules-grid { grid-template-columns: repeat(6, 1fr); }
}

@media (max-width: 1100px) {
  .modules-grid { grid-template-columns: repeat(2, 1fr); }
}

.mod-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  padding: 20px 18px 16px 18px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
  display: block;
}

.mod-card::before {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent) 0%, var(--accent-2) 100%);
  opacity: 0;
  transition: opacity 0.2s;
}

.mod-card:hover {
  border-color: rgba(26,108,246,0.25);
  box-shadow: 0 4px 20px rgba(26,108,246,0.1);
  transform: translateY(-2px);
}

.mod-card:hover::before { opacity: 1; }

.mod-icon-wrap {
  width: 38px; height: 38px;
  border-radius: var(--radius-md);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 14px;
  transition: all 0.2s;
}

.mod-card:hover .mod-icon-wrap {
  box-shadow: 0 0 16px var(--accent-glow);
}

.mod-name {
  font-size: 13px !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  margin-bottom: 4px !important;
  line-height: 1.3 !important;
}

.mod-desc {
  font-size: 11px !important;
  color: var(--text-secondary) !important;
  line-height: 1.55 !important;
  margin-bottom: 14px !important;
}

.mod-arrow {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  transition: all 0.2s;
}

.mod-card:hover .mod-arrow {
  color: var(--accent);
  gap: 7px;
}

/* Icon colors per module */
.icon-blue   { background: var(--accent-bg); color: var(--accent); }
.icon-teal   { background: #F0FDFA; color: #0D9488; }
.icon-purple { background: #F5F3FF; color: #7C3AED; }
.icon-red    { background: #FEF2F2; color: #DC2626; }
.icon-amber  { background: var(--warning-bg); color: var(--warning); }
.icon-indigo { background: #EEF2FF; color: #4F46E5; }
.icon-green  { background: var(--success-bg); color: var(--success); }

/* =====================================================
   TIP CARD
   ===================================================== */
.tip-strip {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 20px;
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  box-shadow: var(--shadow-xs);
}

.tip-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 2px;
}

.tip-text {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* =====================================================
   STREAMLIT OVERRIDES
   ===================================================== */

/* Multiselect */
div[data-testid="stMultiSelect"] label p {
  font-size: 13px !important;
  font-weight: 600 !important;
  color: var(--text-primary) !important;
  font-family: var(--font) !important;
}

div[data-testid="stMultiSelect"] div[data-baseweb="select"] {
  border-radius: var(--radius-md) !important;
  border: 1.5px solid var(--border) !important;
  background: var(--bg-card) !important;
}

/* Alert boxes */
div[data-testid="stAlert"] {
  border-radius: var(--radius-md) !important;
  font-family: var(--font) !important;
  font-size: 13px !important;
}

/* Buttons (global) */
.stButton > button {
  border-radius: var(--radius-md) !important;
  background: var(--accent) !important;
  color: white !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  border: none !important;
  padding: 8px 18px !important;
  font-family: var(--font) !important;
  transition: background 0.2s, box-shadow 0.2s !important;
  box-shadow: 0 2px 8px rgba(26,108,246,0.2) !important;
}

.stButton > button:hover {
  background: var(--accent-hover) !important;
  box-shadow: 0 4px 14px rgba(26,108,246,0.3) !important;
}

/* Tabs */
div[data-testid="stTabs"] button {
  font-family: var(--font) !important;
  font-weight: 600 !important;
  font-size: 13px !important;
}

/* DataFrames */
div[data-testid="stDataFrame"] {
  border-radius: var(--radius-md) !important;
  overflow: hidden !important;
  border: 1px solid var(--border) !important;
}

/* Number / Text inputs */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
  border-radius: var(--radius-md) !important;
  border: 1.5px solid var(--border) !important;
  font-family: var(--font) !important;
  font-size: 13px !important;
  background: var(--bg-card) !important;
}

div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* Headings */
h1, h2, h3, h4 {
  font-family: var(--font) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* File uploader */
div[data-testid="stFileUploader"] {
  border-radius: var(--radius-md) !important;
}

div[data-testid="stFileUploadDropzone"] {
  border-radius: var(--radius-md) !important;
  border: 2px dashed var(--border) !important;
  background: var(--bg-page) !important;
  transition: border-color 0.2s !important;
}

div[data-testid="stFileUploadDropzone"]:hover {
  border-color: var(--accent) !important;
  background: var(--accent-bg) !important;
}

/* Select boxes (general) */
div[data-baseweb="select"] > div {
  font-family: var(--font) !important;
  font-size: 13px !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border-radius: var(--radius-lg) !important;
  border: 1px solid var(--border) !important;
  padding: 16px 18px !important;
  box-shadow: var(--shadow-xs) !important;
}

div[data-testid="stMetric"] label {
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
  color: var(--text-muted) !important;
  font-family: var(--font) !important;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
  font-size: 26px !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  font-family: var(--font) !important;
}

/* Plotly charts */
.js-plotly-plot .plotly .modebar { display: none !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# SVG ICONS (Lucide-style)
# =========================
def icon(name, size=16, cls=""):
    icons = {
        "bar-chart": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/></svg>',
        "trending-up": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
        "sigma": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><path d="M18 7H7l-4 5 4 5h11"/><path d="M18 12H7"/></svg>',
        "activity": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        "zap": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        "clock": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "clipboard": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>',
        "dollar": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "bell": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
        "alert": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><triangle points="10.29 3.86 1.82 18 2 18 22 18 22.18 18 13.71 3.86 10.29 3.86"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "sun": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
        "chevron-right": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><polyline points="9 18 15 12 9 6"/></svg>',
        "upload": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>',
        "info": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
        "help": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "file": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>',
        "trash": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>',
        "settings": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="{cls}"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    }
    return icons.get(name, "")


# =========================
# QUICK ACCESS HELPER
# =========================
def _quick_access_html():
    all_mods = [
        ("Capacidad",                "bar-chart",   "icon-blue",   "Indices Cp, Cpk y analisis de capacidad."),
        ("Graficos de Control",      "trending-up", "icon-teal",   "Cartas de control en tiempo real."),
        ("Estadistica",              "sigma",       "icon-purple", "Analisis descriptivo y normalidad."),
        ("Monitoreo en Tiempo Real", "activity",    "icon-red",    "Alertas automaticas con datos en vivo."),
        ("Potencia",                 "zap",         "icon-amber",  "Sensibilidad del sistema de monitoreo."),
        ("ARL y ATS",                "clock",       "icon-indigo", "Calculo de ARL, ATS y desempeno."),
    ]
    st.markdown("<div class='section-header'>Acceso rapido a modulos</div>", unsafe_allow_html=True)
    grid_html = '<div class="modules-grid">'
    for name, ico, color, desc in all_mods:
        grid_html += f"""<div class="mod-card">
          <div class="mod-icon-wrap {color}">{icon(ico, 18)}</div>
          <div class="mod-name">{name}</div>
          <div class="mod-desc">{desc}</div>
          <div class="mod-arrow">{icon("chevron-right", 12)} Ver modulo</div>
        </div>"""
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)
    tip_html = (
        '<div class="tip-strip">'
        + '<span style="color:var(--accent);flex-shrink:0">' + icon("info", 16) + "</span>"
        + "<div>"
        + '<div class="tip-label">Consejo</div>'
        + '<div class="tip-text">Carga un archivo CSV o Excel para habilitar todos los modulos de analisis.</div>'
        + "</div></div>"
    )
    st.markdown(tip_html, unsafe_allow_html=True)



# =========================
# SIDEBAR
# =========================
MODULOS = {
    "Fase 1":    ["Capacidad", "Gráficos de Control", "Estadística"],
    "Fase 2":    ["Monitoreo en Tiempo Real", "Potencia", "ARL y ATS"],
    "Planes de Muestreo":            ["Diseño y Planes"],
    "Análisis Económico (Mermas)":   ["Optimización de Peso Seteado"],
}

ICONOS = {
    "Capacidad":                   "bar-chart",
    "Gráficos de Control":         "trending-up",
    "Estadística":                 "sigma",
    "Monitoreo en Tiempo Real":    "activity",
    "Potencia":                    "zap",
    "ARL y ATS":                   "clock",
    "Diseño y Planes":             "clipboard",
    "Optimización de Peso Seteado":"dollar",
}

ICON_COLORS = {
    "Capacidad":                   "icon-blue",
    "Gráficos de Control":         "icon-teal",
    "Estadística":                 "icon-purple",
    "Monitoreo en Tiempo Real":    "icon-red",
    "Potencia":                    "icon-amber",
    "ARL y ATS":                   "icon-indigo",
    "Diseño y Planes":             "icon-green",
    "Optimización de Peso Seteado":"icon-amber",
}

MOD_DESC = {
    "Capacidad":                    "Índices Cp, Cpk y análisis de capacidad del proceso.",
    "Gráficos de Control":          "Cartas de control para monitorear la estabilidad.",
    "Estadística":                  "Estadística descriptiva y pruebas de normalidad.",
    "Monitoreo en Tiempo Real":     "Alertas automáticas y monitoreo con datos en vivo.",
    "Potencia":                     "Evalúa la sensibilidad del sistema de monitoreo.",
    "ARL y ATS":                    "Calcula ARL, ATS y desempeño temporal del sistema.",
    "Diseño y Planes":              "Diseño de planes de muestreo de aceptación.",
    "Optimización de Peso Seteado": "Análisis económico y optimización de mermas.",
}

with st.sidebar:
    try:
        st.image("logo2.png", use_container_width=False, width=52)
    except Exception:
        st.markdown(
            f"<div style='text-align:center;padding:28px 0 0 0;color:#79B8FF'>{icon('settings',32)}</div>",
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-name">PRO-STATS</div>
        <div class="sb-brand-tagline">Control Estadístico</div>
    </div>
    <div class="sb-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown("<span class='sb-label'>Entorno</span>", unsafe_allow_html=True)
    fase = st.selectbox("Entorno:", list(MODULOS.keys()), label_visibility="collapsed")

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    opciones = MODULOS[fase]
    fase_label = fase.replace("Análisis Económico (Mermas)", "Económico")[:14].upper()
    st.markdown(f"<span class='sb-label'>Módulos</span>", unsafe_allow_html=True)

    menu = st.selectbox("Módulo:", opciones, label_visibility="collapsed")

    for op in opciones:
        active = "active" if op == menu else ""
        st.markdown(
            f"""<div class="sb-nav-item {active}">
                  <span class="sb-icon">{icon(ICONOS.get(op,'file'))}</span>
                  {op}
               </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-help">
        <div class="sb-help-title">Documentación</div>
        <div class="sb-help-text">Consulta guías técnicas y soporte en el portal oficial.</div>
    </div>
    """, unsafe_allow_html=True)

    st.button(f"Ayuda y soporte", use_container_width=True)

    st.markdown("<div class='sb-footer'>© 2025 PRO-STATS<br>Todos los derechos reservados</div>", unsafe_allow_html=True)

# =========================
# TOPBAR
# =========================
st.markdown(f"""
<div class="topbar">
  <div class="topbar-left">
    <div class="topbar-breadcrumb">
      <span>PRO-STATS</span>
      {icon('chevron-right', 12)}
      <span>{fase}</span>
      {icon('chevron-right', 12)}
      <span class="crumb-active">{menu}</span>
    </div>
  </div>
  <div class="topbar-right">
    <div class="topbar-btn">{icon('sun', 15)}</div>
    <div class="topbar-btn">
      {icon('bell', 15)}
      <div class="topbar-badge">2</div>
    </div>
    <div class="topbar-separator"></div>
    <div class="topbar-user">
      <div class="topbar-avatar">U</div>
      <div>
        <div class="topbar-username">Usuario</div>
        <div class="topbar-role">Analista</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================
# PAGE HEADER
# =========================
st.markdown(f"""
<div class="page-header">
  <div class="page-header-left">
    <div class="page-eyebrow">
      <span class="eyebrow-tag">{fase}</span>
    </div>
    <div class="page-title">{menu}</div>
    <p class="page-desc">{MOD_DESC.get(menu, "Módulo de análisis estadístico profesional.")}</p>
  </div>
  <div class="page-header-right">
    <div class="status-pill">
      <div class="status-dot"></div>
      Sistema activo
    </div>
    <span class="btn-primary">{icon('bar-chart', 14)} Iniciar análisis</span>
    <span class="btn-outline">{icon('file', 14)} Exportar</span>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================
# CONTENT
# =========================
st.markdown("<div class='content-area'>", unsafe_allow_html=True)

# ─── MÓDULOS SIN DATOS ───
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
    col_upload, col_recent = st.columns([3, 1.3])

    with col_upload:
        st.markdown(f"""
        <div class="card">
          <div class="upload-header">
            <div class="upload-icon">{icon('upload', 20)}</div>
            <div>
              <div class="card-title">Carga de datos</div>
              <p class="card-subtitle">Sube tu archivo CSV o Excel para comenzar el análisis del proceso.</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = load_data()

        # Registrar en historial si es nuevo
        if uploaded_file is not None and hasattr(uploaded_file, 'name'):
            fname = uploaded_file.name
            # Evitar duplicados consecutivos
            existing = [f["name"] for f in st.session_state.file_history]
            if fname not in existing:
                ext = fname.rsplit(".", 1)[-1].upper() if "." in fname else "FILE"
                size_kb = getattr(uploaded_file, "size", 0)
                size_str = f"{size_kb/1024:.1f} KB" if size_kb < 1024*1024 else f"{size_kb/1024/1024:.1f} MB"
                st.session_state.file_history.insert(0, {
                    "name": fname,
                    "ext": ext,
                    "size": size_str,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                })
                # Conservar solo los últimos 8
                st.session_state.file_history = st.session_state.file_history[:8]

        df = uploaded_file

    with col_recent:
        # Archivos recientes — FUNCIONAL con session_state
        history = st.session_state.file_history
        rows_html = ""
        if history:
            to_delete = None
            for i, f in enumerate(history[:5]):
                ext = f.get("ext", "FILE")
                badge_cls = "badge-xlsx" if ext in ("XLSX","XLS") else ("badge-csv" if ext == "CSV" else "badge-other")
                rows_html += f"""
                <div class="file-row">
                  <div class="file-type-badge {badge_cls}">{ext}</div>
                  <div class="file-info">
                    <div class="file-name">{f['name']}</div>
                    <div class="file-meta">{f['date']} · {f['size']}</div>
                  </div>
                </div>"""
        else:
            rows_html = '<div style="color:var(--text-muted);font-size:12px;padding:8px 0;text-align:center;">Sin archivos recientes</div>'

        st.markdown(f"""
        <div class="card-sm">
          <div class="card-title" style="margin-bottom:12px!important;">
            {icon('file', 14)} Archivos recientes
          </div>
          <div class="files-list">{rows_html}</div>
        </div>
        """, unsafe_allow_html=True)

        # Botón limpiar historial
        if history:
            if st.button("Limpiar historial", use_container_width=True):
                st.session_state.file_history = []
                st.rerun()

    # ─── ANÁLISIS ───
    if df is not None:
        df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all')

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        cols_seleccionadas = st.multiselect(
            "Selecciona las columnas a analizar:",
            df.select_dtypes(include=['number']).columns
        )
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
            _quick_access_html()

    else:
        _quick_access_html()

st.markdown("</div>", unsafe_allow_html=True)  # cierre content-area