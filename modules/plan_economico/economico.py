import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_modulo_economico():
    """
    Renderiza el Módulo de Análisis Económico para comparar el costo 
    de sobrellenado (Giveaway) con un diseño de panel corporativo.
    """
    
    # CSS Profesional
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Panel del Título */
        .header-panel {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 25px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        /* Estilos de Tarjetas KPI */
        .kpi-container { 
            display: grid; 
            grid-template-columns: repeat(3, 1fr); 
            gap: 20px; 
            margin: 25px 0; 
        }
        .kpi-card { 
            background-color: #ffffff; 
            padding: 24px; 
            border-radius: 10px; 
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); 
            text-align: center; 
        }
        .kpi-card.highlight-red { border-top: 4px solid #ef4444; }
        .kpi-card.highlight-neutral { border-top: 4px solid #64748b; }
        .kpi-card.highlight-green { border-top: 4px solid #10b981; }
        
        .kpi-val { 
            font-size: 24px; 
            font-weight: 600; 
            color: #1e293b; 
            margin-top: 8px; 
        }
        .kpi-lbl { 
            font-size: 12px; 
            color: #64748b; 
            text-transform: uppercase; 
            letter-spacing: 0.05em; 
            font-weight: 600; 
        }
        </style>
    """, unsafe_allow_html=True)

    # Encabezado con Panel
    st.markdown("""
        <div class='header-panel'>
            <h1 style='margin: 0; color: #0f172a; font-size: 28px;'>Análisis Económico y Optimización</h1>
            <p style='margin: 10px 0 0 0; color: #475569; font-size: 15px;'>
            Comparativa financiera del costo por sobrellenado. Ingrese los parámetros operativos para evaluar el ahorro potencial.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Configuración de parámetros en columnas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align: center; font-size: 18px; color: #334155;'>Parámetros Comerciales</h3>", unsafe_allow_html=True)
        lie_critico = st.number_input("Límite Comercial Exigido (kg)", value=None, placeholder="Ej. 18.14", step=0.01)
        prod_anual = st.number_input("Producción Anual (Cajas)", value=None, placeholder="Ej. 150000", step=1000)
        costo_caja = st.number_input("Costo Unitario por Caja (USD)", value=None, placeholder="Ej. 8.65", step=0.05)

    with col2:
        st.markdown("<h3 style='text-align: center; font-size: 18px; color: #334155;'>Escenarios Operativos</h3>", unsafe_allow_html=True)
        media_actual = st.number_input("Media Operacional Actual (kg)", value=None, placeholder="Ej. 18.73", step=0.01)
        media_propuesta = st.number_input("Media Operacional Propuesta (kg)", value=None, placeholder="Ej. 18.67", step=0.01)

    st.divider()

    # VALIDACIÓN
    if None in [lie_critico, prod_anual, costo_caja, media_actual, media_propuesta]:
        st.info("Por favor, complete todos los campos numéricos para generar el análisis económico.")
        return 

    # Motor de cálculo
    delta_actual = media_actual - lie_critico
    sobrepeso_anual_actual = prod_anual * delta_actual
    cajas_extra_actual = sobrepeso_anual_actual / lie_critico
    costo_anual_actual = cajas_extra_actual * costo_caja

    delta_propuesto = media_propuesta - lie_critico
    sobrepeso_anual_propuesto = prod_anual * delta_propuesto
    cajas_extra_propuesto = sobrepeso_anual_propuesto / lie_critico
    costo_anual_propuesto = cajas_extra_propuesto * costo_caja

    ahorro_anual = costo_anual_actual - costo_anual_propuesto
    cajas_ahorradas = cajas_extra_actual - cajas_extra_propuesto

    # Visualización de KPIs
    st.markdown("<h3 style='text-align: center; color: #1e293b; margin-top: 20px;'>Indicadores Financieros</h3>", unsafe_allow_html=True)
    
    kpi_html = f"""
    <div class='kpi-container'>
        <div class='kpi-card highlight-red'>
            <div class='kpi-lbl'>Costo Actual</div>
            <div class='kpi-val'>${costo_anual_actual:,.2f}</div>
        </div>
        <div class='kpi-card highlight-neutral'>
            <div class='kpi-lbl'>Costo Propuesto</div>
            <div class='kpi-val'>${costo_anual_propuesto:,.2f}</div>
        </div>
        <div class='kpi-card highlight-green'>
            <div class='kpi-lbl'>Ahorro Neto</div>
            <div class='kpi-val'>${ahorro_anual:,.2f}</div>
        </div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)

    # Tabla Resumen
    data_resumen = {
        "Variable": ["Δ Sobrellenado", "Sobrellenado Total", "Cajas Regaladas", "Costo Anual"],
        "Plan Actual": [f"{delta_actual:.2f} kg", f"{sobrepeso_anual_actual:,.1f} kg", f"{int(cajas_extra_actual):,} cj", f"${costo_anual_actual:,.2f}"],
        "Plan Propuesto": [f"{delta_propuesto:.2f} kg", f"{sobrepeso_anual_propuesto:,.1f} kg", f"{int(cajas_extra_propuesto):,} cj", f"${costo_anual_propuesto:,.2f}"],
        "Ahorro": [f"{delta_actual - delta_propuesto:.2f} kg", f"{sobrepeso_anual_actual - sobrepeso_anual_propuesto:,.1f} kg", f"{int(cajas_ahorradas):,} cj", f"${ahorro_anual:,.2f}"]
    }
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(data_resumen).set_index("Variable"), use_container_width=True)

    # Gráfico
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Plan Actual', 'Plan Propuesto'], 
        y=[costo_anual_actual, costo_anual_propuesto], 
        marker_color=['#ef4444', '#10b981'], 
        texttemplate='$%{y:,.2f}', 
        textposition='outside',
        width=0.4
    ))
    
    fig.update_layout(
        title={
            'text': "Comparativa de Costos (USD)",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=60, l=20, r=20, b=20),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        xaxis=dict(showgrid=False)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Llamada a la función
render_modulo_economico()