import streamlit as st
from utils.oauth import auth_email, check_auth, login, logout, cookies


def main():
    if not check_auth():
        login()
        st.stop()

    st.title("OTTO Eavesdropping")
    st.write(f"Welcome, {auth_email()}!")
    logout()

if __name__ == "__main__":
    main()
