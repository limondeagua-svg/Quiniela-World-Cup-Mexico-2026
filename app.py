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
        [data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 35px !important; }
        .stDataFrame { background-color: #1c1f26; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

archivo = 'quiniela_actualizada_2026.xlsx'

@st.cache_data(ttl=30)
def cargar_datos_acumulados():
    try:
        xl = pd.ExcelFile(archivo)
        resumen = {} 
        total_goles_reales_acumulado = 0
        
        # Configuración: Hoja -> Índice de fila de goles (Fila Excel - 1)
        config_hojas = {
            'FIFA WORLD CUP MEXICO 2026': 75,
            '16os': 19
        }
        
        for hoja, fila_goles in config_hojas.items():
            if hoja not in xl.sheet_names:
                continue
            
            df = pd.read_excel(archivo, sheet_name=hoja, header=None, dtype=str)
            filas, columnas = df.shape
            
            # 1. Goles Reales (Celda GXX -> Columna índice 6)
            if filas > fila_goles and columnas > 6:
                try:
                    valor_g_real = df.iloc[fila_goles, 6]
                    if pd.notna(valor_g_real) and str(valor_g_real).strip() != '':
                        total_goles_reales_acumulado += int(float(valor_g_real))
                except:
                    pass
            
            # 2. Participantes, Puntos y Predicciones
            if filas > 2 and columnas > 7:
                nombres = df.iloc[1, 7:].tolist()
                puntos = df.iloc[2, 7:].tolist()
                
                # Predicciones de goles
                if filas > fila_goles:
                    pred_goles = df.iloc[fila_goles, 7:].tolist()
                else:
                    pred_goles = [0] * len(nombres)
                
                for i in range(len(nombres)):
                    nombre = str(nombres[i]).strip()
                    if nombre == 'nan' or not nombre or nombre == 'None':
                        continue
                    
                    try: pts = int(float(puntos[i]))
                    except: pts = 0
                    
                    try: g_p = int(float(pred_goles[i]))
                    except: g_p = 0
                    
                    if nombre not in resumen:
                        resumen[nombre] = {'Puntos': 0, 'Goles Predichos': 0}
                    
                    resumen[nombre]['Puntos'] += pts
                    resumen[nombre]['Goles Predichos'] += g_p

        # 3. Formatear Ranking Final
        datos_lista = []
        for nombre, valores in resumen.items():
            dif = abs(valores['Goles Predichos'] - total_goles_reales_acumulado)
            datos_lista.append({
                'Participante': nombre,
                'Puntos Totales': valores['Puntos'],
                'Goles Predichos (Suma)': valores['Goles Predichos'],
                'Diferencia Final': dif
            })
            
        df_final = pd.DataFrame(datos_lista)
        if not df_final.empty:
            df_final = df_final.sort_values(by=['Puntos Totales', 'Diferencia Final'], 
                                           ascending=[False, True]).reset_index(drop=True)
            df_final.index += 1
        
        return df_final, total_goles_reales_acumulado

    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
        return pd.DataFrame(), 0

# --- PROCESO ---
df_ranking, goles_reales_total = cargar_datos_acumulados()

if not df_ranking.empty:
    st.title("🏆 RANKING ACUMULADO: GRUPOS + 16avos")
    
    # MÉTRICAS SUPERIORES
    m1, m2, m3 = st.columns(3)
    m1.metric("Goles Reales (Acumulado)", goles_reales_total)
    m2.metric("Puntaje Líder", f"{df_ranking.iloc[0]['Puntos Totales']} pts")
    m3.metric("Total Participantes", len(df_ranking))
    
    st.markdown("---")
    
    # PODIO
    c1, c2, c3 = st.columns(3)
    with c2: # 1RO
        st.markdown(f"""<div class='podium-card' style='border-color:#FFD700;'>🥇 1ER LUGAR<br>
        <b style='font-size:32px;'>{df_ranking.iloc[0]['Participante']}</b><br>
        <span style='font-size:20px; color:#FFD700;'>{df_ranking.iloc[0]['Puntos Totales']} pts</span></div>""", unsafe_allow_html=True)
    with c1: # 2DO
        if len(df_ranking) >= 2:
            st.markdown(f"""<div class='podium-card' style='border-color:#C0C0C0; margin-top:30px;'>🥈 2DO LUGAR<br>
            <b style='font-size:24px;'>{df_ranking.iloc[1]['Participante']}</b><br>
            {df_ranking.iloc[1]['Puntos Totales']} pts</div>""", unsafe_allow_html=True)
    with c3: # 3RO
        if len(df_ranking) >= 3:
            st.markdown(f"""<div class='podium-card' style='border-color:#CD7F32; margin-top:30px;'>🥉 3ER LUGAR<br>
            <b style='font-size:24px;'>{df_ranking.iloc[2]['Participante']}</b><br>
            {df_ranking.iloc[2]['Puntos Totales']} pts</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # TABLA Y GRÁFICA
    col_t, col_g = st.columns([1, 2])
    with col_t:
        st.subheader("📋 Clasificación General")
        st.dataframe(df_ranking[['Participante', 'Puntos Totales', 'Diferencia Final']], use_container_width=True)
        st.caption("Nota: La diferencia se calcula contra la suma de goles reales de ambas fases.")
    
    with col_g:
        st.subheader("📊 Gráfico de Rendimiento")
        # CORRECCIÓN AQUÍ: Usamos una lista de colores válida en lugar de solo 'Gold'
        fig = px.bar(df_ranking, 
                     x='Participante', 
                     y='Puntos Totales', 
                     color='Puntos Totales', 
                     color_continuous_scale=['#4d3d00', '#FFD700', '#FFEA00'], # Escala de marrón a dorado
                     text='Puntos Totales')
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font_color="white",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Sube el archivo Excel actualizado para ver el ranking acumulado.")

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/FIFA_World_Cup_2026_Logo.svg/1200px-FIFA_World_Cup_2026_Logo.svg.png", width=120)
    if st.button("🔄 Refrescar Datos"):
        st.cache_data.clear()
        st.rerun()
