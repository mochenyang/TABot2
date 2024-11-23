from UI import *
import streamlit as st


# Authentication
st.title("Please Login")
authenticator, credentials = get_authenticator()
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Welcome {name}!")
    authenticator.logout("Logout", "main")
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")

# Step 5: Create New Account
with st.expander("Create New Account"):
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    new_name = st.text_input("What you like to be called within the app")
    if st.button("Create Account"):
        if new_username in credentials["usernames"]:
            st.error("Username already exists!")
        else:
            # Hash the password using stauth.Hasher
            hashed_password = stauth.Hasher([new_password]).generate()[0]
            credentials["usernames"][new_username] = {
                "name": new_name,
                "password": hashed_password,
            }
            save_credentials_to_yaml(credentials)
            st.success("Account created successfully! Please log in.")


# # Main Chatbot interface (right side)
# st.title("TABot")
# st.caption("A GenAI Research Assistant powered by OpenAI and Streamlit")
# Chat()

# # Create a sidebar of other functions (left side)
# st.sidebar.title("Welcome!")
# # 1. A button to clear the current chat and start a new one
# if st.sidebar.button("New Chat"):
#     st.session_state.clear()
#     st.rerun()