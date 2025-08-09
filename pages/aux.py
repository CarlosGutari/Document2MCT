# -*- coding: utf-8 -*-

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

import json

# Título de la aplicación

st.set_page_config(layout="wide") 



with stylable_container(key="green_button",css_styles="button {float:right}"):
    col1, col2 = st.columns(2)
    with col1:
        st.title("Aplicación para Modificar y Descargar un Archivo JSON")
    with col2:
        if st.button("Volver al Inicio", 
                     type="primary", 
                     icon="⬅️", 
                     disabled = False):
            st.switch_page("main.py")

# Cargar el archivo JSON desde el sistema del usuario
uploaded_file = st.file_uploader("Sube tu archivo JSON", type=["json"])

if uploaded_file is not None:
    # Leer el archivo cargado
    data = json.load(uploaded_file)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Contenido actual del archivo JSON:")
        st.json(data[:])

    data[0]['question'] = "quien ere?"

    with col2:
        st.subheader("Contenido modificado del archivo JSON:")
        st.json(data[:])


    json_string = json.dumps(data, indent=4)
    st.download_button(
        label="Descargar archivo JSON modificado",
        data=json_string,
        file_name="archivo_modificado.json",
        mime="application/json"
    )
