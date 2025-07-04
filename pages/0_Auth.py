import streamlit as st
from utils.auth import init_db, create_user, authenticate_user

st.set_page_config(page_title="Authentication", page_icon="🔐")
st.title("🔐 User Authentication")

# Initialize DB table
init_db()

# Session state to track user
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user" not in st.session_state:
    st.session_state["user"] = ""

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success(f"✅ Welcome, {username}!")
            st.session_state["authenticated"] = True
            st.session_state["user"] = username
        else:
            st.error("❌ Invalid username or password")

elif choice == "Sign Up":
    st.subheader("Create New Account")
    new_user = st.text_input("New Username")
    new_password = st.text_input("New Password", type='password')
    if st.button("Sign Up"):
        if create_user(new_user, new_password):
            st.success("✅ Account created successfully! Please login.")
        else:
            st.error("⚠️ Username already exists or error occurred.")

# Show logout and protected content if logged in
if st.session_state["authenticated"]:
    st.markdown("---")
    st.success(f"You are logged in as **{st.session_state['user']}**")
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["user"] = ""
        st.experimental_rerun()
