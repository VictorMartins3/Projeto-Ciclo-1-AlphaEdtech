import streamlit as st
import os
from PIL import Image
from dependancies import input_user_cnh
from dependancies import input_user_rg
import sys

# Adicionando o caminho para importação dos módulos do projeto
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

from services.preprocessing import *
from services.ocr_service import *
from services.cnh_detection import cnh_detection
from services.rg_detection import rg_detection


def UploadCNH():
    if "form_submitted" not in st.session_state:
        st.session_state["form_submitted"] = False
    if "ocr_data" not in st.session_state:
        st.session_state["ocr_data"] = None

    st.write(" ")
    st.write(" ")

    with st.form(key="include_cliente_foto"):
        uploaded_file = st.file_uploader("Imagem", type=["jpg", "png"])
        input_button_submit = st.form_submit_button("Enviar")

        if input_button_submit:
            if uploaded_file is not None:
                st.session_state["form_submitted"] = True
                image_bytes = uploaded_file.read()
                image_array = np.frombuffer(image_bytes, dtype=np.uint8)

                imagem_alinhada = preprocess(image_array)
                st.image(imagem_alinhada, caption="Imagem Alinhada")
                ocr_results = ocr(imagem_alinhada)

                try:
                    st.session_state["ocr_data"] = cnh_detection(
                        imagem_alinhada, ocr_results
                    )
                    for key, value in st.session_state["ocr_data"].items():
                        st.write(f"{key}: {value}")
                    st.session_state["show_form"] = (
                        True  # Defina um flag para mostrar o formulário
                    )
                except Exception as e:
                    st.error(f"Erro ao processar CNH: {str(e)}")
                    st.session_state["show_form"] = False
            else:
                st.error(
                    "Nenhum arquivo foi carregado. Por favor, faça upload de um arquivo e tente novamente."
                )
                st.session_state["show_form"] = False

    # Se os dados do OCR estão disponíveis e o flag show_form for True, mostra o formulário
    if st.session_state.get("form_submitted") and st.session_state.get("show_form"):
        filtered_data = {
            key: st.session_state["ocr_data"][key]
            for key in [
                "nome",
                "rg",
                "emissor",
                "uf",
                "cpf",
                "data_nascimento",
                "registro",
                "autenticacao",
            ]
            if key in st.session_state["ocr_data"]
        }
        input_user_cnh(**filtered_data)


def UploadRG():
    st.write(" ")
    st.write(" ")

    with st.form(key="include_cliente_foto"):
        uploaded_file = st.file_uploader("Imagem", type=["jpg", "png"])

        input_button_submit = st.form_submit_button("Enviar")

        if input_button_submit:
            if uploaded_file is not None:
                image_bytes = uploaded_file.read()
                image_array = np.frombuffer(image_bytes, dtype=np.uint8)

                # Carragando a imagem e Alinhando a imagem
                imagem_alinhada = preprocess(image_array)

                # Mostrando a imagem alinhada
                st.image(imagem_alinhada, caption="Imagem Alinhada")

                # Realizando o OCR
                ocr_results = ocr(imagem_alinhada)

                try:
                    dados = cnh_detection(imagem_alinhada, ocr_results)
                except Exception as e:
                    st.write("erro: ", e)

                st.write("Nome: ", dados["nome"])

                st.write("RG: ", dados["rg"])

                st.write("CPF: ", dados["cpf"])

                st.write("Data de Nascimento: ", dados["data de nascimento"])

            else:
                st.error("Nenhum arquivo foi carregado.")

    st.write(" ")
    st.write(" ")

    st.write(
        "Confira seus dados, e caso encontre algum erro por favor corrija antes de enviar."
    )

    # Chamada para função de entrada de dados
    input_user_rg()


def Instrucoes():
    st.subheader("Upload de arquivos")

    st.write(" ")
    st.write(" ")

    st.write(
        """Faça agora o upload do seu documento. Se atente as instruções
        para ter a melhor experiência possível."""
    )

    st.write("""1. Garanta que a foto tenha uma boa qualidade.""")
    st.write("""2. De preferência em um fundo preto.""")
    st.write("""3. Centralize a imagem.""")
    st.write(
        """4. Após a imagem ser processada confirme as informações antes de submeter."""
    )

    image_tutorial = Image.open(r"app/imagens/tutorial.png")
    new_size = (700, 500)
    image = image_tutorial.resize(new_size)
    st.image(image, caption="Exemplo de foto adequada")

    st.write(" ")
    st.write(" ")

    if "selected_document" not in st.session_state:
        st.session_state.selected_document = "Escolha"
    if "upload_mode" not in st.session_state:
        st.session_state.upload_mode = None  # This will control which section to show

    document_options = ["Escolha", "CNH", "RG"]
    selected = st.selectbox(
        "Selecione qual documento você deseja adicionar:",
        document_options,
        index=document_options.index(st.session_state.selected_document),
    )
    st.session_state.selected_document = selected

    if selected == "CNH":
        if st.button("Upload Photo"):
            st.session_state.upload_mode = "upload_photo"
        elif st.button("Manual Input"):
            st.session_state.upload_mode = "manual_input"

    elif selected == "RG":
        st.session_state.upload_mode = "upload_rg"

    # Execute functions based on session state
    if st.session_state.upload_mode == "upload_photo":
        UploadCNH()
    elif st.session_state.upload_mode == "manual_input":
        input_user_cnh()
    elif st.session_state.upload_mode == "upload_rg":
        UploadRG()

    # Reset the upload mode if the user goes back to choose document type
    if st.session_state.selected_document == "Escolha":
        st.session_state.upload_mode = None
