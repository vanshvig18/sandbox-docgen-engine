import streamlit as st
import psycopg2
import hashlib

# PostgreSQL connection params — update if needed
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
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return True
    except psycopg2.Error:
        return False
    finally:
        cur.close()
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None

# Initialize DB
init_db()

# Streamlit app UI
st.title("Simple Auth App")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

menu = ["Login", "Sign Up"]
choice = st.selectbox("Choose action", menu)

if choice == "Sign Up":
    st.subheader("Create a new account")
    new_user = st.text_input("Username", key="signup_user")
    new_password = st.text_input("Password", type="password", key="signup_pass")
    if st.button("Sign Up"):
        if new_user and new_password:
            success = create_user(new_user, new_password)
            if success:
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists or error occurred.")
        else:
            st.warning("Please enter username and password.")

elif choice == "Login":
    st.subheader("Login to your account")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success(f"Welcome back, {username}!")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Invalid username or password")

if st.session_state.logged_in:
    st.markdown("---")
    st.write(f"Logged in as **{st.session_state.username}**")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()
