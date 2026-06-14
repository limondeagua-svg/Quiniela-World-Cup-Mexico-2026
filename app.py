import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="wide", page_icon="🏆")

st.title("🏆 Quiniela Familiar - Mundial 2026")
st.markdown("---")

archivo = 'QUINIELA WORLD CUP MEXICO 2026 FINAL.xlsx'

try:
    # Leemos el Excel usando la fila 1 como encabezado (donde están tus columnas de juego)
    df_excel = pd.read_excel(archivo, sheet_name='FIFA WORLD CUP MEXICO 2026', header=1)
    
    nombres_finales = []
    puntos_finales = []
    
    # Recorremos cada columna del Excel para buscar a tus participantes
    for col in df_excel.columns:
        # Si la columna contiene el nombre de alguien o coincide con tu formato del Excel
        if any(p in str(col) for p in ['David', 'Teté', 'Paty', 'SAM', 'Yaya', 'Yayo', 'Fer Marin', 'Armandin', 'JORGE', 'Ivan', 'Brenda']):
            nombres_finales.append(str(col)) # Guardamos el nombre completo original (ej: "1/David")
            valor_puntos = df_excel.loc[0, col]
            puntos_finales.append(int(valor_puntos) if pd.notna(valor_puntos) else 0)

    # 2. Creamos el DataFrame de posiciones ordenadas
    df_posiciones = pd.DataFrame({
        'Participante': nombres_finales,
        'Puntos': puntos_finales
    }).sort_values(by='Puntos', ascending=False).reset_index(drop=True)
    
    # Identificamos al líder real
    lider_actual = df_posiciones.loc[0, 'Participante']
    puntos_lider = df_posiciones.loc[0, 'Puntos']
    cant_participantes = len(df_posiciones)
    
    # 3. INTERFAZ VISUAL EN STREAMLIT
    st.subheader("📊 Estado del Campeonato")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="👑 Líder de la Quiniela", value=lider_actual)
    with col2:
        st.metric(label="📈 Puntaje Máximo", value=f"{puntos_lider} pts")
    with col3:
        st.metric(label="👥 Participantes Activos", value=f"{cant_participantes} Jugadores")
        
    st.markdown("---")
    
    # Distribución en pantalla (Tabla izquierda, Gráfica derecha)
    col_tabla, col_grafica = st.columns([1, 1.2])
    
    with col_tabla:
        st.subheader("📋 Tabla de Posiciones")
        st.dataframe(
            df_posiciones, 
            use_container_width=True,
            column_config={
                "Puntos": st.column_config.NumberColumn("Aciertos Totales", format="%d ⭐")
            }
        )
        
    with col_grafica:
        st.subheader("📊 Rendimiento General")
        fig = px.bar(
            df_posiciones, 
            x='Participante', 
            y='Puntos',
            color='Puntos',
            color_continuous_scale='Blues',
            text='Puntos'
        )
        fig.update_layout(xaxis_title="Jugadores", yaxis_title="Puntos", showlegend=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error(f"❌ No se encontró el archivo '{archivo}' en tu repositorio de GitHub.")
except Exception as e:
    st.error(f"⚡ Ocurrió un error inesperado: {e}")
