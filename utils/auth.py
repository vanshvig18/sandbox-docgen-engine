import psycopg2
from psycopg2 import sql
import bcrypt

# Local DB config
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "vanshvig18"
DB_HOST = "localhost"
DB_PORT = "5432"



def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def register_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
    except psycopg2.Error:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
        return True
    return False
