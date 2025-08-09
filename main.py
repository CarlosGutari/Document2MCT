import streamlit as st
from streamlit_extras.buy_me_a_coffee import button

st.set_page_config(page_title="App Multipágina", page_icon="🌟")

st.title("Bienvenido a la App Multipágina")

st.write("Selecciona una opción para continuar:")

col1, col2 = st.columns(2)

with col1:
    if st.button("Ir a TestMaker"):
        st.switch_page("pages/TestMaker.py")

with col2:
    if st.button("Ir a Upload/Download"):
        st.switch_page("pages/aux.py")
                
button(username="fake-username", floating=True, width=250)