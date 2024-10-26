import os
from dotenv import load_dotenv
import streamlit as st
import logging


load_dotenv()

if os.environ.get("OTTO_ENV") == 'DEV':
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.WARN)

pg = st.navigation([
    st.Page("pages/main.py", title="Main", icon=":material/home:"),
    st.Page("pages/travelers.py", title="Traveler Inspector", icon=":material/detection_and_zone:"),
    st.Page("pages/conversations.py", title="Conversation Inspector", icon=":material/pageview:"),
])
pg.run()
