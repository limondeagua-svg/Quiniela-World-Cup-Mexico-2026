import streamlit as pd
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="wide", page_icon="🏆")

st.title("🏆 Quiniela Familiar - Mundial 2026")
st.markdown("---")

archivo = 'QUINIELA WORLD CUP MEXICO 2026 FINAL.xlsx'

try:
    # Leemos la hoja directo desde la fila de los nombres (Fila 1 del Excel es índice 0)
    df_excel = pd.read_excel(archivo, sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
    
    # Listas para guardar la información limpia
    nombres_limpios = []
    puntos_limpios = []
    
    # Tu Excel tiene los nombres en la fila 0, desde la columna H (índice 7) en adelante
    # Vamos a recorrer las columnas de la 7 a la 31 (las 25 columnas de participantes potenciales)
    for col_idx in range(7, 32):
        nombre_celda = df_excel.iloc[0, col_idx]
        puntos_celda = df_excel.iloc[1, col_idx]
        
        # Si la celda del nombre no está vacía y no dice 'nombre' de relleno
        if pd.notna(nombre_celda) and str(nombre_celda).strip() != '' and 'nombre' not in str(nombre_celda).lower():
            # Limpiamos el nombre por si trae formato "1/David" -> dejamos solo "David"
            nombre_final = str(nombre_celda).split('/')[-1].strip()
            nombres_limpios.append(nombre_final)
            
            # Validamos los puntos de manera segura
            try:
                if pd.notna(puntos_celda):
                    puntos_limpios.append(int(float(puntos_celda)))
                else:
                    puntos_limpios.append(0)
            except ValueError:
                puntos_limpios.append(0) # Si hay texto por error en los puntos, le asigna 0

    # 2. CREAMOS EL DATAFRAME DE POSICIONES
    if len(nombres_limpios) > 0:
        df_posiciones = pd.DataFrame({
            'Participante': nombres_limpios,
            'Puntos': puntos_limpios
        }).sort_values(by='Puntos', ascending=False).reset_index(drop=True)
        
        # Definimos al líder de forma segura
        lider_actual = df_posiciones.loc[0, 'Participante']
        puntos_lider = df_posiciones.loc[0, 'Puntos']
        cant_participantes = len(df_posiciones)
    else:
        # Valores de respaldo por si el Excel viene totalmente vacío
        df_posiciones = pd.DataFrame(columns=['Participante', 'Puntos'])
        lider_actual = "Nadie aún"
        puntos_lider = 0
        cant_participantes = 0
    
    # 3. DISEÑO DE INTERFAZ EN STREAMLIT
    st.subheader("📊 Estado del Campeonato")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="👑 Líder de la Quiniela", value=lider_actual)
    with col2:
        st.metric(label="📈 Puntaje Máximo", value=f"{puntos_lider} pts")
    with col3:
        st.metric(label="👥 Participantes Activos", value=cant_participantes)
        
    st.markdown("---")
    
    # Distribución de pantallas (Tabla a la izquierda, Gráfica a la derecha)
    if cant_participantes > 0:
        col_tabla, col_grafica = st.columns([1, 1.2])
        
        with col_tabla:
            st.subheader("📋 Tabla de Posiciones")
            st.dataframe(
                df_posiciones, 
                use_container_width=True,
                column_config={
                    "Puntos": st.column_config.NumberColumn("Puntos Totales", format="%d ⭐")
                }
            )
            
        with col_grafica:
            st.subheader("📊 Rendimiento General")
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
    else:
        st.warning("⚠️ No se detectaron participantes con el formato correcto en las columnas H a AF de la fila 1.")
        
    st.markdown("---")
    
    with st.expander("🔍 Ver Matriz Completa de la Quiniela (Datos del Excel)"):
        df_completo = pd.read_excel(archivo, sheet_name='FIFA WORLD CUP MEXICO 2026')
        st.dataframe(df_completo)

except FileNotFoundError:
    st.error(f"❌ No se encontró el archivo '{archivo}' en tu repositorio de GitHub.")
except Exception as e:
    st.error(f"⚡ Ocurrió un error al procesar el archivo: {e}")
