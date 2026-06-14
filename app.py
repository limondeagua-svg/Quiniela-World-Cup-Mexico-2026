import streamlit as st
import pandas as pd

st.title("Diagnóstico de datos")

# Intentamos leer el archivo
try:
    df = pd.read_excel('quiniela_actualizada_2026.xlsx', sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
    st.write("Archivo cargado con éxito")
    
    # Vamos a mostrar los nombres que detecta en la fila 2 (índice 1)
    st.write("Nombres detectados en fila 2 (índice 1):")
    st.write(df.iloc[1, :].tolist())
    
    # Vamos a mostrar qué hay en la fila 3 (índice 2)
    st.write("Valores en fila 3 (índice 2):")
    st.write(df.iloc[2, :].tolist())
    
except Exception as e:
    st.write(f"Error al leer: {e}")
