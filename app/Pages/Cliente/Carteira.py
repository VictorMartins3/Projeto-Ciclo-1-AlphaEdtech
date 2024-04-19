import streamlit as st

def MostraCarteira():

    st.subheader('Minha carteira')
    
    st.write(" ")
    
    st.write('''Esse é o espaço para você visualizar e gerenciar seus documentos adicionados.''')
    
    st.write(" ")
    
    st.selectbox("Selecione o documento que você deseja visualizar", ["CNH", "RG"])
    