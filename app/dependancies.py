import streamlit as st
import psycopg2
import datetime
import re
import bcrypt

def connect_to_postgresql():
    try:
        conn = psycopg2.connect(
            dbname="projeto_test",
            user="postgres",
            password="%Jbkhawbkahgd1",
            host="localhost"
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(f"Erro ao conectar ao banco de dados: {error}")
        return None

conn = connect_to_postgresql()

def insert_user(email, username, password):
    try:
        cursor = conn.cursor()

        date_joined = datetime.datetime.now()

        hashed_password = hash_password(password)

        insert_query = """
            INSERT INTO users (email, username, password, date_joined)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(insert_query, (email, username, hashed_password.decode('utf-8'), date_joined))

        conn.commit()
        
        cursor.close()

        st.success('Conta criada com sucesso!')
        st.balloons()
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(f"Erro ao inserir usuário: {error}")

def fetch_users():
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT email, username, password FROM users")
        users = cursor.fetchall()

        cursor.close()

        user_list = []
        for email, username, password in users:
            user_list.append({'key': email, 'username': username, 'password': password})

        return user_list
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(f"Erro ao buscar usuários: {error}")
        return []

def get_user_emails():
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM users")
        emails = cursor.fetchall()

        cursor.close()

        return [email[0] for email in emails]
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(f"Erro ao obter emails dos usuários: {error}")
        return []

def get_usernames():
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users")
        usernames = cursor.fetchall()

        cursor.close()

        return [username[0] for username in usernames]
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(f"Erro ao obter usernames dos usuários: {error}")
        return []
    
def validate_email(email):
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return re.match(pattern, email)

def validate_username(username):
    pattern = "^[a-zA-Z0-9]*$"
    return re.match(pattern, username)

def validate_password(password):
    return len(password) >= 6

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Cadastrar]')
        email = st.text_input(':blue[Email]', placeholder='Digite seu Email')
        username = st.text_input(':blue[Usuário]', placeholder='Digite seu Nome de Usuário')
        password1 = st.text_input(':blue[Senha]', placeholder='Digite sua Senha', type='password')
        password2 = st.text_input(':blue[Confirmar Senha]', placeholder='Confirme sua Senha', type='password')

        if st.form_submit_button('Cadastrar'):
            if email:
                if validate_email(email):
                    if email not in get_user_emails():
                        if validate_username(username):
                            if username not in get_usernames():
                                if len(username) >= 2:
                                    if len(password1) >= 6:
                                        if password1 == password2:
                                            insert_user(email, username, password1)
                                        else:
                                            st.warning('As senhas não correspondem')
                                    else:
                                        st.warning('A senha é muito curta')
                                else:
                                    st.warning('Nome de usuário muito curto')
                            else:
                                st.warning('Nome de usuário já existe')
                        else:
                            st.warning('Nome de usuário inválido')
                    else:
                        st.warning('Email já cadastrado')
                else:
                    st.warning('Email inválido')

# Executa a página de cadastro
# sign_up()
