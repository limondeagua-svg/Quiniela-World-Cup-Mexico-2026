import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="wide")

st.title("🏆 Quiniela Mundial 2026")

# 1. Carga de datos
# Asegúrate de que el nombre del archivo sea exactamente igual al de tu repositorio
archivo = 'QUINIELA WORLD CUP MEXICO 2026 FINAL.xlsx'
df = pd.read_excel(archivo)

# 2. Lógica para encontrar al líder
# Ajusta 'Nombre' y 'Puntos' si tus columnas tienen otros nombres en el Excel
lider = df.groupby('Nombre')['Puntos'].sum().idxmax()
puntaje_lider = df.groupby('Nombre')['Puntos'].sum().max()

# 3. Mostrar el componente de métricas (LA MEJORA)
st.subheader("Marcador en tiempo real")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="🏆 Líder actual", value=lider)
with col2:
    st.metric(label="📈 Puntos acumulados", value=puntaje_lider)

st.divider()

# 4. Mostrar la tabla de datos
st.subheader("Tabla de posiciones")
st.dataframe(df)

# Opcional: Si quieres mostrar una gráfica de barras básica de los puntos
st.subheader("Gráfica de puntos")
fig = px.bar(df.groupby('Nombre')['Puntos'].sum().reset_index(), x='Nombre', y='Puntos', color='Nombre')
st.plotly_chart(fig)
