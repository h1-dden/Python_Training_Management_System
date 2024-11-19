import streamlit as st
from services import user_verification

def user_login():
    st.subheader("Login")
    st.session_state.username = st.text_input("Username", value=st.session_state.username)
    st.session_state.password = st.text_input("Password", type="password", value=st.session_state.password)
    login_button = st.button("Login" )

    if login_button:
        user_verification.authenticate(st.session_state.username, st.session_state.password)
