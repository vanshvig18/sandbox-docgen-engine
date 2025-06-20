import streamlit as st
from document_uploader import app as uploader_app
from template_mapping import app as mapping_app

PAGES = {
    "Document Uploader": uploader_app,
    "Template Mapping": mapping_app
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page()
