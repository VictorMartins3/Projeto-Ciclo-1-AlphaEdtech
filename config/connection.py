import logging
import os

import psycopg2
import streamlit as st

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


def connect_to_postgresql():
    """Create and return a connection to the PostgreSQL database."""
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
        logging.error(f"Failed to connect to the database: {error}")
        st.error(f"Error connecting to the database: {error}")
        return None
