import streamlit as st
from llama_index import GPTSimpleVectorIndex
from pathlib import Path

from components.sidebar import add_to_sidebar
from utils.qa_template import QA_PROMPT

st.set_page_config(
    page_title="Query",
    page_icon="👋",
)

add_to_sidebar()

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
        
          
query_str = st.text_area("Ask a question about your Markdown notes", on_change=clear_submit)
with st.expander("Advanced Options"):
    show_context = st.checkbox("Show all chunks retrieved from local vector index search")
    show_final_query = st.checkbox("Show final templated query")


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
        response = index.query(query_str, mode="embedding", text_qa_template=QA_PROMPT)
        st.markdown(response)
        st.markdown(response.get_formatted_sources())


