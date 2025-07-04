import streamlit as st
from utils.auth import init_db, register_user, login_user

st.set_page_config(page_title="Authentication", page_icon="🔐")
st.title("User Authentication")

init_db()  # ensure table is created

menu = ["Login", "Register"]
choice = st.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid credentials")

elif choice == "Register":
    st.subheader("Register")
    new_user = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Register"):
        try:
            register_user(new_user, new_password)
            st.success("Registration successful. Go to Login.")
        except:
            st.error("Username already exists")
