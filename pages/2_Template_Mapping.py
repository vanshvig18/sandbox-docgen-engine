import streamlit as st
import pandas as pd

st.title("Template Mapping")

if 'uploaded_data' not in st.session_state:
    st.warning("Please upload files first on the Document Uploader page.")
else:
    uploaded_data = st.session_state['uploaded_data']

    for filename, data in uploaded_data.items():
        st.write(f"### {filename}")

        if isinstance(data, pd.DataFrame):
            st.dataframe(data.head())

            columns = data.columns.tolist()
            name_col = st.selectbox(f"Select column for 'Name' in {filename}", options=columns, key=f"name_{filename}")
            date_col = st.selectbox(f"Select column for 'Date' in {filename}", options=columns, key=f"date_{filename}")

            st.write(f"Mapped Name column: **{name_col}**, Date column: **{date_col}**")
        else:
            st.text(data[:500])
