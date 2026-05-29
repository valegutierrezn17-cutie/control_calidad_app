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
from modules.reporter import generar_reporte_pdf

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
.sidebar-title { font-size: 22px; font-weight: 700; text-align: center; padding: 10px 0 20px 0; color: white !important; }
.main-title { font-size: 38px; font-weight: 800; color: #1B2631; margin-bottom: 0.2rem; }
.subtitle { color: #5D6D7E; font-size: 16px; margin-bottom: 2rem; }
.card { background: rgba(255,255,255,0.72); border-radius: 22px; padding: 24px; border: 1px solid rgba(255,255,255,0.5); box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 20px; }
.stButton>button { border-radius: 14px; background: linear-gradient(135deg, #3498DB, #2E86C1); color: white; font-weight: 600; }
.modules-section-title { font-size: 13px; font-weight: 700; color: #8A9BB0; letter-spacing: 0.08em; text-transform: uppercase; margin: 2rem 0 1rem 0; }
.module-card { background: #ffffff; border-radius: 20px; padding: 32px 28px 28px 28px; border: 1px solid #E8EEF5; box-shadow: 0 2px 12px rgba(0,0,0,0.045); transition: box-shadow 0.2s, transform 0.2s; display: flex; flex-direction: column; align-items: flex-start; gap: 12px; min-height: 170px; }
</style>
""", unsafe_allow_html=True)

st.sidebar.image("logo2.png", use_container_width=True)
st.sidebar.markdown("<div class='sidebar-title'>Control Estadístico de Procesos</div>", unsafe_allow_html=True)

fase = st.sidebar.selectbox("Selecciona el Entorno:", ["Inicio", "Fase 1", "Fase 2", "Planes de Muestreo", "Análisis Económico (Mermas)"])

menu = None
if fase == "Fase 1": menu = st.sidebar.selectbox("Módulos Fase 1:", ["Capacidad", "Gráficos", "Estadística"])
elif fase == "Fase 2": menu = st.sidebar.selectbox("Módulos Fase 2:", ["Monitoreo en Tiempo Real", "Potencia", "ARL"])
elif fase == "Planes de Muestreo": menu = st.sidebar.selectbox("Herramientas de Muestreo:", ["Diseño y Planes"])
elif fase == "Análisis Económico (Mermas)": menu = st.sidebar.selectbox("Simulación Financiera:", ["Optimización de Peso Seteado"])

st.markdown("<div class='main-title'>Sistema de Control de Calidad</div>", unsafe_allow_html=True)

if fase == "Inicio":
    st.write("Bienvenido al sistema. Selecciona un módulo en la barra lateral.")
elif fase == "Planes de Muestreo":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    render_muestreo_modulo()
    st.markdown("</div>", unsafe_allow_html=True)
elif fase == "Análisis Económico (Mermas)":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    render_modulo_economico()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    df = load_data()
    if df is not None:
        df = df.apply(pd.to_numeric, errors='coerce').dropna(how='all')
        cols_seleccionadas = st.multiselect("Selecciona las columnas:", df.select_dtypes(include=['number']).columns)
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

            st.markdown("---")
            with st.expander("📄 Generar Reporte Técnico"):
                conclusiones = st.text_area("Conclusiones:", height=100)
                if st.button("Compilar PDF"):
                    pdf_bytes = generar_reporte_pdf("Reporte", data_subset, {}, conclusiones)
                    st.download_button(
                        label="Descargar Reporte PDF",
                        data=pdf_bytes,
                        file_name="reporte.pdf",
                        mime="application/pdf"
                    )
    st.markdown("</div>", unsafe_allow_html=True)