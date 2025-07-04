import os
import streamlit as st
import psycopg2
import bcrypt

def connect_db():
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="vanshbvig18"
    )
    return conn

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def signup_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cur.fetchone():
        return False
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
    conn.commit()
    cur.close()
    conn.close()
    return True

def login_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=%s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode()):
        return True
    return False
