import streamlit as st
from dependancies import verify_user, pull_data, delete_data


def MostraCarteira():

    st.subheader("Minha carteira")

    st.write(" ")

    st.write(
        """Esse é o espaço para você visualizar seus documentos adicionados,
            você também pode atualizar seus dados na página de upload"""
    )

    st.write(" ")

    document_options = ["Escolha", "CNH", "RG"]
    selected = st.selectbox(
        "Selecione o documento que você deseja visualizar", document_options
    )

    dados_rg = ["Nome", "CPF", "RG", "Data de nascimento"]
    dados_cnh = [
        "Nome",
        "CPF",
        "RG",
        "Orgão Emissor",
        "UF",
        "Data de nascimento",
        "Número do registro",
        "Número verifiador",
    ]
    i = 0

    st.write(" ")
    st.write(" ")

    if selected == "CNH":
        if verify_user("cnh"):
            data = pull_data("cnh")[0]
            with st.container(height=350):
                for key, value in data.items():
                    st.write(f"{dados_cnh[i]}: {value}")
                    i += 1
            st.write(" ")
            st.write(" ")

            delete_cnh = st.button(
                "Deletar Documento",
                key="delete cnh",
                help="Ao clicar você irá deletar os dados do documento salvo.",
                type="primary",
            )
            if delete_cnh:
                try:
                    delete_data("cnh")
                    st.success(
                        "Seus dados foram excluídos com sucesso. Por favor recarregue a página."
                    )
                except Exception as e:
                    st.write(f"Erro: {e}")
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
            delete_rg = st.button(
                "Deletar Documento",
                key="delete rg",
                help="Ao clicar você irá deletar os dados do documento salvo.",
                type="primary",
            )
            if delete_rg:
                try:
                    delete_data("rg")
                    st.success(
                        "Seus dados foram excluídos com sucesso. Por favor recarregue a página."
                    )
                except Exception as e:
                    st.write(f"Erro: {e}")
        else:
            st.warning(
                "Você não possui RG cadastrado. Por favor, faça upload do seu RG e tente novamente."
            )
