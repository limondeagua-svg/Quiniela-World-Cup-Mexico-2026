import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="Quiniela Familiar 2026")

# 2. Carga de datos robusta
@st.cache_data(ttl=60) 
def cargar_datos():
    # Leemos sin encabezado para detectar manualmente dónde están los nombres
    df = pd.read_excel('quiniela_actualizada_2026.xlsx', sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
    return df

df = cargar_datos()

# 3. Lógica para encontrar los nombres y puntos
# Suponemos que los nombres están en la fila 2 (índice 1)
# y los puntos están en la fila 3 (índice 2)
# Vamos a extraer todas las columnas a partir de la columna I (índice 8)
nombres_raw = df.iloc[1, 8:]
puntos_raw = df.iloc[2, 8:]

datos_procesados = []
for i in range(len(nombres_raw)):
    nombre = str(nombres_raw.iloc[i]).strip()
    puntos = puntos_raw.iloc[i]
    
    # Filtramos para que solo tome nombres válidos (no vacíos, no nulos)
    if nombre and nombre != 'nan' and 'Unnamed' not in nombre:
        try:
            puntos_val = int(float(puntos))
        except:
            puntos_val = 0
        datos_procesados.append({'Participante': nombre, 'Puntos': puntos_val})

df_ranking = pd.DataFrame(datos_procesados).sort_values(by='Puntos', ascending=False).reset_index(drop=True)

# 4. Interfaz
st.title("🏆 QUINIELA FAMILIAR - WORLD CUP 2026")

if st.button('🔄 Refrescar datos de GitHub'):
    st.cache_data.clear()
    st.rerun()

st.markdown("---")

# Estilos
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; }
        .podium-card { background-color: #1c1f26; border: 2px solid #FFD700; padding: 20px; border-radius: 15px; text-align: center; color: white; }
    </style>
""", unsafe_allow_html=True)

# Visualización
c1, c2, c3 = st.columns(3)
if len(df_ranking) >= 3:
    c1.markdown(f"<div class='podium-card'>🥇 1ER<br><b>{df_ranking.iloc[0]['Participante']}</b><br>{df_ranking.iloc[0]['Puntos']} pts</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='podium-card'>🥈 2DO<br><b>{df_ranking.iloc[1]['Participante']}</b><br>{df_ranking.iloc[1]['Puntos']} pts</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='podium-card'>🥉 3ER<br><b>{df_ranking.iloc[2]['Participante']}</b><br>{df_ranking.iloc[2]['Puntos']} pts</div>", unsafe_allow_html=True)

st.subheader("📊 Tabla General")
st.dataframe(df_ranking, use_container_width=True, hide_index=True)
