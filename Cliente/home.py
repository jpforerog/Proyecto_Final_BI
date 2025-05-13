import streamlit as st

if 'page' not in st.session_state:
    st.session_state.page = "home"

st.set_page_config(page_title="Inicio", layout="wide")

st.title("Bienvenido al Sistema de Análisis Deportivo Colombiano ⚽")

col1, col2 = st.columns(2)
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/FCF-Logo-2023.svg/800px-FCF-Logo-2023.svg.png", 
            use_container_width=True)

with col2:
    st.markdown("""
    ## Selecciona el módulo que deseas usar:
    """)
    
    if st.button("📊 Módulo de Rendimiento", help="Ver análisis detallado de rendimiento"):
        st.switch_page("pages/performance.py")
        st.rerun()
        
    if st.button("📈 Módulo de Grupos de jugadores", 
                help="Ver estadísticas avanzadas y comparativas"):
        st.switch_page("pages/stats.py")
        st.rerun()
    
    st.markdown("---")
    st.write("Versión 1.0")

# Navegación
if st.session_state.page == "rendimiento":
    st.switch_page("pages/rendimiento.py")
elif st.session_state.page == "estadisticas":
    st.switch_page("pages/estadisticas.py")