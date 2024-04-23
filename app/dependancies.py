import json
from datetime import datetime
import os
import sys
import psycopg2
import streamlit as st

# Adicionando o caminho para importação dos módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.connection import connect_to_postgresql
from utils.validations import *
from repo.users import get_user_emails, get_usernames, insert_user

# SQL queries:
def insert_user_cnh(json_data):
    conn = connect_to_postgresql()
    if conn:
        try:
            with conn:
                with conn.cursor() as cursor:
                    if not verify_user("cnh"):
                        data = json.loads(json_data)
                        insert_query = """
                            INSERT INTO doc_cnh (name, cpf_number, rg_number, issuing_body, uf, birthdate, registration_number, validator_number, id_user)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(
                            insert_query,
                            (
                                data["name"],
                                data["cpf_number"],
                                data["rg_number"],
                                data["issuing_body"],
                                data["uf"],
                                data["birthdate"],
                                data["registration_number"],
                                data["validator_number"],
                                st.session_state.id_user,
                            ),
                        )
                        st.success("Dados inseridos com sucesso!")
                        st.balloons()
                    else:
                        st.warning(
                            "Você já possui um documento de CNH na sua carteira."
                        )
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao inserir dados: {error}")


def insert_user_rg(json_data):
    conn = connect_to_postgresql()
    if conn:
        try:
            with conn:
                with conn.cursor() as cursor:
                    if not verify_user("rg"):
                        data = json.loads(json_data)
                        insert_query = """
                            INSERT INTO doc_rg (name, rg_number, cpf_number, birthdate, id_user)
                            VALUES (%s, %s, %s, %s, %s)
                        """
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
                        st.success("Dados inseridos com sucesso!")
                        st.balloons()
                    else:
                        st.warning("Você já possui um documento de RG na sua carteira.")
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao inserir dados: {error}")


def update_user_cnh(json_data):
    conn = connect_to_postgresql()
    if conn:
        try:
            with conn:
                with conn.cursor() as cursor:
                    data = json.loads(json_data)
                    update_query = """
                        UPDATE doc_cnh
                        SET name = %s,
                            cpf_number = %s,
                            rg_number = %s,
                            issuing_body = %s,
                            uf = %s,
                            birthdate = %s,
                            registration_number = %s,
                            validator_number = %s
                        WHERE id_user = %s
                    """
                    cursor.execute(
                        update_query,
                        (
                            data["name"],
                            data["cpf_number"],
                            data["rg_number"],
                            data["issuing_body"],
                            data["uf"],
                            data["birthdate"],
                            data["registration_number"],
                            data["validator_number"],
                            st.session_state.id_user,
                        ),
                    )
                    st.success("Dados da CNH atualizados com sucesso!")
                    st.balloons()
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao atualizar dados: {error}")


def update_user_rg(json_data):
    conn = connect_to_postgresql()
    if conn:
        try:
            with conn:
                with conn.cursor() as cursor:
                    data = json.loads(json_data)
                    update_query = """
                        UPDATE doc_rg
                        SET name = %s,
                            cpf_number = %s,
                            birthdate = %s,
                            rg_number = %s
                        WHERE id_user = %s
                    """
                    cursor.execute(
                        update_query,
                        (
                            data["name"],
                            data["cpf_number"],
                            data["birthdate"],
                            data["rg_number"],
                            st.session_state.id_user,
                        ),
                    )
                    st.success("Dados do RG atualizados com sucesso!")
                    st.balloons()
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao atualizar dados: {error}")


def verify_user(doc_type):
    conn = connect_to_postgresql()
    if conn:
        try:
            with conn:
                with conn.cursor() as cursor:
                    query = ""
                    if doc_type == "cnh":
                        query = "SELECT id_user FROM doc_cnh WHERE id_user = %s"
                    elif doc_type == "rg":
                        query = "SELECT id_user FROM doc_rg WHERE id_user = %s"

                    if query:
                        cursor.execute(query, (st.session_state.id_user))
                        return cursor.fetchone() is not None
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao verificar usuário: {error}")
            return False


def pull_data(doc_type):
    conn = (
        connect_to_postgresql()
    )  # Certifique-se de que esta função retorna um objeto de conexão adequado
    data_list = []
    if conn:
        try:
            with conn:
                with conn.cursor() as cursor:
                    # Define a query e os parâmetros com base no tipo de documento
                    if doc_type == "cnh":
                        sql = "SELECT name, cpf_number, rg_number, issuing_body, uf, birthdate, registration_number, validator_number FROM doc_cnh WHERE id_user = %s"
                        params = (st.session_state.id_user,)
                    elif doc_type == "rg":
                        sql = "SELECT name, cpf_number, rg_number, birthdate FROM doc_rg WHERE id_user = %s"
                        params = (st.session_state.id_user,)

                    # Executa a consulta
                    cursor.execute(sql, params)
                    results = cursor.fetchall()

                    # Processa cada linha dos resultados
                    for row in results:
                        data_dict = {
                            desc[0]: value
                            for desc, value in zip(cursor.description, row)
                        }
                        data_list.append(data_dict)

            return data_list
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao buscar dados: {error}")
            return []
        finally:
            conn.close()  # Assegura que a conexão seja fechada após a execução
    else:
        st.error("Falha ao conectar ao banco de dados.")
        return []


def delete_data(doc_type):
    conn = connect_to_postgresql()
    if conn:
        try:
            with conn:
                with conn.cursor() as cursor:
                    if doc_type == "cnh":
                        cursor.execute(
                            "DELETE FROM doc_cnh WHERE id_user = %s",
                            (st.session_state.id_user,),
                        )
                    elif doc_type == "rg":
                        cursor.execute(
                            "DELETE FROM doc_rg WHERE id_user = %s",
                            (st.session_state.id_user,),
                        )

                    conn.commit()
                    return True
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao deletar dados: {error}")
            return False


# Functions app:
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
            data_nascimento = st.text_input(
                ":green_car[Data De nascimento]",
                value=data_nascimento,
                placeholder="DD/MM/YYYY",
                help="Sua data de nascimento.",
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
                                        "issuing_body": org_emissor,
                                        "uf": uf,
                                        "birthdate": postgres_date,
                                        "rg_number": rg,
                                    }
                                    dados_json = json.dumps(dados)
                                    insert_user_cnh(dados_json)
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
            data_nascimento = st.text_input(
                ":green_car[Data De nascimento]",
                value=data_nascimento,
                placeholder="DD/MM/YYYY",
                help="Sua data de nascimento.",
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
                        else:
                            st.warning("Insira a data de nascimento.")
                    else:
                        st.warning("Insira um RG válido.")
                else:
                    st.warning("Insira um CPF válido.")
            else:
                st.warning("Insira um nome válido.")


def input_update_user_cnh(
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

        enviar_dados = st.form_submit_button("Atualizar")
        if enviar_dados:
            if nome and validate_name(nome):
                if numero_validador:
                    if org_emissor:
                        if uf and len(uf) == 2:
                            if cpf and validate_cpf(cpf):
                                if data_nascimento:
                                    dados = {
                                        "name": nome,
                                        "cpf_number": cpf,
                                        "validator_number": numero_validador,
                                        "registration_number": numero_registro,
                                        "issuing_body": org_emissor,
                                        "uf": uf,
                                        "birthdate": data_nascimento,
                                        "rg_number": rg,
                                    }
                                    dados_json = json.dumps(dados)
                                    update_user_cnh(dados_json)
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


def input_update_user_rg(
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

        enviar_dados = st.form_submit_button("Atualizar")
        if enviar_dados:
            if nome and validate_name(nome):
                if cpf and validate_cpf(cpf):
                    if rg:
                        if data_nascimento:
                            dados = {
                                "name": nome,
                                "cpf_number": cpf,
                                "rg_number": rg,
                                "birthdate": data_nascimento,
                            }
                            dados_json = json.dumps(dados)
                            update_user_rg(dados_json)
                        else:
                            st.warning("Insira a data de nascimento.")
                    else:
                        st.warning("Insira um RG válido.")
                else:
                    st.warning("Insira um CPF válido.")
            else:
                st.warning("Insira um nome válido.")
