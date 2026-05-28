import streamlit as st
import pandas as pd
import sys
import os

# Configuración de rutas
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

# Configuración de página
st.set_page_config(layout="wide", page_title="PRO-STATS | Control de Calidad", page_icon="⚙️")

# CSS Profesional
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
.stApp { background: #F0F4F8; font-family: 'Plus Jakarta Sans', sans-serif; }
.card { background: white; padding: 24px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 20px; }
.hero-title { font-size: 42px; font-weight: 800; color: #0F172A; }
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.image("logo2.png", width=100)
    st.markdown("### PRO-STATS")
    fase = st.selectbox("Entorno:", ["Fase 1", "Fase 2", "Planes de Muestreo", "Análisis Económico (Mermas)"])
    
    if fase == "Fase 1": menu = st.selectbox("Módulo:", ["Capacidad", "Gráficos de Control", "Estadística"])
    elif fase == "Fase 2": menu = st.selectbox("Módulo:", ["Monitoreo en Tiempo Real", "Potencia", "ARL y ATS"])
    else: menu = None

# HEADER
st.markdown('<div class="hero-title">Sistema de Control de Calidad</div>', unsafe_allow_html=True)
st.subheader("Monitoreo estadístico y simulación avanzada")

# LÓGICA PRINCIPAL
st.markdown('<div class="card">', unsafe_allow_html=True)

try:
    if fase == "Planes de Muestreo":
        render_muestreo_modulo()
    elif fase == "Análisis Económico (Mermas)":
        render_modulo_economico()
    else:
        df = load_data()
        if df is not None:
            df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all')
            cols = st.multiselect("Selecciona columnas:", df.columns)
            if cols:
                data = df[cols].copy()
                if fase == "Fase 1":
                    if menu == "Capacidad": capability_analysis(data)
                    elif menu == "Gráficos de Control": control_chart_module(data)
                    elif menu == "Estadística": normality_analysis(data)
                elif fase == "Fase 2":
                    if menu == "Monitoreo en Tiempo Real": arl_live_simulation()
                    elif menu == "Potencia": ejecutar_potencia(data)
                    elif menu == "ARL y ATS": arl_analysis(data)
            else:
                st.info("Selecciona columnas para visualizar el análisis.")
        else:
            st.warning("No se pudieron cargar los datos. Verifica el archivo.")
except Exception as e:
    st.error(f"Ocurrió un error inesperado en la ejecución: {e}")

st.markdown('</div>', unsafe_allow_html=True)