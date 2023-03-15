import streamlit as st
from llama_index import GPTSimpleVectorIndex, GPTChromaIndex
import chromadb
from chromadb.config import Settings
from llama_index.readers.chroma import ChromaReader
from llama_index.indices import GPTListIndex
from pathlib import Path

from components.sidebar import add_to_sidebar
from utils.qa_template import QA_PROMPT

from utils.chroma import create_chroma_client, get_chroma_collection, load_chroma_index, query_index

st.set_page_config(
    page_title="Query",
    page_icon="👋",
)

add_to_sidebar()

st.write("# ChatObsidian 👋")

def clear_submit():
    st.session_state["submit"] = False

clear_submit()
              
query_str = st.text_area("Ask a question about your Markdown notes", on_change=clear_submit)
with st.expander("Advanced Options"):
    show_context = st.checkbox("Show all chunks retrieved from local vector index search")
    show_final_query = st.checkbox("Show final templated query")

chroma_client = create_chroma_client()
st.write(chroma_client.list_collections())
chroma_collection = chroma_client.get_collection("markdown_notes")
st.write("documents in collection:  " + str(chroma_collection.count()))



button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    elif not query_str:
        st.error("Please enter a question!")
    else:
        st.session_state["submit"] = True
        collection = "markdown_notes"
        index = None
        index = load_chroma_index(collection)
        if index:
            st.write('Index loaded')
            response = query_index(query_str, collection)
            st.markdown(response)
            st.markdown(response.get_formatted_sources())
        else:
            st.write('Index not found')
            st.error("Please index your documents!")
        

