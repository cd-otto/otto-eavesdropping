import json
import streamlit as st
from utils.query import query_database
from utils.oauth import check_auth


def callback():
    st.write("**Callback called**")
    dict = st.session_state['email_df']
    st.code(json.dumps(dict))

def travelers_inspector():
    if not check_auth():
        st.switch_page("pages/main.py")

    st.title("Traveler Inspector")
    st.write("Let's check out all travelers to see what conversations they're having with OTTO.")
    traveler_sql = """
        SELECT email, count(*) as message_count
        FROM checkpoint_thread_view
        GROUP BY 1
        ORDER BY 2 DESC
    """
    try:
        df = query_database(traveler_sql)
        st.dataframe(df, on_select=callback, selection_mode='single-row', key='email_df')
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    travelers_inspector()
