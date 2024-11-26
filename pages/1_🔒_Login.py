import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit as st

st.set_page_config(page_title="Account Management", page_icon="🔒")

def append_credentials_to_yaml(new_credential, filename="credentials.yaml"):
    new_credential_dir = yaml.dump(new_credential, indent=4)
    with open(filename, "a") as file:
        file.write('  ' + new_credential_dir)
        
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

# Authentication
authenticator.login()

if st.session_state['authentication_status']:
    st.success(f"Welcome {st.session_state['name']}!")
    # Logout button
    authenticator.logout()
elif st.session_state['authentication_status'] == False:
    st.error("Username/password is incorrect")
elif st.session_state['authentication_status'] == None:
    st.warning("Please enter your username and password")

# Step 5: Create New Account
with st.expander("Create New Account"):
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    new_name = st.text_input("What you like to be called in the app")
    if st.button("Create Account"):
        if new_username in credentials["usernames"]:
            st.error("Username already exists!")
        else:
            new_credential = {new_username: 
                {"name": new_name, 
                 "password": new_password, 
                 "email": "email@email"}
            }
            # Hash the password using stauth.Hasher
            new_credential_hashed = stauth.Hasher.hash_passwords({"usernames": new_credential})['usernames']
            append_credentials_to_yaml(new_credential_hashed)
            st.success("Account created successfully! Please log in.")