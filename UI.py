from bot import *
#from db import *
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


# The authentication-related objects and methods
def save_credentials_to_yaml(credentials, filename="credentials.yaml"):
    with open(filename, "w") as file:
        yaml.dump(credentials, file, default_flow_style=False)

def get_authenticator():
    # load or initiate credentials
    try:
        with open("credentials.yaml") as file:
            credentials = yaml.load(file, Loader=SafeLoader)
    except FileNotFoundError:
        credentials = {"usernames": {}}
    
    authenticator = stauth.Authenticate(
        # set cookie_expiry_days to 0 to make the session expire when the browser is closed
        credentials, "auth_app", "auth_key", cookie_expiry_days=0
    )
    return [authenticator, credentials]

# The main chatbot UI
def Chat():
    # initialize a thread and store it in db
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