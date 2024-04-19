import streamlit as st

def InicioAdministrador():
    st.subheader("Bem vindo")

    st.write("Essa é a página onde você poderá conferir informações relevantes sobre o sistema.")
    
    option = st.selectbox(
    'Escolha uma informação para conferir',
    ('Número de usuários', 'Inscrições por data')
    )

    