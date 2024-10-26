import streamlit as st
import json
from utils.query import query_database
from utils.oauth import check_auth


def conversation_inspector():
    if not check_auth():
        st.switch_page("pages/main.py")

    st.title("Conversation Inspector")
    st.write("Let's look at historical conversations between OTTO and travelers to help improve precision and quality.")
    thread_id = st.text_input("Thread ID", value=st.query_params.get('thread_id', ""), placeholder="like 5248 in https://local.dev.otto-demo.com:3000/trips/5248")
    if thread_id:
        # if st.button("Get the conversation thread"):
            query = f"SELECT * FROM checkpoint_thread_view WHERE thread_id={thread_id}"
            try:
                df = query_database(query)
                user_id = df.iloc[0]['user_id']
                email = df.iloc[0]['email']
                st.code(f'Context: user_id={user_id}, email={email}, thread_id={thread_id}')
                st.subheader("Thread:")
                for _, row in df.iterrows():
                    msg = json.loads(row['data'])
                    message_type = msg['data']['additional_kwargs'].get('message_type', "")
                    agent_type = msg['data']['additional_kwargs'].get('agent_classification', "")

                    if msg['type'] == 'ai':
                        if agent_type == "Hotels":
                            avatar = ':material/hotel:'
                        elif agent_type == "Flights":
                            avatar = ':material/flight:'
                        else:
                            avatar = ':material/smart_toy:'
                    elif msg['type'] == 'human':
                        if message_type == "silent_prompt":
                            avatar = ':material/mic_off:'
                        else:
                            avatar = ':material/face:'
                    elif msg['type'] == 'function':
                        avatar = ':material/function:'
                    
                    with st.chat_message(name=msg['type'], avatar=avatar):
                        st.write(msg['data']['content'])
                        st.json(msg, expanded=False)
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    conversation_inspector()
