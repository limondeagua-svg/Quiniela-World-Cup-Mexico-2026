import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="Quiniela 2026")

# 2. Carga de datos
@st.cache_data(ttl=60)
def cargar_datos():
    df = pd.read_excel('quiniela_actualizada_2026.xlsx', sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
    nombres = df.iloc[1, 7:18].astype(str).tolist()
    puntos = df.iloc[2, 7:18].tolist()
    
    data = []
    for i in range(len(nombres)):
        if nombres[i] != 'nan':
            try:
                p = int(float(puntos[i]))
            except:
                p = 0
            data.append({'Participante': nombres[i], 'Puntos': p})
            
    return pd.DataFrame(data).sort_values(by='Puntos', ascending=False).reset_index(drop=True)

df_ranking = cargar_datos()

# 3. Estilos CSS (Modo oscuro total)
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; color: white; }
        .podium-card { background-color: #1c1f26; border: 2px solid #FFD700; padding: 20px; border-radius: 15px; text-align: center; color: white; margin: 10px; }
        
        /* Ajuste para que la tabla parezca parte del tema oscuro */
        [data-testid="stDataFrame"] {
            border: 1px solid #333;
            background-color: #1c1f26;
        }
        h1, h2, h3 { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

# 4. Interfaz
st.title("🏆 QUINIELA FAMILIAR - WORLD CUP 2026")

if st.button('🔄 Refrescar datos'):
    st.cache_data.clear()
    st.rerun()

# 5. Podio
st.markdown("---")
c1, c2, c3 = st.columns(3)
if len(df_ranking) >= 3:
    c1.markdown(f"<div class='podium-card'>🥈 2DO<br><b>{df_ranking.iloc[1]['Participante']}</b><br>{df_ranking.iloc[1]['Puntos']} pts</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='podium-card'>🥇 1ER<br><b>{df_ranking.iloc[0]['Participante']}</b><br>{df_ranking.iloc[0]['Puntos']} pts</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='podium-card'>🥉 3ER<br><b>{df_ranking.iloc[2]['Participante']}</b><br>{df_ranking.iloc[2]['Puntos']} pts</div>", unsafe_allow_html=True)

st.markdown("---")

# 6. Gráfica (Tonos dorados) y Tabla
col_graf, col_tab = st.columns([2, 1])

with col_graf:
    st.subheader("📈 Ranking de Puntos")
    fig = px.bar(df_ranking, x='Participante', y='Puntos', color='Puntos', 
                 color_continuous_scale=['#FFD700', '#DAA520', '#B8860B'], text='Puntos')
    fig.update_layout(xaxis_title="", yaxis_title="Puntos", paper_bgcolor='rgba(0,0,0,0)', 
                      plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with col_tab:
    st.subheader("📋 Tabla")
    st.dataframe(df_ranking, use_container_width=True, hide_index=True)
