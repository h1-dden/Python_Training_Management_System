import streamlit as st
from view import user_logout

def create_sidebar():
    # Sidebar for navigation and logout
    st.sidebar.write(f"Logged in as: **{st.session_state.role.capitalize()}**")
    if st.sidebar.button("Logout"):
        user_logout.logout()

    # Sidebar navigation
    st.sidebar.header("Navigation")
    if st.sidebar.button("Home"):
        st.session_state.page = "Home"
    if st.sidebar.button("Employee Dashboard"):
        st.session_state.page = "Employee Dashboard"
    if st.sidebar.button("Training Dashboard"):
        st.session_state.page = "Training Dashboard"