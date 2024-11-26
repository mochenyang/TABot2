import time
from openai import OpenAI
import streamlit as st
import pymongo

st.set_page_config(page_title="Chat", page_icon="🤖")

# connect to OpenAI
client = OpenAI(
    organization="org-OLj35i3NXxpSuuOGH1a1HxNm",
    project="proj_GB1WRZh96Njv1a7nASGFgcZT")

assistant_id = "asst_81TxmQ0vUYW0zxBLYaBoXSf8"

# connect to mongodb
dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = dbclient["TABot"]
conversation_col = mydb["conversation"]
user_col = mydb["user"]
thread_col = mydb["thread"]

## Chat Functions
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

## DB Functions
# store a conversation
def insert_conversation(user, thread, query, response):
    record = { "user": user, "thread": thread, "time": time.time(), "query": query, "response": response }
    _ = conversation_col.insert_one(record)


# store a thread
def insert_thread(thread, status):
    record = { "thread": thread , "status": status}
    _ = thread_col.insert_one(record)


# get all open threads and return thread ID in a list
def get_open_threads():
    open_threads = []
    for thread in thread_col.find({"status": "open"}):
        open_threads.append(thread["thread"])
    return open_threads


## Chat UI
# initialize a thread and store it in db
if st.session_state['authentication_status']:
    if st.button("Start New Chat"):
        del st.session_state["thread_initialized"]
        del st.session_state["thread_id"]
        del st.session_state["messages"]
    
    if 'thread_initialized' not in st.session_state:
        thread_init()
        #insert_thread(session['thread_id'], "open")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
        
    user_input = st.chat_input()
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        response = ask_assistant(user_input)
        # store in database
        #insert_conversation(session['user_id'], session['thread_id'], userText, response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
else:
    st.error("Please log in or create an account before starting a chat.")


# # 1. A button to clear the current chat and start a new one
# if st.sidebar.button("New Chat"):
#     st.session_state.clear()
#     st.rerun()