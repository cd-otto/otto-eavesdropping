import json
import logging
import os
import streamlit as st
from utils.query import query_database
from utils.oauth import check_auth


logger = logging.getLogger(__name__)
traveler_list_sql = """
    SELECT email, count(*) as message_count
    FROM checkpoint_thread_view
    GROUP BY 1
    ORDER BY 2 DESC
"""
traveler_threads_sql = """
    SELECT email, title, thread_id, count(*) as message_count
    FROM checkpoint_thread_view
    WHERE email IN ({email_comma_list})
    GROUP BY 1, 2, 3
    ORDER BY 3 DESC
"""

def on_traveler_selected():
    dict = st.session_state['dfTravelers']
    st.session_state['selected_travelers'] = dict['selection']['rows']
    logger.info('traveler selected: %s', st.session_state['selected_travelers'])

def on_thread_selected():
    dict = st.session_state['dfThreads']
    st.session_state['selected_thread'] = dict['selection']['rows'][0]
    logger.info('thread selected: %s', st.session_state['selected_thread'])

def traveler_list():
    try:
        dfTravelers = query_database(traveler_list_sql)
        st.dataframe(dfTravelers, on_select=on_traveler_selected, selection_mode='multi-row', key='dfTravelers')
    except Exception as e:
        st.error(f"An error occurred: {e}")

def selected_traveler_list():
    if 'selected_travelers' not in st.session_state:
        st.write('No traveler selected.')
        st.stop()
    try:
        dfTravelers = query_database(traveler_list_sql)
        emails = []
        for row in st.session_state['selected_travelers']:
            emails.append(dfTravelers.iloc[row]['email'])
        sql = traveler_threads_sql.format(email_comma_list=','.join([f"'{e}'" for e in emails]))
        logger.info(sql)
        dfThreads = query_database(sql)
        if 'selected_thread' in st.session_state:
            row = dfThreads.iloc[st.session_state['selected_thread']]
            st.write(f"Before navigating away, copy this thread_id: {row['thread_id']}")
            if st.button("Open Conversation Inspector"):
                st.switch_page("pages/conversations.py")
            if st.button("Back to selected travelers"):
                del st.session_state['selected_thread']
                st.rerun()
        else:
            st.dataframe(dfThreads, on_select=on_thread_selected, selection_mode='single-row', key='dfThreads')
            if st.button("Back to traveler list"):
                del st.session_state['selected_travelers']
                st.rerun()
    except Exception as e:
        st.error(f"An error occurred: {e}")

def travelers_inspector():
    if not check_auth():
        st.switch_page("pages/main.py")

    st.title("Traveler Inspector")
    st.write("Let's check out all travelers to see what conversations they're having with OTTO.")

    # tab_list, tab_selected = st.tabs(["Traveler List", "Threads of Selected Travelers"])
    if 'selected_travelers' not in st.session_state:
        traveler_list()
    else:
        selected_traveler_list()

travelers_inspector()
