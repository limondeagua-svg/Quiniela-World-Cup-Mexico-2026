import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Quiniela Mundial 2026", layout="wide", page_icon="🏆")

# APLICACIÓN DE ESTILO PREMIUM: Fondo negro y letras doradas (Gold & Black Theme)
st.markdown(
    """
    <style>
    /* Fondo principal de la app */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    /* Títulos principales en Dorado */
    h1, h2, h3, .stMarkdown p strong {
        color: #FFD700 !important;
        font-family: 'Georgia', serif;
    }
    /* Estilo personalizado para las tarjetas de métricas */
    .metric-box {
        background-color: #1A1C23;
        border: 2px solid #FFD700;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(255, 215, 0, 0.15);
    }
    .metric-title {
        color: #AAAAAA;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #FFD700;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏆 QUINIELA FAMILIAR - WORLD CUP 2026")
st.markdown("---")

archivo = 'QUINIELA WORLD CUP MEXICO 2026 FINAL.xlsx'

try:
    # Leemos el Excel usando la fila 1 como encabezado
    df_excel = pd.read_excel(archivo, sheet_name='FIFA WORLD CUP MEXICO 2026', header=1)
    
    nombres_finales = []
    puntos_finales = []
    
    # Lista de tus 11 participantes reales
    participantes_reales = ['Paty', 'Fer Marin', 'Armandin', 'Yayo', 'David', 'SAM', 'Yaya', 'JORGE', 'Teté', 'Ivan', 'Brenda']
    
    for col in df_excel.columns:
        if any(p == str(col) for p in participantes_reales):
            nombres_finales.append(str(col))
            valor_puntos = df_excel.loc[0, col]
            puntos_finales.append(int(valor_puntos) if pd.notna(valor_puntos) else 0)

    # 2. Creamos el DataFrame de posiciones ordenadas
    df_posiciones = pd.DataFrame({
        'Participante': nombres_finales,
        'Puntos': puntos_finales
    }).sort_values(by='Puntos', ascending=False).reset_index(drop=True)
    
    # CORRECCIÓN DE LA FOTO 1: Hacer que el índice empiece en 1 en lugar de 0
    df_posiciones.index = df_posiciones.index + 1
    df_posiciones.index.name = 'Lugar'
    
    # Identificamos al líder real desde la posición 1
    lider_actual = df_posiciones.iloc[0]['Participante']
    puntos_lider = df_posiciones.iloc[0]['Puntos']
    cant_participantes = len(df_posiciones)
    
    # 3. INTERFAZ VISUAL EN TARJETAS NEGRAS CON BORDE DORADO
    st.subheader("📊 Estado del Campeonato")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="metric-box"><div class="metric-title">👑 Líder de la Quiniela</div><div class="metric-value">{lider_actual}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box"><div class="metric-title">📈 Puntaje Máximo</div><div class="metric-value">{puntos_lider} pts</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-box"><div class="metric-title">👥 Participantes Activos</div><div class="metric-value">{cant_participantes} Jugadores</div></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Distribución en pantalla (Tabla izquierda, Gráfica derecha)
    col_tabla, col_grafica = st.columns([1, 1.2])
    
    with col_tabla:
        st.subheader("📋 Tabla de Posiciones")
        # Mostramos la tabla con los índices corregidos (1, 2, 3...)
        st.dataframe(
            df_posiciones, 
            use_container_width=True,
            column_config={
                "Puntos": st.column_config.NumberColumn("Aciertos Totales", format="%d ⭐")
            }
        )
        
    with col_grafica:
        st.subheader("📊 Rendimiento General")
        # Gráfica de barras adaptada al nuevo estilo oscuro/dorado
        fig = px.bar(
            df_posiciones.reset_index(), 
            x='Participante', 
            y='Puntos',
            color='Puntos',
            color_continuous_scale=['#4A3B00', '#FFD700'], # Degradado de dorado oscuro a brillante
            text='Puntos'
        )
        fig.update_layout(
            paper_bgcolor='#0E1117',
            plot_bgcolor='#1A1C23',
            font_color='#FFFFFF',
            xaxis_title="Jugadores", 
            yaxis_title="Puntos", 
            showlegend=False
        )
        fig.update_traces(textposition='outside', marker_line_color='#FFD700', marker_line_width=1.5)
        st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error(f"❌ No se encontró el archivo '{archivo}' en tu repositorio de GitHub.")
except Exception as e:
    st.error(f"⚡ Ocurrió un error inesperado: {e}")
