import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Template Mapping", layout="wide")

# Sidebar Navigation
st.sidebar.title("📚 Navigation")
st.sidebar.markdown("### ➤ main")
st.sidebar.markdown("### ➤ Auth")
st.sidebar.markdown("### ➤ Document Uploader")
st.sidebar.markdown("### **Template Mapping**", help="You're here")

# Main Title
st.markdown("<h2 style='color:#00FFAA;'>🧾 Template Mapping and ML Documentation</h2>", unsafe_allow_html=True)

# Check if session state has uploaded files
if 'uploaded_data' not in st.session_state:
    st.warning("⚠️ Please upload files first on the Document Uploader page.")
else:
    uploaded_data = st.session_state['uploaded_data']

    section_contents = {
        "name": None,
        "date": None,
        "overview": None,
        "motivation": None,
        "success": None,
        "requirements": None,
        "in_scope": None,
        "out_scope": None,
        "problem": None,
        "data": None,
        "techniques": None,
        "validation": None,
    }

    for filename, data in uploaded_data.items():
        with st.expander(f"📁 {filename}", expanded=False):
            if isinstance(data, pd.DataFrame):
                st.dataframe(data.head())
                for key in section_contents:
                    if section_contents[key] is None:
                        st.markdown(f"**Mapping for: {key.replace('_', ' ').title()}**")
                        row_index = st.number_input(
                            f"Select row index in {filename}", min_value=0, max_value=len(data) - 1, key=f"row_{key}_{filename}"
                        )
                        col_name = st.selectbox(
                            f"Select column for {key.replace('_', ' ').title()} in {filename}",
                            options=data.columns.tolist(),
                            key=f"col_{key}_{filename}"
                        )
                        cell_value = data.at[row_index, col_name]
                        if pd.notna(cell_value):
                            section_contents[key] = str(cell_value)

            elif isinstance(data, str):
                st.text_area("📜 File Preview", data[:500], height=200)
                for key in section_contents:
                    if section_contents[key] is None:
                        input_val = st.text_input(f"Enter value for '{key.replace('_', ' ').title()}' from {filename}", key=f"input_{key}_{filename}")
                        if input_val:
                            section_contents[key] = input_val

    # Generate combined doc
    st.success("✅ Document Generated Successfully!")
    final_doc = f"""# ML Documentation

## Project: {section_contents['name']}  
**Author**:  
**Application Date**: {section_contents['date']}

### Description
{section_contents['overview']}

---

### Sections

- **Motivation**: {section_contents['motivation']}  
- **Success Metrics**: {section_contents['success']}  
- **Requirements & Constraints**: {section_contents['requirements']}  
  - In‑Scope: {section_contents['in_scope']}  
  - Out‑of‑Scope: {section_contents['out_scope']}  

### Methodology

- **Problem Statement**: {section_contents['problem']}  
- **Data**: {section_contents['data']}  
- **Techniques**: {section_contents['techniques']}  
- **Training & Evaluation**: {section_contents['validation']}  
"""

    st.subheader("📄 Preview")
    st.code(final_doc, language="markdown")

    st.download_button("⬇️ Download Final Documentation", final_doc, file_name="ML_Documentation.txt", mime='text/plain')
