
import streamlit as st
import bcrypt

# Define user credentials for login
USER_CREDENTIALS = {
    'admin': {
        'password': bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()),
        'role': 'admin'
    },
    'user': {
        'password': bcrypt.hashpw("user123".encode(), bcrypt.gensalt()),
        'role': 'user'
    }
}

# Authenticate user function
def authenticate(username, password):

    """ Authenticate user based on provided credentials """

    user = USER_CREDENTIALS.get(username)
    if user and bcrypt.checkpw(password.encode(), user['password']):
        st.session_state.logged_in = True
        st.session_state.role = user['role']
        st.session_state.username = ""
        st.session_state.password = ""
        st.rerun()
    else:
        st.error("Invalid username or password.")