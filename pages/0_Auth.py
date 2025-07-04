import streamlit as st
from utils import auth

auth.init_db()

st.title("🔐 User Authentication")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if auth.authenticate_user(username, password):
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid credentials")

elif choice == "Register":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Register"):
        if auth.add_user(new_user, new_pass):
            st.success("Account created successfully! Go to Login.")
        else:
            st.warning("Username already exists.")
