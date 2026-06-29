import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="Quiniela Familiar 2026 - Acumulado")

# --- ESTILO CSS ---
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
        h1, h2, h3 { color: #FFD700 !important; text-align: center; }
        .stTable { color: white; }
        [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 35px !important; }
    </style>
""", unsafe_allow_html=True)

# 2. CONFIGURACIÓN DE CARGA
archivo = 'quiniela_actualizada_2026.xlsx'
# Lista de pestañas a procesar (puedes agregar más en el futuro)
pestañas_a_sumar = ['FIFA WORLD CUP MEXICO 2026', '16os']

@st.cache_data(ttl=60)
def cargar_datos_acumulados():
    try:
        xl = pd.ExcelFile(archivo)
        resumen = {} # Diccionario para acumular: { 'Nombre': [puntos, goles_pred] }
        total_goles_reales_acumulado = 0
        
        for hoja in pestañas_a_sumar:
            if hoja in xl.sheet_names:
                # Cargar hoja actual
                df = pd.read_excel(archivo, sheet_name=hoja, header=None, dtype=str)
                
                # 1. Extraer Goles Reales (Celda G76 -> Fila 75, Col 6)
                try:
                    g_real = int(float(df.iloc[75, 6]))
                    total_goles_reales_acumulado += g_real
                except:
                    pass # Si no hay datos en G76 de esa hoja, no suma nada

                # 2. Identificar Participantes (Desde Columna H / Índice 7)
                nombres = df.iloc[1, 7:].tolist()
                puntos = df.iloc[2, 7:].tolist()
                pred_goles = df.iloc[75, 7:].tolist() # Fila 76 para predicciones
                
                for i in range(len(nombres)):
                    nombre = str(nombres[i]).strip()
                    if nombre == 'nan' or not nombre:
                        continue
                    
                    # Limpiar Puntos
                    try: pts = int(float(puntos[i]))
                    except: pts = 0
                    
                    # Limpiar Goles Predichos
                    try: g_p = int(float(pred_goles[i]))
                    except: g_p = 0
                    
                    # Acumular en el diccionario
                    if nombre not in resumen:
                        resumen[nombre] = {'Puntos': 0, 'Goles Predichos': 0}
                    
                    resumen[nombre]['Puntos'] += pts
                    resumen[nombre]['Goles Predichos'] += g_p

        # 3. Procesar Ranking final con Desempate
        datos_lista = []
        for nombre, valores in resumen.items():
            dif = abs(valores['Goles Predichos'] - total_goles_reales_acumulado)
            datos_lista.append({
                'Participante': nombre,
                'Puntos Totales': valores['Puntos'],
                'Goles Predichos (Acum)': valores['Goles Predichos'],
                'Diferencia Goles': dif
            })
            
        df_final = pd.DataFrame(datos_lista)
        # Ordenar por Puntos (Desc) y luego por Diferencia (Asc)
        df_final = df_final.sort_values(by=['Puntos Totales', 'Diferencia Goles'], 
                                       ascending=[False, True]).reset_index(drop=True)
        df_final.index += 1
        
        return df_final, total_goles_reales_acumulado

    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
        return pd.DataFrame(), 0

# --- EJECUCIÓN ---
df_ranking, goles_reales_total = cargar_datos_acumulados()

if not df_ranking.empty:
    st.title("🏆 QUINIELA FAMILIAR - ACUMULADO")
    st.markdown("### Fases: Grupos + 16avos")
    
    # MÉTRICA GOLES
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Goles Reales Acumulados (G76)", goles_reales_total)
    col_m2.metric("Líder de la Tabla", df_ranking.iloc[0]['Participante'])
    
    st.markdown("---")
    
    # 3. PODIO
    c1, c2, c3 = st.columns(3)
    # 1er Lugar (Centro) - Cambiamos orden visual para que el 1er lugar destaque al centro
    with c2:
        st.markdown(f"""
            <div class='podium-card' style='border-width: 4px; transform: scale(1.05);'>
                <div style='font-size: 16px; color: #FFD700;'>🥇 1ER LUGAR</div>
                <div style='font-size: 38px; font-weight: bold;'>{df_ranking.iloc[0]['Participante']}</div>
                <div style='font-size: 22px; color: #FFD700;'>{df_ranking.iloc[0]['Puntos Totales']} pts</div>
                <div style='font-size: 14px; color: #888;'>Dif. Goles: {df_ranking.iloc[0]['Diferencia Goles']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # 2do Lugar (Izquierda)
    with c1:
        if len(df_ranking) >= 2:
            st.markdown(f"""
                <div class='podium-card' style='margin-top: 20px;'>
                    <div style='font-size: 14px; color: #C0C0C0;'>🥈 2DO LUGAR</div>
                    <div style='font-size: 28px; font-weight: bold;'>{df_ranking.iloc[1]['Participante']}</div>
                    <div style='font-size: 18px;'>{df_ranking.iloc[1]['Puntos Totales']} pts</div>
                </div>
            """, unsafe_allow_html=True)
    
    # 3er Lugar (Derecha)
    with c3:
        if len(df_ranking) >= 3:
            st.markdown(f"""
                <div class='podium-card' style='margin-top: 20px;'>
                    <div style='font-size: 14px; color: #CD7F32;'>🥉 3ER LUGAR</div>
                    <div style='font-size: 24px; font-weight: bold;'>{df_ranking.iloc[2]['Participante']}</div>
                    <div style='font-size: 18px;'>{df_ranking.iloc[2]['Puntos Totales']} pts</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. TABLA Y GRÁFICA
    col_tab, col_graf = st.columns([1.2, 2])
    
    with col_tab:
        st.subheader("📋 Tabla General")
        st.dataframe(df_ranking, use_container_width=True, hide_index=False)
        st.info("El desempate considera la cercanía al total acumulado de goles reales.")
        
    with col_graf:
        st.subheader("📊 Rendimiento Acumulado")
        fig = px.bar(df_ranking, x='Participante', y='Puntos Totales', 
                     color='Puntos Totales',
                     color_continuous_scale=['#4d3d00', '#FFD700'],
                     text='Puntos Totales')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          font_color="white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.error("No se pudieron cargar los datos. Verifica el archivo Excel y los nombres de las pestañas.")

# BOTÓN REFRESCAR EN SIDEBAR
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/FIFA_World_Cup_2026_Logo.svg/1200px-FIFA_World_Cup_2026_Logo.svg.png", width=150)
    if st.button("🔄 Sincronizar Datos"):
        st.cache_data.clear()
        st.rerun()
