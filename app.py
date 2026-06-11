import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="wide")
st.title("🏆 Quiniela World Cup México 2026")
st.markdown("### *Resultados en tiempo real*")
st.write("---")

@st.cache_data
def cargar_y_limpiar_datos():
    archivo_ruta = "QUINIELA WORLD CUP MEXICO 2026 FINAL.xlsx"
    
    # 1. Buscamos la fila de encabezados reales de la familia
    df_crudo = pd.read_excel(archivo_ruta, header=None)
    
    participantes_validos = ['David', 'Teté', 'Paty', 'SAM', 'Yaya', 'Yayo', 'Fer Marin', 'Jorge']
    fila_encabezados = 3  # Por defecto fila 4 (índice 3 en Python)
    
    for idx, fila in df_crudo.head(10).iterrows():
        valores_fila = [str(v).strip().lower() for v in fila.dropna()]
        coincidencias = sum(1 for p in participantes_validos if p.lower() in valores_fila)
        if coincidencias >= 2:
            fila_encabezados = idx
            break
            
    # Leemos el Excel completo desde los títulos reales
    df = pd.read_excel(archivo_ruta, skiprows=fila_encabezados)
    df.columns = df.columns.str.strip()
    
    # 2. Identificamos las columnas de la familia
    familia_real = [col for col in df.columns if any(p.lower() == str(col).lower() for p in participantes_validos)]
    
    # -----------------------------------------------------------------
    # CORTE RADICAL POR NÚMERO DE FILA (Adiós definitivo a la fila 76)
    # -----------------------------------------------------------------
    # Como el Mundial tiene un número fijo de partidos, limitamos el análisis
    # a las primeras 72 filas de datos después de los encabezados.
    # Esto corta el Excel a la altura del último partido y tritura la fila 76, 77 o cualquier nota inferior.
    df = df.iloc[:72].reset_index(drop=True)
    
    # Limpieza final por seguridad en las celdas vacías del bloque de partidos
    if 'LOCAL' in df.columns:
        df = df[df['LOCAL'].notna()]

    puntos_por_persona = []
    
    for integrante in familia_real:
        nombre_bonito = next((p for p in participantes_validos if p.lower() == integrante.lower()), integrante)
        
        if integrante in df.columns:
            # Convertimos la columna a número de forma flexible
            serie_puntos = pd.to_numeric(df[integrante], errors='coerce').fillna(0)
            total_puntos = int(serie_puntos.sum())
            
            puntos_por_persona.append({
                'Participante': nombre_bonito,
                'Puntos': total_puntos
            })
            
    # Creamos la tabla de posiciones finales
    df_posiciones = pd.DataFrame(puntos_por_persona)
    if df_posiciones.empty:
        df_posiciones = pd.DataFrame(columns=['Participante', 'Puntos'])
    else:
        df_posiciones = df_posiciones.sort_values(by='Puntos', ascending=False)
        
    return df_posiciones

try:
    df_posiciones = cargar_y_limpiar_datos()

    if not df_posiciones.empty:
        # 4. Obtener al líder actual
        lider = df_posiciones.iloc[0]['Participante']
        puntos_lider = int(df_posiciones.iloc[0]['Puntos'])

        # 5. Armar la interfaz gráfica
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div style="background-color:#1E1E1E; padding:30px; border-radius:15px; border-left: 10px solid #FFD700; text-align: center;">
                <p style="color:#FFF; margin:0; font-size:18px; letter-spacing: 2px;">🥇 LÍDER ACTUAL</p>
                <h1 style="color:#FFD700; margin:0; font-size:65px; font-weight: bold; text-shadow: 2px 2px 4px #000;">{lider}</h1>
                <p style="color:#FFD700; margin:5px 0 0 0; font-size:24px;">{puntos_lider} Puntos</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.write("🛡️ *Límite estricto de partidos activado: El tablero calcula únicamente las celdas de los partidos oficiales, bloqueando de forma absoluta cualquier dato de desempate inferior.*")

        # 6. Gráfica de barras horizontales interactiva
        with col2:
            fig = px.bar(
                df_posiciones, 
                x='Puntos', 
                y='Participante', 
                orientation='h',
                title="Tabla General de Posiciones de la Familia",
                labels={'Puntos': 'Puntos Totales', 'Participante': 'Familia'},
                color='Puntos',
                color_continuous_scale=px.colors.sequential.YlOrRd
            )
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        # 7. Tabla de posiciones en formato de datos inferior
        st.write("### 📋 Tabla General de Posiciones")
        st.dataframe(df_posiciones, use_container_width=True, hide_index=True)
        
    else:
        st.error("No se pudieron leer los puntajes de las columnas de la familia.")

except Exception as e:
    st.error(f"Ocurrió un inconveniente al procesar el archivo. Detalles: {e}")