import streamlit as st

def logout():

    """ Logout user and reset session state """

    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.page = "Dashboard"
    st.rerun()