import streamlit as st
from components.sidebar import add_to_sidebar
from llama_index import GPTSimpleVectorIndex
from pathlib import Path
from llama_index import download_loader

st.set_page_config(
    page_title="Index",
    page_icon="👋",
)

st.write("# ChatObsidian 👋")

def clear_submit():
    st.session_state["submit"] = False

clear_submit()

if st.session_state.get("api_key_configured"):
    if Path('index.json').exists():
        index = GPTSimpleVectorIndex.load_from_disk('index.json')
        st.write("Index loaded")
    else:
        st.write("Index not found")
        
          
query_str = st.text_area("Ask a question about the document", on_change=clear_submit)
with st.expander("Advanced Options"):
    show_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
    show_full_doc = st.checkbox("Show parsed contents of the document")


button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    elif not index:
        st.error("Please upload a document!")
    elif not query_str:
        st.error("Please enter a question!")
    else:
        st.session_state["submit"] = True
        # Output Columns
        answer_col, sources_col = st.columns(2)
        response = index.query(query_str, mode="default")
        st.markdown(response)

add_to_sidebar()
