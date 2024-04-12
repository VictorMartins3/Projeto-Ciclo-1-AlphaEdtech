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
        
def insert_user_dados(nome, doc_identidade, org_emissor, uf, cpf, data_nascimento):
    try:
        cursor = conn.cursor()
        
        insert_query = """
            INSERT INTO users_dados (nome, doc_identidade, org_emissor, uf, cpf, data_nascimento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = conn.cursor()
        cursor.execute(insert_query, (nome, doc_identidade, org_emissor, uf, cpf, data_nascimento))

        conn.commit()
        
        cursor.close()

        st.success('Dados inseridos com ssucesso!')
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

def input_dados():                   
    with st.form(key='dados', clear_on_submit=True):
        nome_value = "Luanzeira bananeira"
        cpf_value = "4002-8922"
        st.subheader(':green[Dados]]')
        nome = st.text_input(':blue[Nome]', placeholder='Digite seu Nome Completo', value=nome_value)
        doc_identidade = st.text_input(':blue[Identidade]', placeholder='Digite seu documento da identidade')
        org_emissor = st.text_input(':blue[Órgão Emissor]', placeholder='Digite o órgão emissor')
        uf =  st.text_input(':blue[UF]', placeholder='Digite a UF')
        cpf = st.text_input(':blue[CPF]', placeholder='Digite seu CPF', value=cpf_value)
        min_date = datetime.date(1920, 1, 1)
        data_nascimento = st.date_input('Data de nascimento', value=None, min_value=min_date)
        enviar_dados = st.form_submit_button('Enviar')
        
        if enviar_dados:
            if nome:
                if doc_identidade:
                    if org_emissor:
                        if uf and len(uf) ==2:
                            if cpf:
                                if data_nascimento:
                                    insert_user_dados(nome, doc_identidade, org_emissor, uf, cpf, data_nascimento)
                                else:
                                    st.warning('Insira a data de nascimento')
                            else:
                                st.warning('Insira o CPF')
                        else:
                            st.warning('A UF deve ter dois dígitos.')
                    else:
                        st.warning('Insira o Órgão emissor')
                else:
                    st.warning('Insira a identidade')
            else:
                st.warning('Insira o nome')
                            
            

# Executa a página de cadastro
# sign_up()
