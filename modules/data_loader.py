import streamlit as st
import pandas as pd

def load_data():
    """
    Carga un archivo CSV o Excel sin truncar filas y con manejo de errores.
    """
    file = st.file_uploader("Sube CSV o Excel", type=["csv", "xlsx"])
    
    if file is not None:
        try:
            # 1. Detectar extensión
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # 2. Retornar el DataFrame tal cual se leyó
            # (La limpieza de filas vacías se hace en app.py para tener control total)
            return df
            
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
            return None
    return None