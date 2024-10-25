import streamlit as st
from utils.oauth import cookies

# import logging
# logging.basicConfig(level=logging.INFO)

pg = st.navigation([
    st.Page("pages/main.py", title="Main", icon="🔥"),
    st.Page("pages/conversations.py", title="Conversation Inspector", icon=":material/favorite:"),
])
pg.run()
