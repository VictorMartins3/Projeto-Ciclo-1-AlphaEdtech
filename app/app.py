import streamlit as st
from PIL import Image



st.set_page_config(page_title='Página Inicial', page_icon='🐍', initial_sidebar_state='collapsed')

st.subheader("Cadastramento de CNH e RG online")

st.write('''OCR, ou Reconhecimento Óptico de Caracteres, é uma tecnologia
         revolucionária que transforma letras e números de uma imagem,
         como uma foto de um documento, em texto editável.
         Imagine tirar uma foto de um documento de CNH e, em seguida,
         poder extrair esse texto para um cadastro no seu computador
         como se fosse digitado. Isso é OCR! Ele facilita a extração
         de informações de documentos, tornando o processo de cadastro
         mais rápido e menos propenso a erros. ''')

image = Image.open(r'C:\Users\luanh_g9x\OneDrive\Documents\ocr\projeto_final\app\imagens\exemplo.png')
new_size = (700, 500)
image = image.resize(new_size)
st.image(image, caption='Imagem sobre ocr.')

st.write('''Além da tecnologia da leitura com o OCR, nosso site disponibiza
         o gerenciamento eficiente dessas imagens e os textos, para você
         poder usar sempre que precisar, reunindo todos os seus documentos
         em um só lugar de forma prática. Com a nossa carteira digital,
         lidar com documentos nunca foi tão fácil!''')

st.write(" ")
st.write(" ")
st.write(" ")

col1, col2, col3 = st.columns(3)
col1.subheader('Cadastre-se')
col1.link_button('Cadastro', "Cadastro")
col3.subheader(' Faça Login')
col3.link_button('Login', "Login")
