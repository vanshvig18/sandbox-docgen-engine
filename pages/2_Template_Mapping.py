import streamlit as st
import pandas as pd

def app():
    st.title("Template Mapping")

    if 'uploaded_data' not in st.session_state:
        st.warning("Please upload files first on the Document Uploader page.")
        return

    uploaded_data = st.session_state['uploaded_data']

    for filename, data in uploaded_data.items():
        st.write(f"### {filename}")

        if isinstance(data, pd.DataFrame):
            st.dataframe(data.head())

            # Let user map columns from this file to template fields
            st.write("Map columns for this file:")
            columns = data.columns.tolist()
            # Example: mapping 'Name' and 'Date' fields
            name_col = st.selectbox(f"Select column for 'Name' in {filename}", options=columns, key=f"name_{filename}")
            date_col = st.selectbox(f"Select column for 'Date' in {filename}", options=columns, key=f"date_{filename}")

            st.write(f"Mapped Name column: **{name_col}**, Date column: **{date_col}**")

        else:
            st.text(data[:500])

    # You can add buttons or functions here to generate documents based on mapping

