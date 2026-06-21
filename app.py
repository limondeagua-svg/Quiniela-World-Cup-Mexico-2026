import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="Quiniela & Calendario 2026", page_icon="⚽")

# --- DATA DEL CALENDARIO (Muestra de los partidos inaugurales) ---
# En un escenario real, podrías cargar esto desde un CSV
data_partidos = [
    {"Fecha": "2026-06-11", "Grupo": "A", "Partido": "🇲🇽 México vs 🚩 Por definir", "Sede": "Ciudad de México", "Estadio": "Azteca"},
    {"Fecha": "2026-06-11", "Grupo": "A", "Partido": "🇺🇸 EE.UU. vs 🚩 Por definir", "Sede": "Los Angeles", "Estadio": "SoFi Stadium"},
    {"Fecha": "2026-06-12", "Grupo": "B", "Partido": "🇨🇦 Canadá vs 🚩 Por definir", "Sede": "Toronto", "Estadio": "BMO Field"},
    {"Fecha": "2026-06-12", "Grupo": "B", "Partido": "🇲🇽 México vs 🚩 Por definir", "Sede": "Guadalajara", "Estadio": "Akron"},
    {"Fecha": "2026-07-19", "Grupo": "Final", "Partido": "🏆 FINAL", "Sede": "Nueva Jersey", "Estadio": "MetLife Stadium"},
]
df_calendario = pd.DataFrame(data_partidos)

@st.cache_data(ttl=60)
def cargar_datos_quiniela():
    try:
        df = pd.read_excel('quiniela_actualizada_2026.xlsx', sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
        # Nombres (Fila 2, Col H-R), Puntos (Fila 3, Col H-R), Pred Goles (Fila 76, Col H-R)
        nombres = df.iloc[1, 7:18].values
        puntos = df.iloc[2, 7:18].values
        pred_goles = df.iloc[75, 7:18].values
        goles_reales = int(float(df.iloc[75, 6])) # G76
        
        data = []
        for i in range(len(nombres)):
            n = str(nombres[i]).strip()
            if n != 'nan' and n != '':
                p = int(float(puntos[i])) if pd.notna(puntos[i]) else 0
                g = int(float(pred_goles[i])) if pd.notna(pred_goles[i]) else 0
                data.append({'Participante': n, 'Puntos': p, 'Diferencia': abs(g - goles_reales)})
        
        res = pd.DataFrame(data).sort_values(by=['Puntos', 'Diferencia'], ascending=[False, True]).reset_index(drop=True)
        res.index += 1
        return res, goles_reales
    except:
        return pd.DataFrame(), 0

df_ranking, goles_reales = cargar_datos_quiniela()

# --- INTERFAZ STREAMLIT ---
st.title("🏆 World Cup 2026 Analytics & Quiniela")

# Pestañas principales
tab1, tab2, tab3 = st.tabs(["🥇 Ranking Quiniela", "📅 Calendario de Juegos", "📊 Estadísticas"])

# --- TAB 1: RANKING ---
with tab1:
    st.subheader("Posiciones Actuales")
    c1, c2, c3 = st.columns([1, 1.2, 1])
    if not df_ranking.empty:
        with c2: st.success(f"🥇 **1er Lugar**\n## {df_ranking.iloc[0]['Participante']}\n{df_ranking.iloc[0]['Puntos']} pts")
        st.divider()
        st.dataframe(df_ranking, use_container_width=True)

# --- TAB 2: CALENDARIO INTERACTIVO ---
with tab2:
    st.subheader("📅 Calendario Oficial de Partidos")
    
    # Filtros interactivos
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        search = st.text_input("🔍 Buscar por Equipo (ej. México)", "")
    with col_f2:
        sede_filter = st.selectbox("📍 Filtrar por Sede", ["Todas"] + list(df_calendario['Sede'].unique()))

    # Aplicar Filtros
    df_filtrado = df_calendario.copy()
    if search:
        df_filtrado = df_filtrado[df_filtrado['Partido'].str.contains(search, case=False)]
    if sede_filter != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Sede'] == sede_filter]

    # Mostrar Calendario Estilizado
    if not df_filtrado.empty:
        for _, row in df_filtrado.iterrows():
            with st.expander(f"{row['Fecha']} | {row['Partido']}"):
                c_a, c_b = st.columns(2)
                c_a.write(f"**Estadio:** {row['Estadio']}")
                c_a.write(f"**Sede:** {row['Sede']}")
                c_b.write(f"**Grupo:** {row['Grupo']}")
                if st.button(f"Ver detalles del {row['Partido']}", key=row['Partido']):
                    st.info(f"Aquí puedes añadir datos históricos de los enfrentamientos entre estos equipos.")
    else:
        st.warning("No se encontraron partidos con esos filtros.")

# --- TAB 3: ESTADÍSTICAS ---
with tab3:
    st.subheader("Análisis de la Competencia")
    if not df_ranking.empty:
        fig = px.bar(df_ranking, x='Participante', y='Puntos', color='Puntos', 
                     color_continuous_scale='Gold', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"⚽ **Dato del Mundial:** Se jugarán 104 partidos en total. El total de goles reales capturado en G76 es: {goles_reales}")

# Sidebar
with st.sidebar:
    st.header("Opciones")
    if st.button("🔄 Actualizar Ranking"):
        st.cache_data.clear()
        st.rerun()
    st.write("---")
    st.write("Sedes en 3 países: 🇲🇽 🇺🇸 🇨🇦")
