import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats
import os

# ─────────────────────────────────────────────
# DESIGN TOKENS
# ─────────────────────────────────────────────
C = {
    "bg_base":      "#F0F4F8",
    "bg_panel":     "#FFFFFF",
    "bg_surface":   "#EBF2FA",
    "text_primary": "#1A2332",
    "text_muted":   "#4A6080",
    "text_hint":    "#8AAABB",
    "blue":         "#1A6FC4",
    "border":       "#C9DAEA",
    "red":          "#C0292A",
}

# ─────────────────────────────────────────────
# CSS GLOBAL Y HELPERS
# ─────────────────────────────────────────────
def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');
    .stApp {{ background-color: {C['bg_base']} !important; font-family: 'IBM Plex Sans', sans-serif !important; }}
    .block-container {{ padding: 1.5rem 2rem 3rem 2rem !important; max-width: 1200px !important; }}
    .custom-card {{ background: {C['bg_panel']}; border: 1px solid {C['border']}; border-radius: 10px; padding: 15px; font-family: 'IBM Plex Sans', sans-serif; }}
    h1, h2, h3, p, label {{ font-family: 'IBM Plex Sans', sans-serif; }}
    </style>
    """, unsafe_allow_html=True)

def render_section(title):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;margin:20px 0 10px;
                font-size:10px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;
                color:{C['blue']};">
      {title}
      <span style="flex:1;height:1px;background:{C['border']};display:block;"></span>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(label, value, sub):
    st.markdown(f"""
    <div style="background:{C['bg_panel']};border:1px solid {C['border']};border-radius:10px;
                padding:15px 16px;margin-bottom:10px;">
      <div style="font-size:9px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
                  color:{C['text_hint']};margin-bottom:6px;">{label}</div>
      <div style="font-size:20px;font-weight:700;color:{C['text_primary']};">{value}</div>
      <div style="font-size:10px;color:{C['text_muted']};margin-top:2px;">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MÓDULO PRINCIPAL
# ─────────────────────────────────────────────
def normality_analysis(data_subset):
    inject_css()

    st.markdown(f"""
    <div style="font-size:21px; font-weight:700; letter-spacing:-0.02em; color:{C['text_primary']}; margin-bottom:4px;">
      Informe de Análisis de Normalidad
    </div>
    <div style="font-size:12px; color:{C['text_muted']}; margin-bottom:20px;">
      Evaluación de distribución para validación de requisitos estadísticos.
    </div>
    """, unsafe_allow_html=True)

    data = data_subset.select_dtypes(include=np.number).values.flatten()
    data = data[~np.isnan(data)]

    if len(data) < 3:
        st.warning("Muestra insuficiente: Se requieren al menos 3 datos numéricos.")
        return

    render_section("Resumen Descriptivo")
    cols = st.columns(4)
    
    media = np.mean(data)
    desv_std = np.std(data, ddof=1)
    n_total = len(data)
    curtosis = stats.kurtosis(data)

    with cols[0]: render_metric_card("Media", f"{media:.4f}", "Promedio")
    with cols[1]: render_metric_card("Desv. Est.", f"{desv_std:.4f}", "Dispersión")
    with cols[2]: render_metric_card("Tamaño (N)", f"{n_total}", "Registros")
    with cols[3]: render_metric_card("Curtosis", f"{curtosis:.2f}", "Apuntamiento")

    with st.expander("Ver tabla completa de estadísticos"):
        df_desc = pd.DataFrame({
            "Estadístico": ["Mínimo", "Q1", "Mediana", "Q3", "Máximo", "Rango", "Varianza"],
            "Valor": [np.min(data), np.percentile(data, 25), np.median(data), 
                      np.percentile(data, 75), np.max(data), np.ptp(data), np.var(data, ddof=1)]
        })
        st.table(df_desc.style.format({"Valor": "{:.4f}"}))

    render_section("Gráfico de Probabilidad Normal (QQ-Plot)")
    (osm, osr), (slope, intercept, r) = stats.probplot(data, dist="norm")

    fig_qq = go.Figure()
    fig_qq.add_trace(go.Scatter(x=osm, y=osr, mode='markers', name='Datos', marker=dict(color=C['blue'], size=7)))
    fig_qq.add_trace(go.Scatter(x=osm, y=slope * osm + intercept, mode='lines', name='Ajuste', line=dict(color=C['red'], dash='dot', width=2)))

    fig_qq.update_layout(
        template="plotly_white", height=360, margin=dict(l=32, r=32, t=36, b=36),
        xaxis=dict(gridcolor=C['border'], title="Cuantiles Teóricos"),
        yaxis=dict(gridcolor=C['border'], title="Cuantiles Observados")
    )
    st.plotly_chart(fig_qq, use_container_width=True)

    render_section("Prueba de Normalidad: Shapiro-Wilk")
    stat, p_value = stats.shapiro(data)
    alpha = 0.05
    
    st.markdown(f"""<div class="custom-card">
        <div style="font-weight:600; color:{C['text_primary']}; margin-bottom:5px;">P-Value: {p_value:.6f}</div>
        <div style="font-size:13px; color:{C['text_muted']};">Nivel de significancia (α): {alpha}</div>
    </div>""", unsafe_allow_html=True)

    if p_value > alpha:
        st.success("Conclusión: Los datos siguen una distribución normal.")
        conclusion_text = "Los datos siguen una distribución normal. Es válido aplicar análisis de capacidad."
    else:
        st.error("Conclusión: Los datos NO siguen una distribución normal.")
        conclusion_text = "Los datos no siguen una distribución normal. Los índices de capacidad pueden ser poco confiables."

    st.session_state["estadistica"] = {
        "media": round(media, 4), "desv_std": round(desv_std, 4),
        "n_total": int(n_total), "curtosis": round(curtosis, 4),
        "p_value": round(p_value, 6), "conclusion": conclusion_text
    }

    with st.expander("Ver datos analizados"):
        st.write(data_subset)