import streamlit as st
from utils.settings import settings
import pandas as pd
from sqlalchemy import create_engine
from utils.oauth import check_auth


@st.cache_resource
def create_connection():
    # use postgresql+psycopg:// to force psycopg3
    engine = create_engine(f"postgresql+psycopg://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DATABASE}")
    return engine

def query_database(query):
    engine = create_connection()
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

if not check_auth():
    st.switch_page("pages/main.py")

st.title("Conversation Inspector")
st.write("Let's look at historical conversations between OTTO and customers to help improve precision and quality.")
thread_id = st.text_input("Thread ID", placeholder="like 5248 in https://local.dev.otto-demo.com:3000/trips/5248")
if thread_id:
    if st.button("Get the conversation thread"):
        query = f"SELECT * FROM checkpoint_thread_view WHERE thread_id={thread_id}"
        try:
            data = query_database(query)
            df_grid = data[['message_id', 'input_tokens', 'output_tokens', 'data']]
            user_id = data.iloc[0]['user_id']
            email = data.iloc[0]['email']
            st.write(f'Context: user_id={user_id}, email={email}, thread_id={thread_id}')
            st.write("Thread:")
            st.dataframe(df_grid)
        except Exception as e:
            st.error(f"An error occurred: {e}")
