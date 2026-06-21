import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="Ranking Mundial 2026", page_icon="🏆")

@st.cache_data(ttl=60)
def cargar_datos():
    try:
        # Cargamos el archivo
        df = pd.read_excel('quiniela_actualizada_2026.xlsx', sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
        
        # --- EXTRACCIÓN SEGÚN TUS COORDENADAS ---
        # Columna H a R es índice 7 a 18 en Python
        nombres = df.iloc[1, 7:18].values
        puntos = df.iloc[2, 7:18].values
        prediccion_goles_usuarios = df.iloc[75, 7:18].values # Fila 76 (índice 75)
        
        # Total Goles Reales: Celda G76 -> Fila 76, Columna G (índice 75, 6)
        try:
            goles_reales = int(float(df.iloc[75, 6]))
        except:
            goles_reales = 0
        
        data = []
        for i in range(len(nombres)):
            nombre_str = str(nombres[i]).strip()
            if nombre_str != 'nan' and nombre_str != '':
                try:
                    p = int(float(puntos[i]))
                    g_pred = int(float(prediccion_goles_usuarios[i]))
                except:
                    p, g_pred = 0, 0
                
                # Criterio de desempate: diferencia absoluta
                diferencia = abs(g_pred - goles_reales)
                
                data.append({
                    'Participante': nombre_str, 
                    'Puntos': p, 
                    'Predicción Goles': g_pred,
                    'Diferencia': diferencia
                })
        
        df_res = pd.DataFrame(data)
        
        # --- LÓGICA DE RANKING ---
        # 1. Puntos (Descendente)
        # 2. Diferencia (Ascendente: el que tiene menos diferencia gana)
        df_res = df_res.sort_values(
            by=['Puntos', 'Diferencia'], 
            ascending=[False, True]
        ).reset_index(drop=True)
        
        df_res.index += 1 # Posición 1, 2, 3...
        return df_res, goles_reales
    except Exception as e:
        st.error(f"Error al procesar el Excel: {e}")
        return pd.DataFrame(), 0

df_ranking, goles_totales_reales = cargar_datos()

# 2. Estilos CSS (Modo Premium)
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; color: white; }
        .podium-card { 
            background: linear-gradient(145deg, #1c1f26, #252932); 
            border: 1px solid #444; padding: 20px; border-radius: 15px; 
            text-align: center; 
        }
        .gold { border-top: 5px solid #FFD700; box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.3); }
        .silver { border-top: 5px solid #C0C0C0; }
        .bronze { border-top: 5px solid #CD7F32; }
        .pts { font-size: 32px; font-weight: bold; color: #FFD700; margin: 0; }
        .tie { font-size: 14px; color: #888; }
        h1, h3 { text-align: center; color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 QUINIELA WORLD CUP 2026")
st.markdown(f"<h3 style='color: white !important;'>Total Goles Reales (G76): {goles_totales_reales}</h3>", unsafe_allow_html=True)

if not df_ranking.empty:
    # 3. Podio (Jerarquía Visual)
    st.markdown("---")
    c1, c2, c3 = st.columns([1, 1.2, 1])
    
    with c2: # 1ero
        st.markdown(f"""<div class='podium-card gold'><h4>🥇 1ER LUGAR</h4><h2>{df_ranking.iloc[0]['Participante']}</h2>
        <p class='pts'>{df_ranking.iloc[0]['Puntos']} pts</p>
        <p class='tie'>Diferencia Goles: {df_ranking.iloc[0]['Diferencia']}</p></div>""", unsafe_allow_html=True)
        
    with c1: # 2do
        if len(df_ranking) >= 2:
            st.markdown(f"""<div class='podium-card silver' style='margin-top: 40px;'><h4>🥈 2DO LUGAR</h4><h3>{df_ranking.iloc[1]['Participante']}</h3>
            <p class='pts'>{df_ranking.iloc[1]['Puntos']} pts</p>
            <p class='tie'>Diferencia: {df_ranking.iloc[1]['Diferencia']}</p></div>""", unsafe_allow_html=True)
            
    with c3: # 3ro
        if len(df_ranking) >= 3:
            st.markdown(f"""<div class='podium-card bronze' style='margin-top: 60px;'><h4>🥉 3ER LUGAR</h4><h3>{df_ranking.iloc[2]['Participante']}</h3>
            <p class='pts'>{df_ranking.iloc[2]['Puntos']} pts</p>
            <p class='tie'>Diferencia: {df_ranking.iloc[2]['Diferencia']}</p></div>""", unsafe_allow_html=True)

    st.markdown("---")

    # 4. Gráfico y Tabla
    col_graf, col_tab = st.columns([2, 1])

    with col_graf:
        st.subheader("📊 Rendimiento por Participante")
        fig = px.bar(df_ranking, x='Participante', y='Puntos', color='Puntos',
                     text='Puntos', color_continuous_scale=['#4d3d00', '#FFD700'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with col_tab:
        st.subheader("📋 Tabla Oficial")
        # Tabla con el desempate visible
        st.dataframe(
            df_ranking[['Participante', 'Puntos', 'Diferencia']], 
            use_container_width=True
        )

# Botón de refresco
if st.sidebar.button('🔄 Actualizar Datos'):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("📌 **Criterio de Desempate:** En caso de empate en puntos, el sistema posiciona mejor a quien tenga la menor diferencia respecto al total de goles reales.")
