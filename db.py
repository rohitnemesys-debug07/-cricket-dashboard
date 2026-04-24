import psycopg2
import streamlit as st

def get_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            port=5432,
            sslmode="require"
        )
        return conn

    except Exception as e:
        st.error(f"❌ Database Connection Failed: {e}")
        return None