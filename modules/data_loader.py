import streamlit as st
import pandas as pd

def load_data():
    """
    Carga un archivo CSV o Excel sin truncar filas y con manejo de errores.
    """
    # Se utiliza label_visibility="collapsed" para que el componente se fusione 
    # estéticamente debajo del contenedor de diseño personalizado en app.py
    file = st.file_uploader("Sube CSV o Excel", type=["csv", "xlsx"], label_visibility="collapsed")
    
    if file is not None:
        try:
            # 1. Detectar extensión e importar con el motor adecuado
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                # Se fuerza el motor openpyxl para garantizar compatibilidad con la plantilla .xlsx
                df = pd.read_excel(file, engine="openpyxl")
            
            # 2. Retornar el DataFrame tal cual se leyó
            return df
            
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
            return None
    return None