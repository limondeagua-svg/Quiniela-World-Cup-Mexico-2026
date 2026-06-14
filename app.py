try:
    # Leemos la hoja correspondiente sin procesar encabezados aún
    df_excel = pd.read_excel(archivo, sheet_name='FIFA WORLD CUP MEXICO 2026', header=None)
    
    # 1. BUSCAMOS LA FILA DE LOS NOMBRES
    # Buscamos en qué fila está "Paty" para saber que ahí empiezan los participantes
    fila_nombres = None
    for i in range(len(df_excel)):
        if "Paty" in df_excel.iloc[i].values:
            fila_nombres = i
            break
            
    if fila_nombres is None:
        # Si no encuentra "Paty", usamos la fila 0 por defecto
        fila_nombres = 0

    # Extraemos los nombres limpitos desde la columna H (índice 7)
    fila_nombres_datos = df_excel.iloc[fila_nombres, 7:].dropna().tolist()
    # Limpiamos los nombres por si tienen números como "1/David" -> dejamos solo "David"
    nombres = [str(n).split('/')[-1].strip() for n in fila_nombres_datos if str(n).strip() != '']
    cant_participantes = len(nombres)
    
    # 2. BUSCAMOS LA FILA DE LOS PUNTOS TOTALES
    # Buscamos la fila que está justo debajo de los nombres (fila 2 del excel habitual)
    # Si esa fila contiene los puntos acumulados actuales:
    fila_puntos = fila_nombres + 1
    puntos_raw = df_excel.iloc[fila_puntos, 7:7+cant_participantes].tolist()
    
    # Convertimos a número de forma segura. Si encuentra texto, lo convierte en 0 para que no rompa
    puntos = []
    for p in puntos_raw:
        try:
            puntos.append(int(float(p))) if pd.notna(p) else puntos.append(0)
        except ValueError:
            puntos.append(0) # Si era una palabra como 'Paty', le pone 0 puntos temporalmente
            
    # 3. CREAMOS EL DATAFRAME DE POSICIONES
    df_posiciones = pd.DataFrame({
        'Participante': nombres,
        'Puntos': puntos
    }).sort_values(by='Puntos', ascending=False).reset_index(drop=True)
    
    # 4. LÓGICA DE DETECCIÓN DEL LÍDER
    id_max = df_posiciones['Puntos'].idxmax()
    lider_actual = df_posiciones.loc[id_max, 'Participante']
    puntos_lider = df_posiciones.loc[id_max, 'Puntos']
    
    # 5. DISEÑO DE INTERFAZ EN STREAMLIT
    st.subheader("📊 Estado del Campeonato")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="👑 Líder de la Quiniela", value=lider_actual)
    with col2:
        st.metric(label="📈 Puntaje Máximo", value=f"{puntos_lider} pts")
    with col3:
        st.metric(label="👥 Participantes Activos", value=cant_participantes)
        
    st.markdown("---")
    
    # Distribución de pantallas
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
        
    st.markdown("---")
    
    with st.expander("🔍 Ver Matriz Completa de la Quiniela (Datos del Excel)"):
        df_completo = pd.read_excel(archivo, sheet_name='FIFA WORLD CUP MEXICO 2026')
        st.dataframe(df_completo)

except FileNotFoundError:
    st.error(f"❌ No se encontró el archivo '{archivo}' en tu repositorio de GitHub.")
except Exception as e:
    st.error(f"⚡ Ocurrió un error al procesar el archivo: {e}")
