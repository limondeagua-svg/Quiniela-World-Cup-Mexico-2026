import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Quiniela 2026")

# 1. Carga de datos
@st.cache_data(ttl=60)
def cargar_datos():
    # Leemos el archivo
    df = pd.read_excel('quiniela_actualizada_2026.xlsx', sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
    
    # Extraemos nombres (fila 2, cols 7 a 17) y puntos (fila 3, cols 7 a 17)
    nombres = df.iloc[1, 7:18].astype(str).tolist()
    puntos = df.iloc[2, 7:18].tolist()
    
    # Limpiamos datos
    data = []
    for i in range(len(nombres)):
        if nombres[i] != 'nan':
            try:
                p = int(float(puntos[i]))
            except:
                p = 0
            data.append({'Participante': nombres[i], 'Puntos': p})
            
    return pd.DataFrame(data).sort_values(by='Puntos', ascending=False)

df_ranking = cargar_datos()

# 2. Interfaz
st.title("🏆 QUINIELA FAMILIAR - WORLD CUP 2026")

if st.button('🔄 Actualizar Datos'):
    st.cache_data.clear()
    st.rerun()

# 3. Gráfica de Barras
st.subheader("📈 Ranking de Puntos")
fig = px.bar(df_ranking, x='Participante', y='Puntos', color='Puntos', 
             color_continuous_scale='Viridis', text='Puntos')
fig.update_layout(xaxis_title="Participante", yaxis_title="Puntos Totales")
st.plotly_chart(fig, use_container_width=True)

# 4. Tabla
st.subheader("📋 Tabla General")
st.dataframe(df_ranking, use_container_width=True, hide_index=True)
