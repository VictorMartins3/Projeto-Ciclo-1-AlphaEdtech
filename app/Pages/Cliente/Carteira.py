import streamlit as st
from dependancies import verify_user, pull_data

def MostraCarteira():

    st.subheader('Minha carteira')
    
    st.write(" ")
    
    st.write('''Esse é o espaço para você visualizar seus documentos adicionados,
            você também pode atualizar seus dados na página de upload''')
    
    st.write(" ")
    
    document_options = ["Escolha", "CNH", "RG"]
    selected = st.selectbox("Selecione o documento que você deseja visualizar", document_options)
    
    dados_rg = ["Nome", "CPF", "RG", "Data de nascimento"]
    dados_cnh = ["Nome", "CPF", "RG", "UF", "Data de nascimento", "Número do registro", "Número verifiador"]
    i = 0
    
    st.write(" ")
    st.write(" ")
    
    if selected == "CNH":
        if verify_user("cnh"):
            data = pull_data("cnh")[0]
            with st.container(height=310):
                for key, value in data.items():
                    st.write(f"{dados_cnh[i]}: {value}")
                    i += 1
        else:
            st.warning(
                    "Você não possui CNH cadastrada. Por favor, faça upload de sua CNH e tente novamente."
                )

    elif selected == "RG":
        if verify_user("rg"):
            data = pull_data("rg")[0]
            with st.container(height=185):
                for key, value in data.items():
                    st.write(f"{dados_rg[i]}: {value}")
                    i += 1
        else:
            st.warning(
                    "Você não possui RG cadastrado. Por favor, faça upload do seu RG e tente novamente."
                )