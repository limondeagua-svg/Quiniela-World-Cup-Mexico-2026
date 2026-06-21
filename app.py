import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Quiniela World Cup 2026", page_icon="⚽")

# --- ESTILOS CSS ---
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
        h1, h2, h3, h4 { text-align: center; color: #FFD700 !important; }
        [data-testid="stMetricValue"] { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. CARGA DE DATOS (QUINIELA)
@st.cache_data(ttl=60)
def cargar_datos_quiniela():
    try:
        # Cargamos el archivo (Asegúrate que el nombre sea el correcto)
        df = pd.read_excel('quiniela_actualizada_2026.xlsx', sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
        
        # Extracción: Nombres (Fila 2), Puntos (Fila 3), Pred Goles (Fila 76)
        # Desde Columna H (índice 7) en adelante
        nombres = df.iloc[1, 7:].values
        puntos = df.iloc[2, 7:].values
        pred_goles_usuarios = df.iloc[75, 7:].values
        
        # Total Goles Reales: Celda G76
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
                    g_pred = int(float(pred_goles_usuarios[i]))
                except:
                    p, g_pred = 0, 0
                
                # Desempate: Diferencia absoluta
                diferencia = abs(g_pred - goles_reales)
                
                data.append({
                    'Participante': nombre_str, 
                    'Puntos': p, 
                    'Predicción Goles': g_pred,
                    'Diferencia': diferencia
                })
        
        df_res = pd.DataFrame(data)
        # Ranking: 1. Puntos (Desc), 2. Diferencia (Asc)
        df_res = df_res.sort_values(by=['Puntos', 'Diferencia'], ascending=[False, True]).reset_index(drop=True)
        df_res.index += 1
        return df_res, goles_reales
    except Exception as e:
        st.error(f"Error cargando Excel: {e}")
        return pd.DataFrame(), 0

# 3. DATOS DEL CALENDARIO
data_partidos = [
    {"Fecha": "2026-06-11", "Grupo": "A", "Partido": "🇲🇽 México vs 🚩 Por definir", "Sede": "CDMX", "Estadio": "Azteca"},
    {"Fecha": "2026-06-11", "Grupo": "A", "Partido": "🇺🇸 EE.UU. vs 🚩 Por definir", "Sede": "Los Angeles", "Estadio": "SoFi Stadium"},
    {"Fecha": "2026-06-12", "Grupo": "B", "Partido": "🇨🇦 Canadá vs 🚩 Por definir", "Sede": "Toronto", "Estadio": "BMO Field"},
    {"Fecha": "2026-06-12", "Grupo": "B", "Partido": "🇲🇽 México vs 🚩 Por definir", "Sede": "Guadalajara", "Estadio": "Akron"},
    {"Fecha": "2026-07-19", "Grupo": "Final", "Partido": "🏆 GRAN FINAL", "Sede": "Nueva Jersey", "Estadio": "MetLife Stadium"},
]
df_calendario = pd.DataFrame(data_partidos)

# --- PROCESAMIENTO ---
df_ranking, total_goles_reales = cargar_datos_quiniela()

# --- INTERFAZ ---
st.title("🏆 WORLD CUP 2026: OFICIAL RANKING")

# Métrica destacada
st.write(f"### Total Goles Reales (G76): {total_goles_reales}")

# TABS PRINCIPALES
tab1, tab2, tab3, tab4 = st.tabs(["🥇 Ranking", "📅 Calendario", "📊 Estadísticas", "🌍 Sedes"])

# TAB 1: RANKING Y PODIO
with tab1:
    if not df_ranking.empty:
        st.markdown("### Cuadro de Honor")
        c1, c2, c3 = st.columns([1, 1.2, 1])
        
        with c2: # 1er Lugar
            st.markdown(f"""<div class='podium-card gold'><h4>🥇 1ER LUGAR</h4><h2>{df_ranking.iloc[0]['Participante']}</h2><p class='pts'>{df_ranking.iloc[0]['Puntos']} pts</p><p class='tie'>Diferencia: {df_ranking.iloc[0]['Diferencia']}</p></div>""", unsafe_allow_html=True)
        
        with c1: # 2do Lugar
            if len(df_ranking) >= 2:
                st.markdown(f"""<div class='podium-card silver' style='margin-top: 40px;'><h4>🥈 2DO LUGAR</h4><h3>{df_ranking.iloc[1]['Participante']}</h3><p class='pts'>{df_ranking.iloc[1]['Puntos']} pts</p><p class='tie'>Diferencia: {df_ranking.iloc[1]['Diferencia']}</p></div>""", unsafe_allow_html=True)
                
        with c3: # 3er Lugar
            if len(df_ranking) >= 3:
                st.markdown(f"""<div class='podium-card bronze' style='margin-top: 60px;'><h4>🥉 3ER LUGAR</h4><h3>{df_ranking.iloc[2]['Participante']}</h3><p class='pts'>{df_ranking.iloc[2]['Puntos']} pts</p><p class='tie'>Diferencia: {df_ranking.iloc[2]['Diferencia']}</p></div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Tabla Completa")
        st.dataframe(df_ranking, use_container_width=True)
    else:
        st.warning("No hay datos disponibles.")

# TAB 2: CALENDARIO (CON LLAVES ÚNICAS)
with tab2:
    st.subheader("Calendario de Juegos")
    col_a, col_b = st.columns(2)
    with col_a:
        busqueda = st.text_input("🔍 Buscar selección", "")
    with col_b:
        sede_sel = st.selectbox("📍 Seleccionar Sede", ["Todas"] + list(df_calendario['Sede'].unique()))
    
    filtro = df_calendario.copy()
    if busqueda:
        filtro = filtro[filtro['Partido'].str.contains(busqueda, case=False)]
    if sede_sel != "Todas":
        filtro = filtro[filtro['Sede'] == sede_sel]
        
    for idx, row in filtro.iterrows():
        with st.expander(f"{row['Fecha']} | {row['Partido']}"):
            st.write(f"🏟️ **Estadio:** {row['Estadio']} | 📍 **Sede:** {row['Sede']}")
            # Key única usando btn_{idx} para evitar el error DuplicateElementKey
            if st.button("Ver análisis de este partido", key=f"btn_{idx}"):
                st.info(f"Detalles del encuentro {row['Partido']} próximamente.")

# TAB 3: ESTADÍSTICAS
with tab3:
    if not df_ranking.empty:
        st.subheader("Análisis de Puntos")
        fig = px.bar(df_ranking, x='Participante', y='Puntos', color='Puntos', text='Puntos',
                     color_continuous_scale=['#4d3d00', '#FFD700'], template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de Dispersión: Optimismo vs Realidad
        st.subheader("Optimismo vs Diferencia de Goles")
        fig2 = px.scatter(df_ranking, x='Predicción Goles', y='Diferencia', size='Puntos', color='Participante',
                         template="plotly_dark", title="¿Quién se alejó más del total real?")
        st.plotly_chart(fig2, use_container_width=True)

# TAB 4: MUNDIAL INFO
with tab3:
    st.subheader("🌍 Datos de la Copa 2026")
    sedes_map = pd.DataFrame({
        'lat': [19.4326, 20.6597, 25.6866, 25.7617, 40.7128, 34.0522, 43.6532, 49.2827],
        'lon': [-99.1332, -103.3496, -100.3161, -80.1918, -74.0060, -118.2437, -79.3832, -123.1207]
    })
    st.map(sedes_map)
    st.info("El Mundial 2026 contará con 48 equipos y un total de 104 partidos históricos.")

# SIDEBAR
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/FIFA_World_Cup_2026_Logo.svg/1200px-FIFA_World_Cup_2026_Logo.svg.png", width=120)
    if st.button("🔄 Actualizar Datos"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    st.write("**Regla de Desempate:**")
    st.write("1. Mayor Puntaje.")
    st.write("2. Cercanía al total real de goles (Celda G76 vs Predicciones en Fila 76).")
