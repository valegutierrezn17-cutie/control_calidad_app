import datetime
from fpdf import FPDF

def sanitizar_texto(texto):
    """
    Reemplaza caracteres especiales del español para prevenir fallos 
    de codificación (UnicodeEncodeError) en las fuentes base de FPDF.
    """
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U'
    }
    for original, reemplazo in reemplazos.items():
        texto = texto.replace(original, reemplazo)
    return texto

def generar_reporte_pdf(titulo_modulo, dataframe, metricas, conclusiones_usuario):
    """
    Genera un informe analítico en formato PDF con diseño formal de ingeniería.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # ---- ENCABEZADO INSTITUCIONAL ----
    pdf.set_font("Arial", 'B', 15)
    pdf.set_text_color(30, 41, 59)  # Color pizarra oscuro (Estilo premium)
    pdf.cell(0, 10, sanitizar_texto(titulo_modulo.upper()), ln=True, align='L')
    
    # Línea divisoria estructural
    pdf.set_draw_color(71, 85, 105)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    # Metadatos del informe
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(100, 116, 139)
    fecha_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(0, 5, sanitizar_texto("PRO-STATS // Sistema Avanzado de Control de Calidad"), ln=True)
    pdf.cell(0, 5, sanitizar_texto(f"Fecha de emision: {fecha_str}"), ln=True)
    pdf.ln(8)
    
    # ---- SECCIÓN 1: PARÁMETROS Y CONFIGURACIÓN DEL ANÁLISIS ----
    if metricas:
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 8, sanitizar_texto("1. Parametros del Analisis"), ln=True)
        pdf.ln(2)
        
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(51, 65, 85)
        
        for clave, valor in metricas.items():
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(60, 6, sanitizar_texto(f" {clave}:"), border=0)
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 6, sanitizar_texto(f"{valor}"), border=0, ln=True)
        pdf.ln(6)
        
    # ---- SECCIÓN 2: RESUMEN ESTADÍSTICO DE LOS DATOS ----
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, sanitizar_texto("2. Resumen Estadistico de la Muestra"), ln=True)
    pdf.ln(2)
    
    # Fuente Courier para garantizar que las columnas del DataFrame queden alineadas de forma exacta
    pdf.set_font("Courier", size=8)
    pdf.set_text_color(51, 65, 85)
    
    # Se genera el resumen matemático limitando decimales para mayor orden visual
    resumen_df = dataframe.describe().round(4).to_string()
    
    for linea in resumen_df.split('\n'):
        pdf.cell(0, 4, sanitizar_texto(linea), ln=True)
    pdf.ln(8)
    
    # ---- SECCIÓN 3: DIAGNÓSTICO Y CONCLUSIONES ----
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, sanitizar_texto("3. Conclusiones Preliminares y Diagnostico"), ln=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(15, 23, 42)
    
    # multi_cell procesa los párrafos largos y hace el salto de línea automático
    pdf.multi_cell(0, 5, txt=sanitizar_texto(conclusiones_usuario))
    
    # Retorna el archivo compilado en formato binario listo para Streamlit
    pdf_contenido = pdf.output(dest='S')
    if isinstance(pdf_contenido, str):
        return pdf_contenido.encode('latin-1', 'ignore')
    return pdf_contenido