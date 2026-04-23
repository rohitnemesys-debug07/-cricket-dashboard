import psycopg2
import streamlit as st

def get_connection():
    try:
        # Try using Streamlit secrets (for deployment)
        if "DB_HOST" in st.secrets:
            conn = psycopg2.connect(
                host=st.secrets["DB_HOST"],
                database=st.secrets["DB_NAME"],
                user=st.secrets["DB_USER"],
                password=st.secrets["DB_PASSWORD"],
                port=st.secrets.get("DB_PORT", 5432)
            )
        else:
            # Fallback for local development
            conn = psycopg2.connect(
                host="localhost",
                database="cricket_db",
                user="postgres",
                password="1234567",  # ⚠️ change this
                port="5432"
            )

        return conn

    except Exception as e:
        st.error(f"Database Connection Failed: {e}")
        return None

