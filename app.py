import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="World Cup 2026 Analytics", page_icon="⚽")

@st.cache_data(ttl=60)
def cargar_datos():
    try:
        df = pd.read_excel('quiniela_actualizada_2026.xlsx', sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
        
        # Extracción (H a R -> índice 7 a 18)
        # Nota: Si tienes más participantes, cambia el 18 por el índice final
        nombres = df.iloc[1, 7:18].values
        puntos = df.iloc[2, 7:18].values
        pred_goles = df.iloc[75, 7:18].values
        
        try:
            goles_reales = int(float(df.iloc[75, 6])) # G76
        except:
            goles_reales = 0
        
        data = []
        for i in range(len(nombres)):
            n = str(nombres[i]).strip()
            if n != 'nan' and n != '':
                p = int(float(puntos[i])) if pd.notna(puntos[i]) else 0
                g = int(float(pred_goles[i])) if pd.notna(pred_goles[i]) else 0
                data.append({
                    'Participante': n, 
                    'Puntos': p, 
                    'Predicción Goles': g,
                    'Diferencia': abs(g - goles_reales)
                })
        
        df_res = pd.DataFrame(data).sort_values(by=['Puntos', 'Diferencia'], ascending=[False, True]).reset_index(drop=True)
        df_res.index += 1
        return df_res, goles_reales
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame(), 0

df_ranking, goles_reales = cargar_datos()

# --- ESTILOS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1c1f26; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    h1, h2, h3 { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/FIFA_World_Cup_2026_Logo.svg/1200px-FIFA_World_Cup_2026_Logo.svg.png", width=150)
    st.title("Panel de Control")
    if st.button('🔄 Sincronizar Excel'):
        st.cache_data.clear()
        st.rerun()
    st.info("Criterio de desempate: Cercanía al total de goles reales del torneo.")

# --- CUERPO PRINCIPAL ---
st.title("🏆 FIFA World Cup 2026 - Analytics Portal")

# MÉTRICAS RÁPIDAS
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Goles Reales (G76)", goles_reales)
with m2:
    st.metric("Líder Actual", df_ranking.iloc[0]['Participante'] if not df_ranking.empty else "N/A")
with m3:
    promedio = round(df_ranking['Puntos'].mean(), 1) if not df_ranking.empty else 0
    st.metric("Promedio de Puntos", promedio)
with m4:
    # Cuenta regresiva simple (Ejemplo: Inauguración 11 de Junio 2026)
    dias_faltantes = (datetime(2026, 6, 11) - datetime.now()).days
    st.metric("Días para el Mundial", dias_faltantes if dias_faltantes > 0 else "¡YA EMPEZÓ!")

# NAVEGACIÓN POR TABS
tab1, tab2, tab3 = st.tabs(["🥇 Ranking General", "📊 Estadísticas Interactivas", "🌍 Info Mundial 2026"])

with tab1:
    st.subheader("Cuadro de Honor")
    # Podio estilizado
    c1, c2, c3 = st.columns([1, 1.2, 1])
    if len(df_ranking) >= 3:
        with c2: # Oro
            st.success(f"🥇 **1er Lugar**\n### {df_ranking.iloc[0]['Participante']}\n**{df_ranking.iloc[0]['Puntos']} pts**")
        with c1: # Plata
            st.info(f"🥈 **2do Lugar**\n### {df_ranking.iloc[1]['Participante']}\n**{df_ranking.iloc[1]['Puntos']} pts**")
        with c3: # Bronce
            st.warning(f"🥉 **3er Lugar**\n### {df_ranking.iloc[2]['Participante']}\n**{df_ranking.iloc[2]['Puntos']} pts**")
    
    st.markdown("---")
    st.dataframe(df_ranking, use_container_width=True)

with tab2:
    st.subheader("Análisis de la Quiniela")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Gráfico de burbujas: Puntos vs Predicción de Goles
        st.write("**¿Quién es más optimista?** (Puntos vs Goles Predichos)")
        fig_scatter = px.scatter(
            df_ranking, x="Predicción Goles", y="Puntos",
            size="Puntos", color="Participante",
            hover_name="Participante", size_max=40,
            template="plotly_dark"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col_b:
        # Gráfico de barras de Desempeño
        st.write("**Distribución de Puntajes**")
        fig_bar = px.bar(
            df_ranking, x="Participante", y="Puntos",
            color="Puntos", color_continuous_scale="Viridis",
            template="plotly_dark"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Estadística Extra: El "Gurú de los Goles"
    guru = df_ranking.sort_values(by="Diferencia").iloc[0]
    st.success(f"🎯 **El Gurú de los Goles:** {guru['Participante']} (Solo {guru['Diferencia']} de diferencia)")

with tab3:
    st.subheader("Datos Curiosos del Mundial 2026")
    exp1 = st.expander("🌍 Sedes y Países")
    exp1.write("""
    - **Países:** México, Estados Unidos y Canadá.
    - **Final:** MetLife Stadium, Nueva Jersey (19 de julio de 2026).
    - **Apertura:** Estadio Azteca (El primer estadio en ser 3 veces mundialista).
    """)
    
    exp2 = st.expander("⚽ Formato del Torneo")
    exp2.write("""
    - **Equipos:** 48 (Por primera vez en la historia).
    - **Partidos:** 104 partidos totales.
    - **Grupos:** 12 grupos de 4 equipos.
    """)
    
    # Mapa interactivo de sedes (Ejemplo simplificado)
    sedes = pd.DataFrame({
        'Sede': ['CDMX', 'Guadalajara', 'Monterrey', 'Miami', 'NY/NJ', 'Los Angeles', 'Toronto', 'Vancouver'],
        'lat': [19.4326, 20.6597, 25.6866, 25.7617, 40.7128, 34.0522, 43.6532, 49.2827],
        'lon': [-99.1332, -103.3496, -100.3161, -80.1918, -74.0060, -118.2437, -79.3832, -123.1207]
    })
    st.write("**Mapa de Sedes Principales**")
    st.map(sedes)
