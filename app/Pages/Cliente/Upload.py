import streamlit as st
import os
from PIL import Image

def UploadFoto():
    st.subheader("Upload de arquivos")
    st.write('''Faça agora o upload do seu documento. Se atente as instruções
            para ter a melhor experiência possível. ''')

    st.write('''1. Garanta que a foto tenha uma boa qualidade.''')
    st.write('''2. De preferência em um fundo preto.''')
    st.write('''3. Centralize a imagem.''')
    st.write('''4. Após a imagem ser processada confirme as informações antes de submeter.''')

    image_tutorial = Image.open(r'C:\Users\luanh_g9x\OneDrive\Documents\ocr\projeto_final\app\imagens\tutorial.png')
    new_size = (700, 500)
    image = image_tutorial.resize(new_size)
    st.image(image, caption='Exemplo de foto adequada')


    with st.form(key="include_cliente_foto"):
        input_tipo_documento = st.selectbox("Selecione o documento", ["CNH"])
        file = st.file_uploader('Imagem', type=['jpg', 'png'])
        input_button_submit = st.form_submit_button("Enviar")
        if input_button_submit and input_button_submit is not None:
            bytes_data = file.read()
            image_path = r'C:\Users\luanh_g9x\OneDrive\Documents\ocr\projeto_final\app\imagens\imagens_usuario'
            full_path = os.path.join(image_path, file.name)
            st.success('Arquivo enviado.')
            with open(full_path, "wb") as f:
                f.write(bytes_data)
                
    with st.form(key="include_cliente_informacoes"):
        input_name = st.text_input(label="Insira seu nome")
        input_idade = st.number_input(label="Insira sua idade", format="%d", step=1)
        input_email = st.text_input(label="Insira seu email")
        input_button_submit = st.form_submit_button("Enviar")
        if input_button_submit and input_button_submit is not None:
            bytes_data = file.read()
            image_path = r'C:\Users\luanh_g9x\OneDrive\Documents\ocr\projeto_final\app\imagens\imagens_usuario'
            full_path = os.path.join(image_path, file.name)
            st.success('Arquivo enviado.')
            with open(full_path, "wb") as f:
                f.write(bytes_data)
