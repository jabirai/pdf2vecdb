import streamlit as st

def init_session():
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = {}

def add_uploaded_files(uploaded):
    for file in uploaded:
        if file.name not in st.session_state.uploaded_files:
            st.session_state.uploaded_files[file.name] = file
            st.sidebar.write(f"{file.name}")