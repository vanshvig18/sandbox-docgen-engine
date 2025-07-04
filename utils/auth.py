import psycopg2
import streamlit as st
import hashlib

def get_connection():
    return psycopg2.connect(
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"]
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def create_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        return True
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_pw))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None
