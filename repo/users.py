import logging
import streamlit as st
import psycopg2
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.connection import connect_to_postgresql
from utils.validations import hash_password

def insert_user(email, username, password):
    conn = connect_to_postgresql()
    if conn is not None:
        try:
            with conn:
                with conn.cursor() as cursor:
                    date_joined = datetime.now()
                    hashed_password = hash_password(password)
                    active = True

                    insert_query = """
                        INSERT INTO users (username, email, password, date_joined, active)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(
                        insert_query,
                        (
                            username,
                            email,
                            hashed_password.decode("utf-8"),
                            date_joined,
                            active,
                        ),
                    )

                st.success("Conta criada com sucesso!")
                st.balloons()
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao inserir usuário: {error}")
            logging.error(f"Database operation failed: {error}")


def search_user_id():
    conn = connect_to_postgresql()
    if conn:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id_user FROM users WHERE username = %s",
                    (st.session_state.user,),
                )
                return cursor.fetchone()
            

def fetch_users():
    conn = connect_to_postgresql()
    if conn is not None:
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT email, username, password FROM users")
                    users = cursor.fetchall()

                    return [
                        {"key": email, "username": username, "password": password}
                        for email, username, password in users
                    ]
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao buscar usuários: {error}")
            return []


def get_user_emails():
    conn = connect_to_postgresql()
    if conn:
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT email FROM users")
                    emails = cursor.fetchall()
                    return [email[0] for email in emails]
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao obter emails dos usuários: {error}")
            return []


def get_usernames():
    conn = connect_to_postgresql()
    if conn:
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT username FROM users")
                    usernames = cursor.fetchall()
                    return [username[0] for username in usernames]
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Erro ao obter usernames dos usuários: {error}")
            return []