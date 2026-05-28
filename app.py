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
/* Fondo de la aplicación */
.stApp{ background: linear-gradient(135deg, #f4f7fb 0%, #eef2f7 100%); }
.main .block-container{ padding-top: 1.2rem !important; max-width: 98%; }

/* Fondo oscuro para la Barra Lateral (Sidebar) */
section[data-testid="stSidebar"] { 
    background: #1f2a38 !important; 
}

/* =======================================================================
   PARCHE DEFINITIVO: Control de textos en Sidebar (Sin usar el asterisco *)
   ======================================================================= */
/* Pintamos de blanco SOLO los textos del sistema, títulos y etiquetas del Sidebar */
.sidebar-title { 
    font-size: 24px; 
    font-weight: 700; 
    text-align:center; 
    padding: 10px 0 20px 0; 
    color: white !important; 
}
section[data-testid="stSidebar"] .stMarkdown p { 
    color: white !important; 
    line-height: 1.6 !important;
}
section[data-testid="stSidebar"] label p { 
    color: white !important;  /* Esto hace blanco el título encima del selectbox */
}

/* Forzamos que el texto seleccionado DENTRO del cuadro del selectbox sea oscuro */
div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
    color: #1B2631 !important;
}

/* Aseguramos que la lista desplegable de opciones (al hacer clic) sea blanca con letras oscuras */
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] li * {
    background-color: #FFFFFF !important;
    color: #1B2631 !important;
}

/* Efecto visual cuando pasas el mouse sobre las opciones del menú */
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li:hover * {
    background-color: #F0F4F8 !important;
    color: #2E86C1 !important;
}
/* ======================================================================= */

/* Estilos del Panel Principal */
.main-title{ font-size: 40px; font-weight: 800; color: #1B2631; margin-bottom: 0.2rem; }
.subtitle{ color: #5D6D7E; font-size: 16px; margin-bottom: 2rem; }
.card{ background: rgba(255,255,255,0.72); border-radius: 22px; padding: 24px; border: 1px solid rgba(255,255,255,0.5); box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 20px; }
.stButton>button{ border-radius: 14px; background: linear-gradient(135deg, #3498DB, #2E86C1); color: white; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# SIDEBAR Y ENRUTAMIENTO
st.sidebar.image("logo2.png", use_container_width=True)
st.sidebar.markdown("<div class='sidebar-title'>Control Estadístico de Procesos</div>", unsafe_allow_html=True)

fase = st.sidebar.selectbox(
    "Selecciona el Entorno:",
    ["Fase 1", "Fase 2", "Planes de Muestreo", "Análisis Económico (Mermas)"]
)

if fase == "Fase 1":
    menu = st.sidebar.selectbox(" Módulos Fase 1:", ["Capacidad", "Gráficos", "Estadística"])
elif fase == "Fase 2":
    menu = st.sidebar.selectbox(" Módulos Fase 2:", ["Monitoreo en Tiempo Real", "Potencia", "ARL"])
elif fase == "Planes de Muestreo":
    menu = st.sidebar.selectbox(" Herramientas de Muestreo:", ["Diseño y Planes"])
elif fase == "Análisis Económico (Mermas)":
    menu = st.sidebar.selectbox(" Simulación Financiera:", ["Optimización de Peso Seteado"])

# HEADER
st.markdown("""<div class="main-title">Sistema de Control de Calidad</div><div class="subtitle">Monitoreo estadístico, análisis de capacidad y simulación avanzada</div>""", unsafe_allow_html=True)

# CONTENEDOR PRINCIPAL
st.markdown("<div class='card'>", unsafe_allow_html=True)

# ENRUTAMIENTO PRINCIPAL
if fase == "Planes de Muestreo":
    render_muestreo_modulo()
elif fase == "Análisis Económico (Mermas)":
    render_modulo_economico()
else:
    df = load_data()
    if df is not None:
        df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all')
        cols_seleccionadas = st.multiselect("📌 Selecciona las columnas:", df.select_dtypes(include=['number']).columns)
        if cols_seleccionadas:
            data_subset = df[cols_seleccionadas].copy()
            if fase == "Fase 1":
                if menu == "Capacidad": capability_analysis(data_subset)
                elif menu == "Gráficos": control_chart_module(data_subset)
                elif menu == "Estadística": normality_analysis(data_subset)
            elif fase == "Fase 2":
                if menu == "Monitoreo en Tiempo Real": arl_live_simulation()
                elif menu == "Potencia": ejecutar_potencia(data_subset)
                elif menu == "ARL": arl_analysis(data_subset)
        else:
            st.info("Selecciona columnas para continuar.")
    else:
        st.info("Carga un archivo CSV o Excel para comenzar.")

st.markdown("</div>", unsafe_allow_html=True)