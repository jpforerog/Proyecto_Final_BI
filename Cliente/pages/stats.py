import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from pydantic import BaseModel
from typing import List

# Definición de clases para manejar la respuesta
class RendimientoPartido(BaseModel):
    fecha: str
    rendimiento: float
    
class JugadorCluster(BaseModel):
    jugador_id: str
    partidos: List[RendimientoPartido]
    posiciones: List[str]

# Configuración de la página
st.set_page_config(page_title="Estadísticas", layout="wide")

st.title("📈 Módulo de Estadísticas Avanzadas")

if st.button("← Volver al Inicio"):
    st.switch_page("home.py")
    st.rerun()

# Selectbox y petición GET para obtener los jugadores_ids
st.markdown("### 🔍 Seleccione una categoría para análisis:")
opciones = {
    "1. Defensores Versátiles de Alto Rendimiento": 0.0,
    "2. Mediocampistas Ofensivos Ineficientes": 1.0,
    "3. Extremos Ofensivos con Impacto Moderado": 2.0,
    "4. Mediocampistas Creativos con Rendimiento Limitado": 3.0
}

seleccion = st.selectbox("Categorías disponibles:", list(opciones.keys()))

# Función para mostrar los detalles de un jugador
def mostrar_detalles_jugador(jugador):
    st.subheader(f"📊 {jugador.jugador_id}")

    # Crear columnas para mostrar información básica
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("#### Posiciones")
        for pos in jugador.posiciones:
            st.markdown(f"- {pos}")
    
    # Convertir los últimos 5 partidos a un DataFrame
    ultimos_partidos = jugador.partidos[-5:] if len(jugador.partidos) > 5 else jugador.partidos
    
    datos_partidos = []
    for partido in ultimos_partidos:
        datos_partidos.append({
            "Fecha": partido.fecha,
            "Rendimiento": partido.rendimiento
        })
    
    df_partidos = pd.DataFrame(datos_partidos)
    
    # Mostrar los últimos 5 partidos
    st.write("### Últimos partidos")
    st.dataframe(df_partidos, use_container_width=True)
    
    
    # Estadísticas resumidas
    st.write("### Estadísticas generales")
    
    if jugador.partidos:
        rendimientos_valores = [p.rendimiento for p in jugador.partidos]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Rendimiento promedio", f"{sum(rendimientos_valores)/len(rendimientos_valores):.2f}")
        with col2:
            st.metric("Rendimiento máximo", f"{max(rendimientos_valores):.2f}")
        with col3:
            st.metric("Rendimiento mínimo", f"{min(rendimientos_valores):.2f}")
        with col4:
            st.metric("Partidos analizados", len(jugador.partidos))

# Función para procesar la respuesta y llamar a la API POST
def procesar_respuesta(respuesta_get):
    if respuesta_get.status_code == 200:
        datos = respuesta_get.json()
        jugadores_ids = datos.get("jugadores_ids", [])
        
        if jugadores_ids:
            st.success(f"✅ Datos cargados: {len(jugadores_ids)} jugadores encontrados")
            
            # Realizar la petición POST con los IDs de jugadores
            try:
                url_post = "http://localhost:8000/partidos/grupo/"
                respuesta_post = requests.post(url_post, json={"jugadores_ids": jugadores_ids})
                
                if respuesta_post.status_code == 200:
                    # Procesar la respuesta (lista de JugadorCluster)
                    datos_cluster = respuesta_post.json()
                    
                    # Convertir los datos JSON a objetos JugadorCluster
                    jugadores_cluster = []
                    for jugador_data in datos_cluster:
                        # Convertir partidos a objetos RendimientoPartido
                        partidos = []
                        for partido_data in jugador_data.get("partidos", []):
                            partido = RendimientoPartido(**partido_data)
                            partidos.append(partido)
                        
                        # Crear objeto JugadorCluster
                        jugador = JugadorCluster(
                            jugador_id=jugador_data.get("jugador_id", ""),
                            partidos=partidos,
                            posiciones=jugador_data.get("posiciones", [])
                        )
                        jugadores_cluster.append(jugador)
                    
                    # Vista general de jugadores
                    st.markdown("## Vista general de jugadores")
                    
                    # Crear DataFrame para la tabla general
                    datos_tabla = []
                    for jugador in jugadores_cluster:
                        # Calculamos estadísticas generales
                        rendimientos = [p.rendimiento for p in jugador.partidos]
                        prom_rendimiento = sum(rendimientos) / len(rendimientos) if rendimientos else 0
                        max_rendimiento = max(rendimientos) if rendimientos else 0
                        min_rendimiento = min(rendimientos) if rendimientos else 0
                        
                        datos_tabla.append({
                            "Jugador": jugador.jugador_id,
                            "Posiciones": ", ".join(jugador.posiciones),
                            "Partidos": len(jugador.partidos),
                            "Rend. Promedio": round(prom_rendimiento, 2),
                            "Rend. Máximo": round(max_rendimiento, 2),
                            "Rend. Mínimo": round(min_rendimiento, 2)
                        })
                    
                    df_general = pd.DataFrame(datos_tabla)
                    st.dataframe(df_general, use_container_width=True)
                    
                    # Selector de jugador
                    st.markdown("## Detalles por jugador")
                    jugador_seleccionado = st.selectbox(
                        "Seleccione un jugador para ver detalles:",
                        [jugador.jugador_id for jugador in jugadores_cluster]
                    )
                    
                    # Mostrar detalles del jugador seleccionado
                    if jugador_seleccionado:
                        for jugador in jugadores_cluster:
                            if jugador.jugador_id == jugador_seleccionado:
                                mostrar_detalles_jugador(jugador)
                                break
                else:
                    st.error(f"❌ Error en la petición POST: {respuesta_post.status_code}")
                    if respuesta_post.text:
                        st.code(respuesta_post.text)
            
            except Exception as e:
                st.error(f"⚠️ Error en la petición POST: {str(e)}")
        else:
            st.warning("⚠️ No se encontraron jugadores en este grupo")
    else:
        st.error(f"❌ Error {respuesta_get.status_code} al obtener datos")
        if respuesta_get.text:
            st.code(respuesta_get.text)

# Hacer la petición GET cuando se selecciona una opción
if seleccion:
    grupo_id = opciones[seleccion]
    url_get = f"http://localhost:8000/grupos/{grupo_id}/"
    
    with st.spinner(f"Cargando datos del grupo '{seleccion}'..."):
        try:
            respuesta_get = requests.get(url_get)
            procesar_respuesta(respuesta_get)
        except Exception as e:
            st.error(f"⚠️ Problema de conexión: {str(e)}")