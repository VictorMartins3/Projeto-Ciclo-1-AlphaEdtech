import streamlit as st
from dependancies import verify_user, pull_data

def MostraCarteira():

    st.subheader('Minha carteira')
    
    st.write(" ")
    
    st.write('''Esse é o espaço para você visualizar e gerenciar seus documentos adicionados.''')
    
    st.write(" ")
    
    document_options = ["Escolha", "CNH", "RG"]
    selected = st.selectbox("Selecione o documento que você deseja visualizar", document_options)
    
    if selected == "CNH":
        if verify_user("cnh"):
            data = pull_data("cnh")[0]
            for key, value in data.items():
                st.write(f"{key}: {value}")
        else:
            st.error(
                    "Você não possui CNH cadastrada. Por favor, faça upload de sua CNH e tente novamente."
                )

    elif selected == "RG":
        if verify_user("rg"):
            data = pull_data("rg")[0]
            for key, value in data.items():
                st.write(f"{key}: {value}")
        else:
            st.error(
                    "Você não possui RG cadastrado. Por favor, faça upload do seu RG e tente novamente."
                )