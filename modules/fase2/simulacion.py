import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# =====================================================
# ESTILOS CSS (Mejorados y Estables sin romper el DOM)
# =====================================================
st.markdown("""
<style>

/* =========================
FONDO GENERAL
========================= */
.stApp{
    background-color:#F3F5F7;
}

/* =========================
TÍTULO PRINCIPAL
========================= */
.main-title{
    font-size:42px;
    font-weight:800;
    color:#1F2D3D;
    margin-bottom:10px;
}

.sub-text{
    color:#5D6D7E;
    font-size:16px;
    margin-bottom:20px;
}

/* =========================
TÍTULOS DE SECCIÓN
========================= */
.section-title{
    color:#1B4F72;
    font-size:24px;
    font-weight:700;
    margin-bottom:15px;
}

/* =========================
ESTILO DE CONTENEDORES NATIVOS (Cards)
========================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white !important;
    border-radius: 18px !important;
    padding: 22px !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06) !important;
    border: 1px solid #E5E8EC !important;
    margin-bottom: 10px !important;
}

/* Card HTML pura (para los parámetros independientes) */
.custom-card-html {
    background: white;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    border: 1px solid #E5E8EC;
    margin-bottom: 22px;
}

/* =========================
DISEÑO DE LOS PANELES DE PARÁMETROS
========================= */
.param-grid {
    display: flex;
    gap: 16px;
    margin-top: 10px;
}

.param-card {
    flex: 1;
    background: #F0F4F8;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px 20px;
}

.param-label {
    font-size: 13px;
    font-weight: 600;
    color: #5D6D7E;
    margin-bottom: 6px;
}

.param-value {
    font-size: 26px;
    font-weight: 800;
    color: #1D4ED8;
}

/* =========================
KPI CARDS — PARÁMETROS DE ESTABILIZACIÓN
========================= */
.kpi-params-wrapper {
    background: #FFFFFF;
    border: 1px solid #E4E8EF;
    border-left: 4px solid #1A56DB;
    border-radius: 0 12px 12px 0;
    padding: 20px 24px 18px 24px;
    margin-bottom: 22px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.kpi-params-header {
    font-family: 'IBM Plex Mono', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8492A6;
    border-bottom: 0.5px solid #E4E8EF;
    padding-bottom: 10px;
    margin-bottom: 16px;
}

.kpi-params-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}

.kpi-param-card {
    background: #F0F6FF;
    border: 0.5px solid #C2D8F5;
    border-radius: 8px;
    padding: 14px 18px;
    position: relative;
}

.kpi-param-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #1A56DB;
    border-radius: 8px 0 0 8px;
}

.kpi-param-label {
    font-family: 'IBM Plex Mono', 'Courier New', monospace;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #4A6FA5;
    margin-bottom: 6px;
}

.kpi-param-symbol {
    font-family: 'IBM Plex Mono', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 500;
    color: #7A9CC8;
    margin-bottom: 2px;
}

.kpi-param-value {
    font-family: 'IBM Plex Mono', 'Courier New', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #0C3A7A;
    letter-spacing: -0.5px;
    line-height: 1;
}

.kpi-param-sublabel {
    font-size: 10px;
    color: #7A9CC8;
    margin-top: 5px;
    font-weight: 400;
}

/* =========================
SUBGRUPOS (Contenedores aninados con borde)
========================= */
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FAFBFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 16px !important;
    box-shadow: none !important;
    margin-bottom: 14px !important;
}

/* =========================
MÉTRICAS
========================= */
[data-testid="metric-container"]{
    background:#F8FAFC;
    border:1px solid #E5E7EB;
    padding:18px;
    border-radius:16px;
    box-shadow:none;
}

/* =========================
BOTONES
========================= */
.stButton > button{
    width: 100%;
    border:none;
    border-radius:10px;
    padding:10px 16px;
    font-weight:700;
    font-size:14px;
    background:linear-gradient(
        135deg,
        #1D4ED8,
        #2563EB
    );
    color:white;
    transition:0.25s;
}

.stButton > button:hover{
    transform:translateY(-2px);
    background:linear-gradient(
        135deg,
        #2563EB,
        #3B82F6
    );
}

/* =========================
INPUTS Y RADIOS
========================= */
.stNumberInput input{
    border-radius:10px !important;
}

.stRadio > div{
    background:#F8FAFC;
    padding:10px;
    border-radius:12px;
}

[data-testid="stFileUploader"]{
    border-radius:14px;
    border:1px solid #D6DBDF;
    background:white;
    padding:12px;
}

.stAlert{
    border-radius:14px;
}

[data-testid="stDataFrame"]{
    border-radius:14px;
    overflow:hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCIÓN PRINCIPAL (Mantiene el nombre para app.py)
# =====================================================
def arl_live_simulation():

    # =====================================================
    # HEADER
    # =====================================================
    st.markdown("""
    <div class="main-title">
        📈 Monitoreo en Tiempo Real (Fase II)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sub-text">
        Control Estadístico de Procesos en Línea • PRO-STATS
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # COMPROBACIÓN DE SESIÓN (ESTABLE Y RESPALDADA)
    # =====================================================
    if 'sigma_capacidad' not in st.session_state:
        if 'capacidad_sigma' in st.session_state:
            st.session_state['sigma_capacidad'] = st.session_state['capacidad_sigma']
        else:
            st.session_state['sigma_capacidad'] = 1.0000

    if 'mu_capacidad' not in st.session_state:
        if 'capacidad_media' in st.session_state:
            st.session_state['mu_capacidad'] = st.session_state['capacidad_media']
        else:
            st.session_state['mu_capacidad'] = 0.0000

    mu0 = float(st.session_state['mu_capacidad'])
    sigma = float(st.session_state['sigma_capacidad'])

    if "subgrupos" not in st.session_state:
        st.session_state.subgrupos = [[0.0,0.0,0.0,0.0,0.0]]

    if "carga_id" not in st.session_state:
        st.session_state.carga_id = 0

    # =====================================================
    # 1. PARÁMETROS DE ESTABILIZACIÓN — KPI Cards Profesionales
    # =====================================================
    _card_mu = (
        "<div style='background:#F0F6FF;border:0.5px solid #C2D8F5;"
        "border-left:3px solid #1A56DB;border-radius:8px;padding:14px 18px;'>"
        "<div style='font-family:Courier New,monospace;font-size:9px;font-weight:700;"
        "text-transform:uppercase;letter-spacing:0.12em;color:#4A6FA5;margin-bottom:4px;'>"
        "Media estabilizada</div>"
        "<div style='font-family:Courier New,monospace;font-size:10px;"
        "color:#7A9CC8;margin-bottom:4px;'>&#956;&#8320; &mdash; Grand Mean</div>"
        "<div style='font-family:Courier New,monospace;font-size:28px;font-weight:700;"
        "color:#0C3A7A;letter-spacing:-0.5px;line-height:1;'>"
        + str(round(mu0, 4)) +
        "</div>"
        "<div style='font-size:10px;color:#7A9CC8;margin-top:5px;'>"
        "L&iacute;nea central de la carta X&#772;</div>"
        "</div>"
    )

    _card_sigma = (
        "<div style='background:#F0F6FF;border:0.5px solid #C2D8F5;"
        "border-left:3px solid #1A56DB;border-radius:8px;padding:14px 18px;'>"
        "<div style='font-family:Courier New,monospace;font-size:9px;font-weight:700;"
        "text-transform:uppercase;letter-spacing:0.12em;color:#4A6FA5;margin-bottom:4px;'>"
        "Sigma estabilizada</div>"
        "<div style='font-family:Courier New,monospace;font-size:10px;"
        "color:#7A9CC8;margin-bottom:4px;'>&#963; &mdash; Process Sigma</div>"
        "<div style='font-family:Courier New,monospace;font-size:28px;font-weight:700;"
        "color:#0C3A7A;letter-spacing:-0.5px;line-height:1;'>"
        + str(round(sigma, 4)) +
        "</div>"
        "<div style='font-size:10px;color:#7A9CC8;margin-top:5px;'>"
        "Desviaci&oacute;n est&aacute;ndar del proceso</div>"
        "</div>"
    )

    _wrapper = (
        "<div style='background:#FFFFFF;border:1px solid #E4E8EF;"
        "border-left:4px solid #1A56DB;border-radius:0 12px 12px 0;"
        "padding:20px 24px 18px 24px;margin-bottom:22px;"
        "box-shadow:0 2px 10px rgba(0,0,0,0.05);'>"
        "<div style='font-family:Courier New,monospace;font-size:9px;font-weight:700;"
        "letter-spacing:0.15em;text-transform:uppercase;color:#8492A6;"
        "border-bottom:0.5px solid #E4E8EF;padding-bottom:10px;margin-bottom:16px;'>"
        "Par&aacute;metros de referencia del proceso &nbsp;&middot;&nbsp; Límites Fase I cargados"
        "</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:14px;'>"
        + _card_mu + _card_sigma +
        "</div></div>"
    )

    st.markdown(_wrapper, unsafe_allow_html=True)

    # =====================================================
    # 2. INGRESO DE DATOS DE PLANTA
    # =====================================================
    with st.container(border=True):
        st.markdown('<div class="section-title">📥 Entrada de Datos de Proceso</div>', unsafe_allow_html=True)

        modo = st.radio(
            "Seleccione el método de captura de datos:",
            ["Manual (Ingreso en Línea)", "Importar desde Archivo (Excel/CSV)"],
            horizontal=True,
            key="radio_base"
        )

        if modo == "Importar desde Archivo (Excel/CSV)":
            archivo = st.file_uploader(
                "Cargar historial de subgrupos",
                type=["xlsx","xls","csv"],
                key="file_up_base"
            )

            if archivo is not None:
                try:
                    archivo.seek(0)
                    if archivo.name.endswith(".csv"):
                        try:
                            excel_df = pd.read_csv(archivo)
                        except:
                            archivo.seek(0)
                            excel_df = pd.read_csv(archivo, sep=";")
                    else:
                        excel_df = pd.read_excel(archivo, engine="openpyxl")

                    st.success("Archivo importado correctamente.")
                    st.dataframe(excel_df.head(), use_container_width=True)

                    columnas = st.multiselect(
                        "Seleccione las columnas del subgrupo:",
                        excel_df.columns.tolist(),
                        key="cols_base"
                    )

                    if len(columnas) > 0:
                        if st.button("📥 Cargar Lecturas al Gráfico", key="btn_load_base"):
                            data_raw = excel_df[columnas].copy()
                            data_numeric = data_raw.apply(pd.to_numeric, errors='coerce')
                            nuevos_subgrupos = []

                            for i in range(len(data_numeric)):
                                fila = data_numeric.iloc[i].dropna().tolist()
                                if len(fila) > 0:
                                    nuevos_subgrupos.append(fila)

                            if nuevos_subgrupos:
                                st.session_state.subgrupos = nuevos_subgrupos
                                st.session_state.carga_id += 1
                                st.rerun()

                except Exception as e:
                    st.error(f"Error al procesar el archivo: {e}")

        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("➕ Añadir Nuevo Subgrupo", key="man_sg"):
                st.session_state.subgrupos.append([0.0,0.0,0.0,0.0,0.0])
                st.rerun()

        with c2:
            if st.button("➕ Añadir Muestra a Último Subgrupo", key="man_dt"):
                st.session_state.subgrupos[-1].append(0.0)
                st.rerun()

    # =====================================================
    # 3. DATOS DE MONITOREO
    # =====================================================
    with st.container(border=True):
        st.markdown('<div class="section-title">🧾 Inspección de Subgrupos Activos</div>', unsafe_allow_html=True)

        edited_subgroups = []
        cid = st.session_state.get("carga_id", 0)

        for i, subgroup in enumerate(st.session_state.subgrupos):
            n_datos = len(subgroup)

            with st.container(border=True):
                _sg_header = (
                    "<div style='background:#F1F5F9;margin:-16px -16px 14px -16px;"
                    "padding:10px 16px;border-bottom:1px solid #E2E8F0;'>"
                    "<span style='font-size:13px;font-weight:700;color:#1D4ED8;'>"
                    "Subgrupo Operativo " + str(i+1) +
                    " <span style='display:inline-block;background:#DBEAFE;color:#1D4ED8;"
                    "font-size:11px;font-weight:600;padding:2px 8px;border-radius:20px;"
                    "border:1px solid #BFDBFE;margin-left:8px;'>n&nbsp;=&nbsp;" + str(n_datos) + "</span>"
                    "</span></div>"
                )
                st.markdown(_sg_header, unsafe_allow_html=True)

                spacer, btn_dato, btn_sg = st.columns([3.5, 1.2, 1.2])

                with btn_dato:
                    if st.button("− Remover Muestra", key=f"del_dt_{i}_{cid}"):
                        if len(st.session_state.subgrupos[i]) > 1:
                            st.session_state.subgrupos[i].pop()
                            st.rerun()

                with btn_sg:
                    if st.button("✕ Eliminar SG", key=f"del_sg_{i}_{cid}"):
                        if len(st.session_state.subgrupos) > 1:
                            st.session_state.subgrupos.pop(i)
                            st.rerun()

                max_por_fila = 5
                row_values = []

                for fila_idx in range(0, n_datos, max_por_fila):
                    datos_fila = subgroup[fila_idx:fila_idx + max_por_fila]
                    cols = st.columns(len(datos_fila))

                    for j_rel, _ in enumerate(datos_fila):
                        j_abs = fila_idx + j_rel
                        val = cols[j_rel].number_input(
                            f"Muestra {j_abs+1}",
                            value=float(subgroup[j_abs]),
                            key=f"in_{i}_{j_abs}_{cid}",
                            format="%.2f"
                        )
                        row_values.append(val)

                edited_subgroups.append(row_values)

        st.session_state.subgrupos = edited_subgroups

    # =====================================================
    # PROCESAMIENTO DE LÓGICA ESTADÍSTICA
    # =====================================================
    medias = []
    ucls = []
    lcls = []
    fuera_c = []
    fuera_i = []
    detalles_alerta = []

    for idx, subgroup in enumerate(st.session_state.subgrupos):
        n_actual = len(subgroup)
        m_sub = np.mean(subgroup)

        UCL = mu0 + 3 * (sigma / np.sqrt(n_actual))
        LCL = mu0 - 3 * (sigma / np.sqrt(n_actual))

        medias.append(m_sub)
        ucls.append(UCL)
        lcls.append(LCL)

        estado_media = (m_sub > UCL or m_sub < LCL)
        fuera_c.append(estado_media)

        indices_fallas = [
            j+1 for j, x in enumerate(subgroup) if x > UCL or x < LCL
        ]

        if indices_fallas:
            fuera_i.append(True)
            detalles_alerta.append({
                "Subgrupo": idx + 1,
                "Muestras Fuera de Límites": str(indices_fallas),
                "Estado": "Fuera de Control" if estado_media else "Desviación Puntual"
            })
        else:
            fuera_i.append(False)

    # =====================================================
    # 4. GRÁFICA DE CONTROL
    # =====================================================
    if medias:
        with st.container(border=True):
            fig = go.Figure()
            x_axis = np.arange(1, len(medias)+1)

            fig.add_trace(
                go.Scatter(
                    x=x_axis, y=medias, mode='lines+markers', name='Media de Subgrupo (X̄)',
                    line=dict(color='#1565C0', width=3),
                    marker=dict(
                        size=10,
                        color=['#E53935' if f else '#1565C0' for f in fuera_c],
                        line=dict(color='black', width=1)
                    )
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=x_axis, y=ucls, mode='lines', name='LCS (Límite Control Sup.)',
                    line=dict(color='#E53935', dash='dash', width=2)
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=x_axis, y=lcls, mode='lines', name='LCI (Límite Control Inf.)',
                    line=dict(color='#E53935', dash='dash', width=2)
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=x_axis, y=[mu0]*len(x_axis), mode='lines', name='LC (Línea Central)',
                    line=dict(color='#2E7D32', width=2)
                )
            )

            fig.update_layout(
                template="plotly_white",
                height=480,
                title=dict(
                    text="Carta de Control X̄ en Tiempo Real",
                    x=0.5,
                    xanchor="center",
                    font=dict(size=24, color="#1F2D3D")
                ),
                xaxis=dict(title="Número de Subgrupo", showgrid=True, gridcolor="#EAECEE"),
                yaxis=dict(title="Valor Medio Registrado", showgrid=True, gridcolor="#EAECEE"),
                legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),
                paper_bgcolor="white",
                plot_bgcolor="white"
            )

            st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # 5. MÉTRICAS DE RESULTADO
    # =====================================================
    with st.container(border=True):
        st.markdown('<div class="section-title">📊 Diagnóstico del Estado Actual</div>', unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Subgrupos Evaluados", len(medias))
        with m2:
            st.metric("Puntos Fuera de Control", sum(fuera_c))
        with m3:
            st.metric("Alertas Activas", sum(fuera_i))

    # =====================================================
    # 6. CONCLUSIONES Y REINICIO
    # =====================================================
    with st.container(border=True):
        st.markdown('<div class="section-title">📋 Conclusiones Operativas</div>', unsafe_allow_html=True)

        if sum(fuera_c) == 0 and sum(fuera_i) == 0:
            st.success("Análisis operativo: El proceso se encuentra actualmente bajo Control Estadístico de Procesos (SPC).")
        else:
            if sum(fuera_c) > 0:
                st.error(f"Inestabilidad crítica: Se detectaron {sum(fuera_c)} puntos completamente fuera de los límites de control.")
            if detalles_alerta:
                st.warning(f"Se registraron desviaciones en las muestras de {len(detalles_alerta)} subgrupos.")
                st.dataframe(pd.DataFrame(detalles_alerta), use_container_width=True)

        st.info("""
        **Protocolo de Acción Correctiva (OCAP):**
        * Investigar de inmediato variaciones por causas asignables (herramientas, descalibración, material).
        * Validar la integridad de los datos reportados en las últimas muestras.
        * Suspender o ajustar el proceso si la tendencia fuera de control persiste en subgrupos consecutivos.
        """)

        st.write("")
        rc1, rc2, rc3 = st.columns([1, 2, 1])
        with rc2:
            if st.button("🔄 Reiniciar Historial de Monitoreo", key="reset_base"):
                st.session_state.subgrupos = [[0.0,0.0,0.0,0.0,0.0]]
                st.session_state.carga_id += 1
                st.rerun()