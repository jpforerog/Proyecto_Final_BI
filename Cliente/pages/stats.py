import streamlit as st

st.set_page_config(page_title="Estadísticas", layout="wide")



st.title("📈 Módulo de Estadísticas Avanzadas")

if st.button("← Volver al Inicio"):
    st.switch_page("home.py")
    st.rerun()

st.warning("🚧 Esta sección está en construcción 🚧")
st.image("https://cdn.pixabay.com/photo/2017/06/16/07/26/under-construction-2408061_1280.png",
        use_container_width=True)
