import psycopg2
import streamlit as st

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="cricket_db",
            user="postgres",
            password="1234567",  # ⚠️ replace
            port="5432"
        )
        return conn

    except Exception as e:
        st.error(f"Database Connection Failed: {e}")
        return None
