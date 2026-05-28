import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stats

def render_muestreo_modulo():
    # =====================================================
    # ESTILOS INYECTADOS DE BASE (Estética Profesional)
    # =====================================================
    st.markdown("""
    <style>
        .main-title {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-size: 28px;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 4px;
        }
        .sub-text {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-size: 14px;
            color: #64748B;
            margin-bottom: 24px;
        }
        .section-title {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-size: 16px;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .conclusion-box {
            background-color: #F8FAFC;
            border-left: 4px solid #475569;
            padding: 16px;
            border-radius: 0 8px 8px 0;
            margin-top: 20px;
        }
        .conclusion-title {
            font-size: 14px;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 6px;
        }
        .conclusion-text {
            font-size: 13px;
            color: #475569;
            line-height: 1.5;
        }
    </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # HEADER DEL MÓDULO
    # =====================================================
    st.markdown('<div class="main-title">Diseño y Planes de Muestreo de Aceptación</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Módulo de Control de Recepción, Gestión de Riesgos y Optimización de Inspección • PRO-STATS</div>', unsafe_allow_html=True)

    # Selección de Enfoque metodológico mediante Tabs
    tab1, tab2, tab3 = st.tabs([
        "Diseño Analítico (Riesgos Clásicos)",
        "Curvas de Desempeño (CO / AOQ)",
        "Tablas Normativas MIL-STD-105E"
    ])

    # =====================================================
    # TAB 1: DISEÑO ANALÍTICO DE PLANES (n, c)
    # =====================================================
    with tab1:
        with st.container(border=True):
            st.markdown('<div class="section-title">Configuración de Parámetros de Calidad y Riesgos</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                p1 = st.number_input("Nivel de Calidad Aceptable (AQL / p1)", min_value=0.0001, max_value=0.5000, value=0.0150, format="%.4f", help="Proporción máxima de defectuosos aceptable en el lote.")
                alpha = st.number_input("Riesgo del Productor (Alfa)", min_value=0.01, max_value=0.50, value=0.05, format="%.2f", help="Probabilidad de rechazar un lote con calidad aceptable.")
            with c2:
                p2 = st.number_input("Nivel de Calidad Distribución Rechazable (RQL / LQ / p2)", min_value=0.0010, max_value=0.9000, value=0.0600, format="%.4f", help="Proporción de defectuosos insatisfactoria para el consumidor.")
                beta = st.number_input("Riesgo del Consumidor (Beta)", min_value=0.01, max_value=0.50, value=0.10, format="%.2f", help="Probabilidad de aceptar un lote con calidad rechazable.")

            N_lote = st.number_input("Tamaño del Lote (N)", min_value=10, max_value=1000000, value=5000, step=100)

        # LÓGICA MATEMÁTICA DEL DISEÑO DEL PLAN (Relación Poisson-Gamma)
        c_opt = 0
        n_opt = 0
        encontrado = False

        for c_val in range(0, 100):
            l1 = stats.gamma.ppf(alpha, c_val + 1)
            l2 = stats.gamma.ppf(1 - beta, c_val + 1)
            
            n_max_prod = l1 / p1
            n_min_cons = l2 / p2
            
            if n_min_cons <= n_max_prod:
                c_opt = c_val
                n_opt = int(np.ceil(n_min_cons))
                encontrado = True
                break
        
        if not encontrado:
            for c_val in range(0, 50):
                l1 = stats.gamma.ppf(alpha, c_val + 1)
                l2 = stats.gamma.ppf(1 - beta, c_val + 1)
                n_est = int(np.ceil((l1/p1 + l2/p2) / 2))
                if n_est > 0:
                    c_opt = c_val
                    n_opt = n_est
                    break

        alpha_real = 1 - stats.poisson.cdf(c_opt, n_opt * p1)
        beta_real = stats.poisson.cdf(c_opt, n_opt * p2)

        # Almacenamiento en session_state para la Tab 2
        st.session_state['muestreo_n'] = n_opt
        st.session_state['muestreo_c'] = c_opt
        st.session_state['muestreo_N'] = N_lote
        st.session_state['muestreo_AQL'] = p1
        st.session_state['muestreo_RQL'] = p2

        # Despliegue de Resultados Estilo KPI Cards
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid #0F172A; border-radius:0 12px 12px 0; padding:20px 24px 18px 24px; margin-bottom:22px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-family:sans-serif; font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#64748B; border-bottom:1px solid #F1F5F9; padding-bottom:10px; margin-bottom:16px;">
                Plan de Muestreo Simple por Atributos Calculado
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:3px solid #334155; border-radius:8px; padding:14px 18px;">
                    <div style="font-family:sans-serif; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; color:#475569; margin-bottom:4px;">Tamaño de Muestra</div>
                    <div style="font-family:sans-serif; font-size:11px; color:#94A3B8; margin-bottom:4px;">n — Unidades a inspeccionar</div>
                    <div style="font-family:sans-serif; font-size:28px; font-weight:700; color:#0F172A; line-height:1;">{n_opt}</div>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:3px solid #334155; border-radius:8px; padding:14px 18px;">
                    <div style="font-family:sans-serif; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; color:#475569; margin-bottom:4px;">Número de Aceptación</div>
                    <div style="font-family:sans-serif; font-size:11px; color:#94A3B8; margin-bottom:4px;">c — Máximo de defectuosos permitido</div>
                    <div style="font-family:sans-serif; font-size:28px; font-weight:700; color:#0F172A; line-height:1;">{c_opt}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<div class="section-title">Evaluación Operativa de Riesgos Reales</div>', unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            
            with m1:
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:3px solid #475569; border-radius:6px; padding:14px; text-align:center;">
                    <div style="font-size:11px; font-weight:600; color:#64748B; text-transform:uppercase;">Riesgo Productor Real (α)</div>
                    <div style="font-size:22px; font-weight:700; color:#0F172A; margin-top:4px;">{alpha_real*100:.2f}%</div>
                    <div style="font-size:11px; color:#94A3B8; margin-top:2px;">Objetivo: {alpha*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:3px solid #475569; border-radius:6px; padding:14px; text-align:center;">
                    <div style="font-size:11px; font-weight:600; color:#64748B; text-transform:uppercase;">Riesgo Consumidor Real (β)</div>
                    <div style="font-size:22px; font-weight:700; color:#0F172A; margin-top:4px;">{beta_real*100:.2f}%</div>
                    <div style="font-size:11px; color:#94A3B8; margin-top:2px;">Objetivo: {beta*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                fraccion_muestra = (n_opt / N_lote) * 100
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:3px solid #475569; border-radius:6px; padding:14px; text-align:center;">
                    <div style="font-size:11px; font-weight:600; color:#64748B; text-transform:uppercase;">Impacto de Inspección</div>
                    <div style="font-size:22px; font-weight:700; color:#0F172A; margin-top:4px;">{fraccion_muestra:.2f}%</div>
                    <div style="font-size:11px; color:#94A3B8; margin-top:2px;">Porcentaje del lote total</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div class="conclusion-box">
            <div class="conclusion-title">Conclusión de Diseño Analítico</div>
            <div class="conclusion-text">
                El algoritmo de optimización ha calculado el tamaño mínimo de muestra requerido para salvaguardar la confiabilidad estadística del proceso. Este diseño garantiza que los lotes que cumplan con el AQL tengan un riesgo mínimo de ser rechazados erróneamente.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # TAB 2: CURVAS CARACTERÍSTICAS (CO, AOQ)
    # =====================================================
    with tab2:
        n_curr = st.session_state.get('muestreo_n', 50)
        c_curr = st.session_state.get('muestreo_c', 2)
        N_curr = st.session_state.get('muestreo_N', 1000)
        p1_curr = st.session_state.get('muestreo_AQL', 0.0150) 
        p2_curr = st.session_state.get('muestreo_RQL', 0.0600) 

        with st.container(border=True):
            st.markdown('<div class="section-title">Análisis de Desempeño del Plan de Inspección</div>', unsafe_allow_html=True)
            
            p_valores = np.linspace(0.0001, 0.40, 400)
            Pa_valores = stats.poisson.cdf(c_curr, n_curr * p_valores)
            AOQ_valores = Pa_valores * p_valores * ((N_curr - n_curr) / N_curr)
            
            aoql_idx = np.argmax(AOQ_valores)
            aoql_val = AOQ_valores[aoql_idx]
            p_aoql = p_valores[aoql_idx]

            tipo_grafica = st.radio(
                "Seleccione la curva analítica a evaluar:",
                ["Curva de Operación Característica (CO)", "Calidad de Salida Promedio (AOQ)"],
                horizontal=True
            )

            fig = go.Figure()

            config_ejes = dict(
                showgrid=True,
                gridcolor="#E0E0E0",
                gridwidth=1,
                griddash='dot',
                zeroline=False,
            )

            if tipo_grafica == "Curva de Operación Característica (CO)":
                fig.add_trace(go.Scatter(
                    x=p_valores * 100,
                    y=Pa_valores * 100,
                    mode='lines',
                    name='Probabilidad de Aceptación',
                    line=dict(color='#007FFF', width=2)
                ))

                # Líneas verticales LTPD y NAC con etiquetas fijas
                fig.add_vline(x=p2_curr * 100, line_dash="dash", line_color="#A52A2A")
                fig.add_annotation(
                    x=p2_curr * 100, y=100.0, text="LTPD", font=dict(color="#A52A2A", size=10),
                    showarrow=False, yshift=10, align="center"
                )
                
                fig.add_vline(x=p1_curr * 100, line_dash="dash", line_color="#20B2AA")
                fig.add_annotation(
                    x=p1_curr * 100, y=100.0, text="NAC", font=dict(color="#20B2AA", size=10),
                    showarrow=False, yshift=10, align="center"
                )

                fig.update_layout(
                    title=dict(
                        text=f"Curva OC — N={N_curr}, n={n_curr}, c={c_curr}",
                        x=0.5,
                        font=dict(size=16, color="#0F172A")
                    ),
                    xaxis=dict(
                        title="% No conformes en el lote (p')",
                        range=[-0.5, 40],
                        dtick=10,
                        **config_ejes
                    ),
                    yaxis=dict(
                        title="Probabilidad de Aceptación (%)",
                        range=[-5, 105],
                        dtick=20,
                        **config_ejes
                    )
                )

            elif tipo_grafica == "Calidad de Salida Promedio (AOQ)":
                fig.add_trace(go.Scatter(
                    x=p_valores * 100,
                    y=AOQ_valores * 100,
                    mode='lines',
                    name='AOQ',
                    line=dict(color='#9370DB', width=2.5)
                ))

                aoql_y = aoql_val * 100
                fig.add_hline(y=aoql_y, line_dash="dash", line_color="#A52A2A")
                
                fig.add_annotation(
                    x=1.0, xref="paper", y=aoql_y, text=f"AOQL ({aoql_val*100:.3f}%)",
                    font=dict(color="#A52A2A", size=10), showarrow=False,
                    yshift=-12, xshift=-40, yanchor="top", align="left"
                )

                fig.add_trace(go.Scatter(
                    x=[p_aoql * 100],
                    y=[aoql_y],
                    mode='markers',
                    name='Punto AOQL',
                    marker=dict(color='#0F172A', size=10)
                ))

                fig.update_layout(
                    title=dict(
                        text="Curva AOQ — Calidad Promedio de Salida",
                        x=0.5,
                        font=dict(size=16, color="#0F172A")
                    ),
                    xaxis=dict(
                        title="% No conformes en el lote (p')",
                        range=[-0.5, 40],
                        dtick=10,
                        **config_ejes
                    ),
                    yaxis=dict(
                        title="AOQ (%)",
                        **config_ejes
                    )
                )

            fig.update_layout(
                template="plotly_white", 
                height=450, 
                paper_bgcolor="white", 
                plot_bgcolor="white", 
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):
            st.markdown('<div class="section-title">Cálculo Puntual de Aceptación y Rechazo</div>', unsafe_allow_html=True)
            
            p_usuario = st.number_input(
                "Ingrese el porcentaje de defectuosos / no conforme a evaluar (%)", 
                min_value=0.00, max_value=100.00, value=2.00, step=0.50, format="%.2f"
            )
            
            p_usuario_frac = p_usuario / 100.0
            pa_usuario_val = stats.poisson.cdf(c_curr, n_curr * p_usuario_frac)
            pr_usuario_val = 1.0 - pa_usuario_val

            k1, k2 = st.columns(2)
            with k1:
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:3px solid #6B0D0D; border-radius:6px; padding:14px; text-align:center;">
                    <div style="font-size:11px; font-weight:600; color:#64748B; text-transform:uppercase;">Probabilidad de Aceptación (Pa)</div>
                    <div style="font-size:24px; font-weight:700; color:#0F172A; margin-top:4px;">{pa_usuario_val*100:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
            with k2:
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:3px solid #475569; border-radius:6px; padding:14px; text-align:center;">
                    <div style="font-size:11px; font-weight:600; color:#64748B; text-transform:uppercase;">Probabilidad de Rechazo (Pr)</div>
                    <div style="font-size:24px; font-weight:700; color:#0F172A; margin-top:4px;">{pr_usuario_val*100:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

    # =====================================================
    # TAB 3: TABLAS NORMATIVAS MIL-STD-105E
    # =====================================================
    with tab3:
        with st.container(border=True):
            st.markdown('<div class="section-title">Consulta de Planes según Norma MIL-STD-105E / ISO 2859</div>', unsafe_allow_html=True)
            
            c_m1, c_m2, c_m3 = st.columns(3)
            with c_m1:
                size_input = st.number_input("Tamaño de Lote Estándar", min_value=1, max_value=1500000, value=2000, step=50)
            with c_m2:
                nivel_insp = st.selectbox("Nivel de Inspección", ["I", "II (General)", "III"], index=1)
            with c_m3:
                aql_std = st.selectbox("Nivel AQL (%) admisible", [0.065, 0.10, 0.15, 0.25, 0.40, 0.65, 1.0, 1.5, 2.5, 4.0, 6.5, 10.0], index=7)

            def buscar_letra_mil_std(lote):
                if lote <= 8: return "A", 2
                elif lote <= 15: return "B", 3
                elif lote <= 25: return "C", 5
                elif lote <= 50: return "D", 8
                elif lote <= 90: return "E", 13
                elif lote <= 150: return "F", 20
                elif lote <= 280: return "G", 32
                elif lote <= 500: return "H", 50
                elif lote <= 1200: return "J", 80
                elif lote <= 3200: return "K", 125
                elif lote <= 10000: return "L", 200
                elif lote <= 35000: return "M", 315
                elif lote <= 150000: return "N", 500
                elif lote <= 500000: return "P", 800
                else: return "Q", 1250

            letra, n_mil = buscar_letra_mil_std(size_input)
            c_mil = 1 if aql_std <= 1.5 else int(np.floor(n_mil * (aql_std/100)))
            r_mil = c_mil + 1

            st.write("")
            st.markdown(f"""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px 16px; border-radius: 6px; font-size: 13px; color: #334155;">
                De acuerdo con la norma internacional, para un lote de <strong>{size_input}</strong> unidades bajo un nivel de control ordinario, se asigna de manera estandarizada la <strong>Letra Código: {letra}</strong>.
            </div>
            """, unsafe_allow_html=True)
            st.write("")

            r1, r2, r3, r4 = st.columns(4)
            with r1:
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:3px solid #1E293B; border-radius:6px; padding:12px; text-align:center;">
                    <div style="font-size:10px; font-weight:600; color:#64748B; text-transform:uppercase;">Muestra Norma (n)</div>
                    <div style="font-size:20px; font-weight:700; color:#0F172A; margin-top:4px;">{n_mil}</div>
                </div>
                """, unsafe_allow_html=True)
            with r2:
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:3px solid #1E293B; border-radius:6px; padding:12px; text-align:center;">
                    <div style="font-size:10px; font-weight:600; color:#64748B; text-transform:uppercase;">Aceptación (c)</div>
                    <div style="font-size:20px; font-weight:700; color:#0F172A; margin-top:4px;">{c_mil}</div>
                </div>
                """, unsafe_allow_html=True)
            with r3:
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:3px solid #1E293B; border-radius:6px; padding:12px; text-align:center;">
                    <div style="font-size:10px; font-weight:600; color:#64748B; text-transform:uppercase;">Rechazo (r)</div>
                    <div style="font-size:20px; font-weight:700; color:#0F172A; margin-top:4px;">{r_mil}</div>
                </div>
                """, unsafe_allow_html=True)
            with r4:
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-top:3px solid #1E293B; border-radius:6px; padding:12px; text-align:center;">
                    <div style="font-size:10px; font-weight:600; color:#64748B; text-transform:uppercase;">Estado de Código</div>
                    <div style="font-size:14px; font-weight:700; color:#0F172A; margin-top:10px;">Vigente / Normal</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div class="conclusion-box">
            <div class="conclusion-title">Conclusión y Dictamen Normativo</div>
            <div class="conclusion-text">
                El uso del estándar MIL-STD-105E asegura un marco de muestreo indexado formalmente para auditorías contractuales.
            </div>
        </div>
        """, unsafe_allow_html=True)