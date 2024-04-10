import streamlit as st
import streamlit_authenticator as stauth
from dependancies import fetch_users
from PIL import Image
import os
from Pages.Cliente.Upload import UploadFoto
from Pages.Cliente.Carteira import MostraCarteira
from Pages.Cliente.Inicio import InicioCliente

st.set_page_config(page_title='Login', page_icon='🐍', initial_sidebar_state='expanded')

try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}
    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)
    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')
    
    info, info1 = st.columns(2)

    if username:
        if username in usernames:
            if authentication_status:
                st.sidebar.subheader(f'Bem vindo {username}')
                with st.sidebar:
                    pagina_selecionada = st.selectbox("Selecione uma página", ["Início", "Upload de arquivos", "Minha carteira"])
                Authenticator.logout('Sair', 'sidebar')
                if pagina_selecionada == "Início":
                    InicioCliente()
                elif pagina_selecionada == "Upload de arquivos":
                    UploadFoto()
                elif pagina_selecionada == "Minha carteira":
                    MostraCarteira()
            elif not authentication_status:
                with info:
                    st.error('Senha ou usuário incorreto.')
            else:
                with info:
                    st.warning('Por favor, digite suas informações')
        else:
            with info:
                st.warning('Usuário não existe, por favor, cadastre-se')


except:
    st.success('Atualize a página')
