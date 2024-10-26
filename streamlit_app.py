import os
from dotenv import load_dotenv
import streamlit as st
import logging
from pages.conversations import conversation_inspector
from pages.travelers import travelers_inspector
from pages.main import main


load_dotenv()

if os.environ.get("OTTO_ENV") == 'DEV':
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.WARN)

pg = st.navigation([
    st.Page(main, title="Main", icon=":material/home:"),
    st.Page(travelers_inspector, title="Traveler Inspector", icon=":material/detection_and_zone:"),
    st.Page(conversation_inspector, title="Conversation Inspector", icon=":material/pageview:"),
])
pg.run()
