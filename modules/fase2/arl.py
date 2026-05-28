import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import norm

def arl_analysis(data_subset):

    st.header("ARL y ATS")

    # =========================
    # DATOS BASE
    # =========================
    mu0 = float(data_subset.mean().mean())
    sigma = float(data_subset.std().mean())

    col1, col2 = st.columns(2)

    with col1:
        n = st.number_input("Tamaño de muestra (n)", value=5, step=1)
        mu1 = st.number_input("Media con cambio (μ₁)", value=None, placeholder="Ej: 39.900", format="%.4f")
        alpha = st.number_input("Nivel de significancia (α)", value=0.0027, format="%.4f")

    with col2:
        tiempo_num = st.number_input("Tiempo entre muestras", value=None, placeholder="Ej: 20")
        unidad = st.selectbox("Unidad de tiempo", ["Minutos", "Horas"])

    st.markdown("---")

    # =========================
    # CÁLCULOS
    # =========================
    if mu1 is None or tiempo_num is None:
        st.info("Completa los parámetros para continuar.")
        return

    se = sigma / np.sqrt(n)
    LCS = mu0 + 3 * se
    LCI = mu0 - 3 * se

    ARL0 = 1 / alpha

    if mu1 < mu0:
        z = (LCI - mu1) / se
        potencia = norm.cdf(z)
    else:
        z = (LCS - mu1) / se
        potencia = 1 - norm.cdf(z)

    ARL1 = 1 / potencia if potencia > 0 else np.inf
    ATS = ARL1 * tiempo_num

    st.session_state['resultados_fase2'] = {
        'potencia': potencia,
        'arl': ARL1,
        'beta': 1 - potencia
    }

    # =========================
    # TABLA
    # =========================
    tabla = pd.DataFrame({
        "Parámetro": ["n", "μ₀", "μ₁", "Potencia", "ARL₀", "ARL₁", "ATS"],
        "Valor": [
            n,
            f"{mu0:.4f}",
            f"{mu1:.4f}",
            f"{potencia:.4f}",
            f"{ARL0:.2f}",
            f"{ARL1:.2f}",
            f"{ATS:.2f} {unidad.lower()}"
        ]
    })

    st.subheader("Resultados")
    st.dataframe(tabla, use_container_width=True, hide_index=True)

    # =========================
    # CONCLUSIONES (Limpieza de saltos de línea para evitar errores visuales)
    # =========================
    st.subheader("Conclusión del análisis")

    if potencia >= 0.9:
        concl = f"El sistema de control presenta un desempeño alto.<br><br>• ARL₀ = {ARL0:.0f}: estable ante falsas alarmas<br>• Potencia = {potencia:.2%}: alta capacidad de detección<br>• ARL₁ = {ARL1:.2f}: pocas muestras para detectar cambio<br><br>ATS: {ATS:.2f} {unidad.lower()} (respuesta rápida)."
        st.success("Desempeño Alto")
    elif potencia >= 0.8:
        concl = f"El sistema de control presenta un desempeño aceptable.<br><br>• ARL₀ = {ARL0:.0f}: control adecuado de falsas alarmas<br>• Potencia = {potencia:.2%}: capacidad moderada<br>• ARL₁ = {ARL1:.2f}: detección moderada<br><br>ATS: {ATS:.2f} {unidad.lower()} (posibles retrasos)."
        st.info("Desempeño Aceptable")
    else:
        concl = f"El sistema de control presenta baja sensibilidad.<br><br>• ARL₀ = {ARL0:.0f}: evita falsas alarmas pero detecta poco<br>• Potencia = {potencia:.2%}: alta probabilidad de no detectar<br>• ARL₁ = {ARL1:.2f}: requiere muchas muestras<br><br>ATS: {ATS:.2f} {unidad.lower()} (riesgo de fuera de control)."
        st.warning("Baja Sensibilidad")

    # CUADRO AZUL - CONCLUSIONES
    st.markdown(f'<div style="background-color:#EBF5FB; border-left:8px solid #3498DB; padding:20px; border-radius:16px; margin-top:10px; margin-bottom:20px; box-shadow:0 4px 10px rgba(0,0,0,0.05);"><div style="font-size:22px; font-weight:900; color:#2C3E50; margin-bottom:14px;">📋 Conclusiones</div><div style="font-size:15px; color:#2C3E50; line-height:1.7;">{concl}</div></div>', unsafe_allow_html=True)

    # =========================
    # RECOMENDACIONES
    # =========================
    st.subheader("Recomendaciones")
    recom = "• Incrementar el tamaño de muestra (n) para reducir el ARL₁<br>• Reducir el intervalo entre muestras para disminuir el ATS<br>• Evaluar la magnitud del cambio; cambios pequeños requieren más sensibilidad<br>• Considerar reducir la variabilidad del proceso (σ)"

    # CUADRO AMARILLO - RECOMENDACIONES
    st.markdown(f'<div style="background-color:#FEF9E7; border-left:8px solid #F1C40F; padding:20px; border-radius:16px; margin-top:10px; box-shadow:0 4px 10px rgba(0,0,0,0.05);"><div style="font-size:22px; font-weight:900; color:#2C3E50; margin-bottom:14px;">💡 Recomendaciones</div><div style="font-size:15px; color:#2C3E50; line-height:1.7;">{recom}</div></div>', unsafe_allow_html=True)