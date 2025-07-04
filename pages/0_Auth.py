import streamlit as st
from utils.auth import init_db, register_user, login_user

st.title("User Authentication")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

init_db()

if choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.success(f"Welcome {username}")
        else:
            st.error("Invalid credentials")

elif choice == "Register":
    st.subheader("Create Account")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Register"):
        register_user(new_user, new_pass)
        st.success("Account created successfully. Go to Login.")
