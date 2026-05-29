import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
import pandas as pd

# ─────────────────────────────────────────────
# DESIGN TOKENS — PALETA OSCURA FIJA PARA SIDEBAR
# ─────────────────────────────────────────────
C = {
    "bg_base":    "#F0F4F8",
    "bg_panel":   "#FFFFFF",
    "bg_surface": "#EBF2FA",
    "text_primary": "#1A2332",
    "text_muted":   "#4A6080",
    "text_hint":    "#8AAABB",
    "blue":        "#1A6FC4",
    "border":      "#C9DAEA",
    "teal":        "#1A8A4A",
    "amber":       "#B07A00",
    "orange":      "#C05A00",
    "red":         "#C0292A",
    "bg_input_card": "#FFFFFF",
}

C_SIDEBAR = {
    "bg": "#1A2332",
    "text": "#FFFFFF",
    "border": "#3A4B61",
}

# ─────────────────────────────────────────────
# CSS GLOBAL — Parches de compatibilidad
# ─────────────────────────────────────────────
def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');
    html, body {{ background-color: {C['bg_base']} !important; color: {C['text_primary']} !important; }}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], [data-testid="stMain"] {{ background-color: {C['bg_base']} !important; color: {C['text_primary']} !important; font-family: 'IBM Plex Sans', sans-serif !important; }}
    .block-container {{ background-color: {C['bg_base']} !important; padding: 1.5rem 2rem 3rem 2rem !important; max-width: 1200px !important; }}
    [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {{ background-color: {C_SIDEBAR['bg']} !important; color: {C_SIDEBAR['text']} !important; border-right: 1px solid {C_SIDEBAR['border']} !important; }}
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{ color: {C_SIDEBAR['text']} !important; }}
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {{ background-color: transparent !important; border-color: {C_SIDEBAR['border']} !important; }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div {{ color: {C_SIDEBAR['text']} !important; }}
    [data-testid="stSidebar"] div[role="listbox"] {{ background-color: {C_SIDEBAR['bg']} !important; color: {C_SIDEBAR['text']} !important; }}
    #MainMenu, footer, header {{ visibility: hidden !important; }}
    .stDeployButton {{ display: none !important; }}
    div[data-testid="stToolbar"] {{ visibility: hidden !important; }}
    [data-testid="stDecoration"] {{ display: none !important; }}
    .stTextInput > label {{ font-size: 11px !important; font-weight: 600 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; color: {C['text_muted']} !important; }}
    .stTextInput input {{ background: {C['bg_input_card']} !important; border: 1px solid {C['border']} !important; color: {C['text_primary']} !important; border-radius: 7px !important; font-family: 'JetBrains Mono', monospace !important; font-size: 14px !important; padding: 8px 12px !important; }}
    .stTextInput input:focus {{ border-color: {C['blue']} !important; box-shadow: 0 0 0 3px {C['blue']}22 !important; }}
    [data-testid="stMain"] div[data-testid="stContainer"] {{ background-color: {C['bg_panel']} !important; border: 1px solid {C['border']} !important; border-radius: 10px !important; padding: 18px !important; }}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FUNCIONES AUXILIARES Y CÁLCULOS
# ─────────────────────────────────────────────
def _color_idx(v):
    if v >= 1.33: return C['teal']
    if v >= 1.0:  return C['amber']
    return C['red']

def _color_pnc(v):
    if v < 0.5:  return C['teal']
    if v < 2.0:  return C['amber']
    return C['red']

def clasificar_con_semaforo(Cp, Cpk, Cpu, Cpl):
    es_centrado = abs(Cpu - Cpl) < 0.05
    if Cp >= 1.33 and es_centrado: return "Proceso Capaz y Centrado", "green"
    elif Cp >= 1 and not es_centrado: return "Proceso Capaz pero Descentrado", "yellow"
    elif Cp < 1 and es_centrado: return "Proceso Incapaz pero Centrado", "orange"
    else: return "Proceso Incapaz y Descentrado", "red"

def parse_number(x): return float(str(x).replace(",", ".").strip())

S = {
    "panel": f"background:{C['bg_panel']};border:1px solid {C['border']};border-radius:10px;overflow:hidden;",
    "panel_hdr": f"padding:9px 15px;background:{C['bg_surface']};border-bottom:1px solid {C['border']};font-size:9px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:{C['text_muted']};",
    "row": f"display:flex;justify-content:space-between;align-items:center;padding:8px 15px;border-bottom:1px solid {C['border']}22;",
    "row_last": f"display:flex;justify-content:space-between;align-items:center;padding:8px 15px;",
    "sk": f"font-size:12px;color:{C['text_muted']};",
}

# ─────────────────────────────────────────────
# LÓGICA DE INTERFAZ
# ─────────────────────────────────────────────
def render_topbar():
    st.markdown(f"""
    <div style="font-size:21px; font-weight:700; color:{C['text_primary']}; margin-bottom:20px;">Análisis de Capacidad del Proceso</div>
    """, unsafe_allow_html=True)

def render_section(title):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;margin:16px 0 10px;font-size:10px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:{C['blue']};">
      {title} <span style="flex:1;height:1px;background:{C['border']};display:block;"></span>
    </div>
    """, unsafe_allow_html=True)

def render_status_banner(estado, color_clase):
    colors = {"green": C['teal'], "yellow": C['amber'], "orange": C['orange'], "red": C['red']}
    hex_color = colors[color_clase]
    st.markdown(f"""
    <div style="border-radius:9px;padding:13px 18px;margin:10px 0 16px;display:flex;align-items:center;gap:12px;background:{hex_color}11;border:1px solid {hex_color}44;">
      <div style="width:9px;height:9px;border-radius:50%;background:{hex_color};"></div>
      <div style="font-size:13px;font-weight:600;color:{hex_color};">{estado}</div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_cards(Cp, Cpk, Cpu, Cpl):
    cols = st.columns(4)
    data = [("Cp", Cp), ("Cpk", Cpk), ("Cpu", Cpu), ("Cpl", Cpl)]
    for col, (label, val) in zip(cols, data):
        with col:
            st.markdown(f"""
            <div style="{S['panel']} padding:15px; text-align:center;">
                <div style="font-size:9px; color:{C['text_hint']};">{label}</div>
                <div style="font-size:20px; font-weight:700; color:{_color_idx(val)};">{val:.3f}</div>
            </div>""", unsafe_allow_html=True)

def render_stat_panels(media, sigma, LSL, USL, pnc_total):
    st.markdown(f"""
    <div style="{S['panel']}">
        <div style="{S['panel_hdr']}">Estadísticos Clave</div>
        <div style="{S['row']}"><span style="{S['sk']}">Media</span><span style="font-family:'JetBrains Mono'">{media:.4f}</span></div>
        <div style="{S['row']}"><span style="{S['sk']}">Sigma</span><span style="font-family:'JetBrains Mono'">{sigma:.4f}</span></div>
        <div style="{S['row_last']}"><span style="{S['sk']}">% PNC Total</span><span style="font-family:'JetBrains Mono'; color:{_color_pnc(pnc_total)}">{pnc_total:.3f}%</span></div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ─────────────────────────────────────────────
def capability_analysis(data_df):
    inject_css()
    render_topbar()

    # (Lógica de preparación de datos simplificada para el ejemplo)
    data_df = data_df.apply(pd.to_numeric, errors='coerce').dropna()
    media_global = data_df.mean().mean()
    sigma = data_df.std().mean() 

    # Inputs de límites
    col_l, col_u = st.columns(2)
    with col_l: LSL = st.number_input("LIE (LSL)", value=39.0)
    with col_u: USL = st.number_input("LSE (USL)", value=42.0)

    # Cálculos
    Cp = (USL - LSL) / (6 * sigma)
    Cpu = (USL - media_global) / (3 * sigma)
    Cpl = (media_global - LSL) / (3 * sigma)
    Cpk = min(Cpu, Cpl)
    pnc_total = (norm.cdf(LSL, media_global, sigma) + (1 - norm.cdf(USL, media_global, sigma))) * 100

    render_status_banner(*clasificar_con_semaforo(Cp, Cpk, Cpu, Cpl))
    render_metric_cards(Cp, Cpk, Cpu, Cpl)
    render_stat_panels(media_global, sigma, LSL, USL, pnc_total)

    # ── NUEVA SECCIÓN: ANÁLISIS INVERSO ──
    render_section("Análisis Inverso (Targeting)")
    with st.container():
        st.markdown(f"<p style='color:{C['text_muted']}; font-size:12px;'>Calcular media necesaria para un %PNC objetivo:</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            pnc_obj = st.number_input("% PNC Deseado", value=0.1, step=0.01)
            limite_sel = st.selectbox("Controlar contra:", ["LSE (Superior)", "LIE (Inferior)"])
        with col2:
            st.write(" ")
            if st.button("Calcular Media Target"):
                z = norm.ppf(pnc_obj / 100)
                limite_val = USL if "LSE" in limite_sel else LSL
                # Si es superior: P(X > LSE) = p -> media = LSE - (z * sigma)
                # Si es inferior: P(X < LIE) = p -> media = LIE + (z * sigma)
                media_target = (limite_val - (z * sigma)) if "LSE" in limite_sel else (limite_val + (abs(z) * sigma))
                st.success(f"Media necesaria: **{media_target:.4f}**")

    # ── RESTO DEL REPORTE ──
    render_section("Reporte del Análisis")
    st.info("Aquí irían tus conclusiones y recomendaciones originales.")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    demo_df = pd.DataFrame(np.random.normal(40.5, 0.2, (50, 5)))
    capability_analysis(demo_df)