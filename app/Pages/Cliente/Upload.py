import streamlit as st
import os
from PIL import Image
from dependancies import input_dados
import sys

# Adicionando o caminho para importação dos módulos do projeto
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

from services.preprocessing import *
from services.ocr_service import *
from services.posprocessing import *


def Upload():
    st.subheader("Upload de arquivos")
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

    with st.form(key="include_cliente_foto"):

        input_tipo_documento = st.selectbox("Selecione o documento", ["CNH", "RG"])
        uploaded_file = st.file_uploader("Imagem", type=["jpg", "png"])

        input_button_submit = st.form_submit_button("Enviar")

        if input_button_submit:
            if uploaded_file is not None:
                image_bytes = uploaded_file.read()
                image_array = np.frombuffer(image_bytes, dtype=np.uint8)

                # Carragando a imagem
                image = load_image(image_array)

                # Alinhando a imagem
                imagem_alinhada = align_images(image)

                # Mostrando a imagem alinhada
                st.image(imagem_alinhada, caption="Imagem Alinhada")

                # Realizando o OCR
                ocr_results = ocr(imagem_alinhada)

                # # Mostrar resultado do OCR
                # st.write("Resultado do OCR: ", ocr_results)

                # Verificando a versão da CNH
                cnh_version = verificar_versao_cnh(ocr_results)

                st.write("Versão da CNH: ", cnh_version)

                # Encontrando os pontos chave
                key_points = keypoints(cnh_version)

                # # Mostrar pontos chave
                # st.write("Pontos Chave: ", key_points)

                # Encontrando o nome na imagem
                roi_nome, tp_nome, largura_nome, altura_nome, nome = extract_roi(
                    imagem_alinhada,
                    ocr_results,
                    key_points["nome"],
                    data_type="varchar",
                )

                # Validação do nome
                novo_nome = valida_nome(
                    imagem_alinhada, tp_nome, largura_nome, altura_nome, nome
                )

                st.write("Nome: ", novo_nome)

                # Encontrando o RG na imagem
                roi_rg, tp_rg, largura_rg, altura_rg, rg = extract_roi(
                    imagem_alinhada, ocr_results, key_points["rg"]
                )

                # Validação do RG
                novo_rg = valida_rg(imagem_alinhada, tp_rg, largura_rg, altura_rg, rg)

                st.write("RG: ", novo_rg)

                # Encontrando o CPF na imagem
                roi_cpf, tp_cpf, largura_cpf, altura_cpf, cpf = extract_roi(
                    imagem_alinhada, ocr_results, key_points["cpf"]
                )

                # Validação do CPF
                novo_cpf = valida_cpf(
                    imagem_alinhada, tp_cpf, largura_cpf, altura_cpf, cpf
                )

                st.write("CPF: ", novo_cpf)

            else:
                st.error("Nenhum arquivo foi carregado.")

    st.write(
        "Confira seus dados, e caso encontre algum erro por favor corrija antes de enviar."
    )

    # Chamada para função de entrada de dados
    input_dados()
