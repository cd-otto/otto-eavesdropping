import streamlit as st
from sqlalchemy import create_engine
from utils.settings import settings
import pandas as pd


@st.cache_resource
def create_connection():
    # use postgresql+psycopg:// to force psycopg3
    engine = create_engine(f"postgresql+psycopg://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DATABASE}")
    return engine

@st.cache_data
def query_database(query):
    engine = create_connection()
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result