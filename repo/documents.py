import logging
import streamlit as st
import psycopg2
from datetime import datetime
import os
import sys
import json 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.connection import connect_to_postgresql
from utils.validations import hash_password
from repo.users import verify_user
#Updates:
def update_user_cnh(json_data):
    """
    Updates the driver's license (CNH) information for a user in the database.

    Args:
        json_data (str): A JSON string containing the updated CNH information.

    Returns:
        None
    """
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

                    st.success("CNH data updated successfully!")

                    st.balloons()

        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Error updating data: {error}")


def update_user_rg(json_data):
    """
    Updates the identity card (RG) information for a user in the database.

    Args:
        json_data (str): A JSON string containing the updated RG information.

    Returns:
        None
    """
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

                    st.success("RG data updated successfully!")

                    st.balloons()

        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Error updating data: {error}")

def delete_data(doc_type):
    """
    Deletes a user's document information in the database.

    This function connects to a PostgreSQL database and, depending on the type of document provided,
    deletes the user's document information in the corresponding table.

    Args:
        doc_type (str): The type of the user's document. It should be 'cnh' or 'rg'.

    Returns:
        bool: Returns True if the deletion operation was successful, False otherwise.
    """
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
        
#Inserts:
def insert_user_cnh(json_data):
    """
    Inserts the driver's license (CNH) information for a user into the database if the user doesn't already have a CNH.

    Args:
        json_data (str): A JSON string containing the CNH information to be inserted.

    Returns:
        None
    """
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

                        st.success("Data inserted successfully!")

                        st.balloons()
                    else:
                        st.warning(
                            "You already have a driver's license document in your wallet."
                        )
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Error inserting data: {error}")

def insert_user_rg(json_data):
    """
    Inserts the identity card (RG) information for a user into the database if the user doesn't already have an RG.

    Args:
        json_data (str): A JSON string containing the RG information to be inserted.

    Returns:
        None
    """
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

                        st.success("Data inserted successfully!")

                        st.balloons()
                    else:
                        st.warning("You already have an identity card document in your wallet.")
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Error inserting data: {error}")
