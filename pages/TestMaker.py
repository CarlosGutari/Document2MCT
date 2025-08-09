import streamlit as st
from streamlit_extras.stylable_container import stylable_container

import random
import numpy as np
import json

# def generate_random_question():
#     questions = [
#         ("What is the capital of France?", ["Paris", "London", "Berlin", "Rome"]),
#         ("Who wrote 'Hamlet'?", ["Shakespeare", "Hemingway", "Tolstoy", "Austen"]),
#         ("What is the largest planet in our solar system?", ["Jupiter", "Earth", "Saturn", "Mars"]),
#         ("Which element has the chemical symbol 'O'?", ["Oxygen", "Gold", "Silver", "Iron"])
#     ]
#     return random.choice(questions)

def generate_file_question(MCTList, nquestions):
    
    indexes = random.sample(range(len(MCTList)), nquestions)
    
    st.session_state.question      = []
    st.session_state.option        = []
    st.session_state.optionshuffle = []
    st.session_state.comment       = []
    st.session_state.answer  = [None for i in range(nquestions)]
    st.session_state.commentbox = [None for i in range(nquestions)]
    
    for i in indexes:
        st.session_state.question.append(MCTList[i]['question'])
        st.session_state.option.append(MCTList[i]['options'])
        st.session_state.optionshuffle.append(random.sample(MCTList[i]['options'], 
                                              len(MCTList[i]['options'])))
        st.session_state.comment.append(MCTList[i]['comments'])
    st.session_state.testON =True 
    
# def turn_on_test_from_random():
#     st.session_state.question = []
#     st.session_state.option = []
#     st.session_state.answer = [None for i in range(nquestions)]
#     for i in range(nquestions):
#         QNO = generate_random_question() 
#         st.session_state.question.append(QNO[0])
#         st.session_state.option.append(QNO[1])
        
#     st.session_state.testON =True

def turn_on_test():    
    if UploadedFiles:
        MCTList = []
        for file in UploadedFiles:
            data = json.load(file)
            MCTList.extend(data)
        if targetnquestions > len(MCTList):
            st.toast(f'Hay menos de {targetnquestions} preguntas en total', icon='😕')
        st.session_state.nquestions = np.min((targetnquestions, len(MCTList)))    
        generate_file_question(MCTList, st.session_state.nquestions)        
    else:
        st.toast('NO ENCUENTRO ARCHIVOS', icon='🧐')
        
def turn_off_test():
    st.session_state.testON = False
    
@st.dialog(" 🚧 AVISO 🚧")
def Cancel_Confirmation():
    st.write("SE BORRARA TODO EL CONTENIDO DEL TEST")
    if st.button("Borrar Todo"):
        turn_off_test()
        st.rerun()    
    
    
st.set_page_config(layout="wide", 
                   page_title="Test Generator", 
                   initial_sidebar_state="expanded")



if 'testON' not in st.session_state:
    st.session_state.testON = False
if 'nquestions' not in st.session_state:
    st.session_state.nquestions = 0

# Sidebar: Logo and file uploaders / list
with st.sidebar:
    
    st.title("⬆️ Sube tu Material:")        
    st.image("logo.png", use_container_width=True)
    UploadedFiles = st.file_uploader("Fuentes de información",
                                     label_visibility = "hidden",
                                     accept_multiple_files=True,
                                     type = "json")
    
    #st.file_uploader("Referencias Extra (Opcional)", accept_multiple_files=True)

# Formulario de Inputs de usuario
with stylable_container(key="green_button",css_styles="button {float:right}"):
    col1, col2 = st.columns(2)
    with col1:
        st.title("⚙️  Configura tu Test :")
    with col2:
        if st.button("Volver al Inicio", 
                     type="primary", 
                     icon="⬅️", 
                     disabled = st.session_state.testON):
            st.switch_page("main.py")
        
with st.container(border = True):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        targetnquestions = st.pills("Cantidad de preguntas:", 
                              [5, 10, 20, 30, 40,  50, 100],
                              default = 10,
                              disabled = st.session_state.testON)
    with col2:  
        correctionON = st.toggle("Mostrar Corrección",
                                 disabled = st.session_state.testON)
        verbose_mode = st.toggle("Añadir Comentario",
                                 disabled = st.session_state.testON or not correctionON)
    with col3:
        timerON      = st.toggle("Temporizador [min / pregunta]",
                                 disabled = st.session_state.testON)
        mperq = st.number_input("Minutos/Pregunta",
                                 label_visibility = "collapsed",
                                 min_value = 0.5,
                                 value = 2.0,
                                 step = 0.5,
                                 max_value = 5.0,
                                 disabled = st.session_state.testON or not timerON)
    with col4:
        generate_button = st.button("Generar Test", 
                                    on_click=turn_on_test,
                                    type="primary",
                                    icon="📖",
                                    disabled = st.session_state.testON)
    with col5:
        cancel_button = st.button("Cancelar", 
                                  on_click=Cancel_Confirmation,
                                  disabled =  not st.session_state.testON,
                                  icon="🚫")
        
def CheckAnswer(index):
    answer = st.session_state.option[index].index(st.session_state.answer[index])
    if answer == 0:
        st.session_state.commentbox[index].write("👍")
    else:
        st.session_state.commentbox[index].write("💔")
    if verbose_mode:
        st.session_state.commentbox[index].write(st.session_state.comment[index][answer])

if st.session_state.testON:    
    with st.container():
        st.title("📝 Responde:")
        st.markdown("***")        
        for i in range(st.session_state.nquestions):
            col1, col2 = st.columns([50,50])
            with col1:
                 st.markdown(f"**P{i+1:02d} - {st.session_state.question[i]}**")
                 st.session_state.answer[i] = st.radio(f"Respuesta {i+1:02d}:", 
                                                       st.session_state.optionshuffle[i], 
                                                       index=None,
                                                       label_visibility = "collapsed")
            with col2:
                st.session_state.commentbox[i] = st.container(border=True)
            if st.session_state.answer[i] is not None:
                if correctionON:
                    CheckAnswer(i)                
            else:
                st.session_state.commentbox[i].write("SIN RESPONDER")
                