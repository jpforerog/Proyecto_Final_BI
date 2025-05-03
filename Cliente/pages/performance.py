import streamlit as st
from utils.api_client import get_performance, get_players
import pandas as pd

st.set_page_config(page_title="Rendimiento", layout="wide")

st.title("📊 Módulo de Rendimiento de Jugadores")

if st.button("← Volver al Inicio"):
    st.switch_page("home.py")
    st.rerun()

# Contenido existente
jugadores = get_players()
jugador_seleccionado = st.selectbox("Selecciona un jugador", jugadores, index=0)

    # Contenido principal
col1, col2 = st.columns([3, 2])

with col1:
    st.header(f"Rendimiento de {jugador_seleccionado}")
    
    # Obtener datos de rendimiento
    datos = get_performance(jugador_seleccionado)
    
    if datos and datos["partidos"]:
        df = pd.DataFrame(datos["partidos"])
        df["fecha"] = pd.to_datetime(df["fecha"])
        
        # Gráfico de líneas temporal
        st.line_chart(
            df.set_index("fecha")["rendimiento"],
            use_container_width=True,
            height=400
        )
    else:
        st.warning("No se encontraron datos de rendimiento para este jugador")

with col2:
    st.header("Últimos 5 partidos")
    
    if datos and datos["partidos"]:
        # Mostrar tabla con los últimos partidos
        df_recent = df.sort_values("fecha", ascending=False).head(5)
        st.dataframe(
            df_recent,
            column_config={
                "fecha": "Fecha",
                "rendimiento": st.column_config.NumberColumn(
                    "Rendimiento",
                    format="%.2f ⚽"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Métricas rápidas
        avg_rendimiento = df["rendimiento"].mean()
        max_rendimiento = df["rendimiento"].max()
        
        st.metric("Rendimiento Promedio", f"{avg_rendimiento:.2f}")
        st.metric("Mejor Rendimiento", f"{max_rendimiento:.2f}")
    else:
        st.info("No hay partidos recientes para mostrar")

