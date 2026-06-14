import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Quiniela Familiar 2026")

# ESTILO CSS
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; }
        .podium-card {
            background-color: #1c1f26;
            border: 2px solid #FFD700;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 10px;
        }
        h1 { color: #FFD700; text-align: center; }
        .stTable { color: white; }
    </style>
""", unsafe_allow_html=True)

# Nombre del archivo tal como aparece en tu repositorio
archivo = 'quiniela_actualizada_2026.xlsx'

try:
    # Ajustado al nombre real de la hoja encontrada en el archivo: 'FIFA WORLD CUP MEXICO 2026'
    df = pd.read_excel(archivo, sheet_name='FIFA WORLD CUP MEXICO 2026', header=None, dtype=str)
    
    # Ajusta los índices de filas y columnas según la estructura de tu archivo familiar
    nombres = df.iloc[1, 9:].tolist()
    puntos = df.iloc[2, 9:].tolist()
    
    datos = []
    for n, p in zip(nombres, puntos):
        nombre_limpio = str(n).strip()
        punto_limpio = int(p) if str(p).isdigit() else 0
        if nombre_limpio and nombre_limpio != 'nan':
            datos.append({'Participante': nombre_limpio, 'Puntos': punto_limpio})
            
    df_ranking = pd.DataFrame(datos).sort_values(by='Puntos', ascending=False).reset_index(drop=True)
    df_ranking.index += 1

    st.title("🏆 QUINIELA FAMILIAR - WORLD CUP 2026")
    st.markdown("---")
    
    # PODIO JERÁRQUICO
    c1, c2, c3 = st.columns(3)
    
    # 1er Lugar
    c1.markdown(f"""
        <div class='podium-card'>
            <div style='font-size: 14px; color: #FFD700;'>🥇 1ER LUGAR</div>
            <div style='font-size: 35px; font-weight: bold;'>{df_ranking.iloc[0]['Participante']}</div>
            <div style='font-size: 18px;'>{df_ranking.iloc[0]['Puntos']} pts</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2do Lugar
    c2.markdown(f"""
        <div class='podium-card'>
            <div style='font-size: 14px; color: #C0C0C0;'>🥈 2DO LUGAR</div>
            <div style='font-size: 28px; font-weight: bold;'>{df_ranking.iloc[1]['Participante']}</div>
            <div style='font-size: 18px;'>{df_ranking.iloc[1]['Puntos']} pts</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 3er Lugar
    c3.markdown(f"""
        <div class='podium-card'>
            <div style='font-size: 14px; color: #CD7F32;'>🥉 3ER LUGAR</div>
            <div style='font-size: 20px; font-weight: bold;'>{df_ranking.iloc[2]['Participante']}</div>
            <div style='font-size: 18px;'>{df_ranking.iloc[2]['Puntos']} pts</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # TABLA Y GRÁFICA
    col_tab, col_graf = st.columns([1, 2])
    
    with col_tab:
        st.subheader("📋 Tabla de Posiciones")
        st.dataframe(df_ranking.rename(columns={'Puntos': 'Aciertos Totales'}), use_container_width=True, hide_index=True)
        
    with col_graf:
        st.subheader("📊 Rendimiento General")
        fig = px.bar(df_ranking, x='Participante', y='Puntos', color='Puntos',
                     color_continuous_scale=['#4d3d00', '#FFD700'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          font_color="white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar la hoja: {e}")
