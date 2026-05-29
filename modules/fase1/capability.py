import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
import pandas as pd

# ─────────────────────────────────────────────
# DESIGN TOKENS — PALETA OSCURA FIJA PARA SIDEBAR
# ─────────────────────────────────────────────
C = {
    # Fondo base de la app (claro)
    "bg_base":    "#F0F4F8",   # gris azulado muy claro
    
    # Diseño de cards/paneles (claro)
    "bg_panel":    "#FFFFFF",   # cards blancas
    "bg_surface":  "#EBF2FA",   # azul muy suave
    
    # Diseño de inputs/texto general (oscuro)
    "text_primary": "#1A2332",   # texto oscuro principal
    "text_muted":   "#4A6080",   # texto secundario
    "text_hint":    "#8AAABB",   # placeholder
    
    # Acentuación y bordes
    "blue":        "#1A6FC4",   # azul acento
    "border":      "#C9DAEA",   # bordes claros
    
    # Semáforo
    "teal":        "#1A8A4A",   # verde
    "amber":       "#B07A00",   # amarillo
    "orange":      "#C05A00",   # naranja
    "red":         "#C0292A",   # rojo
    
    # Inputs dentro de cards (blanco)
    "bg_input_card": "#FFFFFF",
}

# Tokens específicos para forzar el tema oscuro en el sidebar
C_SIDEBAR = {
    "bg": "#1A2332",         # Azul muy oscuro (casi negro)
    "text": "#FFFFFF",       # Blanco puro para contraste
    "border": "#3A4B61",     # Borde sutil oscuro
}

# ─────────────────────────────────────────────
# CSS GLOBAL — Parches de compatibilidad
# ─────────────────────────────────────────────
def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

    /* === FONDO GENERAL CLARO === */
    html, body {{
        background-color: {C['bg_base']} !important;
        color: {C['text_primary']} !important;
    }}
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stMain"] {{
        background-color: {C['bg_base']} !important;
        color: {C['text_primary']} !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
    }}
    .block-container {{
        background-color: {C['bg_base']} !important;
        padding: 1.5rem 2rem 3rem 2rem !important;
        max-width: 1200px !important;
    }}

    /* === BARRA LATERAL (SIDEBAR) — FORZAR TEMA OSCURO === */
    [data-testid="stSidebar"],
    [data-testid="stSidebarUserContent"] {{
        background-color: {C_SIDEBAR['bg']} !important;
        color: {C_SIDEBAR['text']} !important;
        border-right: 1px solid {C_SIDEBAR['border']} !important;
    }}
    
    /* Textos nativos de Streamlit en sidebar (labels, captions, markdown) */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label {{
        color: {C_SIDEBAR['text']} !important;
    }}
    
    /* Inputs nativos en sidebar (selectbox) */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background-color: transparent !important;
        border-color: {C_SIDEBAR['border']} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] div {{
        color: {C_SIDEBAR['text']} !important;
    }}
    [data-testid="stSidebar"] div[role="listbox"] {{
        background-color: {C_SIDEBAR['bg']} !important;
        color: {C_SIDEBAR['text']} !important;
    }}
    [data-testid="stSidebar"] div[role="listbox"] li {{
        background-color: transparent !important;
    }}
    [data-testid="stSidebar"] div[role="listbox"] li[aria-selected="true"] {{
        background-color: {C['blue']} !important;
    }}

    /* === ELEMENTOS CLAROS (FUERA DEL SIDEBAR) === */
    /* Ocultar chrome de Streamlit */
    #MainMenu, footer, header {{ visibility: hidden !important; }}
    .stDeployButton {{ display: none !important; }}
    div[data-testid="stToolbar"] {{ visibility: hidden !important; }}
    [data-testid="stDecoration"] {{ display: none !important; }}

    /* Inputs dentro de cards claras */
    .stTextInput > label {{
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: {C['text_muted']} !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
    }}
    .stTextInput input {{
        background: {C['bg_input_card']} !important;
        border: 1px solid {C['border']} !important;
        color: {C['text_primary']} !important;
        border-radius: 7px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        padding: 8px 12px !important;
    }}
    .stTextInput input:focus {{
        border-color: {C['blue']} !important;
        box-shadow: 0 0 0 3px {C['blue']}22 !important;
    }}
    .stTextInput input::placeholder {{ color: {C['text_hint']} !important; }}

    /* Estilo personalizado para el contenedor de especificaciones nativo (fuera del sidebar) */
    [data-testid="stMain"] div[data-testid="stContainer"] {{
        background-color: {C['bg_panel']} !important;
        border: 1px solid {C['border']} !important;
        border-radius: 10px !important;
        padding: 18px !important;
    }}
    
    /* Caption del contenedor (nativo de Streamlit) */
    [data-testid="stMain"] div[data-testid="stContainer"] .stCaptionContainer p {{
        font-size: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: {C['text_muted']} !important;
        margin-bottom: 12px !important;
    }}

    /* Columnas nativas */
    [data-testid="column"] {{ padding: 0 6px !important; }}
    [data-testid="column"]:first-child {{ padding-left: 0 !important; }}
    [data-testid="column"]:last-child  {{ padding-right: 0 !important; }}

    p, span, div, label {{
        font-family: 'IBM Plex Sans', sans-serif;
    }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS DE ESTILO INLINE (PARA RENDER_*)
# ─────────────────────────────────────────────

def _color_idx(v):
    if v >= 1.33: return C['teal']
    if v >= 1.0:  return C['amber']
    return C['red']

def _color_pnc(v):
    if v < 0.5:  return C['teal']
    if v < 2.0:  return C['amber']
    return C['red']

# Estilos de card reutilizables (tema claro)
S = {
    "panel": f"background:{C['bg_panel']};border:1px solid {C['border']};border-radius:10px;overflow:hidden;",
    "panel_hdr": (f"padding:9px 15px;background:{C['bg_surface']};border-bottom:1px solid {C['border']};"
                  f"font-size:9px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;"
                  f"color:{C['text_muted']};font-family:'IBM Plex Sans',sans-serif;"),
    "row": f"display:flex;justify-content:space-between;align-items:center;padding:8px 15px;border-bottom:1px solid {C['border']}22;",
    "row_last": f"display:flex;justify-content:space-between;align-items:center;padding:8px 15px;",
    "sk": f"font-size:12px;color:{C['text_muted']};font-family:'IBM Plex Sans',sans-serif;",
    "sv": f"font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:500;color:{C['text_primary']};",
}

# Constantes estadísticas
D2_CONSTANTS = {
    2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534,
    7: 2.704, 8: 2.847, 9: 2.970, 10: 3.078,
    11: 3.173, 12: 3.258, 13: 3.336, 14: 3.407,
    15: 3.472, 16: 3.532, 17: 3.588, 18: 3.640,
    19: 3.689, 20: 3.735, 21: 3.778, 22: 3.819,
    23: 3.858, 24: 3.895, 25: 3.931
}

def clasificar_con_semaforo(Cp, Cpk, Cpu, Cpl):
    es_centrado = abs(Cpu - Cpl) < 0.05
    if   Cp >= 1.33 and es_centrado:       return "Proceso Capaz y Centrado",        "green"
    elif Cp >= 1    and not es_centrado:   return "Proceso Capaz pero Descentrado",    "yellow"
    elif Cp < 1     and es_centrado:       return "Proceso Incapaz pero Centrado",     "orange"
    else:                                  return "Proceso Incapaz y Descentrado",    "red"

def parse_number(x):
    return float(str(x).replace(",", ".").strip())

# ─────────────────────────────────────────────
# COMPONENTES HTML (PARA ST.MARKDOWN)
# ─────────────────────────────────────────────

def render_topbar():
    # BARRA SUPERIOR — Se mantiene clara para el main content
    topbar_html = f"""
    <div style="display:flex; align-items:center; justify-content:space-between; padding-bottom:16px; border-bottom:2px solid {C['border']}; margin-bottom:20px; background:transparent;">
      <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:38px; height:38px; background:linear-gradient(135deg,#1A4A8A,{C['blue']}); border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0;">
        </div>
        <div>
          <div style="font-size:16px; font-weight:700; letter-spacing:0.03em; color:{C['text_primary']}; font-family:'IBM Plex Sans',sans-serif; line-height:1.2;">
            SPC Manager
          </div>
          <div style="font-size:10px; color:{C['text_muted']}; letter-spacing:0.08em; text-transform:uppercase; font-family:'IBM Plex Sans',sans-serif;">
            Statistical Process Control
          </div>
        </div>
      </div>
      <div style="background:{C['bg_surface']}; border:1px solid {C['border']}; border-radius:6px; padding:4px 12px; font-size:10px; color:{C['text_muted']}; font-family:'JetBrains Mono',monospace; letter-spacing:0.04em;">
        v2.0 &middot; Capacidad
      </div>
    </div>
    """
    st.markdown(topbar_html, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="font-size:21px; font-weight:700; letter-spacing:-0.02em; color:{C['text_primary']}; margin-bottom:4px; font-family:'IBM Plex Sans',sans-serif;">
      Análisis de Capacidad del Proceso
    </div>
    <div style="font-size:12px; color:{C['text_muted']}; margin-bottom:20px; font-family:'IBM Plex Sans',sans-serif;">
      Índices Cp, Cpk y estimación de no conformidades a partir de subgrupos racionales.
    </div>
    """, unsafe_allow_html=True)


def render_section(title):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;margin:16px 0 10px;
                font-size:10px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;
                color:{C['blue']};font-family:'IBM Plex Sans',sans-serif;">
      {title}
      <span style="flex:1;height:1px;background:{C['border']};display:block;"></span>
    </div>
    """, unsafe_allow_html=True)


def render_status_banner(estado, color_clase):
    color_map = {
        "green":  (C['teal'],   "● Proceso Capaz y Centrado"),
        "yellow": (C['amber'],  "● Proceso Capaz pero Descentrado"),
        "orange": (C['orange'], "● Proceso Incapaz pero Centrado"),
        "red":    (C['red'],    "● Proceso Incapaz y Descentrado"),
    }
    hex_color, label = color_map[color_clase]
    st.markdown(f"""
    <div style="border-radius:9px;padding:13px 18px;margin:10px 0 16px;
                display:flex;align-items:center;gap:12px;
                background:{hex_color}11;border:1px solid {hex_color}44;">
      <div style="width:9px;height:9px;border-radius:50%;background:{hex_color};
                  box-shadow:0 0 7px {hex_color};flex-shrink:0;"></div>
      <div style="font-size:13px;font-weight:600;color:{hex_color};
                  font-family:'IBM Plex Sans',sans-serif;">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_cards(Cp, Cpk, Cpu, Cpl):
    def card(label, val, sub):
        col = _color_idx(val)
        return f"""
        <div style="background:{C['bg_panel']};border:1px solid {C['border']};border-radius:10px;
                    padding:15px 16px;position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;left:0;right:0;height:2px;
                      background:linear-gradient(90deg,transparent,{C['blue']}55,transparent);"></div>
          <div style="font-size:9px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
                      color:{C['text_hint']};margin-bottom:6px;font-family:'IBM Plex Sans',sans-serif;">
            {label}
          </div>
          <div style="font-size:24px;font-weight:700;color:{col};letter-spacing:-.02em;line-height:1;
                      font-family:'JetBrains Mono',monospace;">
            {val:.3f}
          </div>
          <div style="font-size:10px;color:{C['text_hint']};margin-top:4px;
                      font-family:'IBM Plex Sans',sans-serif;">
            {sub}
          </div>
        </div>"""

    cols = st.columns(4)
    data = [
        ("Cp — Capacidad Potencial",  Cp,  "Mín. aceptable ≥ 1.00"),
        ("Cpk — Capacidad Real",      Cpk, "Ideal ≥ 1.33"),
        ("Cpu — Índice Superior",     Cpu, "Margen hacia LSE"),
        ("Cpl — Índice Inferior",     Cpl, "Margen hacia LIE"),
    ]
    for col, (label, val, sub) in zip(cols, data):
        with col:
            st.markdown(card(label, val, sub), unsafe_allow_html=True)


def render_stat_panels(media_global, rango_medio, sigma, d2, n,
                       LSL, USL, num_muestras,
                       pnc_inf, pnc_sup, pnc_total):

    def panel(header, rows):
        inner = ""
        for i, (k, v, col) in enumerate(rows):
            is_last = (i == len(rows) - 1)
            row_style = S["row_last"] if is_last else S["row"]
            val_color = col if col else C['text_primary']
            inner += f'<div style="{row_style}"><span style="{S["sk"]}">{k}</span><span style="font-family:\'JetBrains Mono\',monospace;font-size:12px;font-weight:500;color:{val_color};">{v}</span></div>'
        
        return f'<div style="{S["panel"]}"><div style="{S["panel_hdr"]}">{header}</div>{inner}</div>'

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(panel("Estimadores de posición y dispersión", [
            ("Media global (x̄)",    f"{media_global:.4f}", None),
            ("Rango medio (R̄)",     f"{rango_medio:.4f}",  None),
            ("Sigma estimada (σ̂)",   f"{sigma:.4f}",        None),
            (f"Factor d₂  (n={n})",  f"{d2:.3f}",           None),
        ]), unsafe_allow_html=True)

    with col2:
        st.markdown(panel("Límites de especificación", [
            ("LIE (LSL)",           f"{LSL:.4f}",          None),
            ("LSE (USL)",           f"{USL:.4f}",          None),
            ("Tolerancia (USL−LSL)",  f"{(USL-LSL):.4f}",    None),
            ("Subgrupos (m)",        f"{num_muestras}",     None),
        ]), unsafe_allow_html=True)

    with col3:
        st.markdown(panel("Estimación de no conformidades", [
            ("% Bajo LIE",   f"{pnc_inf:.3f}%",   _color_pnc(pnc_inf)),
            ("% Sobre LSE",  f"{pnc_sup:.3f}%",   _color_pnc(pnc_sup)),
            ("Total NC",     f"{pnc_total:.3f}%",  _color_pnc(pnc_total)),
            ("PPM estimados",f"{pnc_total*10000:.0f}", _color_pnc(pnc_total)),
        ]), unsafe_allow_html=True)


def render_report(Cp, Cpu, Cpl):
    es_centrado = abs(Cpu - Cpl) < 0.05

    if Cp >= 1.33 and es_centrado:
        concl = ("El proceso es capaz de cumplir consistentemente con las especificaciones "
                 "establecidas y se encuentra adecuadamente centrado respecto al objetivo. "
                 "La variabilidad observada es baja en relación con los límites de tolerancia, "
                 "garantizando estabilidad operativa y mínima generación de productos no conformes.")
        recom = [
            "Mantener las condiciones actuales del proceso",
            "Continuar monitoreo estadístico con cartas de control",
            "Aplicar programa de mantenimiento preventivo",
            "Implementar ciclos de mejora continua (PDCA/DMAIC)",
        ]
    elif Cp >= 1 and not es_centrado:
        concl = ("El proceso presenta capacidad potencial adecuada; sin embargo, se encuentra "
                 "descentrado respecto al valor objetivo. Aunque la variabilidad es aceptable, "
                 "el desplazamiento del proceso incrementa el riesgo de generar productos fuera "
                 "de especificación.")
        recom = [
            "Ajustar el centrado del proceso hacia el valor nominal",
            "Revisar calibración de equipos y parámetros de ajuste",
            "Verificar estabilidad del proceso posterior al ajuste",
            "Mantener seguimiento estadístico frecuente",
        ]
    elif Cp < 1 and es_centrado:
        concl = ("El proceso se encuentra centrado; sin embargo, presenta una variabilidad "
                 "excesiva respecto a los límites de especificación, impidiendo cumplir "
                 "consistentemente con los requisitos de calidad.")
        recom = [
            "Reducir fuentes de variabilidad del proceso",
            "Revisar estado de maquinaria, herramental y método",
            "Estandarizar procedimientos operativos (SOP)",
            "Fortalecer controles estadísticos en tiempo real",
        ]
    else:
        concl = ("El proceso no es capaz de cumplir adecuadamente con las especificaciones "
                 "debido a la combinación de alta variabilidad y descentrado respecto al objetivo, "
                 "generando un riesgo elevado de productos no conformes.")
        recom = [
            "Reducir variabilidad como acción prioritaria",
            "Ajustar centrado del proceso simultáneamente",
            "Realizar análisis de causa raíz (Ishikawa / 5-Why)",
            "Implementar acciones correctivas con seguimiento",
        ]

    recom_html = "".join(f"""
        <div style="display:flex;align-items:flex-start;gap:8px;padding:6px 0;
                    border-bottom:1px solid {C['border']}55;font-size:12px;
                    color:{C['text_muted']};line-height:1.5;
                    font-family:'IBM Plex Sans',sans-serif;">
          <div style="width:5px;height:5px;border-radius:50%;background:{C['teal']};
                      flex-shrink:0;margin-top:6px;"></div>
          <span>{item}</span>
        </div>""" for item in recom)

    col_c, col_r = st.columns(2)

    with col_c:
        st.markdown(f"""
        <div style="background:{C['bg_panel']};border:1px solid {C['border']};
                    border-left:3px solid {C['blue']};border-radius:10px;
                    padding:18px 20px;min-height:200px;">
          <div style="font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
                      color:{C['text_muted']};margin-bottom:12px;display:flex;align-items:center;
                      gap:6px;font-family:'IBM Plex Sans',sans-serif;">
            &nbsp; Conclusiones
          </div>
          <div style="font-size:12px;color:{C['text_muted']};line-height:1.75;
                      font-family:'IBM Plex Sans',sans-serif;">
            {concl}
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown(f"""
        <div style="background:{C['bg_panel']};border:1px solid {C['border']};
                    border-left:3px solid {C['teal']};border-radius:10px;
                    padding:18px 20px;min-height:200px;">
          <div style="font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
                      color:{C['text_muted']};margin-bottom:12px;display:flex;align-items:center;
                      gap:6px;font-family:'IBM Plex Sans',sans-serif;">
            &nbsp; Recomendaciones
          </div>
          {recom_html}
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FUNCIÓN PRINCIPAL — capability_analysis
# ─────────────────────────────────────────────
def capability_analysis(data_df):

    inject_css()
    render_topbar()

    # ── Preparar datos — LÓGICA ORIGINAL ─────
    data_df = data_df.apply(pd.to_numeric, errors='coerce').dropna()
    if data_df.empty:
        st.error("⚠ No hay datos válidos para procesar.")
        return

    num_muestras, n = data_df.shape
    d2          = D2_CONSTANTS.get(n, 3.931)
    medias_sub  = data_df.mean(axis=1)
    rangos_sub  = data_df.max(axis=1) - data_df.min(axis=1)
    media_global = medias_sub.mean()
    rango_medio  = rangos_sub.mean()
    sigma        = rango_medio / d2

    st.session_state['mu_capacidad']    = media_global
    st.session_state['sigma_capacidad'] = sigma
    
    # ── Ingreso de Parámetros (Manual Override) ──
    render_section("Parámetros del proceso (Opcional)")
    with st.container():
        st.caption("Opcional: Ingrese valores manuales para sobreescribir el cálculo automático")
        col_mu, col_sig = st.columns(2)
        with col_mu:
            mu_input = st.text_input("Media (μ)", placeholder=f"{media_global:.4f}")
        with col_sig:
            sig_input = st.text_input("Sigma (σ)", placeholder=f"{sigma:.4f}")
    
    # Aplicar override si se ingresaron valores
    try:
        if mu_input: media_global = parse_number(mu_input)
        if sig_input: sigma = parse_number(sig_input)
    except:
        st.warning("Valores de Media o Sigma inválidos. Usando valores calculados.")

    # ── Ingreso de límites (ARQUITECTURA COMPATIBLE) ──
    render_section("Límites de especificación")
    
    # Contenedor nativo clara (C['bg_panel']) con inputs claros (C['bg_input_card'])
    with st.container():
        st.caption("Ingrese los límites de tolerancia del proceso")
        
        col_lsl, col_usl = st.columns(2)
        with col_lsl:
            LSL_input = st.text_input("LIE — Límite inferior de especificación",
                                      placeholder="Ej: 39.600", key="lie_input")
        with col_usl:
            USL_input = st.text_input("LSE — Límite superior de especificación",
                                      placeholder="Ej: 41.800", key="lse_input")

    if LSL_input == "" or USL_input == "":
        st.markdown(f"""
        <div style="background:{C['bg_surface']};border:1px dashed {C['border']};
                    border-radius:9px;padding:20px;text-align:center;margin-top:14px;
                    color:{C['text_hint']};font-size:13px;
                    font-family:'IBM Plex Sans',sans-serif;">
          Ingrese los límites LIE y LSE para continuar el análisis
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Validación — LÓGICA ORIGINAL ─────────
    try:
        LSL = parse_number(LSL_input)
        USL = parse_number(USL_input)
    except Exception:
        st.error("⚠ Valores inválidos. Use punto o coma como separador decimal.")
        return

    if sigma == 0 or LSL >= USL:
        st.error("⚠ Verifique los límites de especificación y la variabilidad del proceso.")
        return

    # ── Cálculos — LÓGICA ORIGINAL ───────────
    Cp  = (USL - LSL) / (6 * sigma)
    Cpu = (USL - media_global) / (3 * sigma)
    Cpl = (media_global - LSL) / (3 * sigma)
    Cpk = min(Cpu, Cpl)

    pnc_inf   = norm.cdf(LSL, media_global, sigma) * 100
    pnc_sup   = (1 - norm.cdf(USL, media_global, sigma)) * 100
    pnc_total = pnc_inf + pnc_sup

    # ── Clasificación — LÓGICA ORIGINAL ──────
    estado, color_clase = clasificar_con_semaforo(Cp, Cpk, Cpu, Cpl)

    # ── Render UI ─────────────────────────────
    render_status_banner(estado, color_clase)

    render_section("Índices de capacidad")
    render_metric_cards(Cp, Cpk, Cpu, Cpl)

    render_section("Estadísticos del proceso")
    render_stat_panels(media_global, rango_medio, sigma, d2, n,
                       LSL, USL, num_muestras,
                       pnc_inf, pnc_sup, pnc_total)

    # ── Gráfica — LÓGICA ORIGINAL + tema dark ─
    render_section("Distribución del proceso")

    x_min   = min(media_global - 4*sigma, LSL - sigma)
    x_max   = max(media_global + 4*sigma, USL + sigma)
    x_range = np.linspace(x_min, x_max, 1000)
    y_norm  = norm.pdf(x_range, media_global, sigma)

    fig = go.Figure()

    if pnc_inf > 0.0001:
        x_l = x_range[x_range <= LSL]
        y_l = norm.pdf(x_l, media_global, sigma)
        fig.add_trace(go.Scatter(
            x=np.concatenate(([x_l[0]], x_l, [x_l[-1]])),
            y=np.concatenate(([0], y_l, [0])),
            fill='tozeroy', fillcolor='rgba(248,81,73,0.18)',
            line=dict(width=0), showlegend=False
        ))
        fig.add_annotation(x=float(np.mean(x_l)), y=float(max(y_l)*0.6),
                           text=f"<b>{pnc_inf:.2f}%</b>", showarrow=False,
                           font=dict(size=12, color="#C0292A", family="JetBrains Mono"))

    if pnc_sup > 0.0001:
        x_r = x_range[x_range >= USL]
        y_r = norm.pdf(x_r, media_global, sigma)
        fig.add_trace(go.Scatter(
            x=np.concatenate(([x_r[0]], x_r, [x_r[-1]])),
            y=np.concatenate(([0], y_r, [0])),
            fill='tozeroy', fillcolor='rgba(248,81,73,0.18)',
            line=dict(width=0), showlegend=False
        ))
        fig.add_annotation(x=float(np.mean(x_r)), y=float(max(y_r)*0.6),
                           text=f"<b>{pnc_sup:.2f}%</b>", showarrow=False,
                           font=dict(size=12, color="#C0292A", family="JetBrains Mono"))

    fig.add_trace(go.Scatter(
        x=x_range, y=y_norm, mode='lines',
        line=dict(color='#1A6FC4', width=2.5),
        fill='tozeroy', fillcolor='rgba(26,111,196,0.08)',
        showlegend=False
    ))

    fig.add_vline(x=LSL, line_color="#C0292A", line_width=1.5,
                  annotation=dict(text="LIE", font=dict(color="#C0292A", size=11),
                                  yref="paper", y=1.02))
    fig.add_vline(x=USL, line_color="#C0292A", line_width=1.5,
                  annotation=dict(text="LSE", font=dict(color="#C0292A", size=11),
                                  yref="paper", y=1.02))
    fig.add_vline(x=media_global, line_dash="dot", line_color="#4A6080", line_width=1.2,
                  annotation=dict(text="μ̂", font=dict(color="#4A6080", size=11),
                                  yref="paper", y=1.02))

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F7FAFD",
        height=360,
        showlegend=False,
        margin=dict(l=32, r=32, t=36, b=36),
        xaxis=dict(
            gridcolor="#DDE8F0", zeroline=False,
            tickfont=dict(size=11, color="#4A6080", family="JetBrains Mono"),
            title=dict(text="Valor de la característica",
                       font=dict(size=11, color="#4A6080")),
        ),
        yaxis=dict(
            gridcolor="#DDE8F0", zeroline=False,
            tickfont=dict(size=10, color="#4A6080"),
            title=dict(text="Densidad", font=dict(size=11, color="#4A6080")),
        ),
        font=dict(family="IBM Plex Sans"),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Reporte ───────────────────────────────
    render_section("Reporte del análisis")
    render_report(Cp, Cpu, Cpl)

    # ── Footer — mantiene tema claro ───────────────────
    st.markdown(f"""
    <div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid {C['border']};
                display:flex;justify-content:space-between;align-items:center;">
      <span style="font-size:10px;color:{C['text_hint']};font-family:'JetBrains Mono',monospace;">
        n={n} obs/subgrupo &nbsp;·&nbsp; m={num_muestras} subgrupos &nbsp;·&nbsp; σ̂={sigma:.4f}
      </span>
      <span style="font-size:10px;color:{C['text_hint']};font-family:'IBM Plex Sans',sans-serif;">
        SPC Manager · Análisis de Capacidad
      </span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PÁGINA DEMO — datos sintéticos de prueba
# ─────────────────────────────────────────────
def run_demo():
    np.random.seed(42)
    data_demo = pd.DataFrame(
        np.random.normal(loc=40.7, scale=0.28, size=(25, 5)),
        columns=[f"M{i+1}" for i in range(5)]
    )
    capability_analysis(data_demo)


if __name__ == "__main__":
    # Inyectar CSS global primero para que aplique a la sidebar
    st.set_page_config(layout="wide")
    inject_css()
    
    # Simulación de la sidebar de la imagen para probar contraste
    with st.sidebar:
        # Markdown nativo para "Control Estadístico de Procesos" (en blanco por CSS)
        st.markdown(f"""
        <div style="text-align:center; font-weight:700; font-size:24px; color:{C_SIDEBAR['text']}; font-family:'IBM Plex Sans',sans-serif; margin-bottom:20px;">
          Control<br>Estadístico de<br>Procesos
        </div>
        """, unsafe_allow_html=True)
        
        # Caption nativo (en blanco por CSS)
        st.caption("Selecciona la fase:")
        # Selectbox nativo (en oscuro por CSS)
        st.selectbox("", ["Fase 1"], key="sb_fase")
        
        st.caption("Módulos Fase 1:")
        st.selectbox("", ["Estadística", "Capacidad"], key="sb_modulo")
        
        # Markdown nativo para "Registros cargados" (en blanco por CSS)
        st.markdown(f"**Registros cargados:**<br>13", unsafe_allow_html=True)
        
    run_demo()