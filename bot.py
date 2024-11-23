import time
from openai import OpenAI
import streamlit as st

# global variables
client = OpenAI(
    organization="org-OLj35i3NXxpSuuOGH1a1HxNm",
    project="proj_GB1WRZh96Njv1a7nASGFgcZT")

assistant_id = "asst_81TxmQ0vUYW0zxBLYaBoXSf8"

# initialize a conversation thread and store its ID in session
def thread_init():
    thread = client.beta.threads.create()
    st.session_state['assistant_id'] = assistant_id
    st.session_state['thread_id'] = thread.id
    st.session_state['thread_initialized'] = True

# conversation
def ask_assistant(user_input):
    # user input
    message = client.beta.threads.messages.create(
        thread_id = st.session_state['thread_id'],
        role = "user",
        content = user_input
    )

    #thread_messages = client.beta.threads.messages.list(thread.id)
    #print(thread_messages.data)

    # run assistant
    run = client.beta.threads.runs.create(
        thread_id = st.session_state['thread_id'],
        assistant_id = st.session_state['assistant_id'],
        truncation_strategy = { "type": "last_messages", "last_messages": 20 }
    )

    # check run status
    while (run.status != "completed"):
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id = st.session_state['thread_id'],
            run_id = run.id
        )

    # get assistant response
    response = client.beta.threads.messages.list(
        thread_id = st.session_state['thread_id']
    )

    return response.data[0].content[0].text.value

# TBD: delete thread for cleanup
def thread_delete():
    pass