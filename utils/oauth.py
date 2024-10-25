
import base64
import json
import os
from dotenv import load_dotenv
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from streamlit_oauth import OAuth2Component


load_dotenv()

CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"

cookies = EncryptedCookieManager(
    prefix="otto_eavesdropping_",
    password=os.environ.get("COOKIE_PASSWORD")
)
if not cookies.ready():
    st.stop()

def check_auth():
    if "auth" not in st.session_state and not ("auth_email" in cookies.keys() and str(cookies["auth_email"])):
        return False
    return True

def auth_email():
    if not check_auth():
        st.stop
    return st.session_state.get("auth", str(cookies["auth_email"]))

def auth_token():
    if not check_auth():
        st.stop
    return st.session_state.get("auth", str(cookies["auth_token"]))

def login():
    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_ENDPOINT, TOKEN_ENDPOINT, TOKEN_ENDPOINT, REVOKE_ENDPOINT)
    result = oauth2.authorize_button(
        name="Continue with Google",
        icon="https://www.google.com.tw/favicon.ico",
        redirect_uri="http://localhost:8501",
        scope="openid email profile",
        key="google",
        extras_params={"prompt": "consent", "access_type": "offline"},
        use_container_width=True,
        pkce='S256',
    )
    
    if result:
        st.write(result)
        # decode the id_token jwt and get the user's email address
        id_token = result["token"]["id_token"]
        # verify the signature is an optional step for security
        payload = id_token.split(".")[1]
        # add padding to the payload if needed
        payload += "=" * (-len(payload) % 4)
        payload = json.loads(base64.b64decode(payload))
        email = payload["email"]
        st.session_state["auth"] = email
        st.session_state["token"] = result["token"]
        cookies["auth_email"] = email  # Save in cookie
        cookies["auth_token"] = result["token"]["access_token"]
        st.rerun()

def logout():
    if not check_auth():
        st.stop()
    if st.button("Logout"):
        # Clear session state and cookies
        if "auth" in st.session_state:
            del st.session_state["auth"]
            del st.session_state["token"]
        cookies["auth_email"] = ""
        cookies["auth_token"] = ""
        st.rerun()