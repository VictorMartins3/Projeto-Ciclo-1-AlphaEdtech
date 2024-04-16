import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up
from dependancies import fetch_users
import os
from Pages.Cliente.Upload import Upload
from Pages.Cliente.Carteira import MostraCarteira
from Pages.Cliente.Inicio import InicioCliente
from Pages.Adm.Administrador import InicioAdministrador

st.set_page_config(page_title='App', page_icon='🐍', initial_sidebar_state='expanded')

with open(r"app\style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    

ms = st.session_state
if "themes" not in ms:
    ms.themes = {
        "current_theme": "dark",
        "refreshed": True,
        "dark": {
            "theme.base": "dark",
            "theme.backgroundColor": "black",
            "theme.primaryColor": "#c98bdb",
            "theme.secondaryBackgroundColor": "#262730",
            "theme.textColor": "white",
            "button_face": "🌜",
        },
        "light": {
            "theme.base": "light",
            "theme.backgroundColor": "white",
            "theme.primaryColor": "#5591f5",
            "theme.secondaryBackgroundColor": "#d4d4d4",
            "theme.textColor": "black",
            "button_face": "🌞",
        },
    }


def ChangeTheme():
    previous_theme = ms.themes["current_theme"]
    tdict = (
        ms.themes["light"]
        if ms.themes["current_theme"] == "light"
        else ms.themes["dark"]
    )
    for vkey, vval in tdict.items():
        if vkey.startswith("theme"):
            st._config.set_option(vkey, vval)

    ms.themes["refreshed"] = False
    if previous_theme == "dark":
        ms.themes["current_theme"] = "light"
    elif previous_theme == "light":
        ms.themes["current_theme"] = "dark"


btn_face = (
    ms.themes["light"]["button_face"]
    if ms.themes["current_theme"] == "light"
    else ms.themes["dark"]["button_face"]
)
st.button(btn_face, on_click=ChangeTheme, key="change_tema")


if ms.themes["refreshed"] == False:
    ms.themes["refreshed"] = True
    st.rerun()

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

    Authenticator = stauth.Authenticate(credentials, cookie_name='App', key='abcdef', cookie_expiry_days=4)

    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')
    
    info, info1 = st.columns(2)
    if not authentication_status:
        alterna = st.toggle('Cadastro')
        if alterna:
            sign_up()


    if username:
        if username in usernames:
            if authentication_status:
                if username == "admin":
                    st.sidebar.subheader('Modo administrador')
                    Authenticator.logout('Sair', 'sidebar')
                    InicioAdministrador()                   
                else:
                    st.sidebar.subheader(f'Bem vindo {username}')
                    with st.sidebar:
                        pagina_selecionada = st.selectbox("Selecione uma página", ["Início", "Upload de arquivos", "Minha carteira"])
                    Authenticator.logout('Sair', 'sidebar')
                    if pagina_selecionada == "Início":
                        InicioCliente()
                    elif pagina_selecionada == "Upload de arquivos":
                        Upload()
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
                st.warning('Usuário ou senha não correspondem.')
except:
    st.success('Atualize a página')
