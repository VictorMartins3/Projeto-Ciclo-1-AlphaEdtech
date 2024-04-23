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
