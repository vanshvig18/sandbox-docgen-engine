import streamlit as st
import psycopg2

st.title("🔌 DB Connection Test")

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="vanshvig18",
        host="localhost",
        port="5432"
    )
    st.success("✅ Connected to PostgreSQL successfully!")
    conn.close()
except Exception as e:
    st.error(f"❌ Connection failed:\n\n{e}")
