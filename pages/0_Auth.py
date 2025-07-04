import streamlit as st
from utils.auth import authenticate_user, create_user, init_db

st.set_page_config(page_title="Authentication", page_icon="🔐")
st.title("User Authentication")

# Initialize the PostgreSQL DB (optional if table is already created)
init_db()

# Sidebar menu
menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if authenticate_user(username, password):
            st.success(f"Welcome, {username}!")
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
        else:
            st.error("Invalid credentials")

elif choice == "Sign Up":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')

    if st.button("Sign Up"):
        if create_user(new_user, new_password):
            st.success("Account created successfully!")
        else:
            st.error("Username already exists or error occurred.")
