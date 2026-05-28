import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.stats import norm

def ejecutar_potencia(data_subset):

    st.header("Análisis de Potencia Estadística")

    # =========================
    # DATOS BASE (flexible)
    # =========================
    if 'sigma_capacidad' in st.session_state:
        sigma = float(st.session_state['sigma_capacidad'])
        mu0_base = float(st.session_state['mu_capacidad'])
    else:
        sigma = float(data_subset.std().mean())
        mu0_base = float(data_subset.mean().mean())

    # =========================
    # INTERFAZ
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        mu0 = st.number_input("Media actual (μ₀)", value=mu0_base, format="%.4f")
        sigma_input = st.number_input("Sigma (σ)", value=sigma, format="%.6f")
        n = st.number_input("Tamaño de muestra (n)", value=5, step=1)

    with col2:
        LCS = st.number_input("LCS", value=mu0 + 3*(sigma_input/np.sqrt(n)), format="%.4f")
        LCI = st.number_input("LCI", value=mu0 - 3*(sigma_input/np.sqrt(n)), format="%.4f")
        mu1 = st.number_input("Nueva Media (μ₁)", value=None, placeholder="Ej: 38.000", format="%.4f")
        confianza = st.number_input("Nivel de confianza (%)", value=95.0, min_value=80.0, max_value=99.9, step=0.1)

    # =========================
    # BOTÓN PRINCIPAL
    # =========================
    if st.button("Ejecutar Análisis"):

        if mu1 is None:
            st.warning("Ingresa la nueva media (μ₁).")
            return

        se = sigma_input / np.sqrt(n)
        alpha = 1 - (confianza / 100)

        if mu1 < mu0:
            z = (LCI - mu1) / se
            potencia = norm.cdf(z)
            direccion = "Disminución"
        else:
            z = (LCS - mu1) / se
            potencia = 1 - norm.cdf(z)
            direccion = "Incremento"

        beta = 1 - potencia
        arl1 = 1 / potencia if potencia > 0 else 0

        st.session_state['resultados_fase2'] = {
            'potencia': potencia,
            'arl': arl1,
            'beta': beta
        }

        tabla = pd.DataFrame({
            "Parámetro": [
                "Nivel de confianza",
                "Error Tipo I (α)",
                "Error Tipo II (β)",
                "Potencia (1-β)",
                "ARL₁"
            ],
            "Valor": [
                f"{confianza:.1f}%",
                f"{alpha:.4f}",
                f"{beta:.4f}",
                f"{potencia:.4f}",
                f"{arl1:.2f}"
            ]
        })

        st.subheader("Resumen Estadístico")
        st.dataframe(tabla, use_container_width=True, hide_index=True)

        x = np.linspace(
            min(mu0, mu1, LCI) - 4*se,
            max(mu0, mu1, LCS) + 4*se,
            500
        )

        fig = go.Figure()

        # H0
        fig.add_trace(go.Scatter(
            x=x,
            y=norm.pdf(x, mu0, se),
            name="H0 (En control)",
            line=dict(color='black', width=3)
        ))

        # H1
        fig.add_trace(go.Scatter(
            x=x,
            y=norm.pdf(x, mu1, se),
            name="H1 (Desplazado)",
            line=dict(color='black', width=3, dash='dash')
        ))

        # Límites
        fig.add_vline(x=LCI, line_color="red")
        fig.add_vline(x=LCS, line_color="red")

        # β
        x_beta = x[(x >= LCI) & (x <= LCS)]

        if len(x_beta) > 0:
            fig.add_trace(go.Scatter(
                x=np.concatenate(([x_beta[0]], x_beta, [x_beta[-1]])),
                y=np.concatenate(([0], norm.pdf(x_beta, mu1, se), [0])),
                fill='tozeroy',
                fillcolor='rgba(231,76,60,0.35)',
                line=dict(width=0),
                name=f"Error Tipo II (β = {beta:.3f})"
            ))

        # Potencia
        if mu1 < mu0:
            x_pow = x[x <= LCI]
        else:
            x_pow = x[x >= LCS]

        if len(x_pow) > 0:
            fig.add_trace(go.Scatter(
                x=np.concatenate(([x_pow[0]], x_pow, [x_pow[-1]])),
                y=np.concatenate(([0], norm.pdf(x_pow, mu1, se), [0])),
                fill='tozeroy',
                fillcolor='rgba(52,152,219,0.4)',
                line=dict(width=0),
                name=f"Potencia = {potencia:.3f}"
            ))

        fig.update_layout(
            title=f"Curva de Potencia – {direccion}",
            template="plotly_white",
            xaxis_title="Media",
            yaxis_title="Densidad",
            height=520
        )

        st.plotly_chart(fig, use_container_width=True)

        # =========================
        # CONCLUSIÓN Y RECOMENDACIONES
        # =========================
        st.subheader("Conclusión del Análisis")

        if potencia >= 0.9:
            conclusion = f"El sistema de monitoreo presenta una potencia alta ({potencia:.2%}), indicando excelente capacidad para detectar cambios reales en el proceso. El riesgo de no detectar desplazamientos es bajo ({beta:.2%}), permitiendo una respuesta rápida ante desviaciones."
            recom = "• Mantener el diseño actual del monitoreo<br>• Continuar seguimiento estadístico<br>• Validar periódicamente los límites de control<br>• Mantener estabilidad operativa"
            st.success(conclusion)
        elif potencia >= 0.8:
            conclusion = f"La potencia obtenida ({potencia:.2%}) es aceptable, aunque existe una probabilidad moderada de no detectar ciertos cambios. El sistema puede detectar desplazamientos importantes, pero podría presentar retrasos ante cambios pequeños."
            recom = "• Considerar aumentar el tamaño de muestra<br>• Evaluar reducción de variabilidad<br>• Revisar frecuencia de muestreo<br>• Ajustar límites si es necesario"
            st.info(conclusion)
        else:
            conclusion = f"La potencia del sistema es baja ({potencia:.2%}), indicando alta probabilidad ({beta:.2%}) de no detectar cambios reales. Bajo estas condiciones, el sistema de monitoreo puede no ser confiable para identificar desplazamientos oportunamente."
            recom = "• Incrementar tamaño de muestra<br>• Reducir variabilidad del proceso<br>• Incrementar frecuencia de monitoreo<br>• Replantear estrategia de control"
            st.warning(conclusion)

        st.markdown("### Recomendaciones")
        st.markdown(f"""
            <div style="background-color:#FEF9E7; padding:15px; border-radius:10px; border:1px solid #F9E79F; color:#9A7D0A; font-size:15px; line-height:1.6;">
                {recom}
            </div>
        """, unsafe_allow_html=True)

    # =========================
    # N ÓPTIMO
    # =========================
    st.markdown("---")
    st.subheader("Cálculo de Tamaño de Muestra Óptimo")

    col_o1, col_o2 = st.columns(2)

    with col_o1:
        potencia_obj = st.number_input("Potencia deseada (1-β)", value=0.90, step=0.01, key="n_opt_pot")

    with col_o2:
        mu1_opt = st.number_input("Media a detectar (μ₁ para diseño)", value=None, placeholder="Ej: 38.000", format="%.4f", key="n_opt_mu")

    if st.button("Calcular n óptimo"):

        if mu1_opt is None:
            st.warning("Ingresa la media a detectar.")
            return

        n_opt = None
        for n_test in range(2, 500):
            se_test = sigma / np.sqrt(n_test)
            LCS_test = mu0_base + 3 * se_test
            LCI_test = mu0_base - 3 * se_test

            if mu1_opt < mu0_base:
                z = (LCI_test - mu1_opt) / se_test
                pot = norm.cdf(z)
            else:
                z = (LCS_test - mu1_opt) / se_test
                pot = 1 - norm.cdf(z)

            if pot >= potencia_obj:
                n_opt = n_test
                break

        if n_opt:
            st.success(f"n óptimo: {n_opt}")
            st.info(f"Para detectar un cambio en la media hacia μ₁ = {mu1_opt:.4f} con una potencia de {potencia_obj:.2%}, se requiere un tamaño de muestra mínimo de n = {n_opt}.")
            st.markdown("### Interpretación y Recomendaciones")
            st.write("- Un n mayor aumenta la sensibilidad del gráfico de control\n- Si el n calculado es muy alto, evaluar costo vs beneficio\n- Considerar rediseñar el proceso si el n es excesivo\n- Este cálculo permite construir planes de monitoreo robustos")