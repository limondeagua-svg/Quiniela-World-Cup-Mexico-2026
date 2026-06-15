import streamlit as st
import pandas as pd

# 1. Configuración
st.set_page_config(layout="wide", page_title="Quiniela Familiar 2026")

# 2. Carga de datos
@st.cache_data(ttl=60) 
def cargar_datos():
    return pd.read_excel('quiniela_actualizada_2026.xlsx', sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)

df = cargar_datos()

# 3. Lógica precisa: Paty empieza en índice 7
# Extraemos nombres desde el índice 7 hasta el 17 (que es donde termina Ivan)
nombres = df.iloc[1, 7:18].tolist()
puntos = df.iloc[2, 7:18].tolist()

datos = []
for i in range(len(nombres)):
    nombre = str(nombres[i])
    try:
        punto = int(float(puntos[i]))
    except:
        punto = 0
    # Agregamos solo si el nombre es válido
    if nombre != 'nan' and nombre != 'nan':
        datos.append({'Participante': nombre, 'Puntos': punto})

df_ranking = pd.DataFrame(datos).sort_values(by='Puntos', ascending=False).reset_index(drop=True)

# 4. Interfaz
st.title("🏆 QUINIELA FAMILIAR - WORLD CUP 2026")
st.write(f"Última vez que se leyó el Excel: {pd.to_datetime('now')}")

if st.button('🔄 Refrescar datos'):
    st.cache_data.clear()
    st.rerun()

st.markdown("---")

# Estilos CSS
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
