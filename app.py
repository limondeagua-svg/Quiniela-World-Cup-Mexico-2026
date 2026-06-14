import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="wide", page_icon="🏆")

st.title("🏆 Quiniela Familiar - Mundial 2026")
st.markdown("---")

# 2. Carga del archivo Excel
archivo = 'QUINIELA WORLD CUP MEXICO 2026 FINAL.xlsx'

try:
    # Leemos la hoja correspondiente
    df_excel = pd.read_excel(archivo, sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
    
    # 3. EXTRACCIÓN DINÁMICA DE PARTICIPANTES Y PUNTOS
    # Los nombres están en la fila 0 (Fila 1 de Excel), desde la columna 7 (columna H) en adelante
    nombres = df_excel.iloc[0, 7:].dropna().tolist()
    cant_participantes = len(nombres)
    
    # Los puntos acumulados están en la fila 1 (Fila 2 de Excel), justo debajo de los nombres
    puntos = df_excel.iloc[1, 7:7+cant_participantes].tolist()
    
    # Convertimos los puntos a números enteros por si acaso
    puntos = [int(p) if pd.notna(p) else 0 for p in puntos]
    
    # Creamos un DataFrame limpio solo con las posiciones actuales
    df_posiciones = pd.DataFrame({
        'Participante': nombres,
        'Puntos': puntos
    }).sort_values(by='Puntos', ascending=False).reset_index(drop=True)
    
    # 4. LÓGICA DE DETECCIÓN DEL LÍDER (IMPLEMENTACIÓN NUEVA #1)
    id_max = df_posiciones['Puntos'].idxmax()
    lider_actual = df_posiciones.loc[id_max, 'Participante']
    puntos_lider = df_posiciones.loc[id_max, 'Puntos']
    
    # 5. DISEÑO DE INTERFAZ EN STREAMLIT
    
    # Tarjetas de Métricas Destacadas
    st.subheader("📊 Estado del Campeonato")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="👑 Líder de la Quiniela", value=lider_actual)
    with col2:
        st.metric(label="📈 Puntaje Máximo", value=f"{puntos_lider} pts")
    with col3:
        st.metric(label="👥 Participantes Activos", value=cant_participantes)
        
    st.markdown("---")
    
    # Distribución en dos columnas para los Datos y la Gráfica
    col_tabla, col_grafica = st.columns([1, 1.2])
    
    with col_tabla:
        st.subheader("📋 Tabla de Posiciones")
        # Mostramos la tabla limpia y estilizada
        st.dataframe(
            df_posiciones, 
            use_container_width=True,
            column_config={
                "Puntos": st.column_config.NumberColumn("Puntos Totales", format="%d ⭐")
            }
        )
        
    with col_grafica:
        st.subheader("📊 Rendimiento General")
        # Gráfica de barras usando Plotly (IMPLEMENTACIÓN NUEVA #2)
        fig = px.bar(
            df_posiciones, 
            x='Participante', 
            y='Puntos',
            color='Puntos',
            color_continuous_scale='Viridis',
            text='Puntos'
        )
        fig.update_layout(xaxis_title="Jugadores", yaxis_title="Puntos", showlegend=False)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown("---")
    
    # Vista del Excel completo por si quieren verificar sus apuestas individuales
    with st.expander("🔍 Ver Matriz Completa de la Quiniela (Datos del Excel)"):
        # Mostramos el archivo tal cual viene, saltando las primeras filas decorativas si es necesario
        df_completo = pd.read_excel(archivo, sheet_name='FIFA WORLD CUP MEXICO 2026')
        st.dataframe(df_completo)

except FileNotFoundError:
    st.error(f"❌ No se encontró el archivo '{archivo}' en tu repositorio de GitHub. Revisa que el nombre coincida perfectamente.")
except Exception as e:
    st.error(f"⚡ Ocurrió un error al procesar el archivo: {e}")
