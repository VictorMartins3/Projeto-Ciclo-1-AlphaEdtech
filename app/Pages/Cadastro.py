from dependancies import sign_up
import streamlit as st

st.set_page_config(page_title='Cadastro', page_icon='🐍', initial_sidebar_state='collapsed')

sign_up()

st.subheader("OU")

st.write(" ")

st.link_button('Login', 'Login')