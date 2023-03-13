import streamlit as st
from components.sidebar import add_to_sidebar
from llama_index import GPTSimpleVectorIndex
from pathlib import Path
from llama_index import download_loader

st.set_page_config(
    page_title="Index",
    page_icon="👋",
)

def clear_submit():
    st.session_state["submit"] = False

MarkdownReader = download_loader("MarkdownReader")

loader = MarkdownReader()
documents = loader.load_data(file=Path('./testdata/test2.md'))

if st.session_state.get("api_key_configured"):
    index = GPTSimpleVectorIndex(documents)
          
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
        st.write(response)

add_to_sidebar()

st.write("# Obsidian Chat 👋")
st.write("Document parts:" + str(len(documents)))
st.write(documents)