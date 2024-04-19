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
                    st.write('erro: ',e)
                st.write("Versão da CNH: ", dados['versao'])

                st.write("Nome: ", dados['nome'])

                st.write("RG: ", dados['rg'])

                st.write("Emissor: ", dados['emissor'])

                st.write("UF: ", dados['uf'])

                st.write("CPF: ", dados['cpf'])

                st.write("Data de Nascimento: ", dados['data de nascimento'])

                st.write("Nº de Registro: ", dados['registro'])
        
                st.write("Nº de Autenticação: ", dados['numero verificador'])

            else:
                st.error("Nenhum arquivo foi carregado.")
    
    st.write(" ")
    st.write(" ")
    
    st.write(
        "Confira seus dados, e caso encontre algum erro por favor corrija antes de enviar."
    )

    # Chamada para função de entrada de dados
    input_user_cnh()

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
                        dados = rg_detection(imagem_alinhada, ocr_results)
                except Exception as e:
                    st.write('erro: ',e)
                st.write("Nome: ", dados['nome'])

                st.write("RG: ", dados['rg'])

                st.write("CPF: ", dados['cpf'])

                st.write("Data de Nascimento: ", dados['data de nascimento'])

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
            para ter a melhor experiência possível. """
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
    
    tipo_documento = st.selectbox(
                            "Selecione qual documento você deseja adicionar:",
                            ["Escolha", "CNH", "RG"],
                        )
    
    if tipo_documento == "CNH":
        UploadCNH()
    elif tipo_documento == "RG":
        UploadRG()