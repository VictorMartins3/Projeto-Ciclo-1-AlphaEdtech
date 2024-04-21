import streamlit as st
import psycopg2
from datetime import datetime
import re
import bcrypt
import os
from dotenv import load_dotenv
import json

# Carregar variaveis do arquivo .env
load_dotenv()


def connect_to_postgresql():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(f"Erro ao conectar ao banco de dados: {error}")
        return None

conn = connect_to_postgresql()

def insert_user(email, username, password):
    try:
        cursor = conn.cursor()

        date_joined = datetime.now()

        hashed_password = hash_password(password)

        active = False

        insert_query = """
            INSERT INTO users (username, email, password, date_joined, active)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (username, email, hashed_password.decode("utf-8"), date_joined, active),
        )

        conn.commit()

        cursor.close()

        st.success("Conta criada com sucesso!")
        st.balloons()
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(f"Erro ao inserir usuário: {error}")

def search_user_id():
    cursor = conn.cursor()
    cursor.execute("SELECT id_user FROM users WHERE username = %s", (st.session_state.user,))
    user_id = cursor.fetchone()

    cursor.close()
    return user_id
def insert_user_cnh(json_data):
    try:
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO doc_cnh (name, cpf_number, rg_number, uf, birthdate, registration_number, validator_number, id_user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = json.loads(json_data)

        cursor.execute(
            insert_query,
            (
                data["name"],
                data["cpf_number"],
                data["rg_number"],
                data["uf"],
                data["birthdate"],
                data["registration_number"],
                data["validator_number"],
                st.session_state.id_user,
            ),
        )

        conn.commit()

        cursor.close()
        st.success("Dados inseridos com sucesso!")
        st.balloons()
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(f"Erro ao inserir dados: {error}")


def insert_user_rg(json_data):
    try:
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO doc_rg (name, rg_number, cpf_number, birthdate, id_user)
            VALUES (%s, %s, %s, %s, %s)
        """

        data = json.loads(json_data)

        cursor.execute(
            insert_query,
            (
                data["name"],
                data["rg_number"],
                data["cpf_number"],
                data["birthdate"],
                st.session_state.id_user,
            ),
        )

        conn.commit()

        cursor.close()

        st.success("Dados inseridos com sucesso!")
        st.balloons()
    except (Exception, psycopg2.DatabaseError) as error:
        st.error(f"Erro ao inserir dados: {error}")


def fetch_users():
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT email, username, password FROM users")
        users = cursor.fetchall()

        cursor.close()

        user_list = []
        for email, username, password in users:
            user_list.append({"key": email, "username": username, "password": password})

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

def verify_user(doc):
    cursor = conn.cursor()

    if doc == "cnh":
        cursor.execute("SELECT id_user FROM doc_cnh WHERE id_user = %s", (st.session_state.id_user,))
        usernames = cursor.fetchall()
        cursor.close()
        if usernames:
            return True
        else:
            return False
    elif doc == "rg":
        cursor.execute("SELECT id_user FROM doc_cnh WHERE id_user = %s", (st.session_state.id_user,))
        usernames = cursor.fetchall()
        cursor.close()
        if usernames:
            return True
        else:
            return False
def validate_email(email):
    pattern = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
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


def validate_name(nome):
    if 10 < len(nome) < 100:
        # Verifica se todos os caracteres são letras, espaços ou acentuações
        if all(char.isalpha() or char.isspace() for char in nome):
            return True
    return False


def validate_cpf(cpf: str) -> bool:
    # Verifica a formatação do CPF
    if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação dos dígitos verificadores
    sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False
    return True


def sign_up():
    with st.form(key="signup", clear_on_submit=True):
        st.subheader(":green[Cadastrar]")
        email = st.text_input(":green[Email]", placeholder="Digite seu Email")
        username = st.text_input(
            ":green[Usuário]", placeholder="Digite seu Nome de Usuário"
        )
        password1 = st.text_input(
            ":green[Senha]", placeholder="Digite sua Senha", type="password"
        )
        password2 = st.text_input(
            ":green[Confirmar Senha]", placeholder="Confirme sua Senha", type="password"
        )

        if st.form_submit_button("Cadastrar"):

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
                                            st.warning("As senhas não correspondem")
                                    else:
                                        st.warning("A senha é muito curta")
                                else:
                                    st.warning("Nome de usuário muito curto")
                            else:
                                st.warning("Nome de usuário já existe")
                        else:
                            st.warning("Nome de usuário inválido")
                    else:
                        st.warning("Email já cadastrado")
                else:
                    st.warning("Email inválido")


def input_user_cnh(
    nome=None,
    rg=None,
    emissor=None,
    uf=None,
    cpf=None,
    data_nascimento=None,
    registro=None,
    verificador=None,
):

    with st.form(key="dados", clear_on_submit=True):
        st.subheader(":green_car[Dados CNH]")  # Correção do emoji
        nome = st.text_input(
            ":green_car[Nome]", value=nome, placeholder="Digite seu Nome Completo"
        )
        cpf = st.text_input(
            ":green_car[CPF]",
            value=cpf,
            placeholder="Digite seu CPF",
            help="Exemplo: 123.456.789-10",
        )
        rg = st.text_input(
            ":green_car[RG]",
            value=rg,
            placeholder="Digite seu RG",
            help="Exemplo: 1234567",
        )
        numero_validador = st.text_input(
            ":green_car[Número validador da CNH]",
            value=verificador,
            placeholder="Digite o número validador da CNH",
            help="Números na posição vertical",
        )
        numero_registro = st.text_input(
            ":green_car[Número de Registro da CNH]",
            value=registro,
            placeholder="Digite o número de Registro da CNH",
            help="Número de Registro",
        )
        org_emissor = st.text_input(
            ":green_car[Órgão Emissor]",
            value=emissor,
            placeholder="Digite o órgão emissor",
            help="Exemplo: SSP",
        )
        uf = st.text_input(
            ":green_car[UF]",
            value=uf,
            placeholder="Digite a UF",
            help="Siglas do estado em que a CNH foi emitida.",
        )
        # Alternativa para exibir o calendário
        if data_nascimento != None:
            data_nascimento = st.text_input(
                ":green_car[Data de nascimento]",
                value=data_nascimento,
                placeholder="DD/MM/YYYY",
            )

        else:
            data_nascimento = st.date_input(
                ":green_car[Data de nascimento]", value=None, format="DD/MM/YYYY"
            )

        enviar_dados = st.form_submit_button("Enviar")
        if enviar_dados:
            if nome and validate_name(nome):
                if numero_validador:
                    if org_emissor:
                        if uf and len(uf) == 2:
                            if cpf and validate_cpf(cpf):
                                if data_nascimento:
                                    data_nascimento_obj = datetime.strptime(
                                        data_nascimento, "%d/%m/%Y"
                                    )
                                    postgres_date = data_nascimento_obj.strftime(
                                        "%Y-%m-%d"
                                    )
                                    dados = {
                                        "name": nome,
                                        "cpf_number": cpf,
                                        "validator_number": numero_validador,
                                        "registration_number": numero_registro,
                                        "org_emissor": org_emissor,
                                        "uf": uf,
                                        "birthdate": postgres_date,
                                        "rg_number": rg,
                                    }
                                    dados_json = json.dumps(dados)
                                    insert_user_cnh(dados_json)
                                    st.write(dados)
                                else:
                                    st.warning("Insira a data de nascimento.")
                            else:
                                st.warning("Insira o CPF")
                        else:
                            st.warning("A UF deve ter dois dígitos.")
                    else:
                        st.warning("Insira o Órgão emissor.")
                else:
                    st.warning("Número inválido.")
            else:
                st.warning("Insira um nome válido.")


def input_user_rg(
    nome=None,
    rg=None,
    cpf=None,
    data_nascimento=None,
):

    with st.form(key="dados", clear_on_submit=True):
        st.subheader(":green_car[Dados RG]")
        nome = st.text_input(
            ":green_car[Nome]", value=nome, placeholder="Digite seu Nome Completo"
        )
        rg = st.text_input(
            ":green_car[RG]",
            value=rg,
            placeholder="Digite seu RG",
            help="Exemplo: 1234567",
        )

        cpf = st.text_input(
            ":green_car[CPF]",
            value=cpf,
            placeholder="Digite seu CPF",
            help="Exemplo: 123.456.789-10",
        )

        # Alternativa para exibir o calendário
        if data_nascimento != None:
            data_nascimento = st.text_input(
                ":green_car[Data de nascimento]",
                value=data_nascimento,
                placeholder="DD/MM/YYYY",
            )

        else:
            data_nascimento = st.date_input(
                ":green_car[Data de nascimento]", value=None, format="DD/MM/YYYY"
            )

        enviar_dados = st.form_submit_button("Enviar")
        if enviar_dados:
            if nome and validate_name(nome):
                if cpf and validate_cpf(cpf):
                    if rg:
                        if data_nascimento:
                            data_nascimento_obj = datetime.strptime(
                                data_nascimento, "%d/%m/%Y"
                            )
                            postgres_date = data_nascimento_obj.strftime("%Y-%m-%d")
                            dados = {
                                "name": nome,
                                "cpf_number": cpf,
                                "rg_number": rg,
                                "birthdate": postgres_date,
                            }
                            dados_json = json.dumps(dados)
                            insert_user_rg(dados_json)
                            st.write(dados)
                        else:
                            st.warning("Insira a data de nascimento.")
                    else:
                        st.warning("Insira um RG válido.")
                else:
                    st.warning("Insira um CPF válido.")
            else:
                st.warning("Insira um nome válido.")
