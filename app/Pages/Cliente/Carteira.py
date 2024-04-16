import streamlit as st

def MostraCarteira():

    st.subheader('Minha carteira')
    st.write('''Esse é o espaço para você visualizar e gerenaciar seus documentos adicionados.''')
    st.write('''Escolha qual documento você deseja visualizar: ''')
    
    st.selectbox("Selecione o documento que você deseja visualizar", ["CNH", "RG"])
    