import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

# =========================
# ESTILO VISUAL
# =========================
st.markdown("""
<style>
.block-container {padding-top: 1rem;}
.box {
    background-color:#F4F6F7;
    padding:15px;
    border-radius:10px;
    border:1px solid #D5D8DC;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CONSTANTES SPC
# =========================
SPC = {
    2: {'A2': 1.880, 'D3': 0.000, 'D4': 3.267},
    3: {'A2': 1.023, 'D3': 0.000, 'D4': 2.574},
    4: {'A2': 0.729, 'D3': 0.000, 'D4': 2.282},
    5: {'A2': 0.577, 'D3': 0.000, 'D4': 2.114},
    6: {'A2': 0.483, 'D3': 0.000, 'D4': 2.004},
    7: {'A2': 0.419, 'D3': 0.076, 'D4': 1.924},
    8: {'A2': 0.373, 'D3': 0.136, 'D4': 1.864},
    9: {'A2': 0.337, 'D3': 0.184, 'D4': 1.816},
    10: {'A2': 0.308, 'D3': 0.223, 'D4': 1.777}
}

# =========================
# DETECCIÓN DE TENDENCIA
# =========================
def detectar_tendencia(data):

    count = 0

    for i in range(1, len(data)):

        if data[i] > data[i - 1]:
            count += 1

            if count >= 6:
                return True
        else:
            count = 0

    return False

# =========================
# FUNCIÓN PRINCIPAL
# =========================
def control_chart_module(data_df):

    st.subheader("Análisis de Control Estadístico del Proceso")

    data_df = data_df.dropna()

    m, n = data_df.shape

    const = SPC.get(n, SPC[10])

    # =========================
    # CÁLCULOS (NO TOCAR)
    # =========================
    medias = data_df.mean(axis=1)
    rangos = data_df.max(axis=1) - data_df.min(axis=1)

    X_barra = medias.mean()
    R_barra = rangos.mean()

    LCS_X = X_barra + const['A2'] * R_barra
    LCI_X = X_barra - const['A2'] * R_barra

    LCS_R = const['D4'] * R_barra
    LCI_R = const['D3'] * R_barra

    st.session_state['LCS_fase1'] = LCS_X
    st.session_state['LCC_fase1'] = X_barra
    st.session_state['LCI_fase1'] = LCI_X

    # =========================
    # FUNCIÓN DE GRÁFICA
    # =========================
    def plot_spc(y, LCC, LCS, LCI, title, label):

        fuera = (y > LCS) | (y < LCI)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            y=y,
            mode='lines+markers',
            line=dict(color='#2C3E50', width=2),
            marker=dict(
                size=9,
                color=np.where(fuera, '#E74C3C', '#2980B9'),
                line=dict(width=1, color='black')
            ),
            name="Subgrupos"
        ))

        fig.add_hline(
            y=LCC,
            line_color="green",
            annotation_text="LCC"
        )

        fig.add_hline(
            y=LCS,
            line_color="red",
            line_dash="dash",
            annotation_text="LCS"
        )

        fig.add_hline(
            y=LCI,
            line_color="red",
            line_dash="dash",
            annotation_text="LCI"
        )

        fig.add_hrect(
            y0=LCI,
            y1=LCS,
            fillcolor="lightgreen",
            opacity=0.15
        )

        fig.update_layout(
            title=title,
            template="plotly_white",
            height=420
        )

        return fig, fuera

    # =========================
    # CARTA X̄
    # =========================
    st.markdown(
        "<div class='box'><b> Carta X̄ (Media)</b></div>",
        unsafe_allow_html=True
    )

    fig_x, fuera_x = plot_spc(
        medias,
        X_barra,
        LCS_X,
        LCI_X,
        "Carta X̄",
        "Media"
    )

    st.plotly_chart(fig_x, use_container_width=True)

    # =========================
    # GUARDAR IMAGEN X̄
    # =========================
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    fig_x.write_image("outputs/control_xbar.png")

    # 🔥 CONCLUSIÓN X̄
    st.markdown("**Conclusión Carta X̄:**")

    if any(fuera_x):

        conclusion_x = (
            "Se evidencian puntos fuera de control, indicando la presencia "
            "de causas especiales que afectan la media del proceso."
        )

        st.error(conclusion_x)

    elif detectar_tendencia(medias):

        conclusion_x = (
            "Se detecta una tendencia creciente en la media, lo cual puede "
            "anticipar una futura pérdida de control."
        )

        st.warning(conclusion_x)

    else:

        conclusion_x = (
            "La media del proceso se mantiene estable, "
            "sin evidencia de causas especiales."
        )

        st.success(conclusion_x)

    # =========================
    # CARTA R
    # =========================
    st.markdown(
        "<div class='box'><b> Carta R (Variabilidad)</b></div>",
        unsafe_allow_html=True
    )

    fig_r, fuera_r = plot_spc(
        rangos,
        R_barra,
        LCS_R,
        LCI_R,
        "Carta R",
        "Rango"
    )

    st.plotly_chart(fig_r, use_container_width=True)

    # =========================
    # GUARDAR IMAGEN R
    # =========================
    fig_r.write_image("outputs/control_r.png")

    # 🔥 CONCLUSIÓN R
    st.markdown("**Conclusión Carta R:**")

    if any(fuera_r):

        conclusion_r = (
            "Se presentan puntos fuera de control en la variabilidad, "
            "indicando inconsistencias en el proceso."
        )

        st.error(conclusion_r)

    elif detectar_tendencia(rangos):

        conclusion_r = (
            "Se observa tendencia en la dispersión, "
            "lo que puede indicar inestabilidad futura."
        )

        st.warning(conclusion_r)

    else:

        conclusion_r = (
            "La variabilidad del proceso es estable "
            "y bajo control estadístico."
        )

        st.success(conclusion_r)

    # =========================
    # RECOMENDACIONES FINALES
    # =========================
    st.markdown(
        "<div class='box'><b> Recomendaciones Generales</b></div>",
        unsafe_allow_html=True
    )

    if any(fuera_x) or any(fuera_r):

        recomendacion = """
        - Investigar causas especiales (máquina, método, material o mano de obra)
        - No ajustar el proceso sin identificar la causa raíz
        - Segmentar los datos para detectar patrones
        """

        st.warning(recomendacion)

    elif detectar_tendencia(medias) or detectar_tendencia(rangos):

        recomendacion = """
        - Monitorear el proceso más frecuentemente
        - Evaluar posibles cambios graduales en condiciones operativas
        """

        st.info(recomendacion)

    else:

        recomendacion = """
        - El proceso está bajo control estadístico
        - Se recomienda continuar monitoreo
        - Puede procederse a análisis de capacidad del proceso
        """

        st.success(recomendacion)

    # =========================
    # TABLA
    # =========================
    st.subheader("Resumen de Límites")

    tabla = pd.DataFrame({
        "Parámetro": ["LCS", "LCC", "LCI"],
        "X̄": [
            round(LCS_X, 4),
            round(X_barra, 4),
            round(LCI_X, 4)
        ],
        "R": [
            round(LCS_R, 4),
            round(R_barra, 4),
            round(LCI_R, 4)
        ]
    })

    st.dataframe(tabla, use_container_width=True, hide_index=True)

    # =========================
    # GUARDAR RESULTADOS PARA PDF
    # =========================
    st.session_state["control_charts"] = {
        "X_barra": round(X_barra, 4),
        "R_barra": round(R_barra, 4),
        "LCS_X": round(LCS_X, 4),
        "LCI_X": round(LCI_X, 4),
        "LCS_R": round(LCS_R, 4),
        "LCI_R": round(LCI_R, 4),
        "conclusion_x": conclusion_x,
        "conclusion_r": conclusion_r,
        "recomendacion": recomendacion
    }