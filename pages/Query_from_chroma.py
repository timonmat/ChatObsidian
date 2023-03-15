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

chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                    persist_directory="./.chromadb"
                                ))
st.write(chroma_client.list_collections())
chroma_collection = chroma_client.get_collection("markdown_notes")
st.write("documents in collection:  " + str(chroma_collection.count()))

if st.session_state.get("api_key_configured"):
    if Path('./.chromadb/chroma_index.json').exists():
        index = GPTChromaIndex.load_from_disk('./.chromadb/chroma_index.json', chroma_collection=chroma_collection)
        st.write("Index loaded")
    else:
        st.write("Index not found")
        
          
query_str = st.text_area("Ask a question about your Markdown notes", on_change=clear_submit)
with st.expander("Advanced Options"):
    show_context = st.checkbox("Show all chunks retrieved from local vector index search")
    show_final_query = st.checkbox("Show final templated query")

chroma_client = create_chroma_client()
# chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chromadb"))
st.write(chroma_client.list_collections())
chroma_collection = chroma_client.get_collection("markdown_notes")
st.write("documents in collection:  " + str(chroma_collection.count()))
#st.error(chroma_client.heartbeat())


button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    elif not index:
        st.error("Please index your documents!")
    elif not query_str:
        st.error("Please enter a question!")
    else:
        st.session_state["submit"] = True
        index = None
        # index = load_chroma_index(chroma_collection)
        collection = "markdown_notes"
        index = load_chroma_index(collection)
        if index:
            st.write('Index loaded')
            response = query_index(query_str, collection)
            # response = index.query(query_str, chroma_collection=chroma_collection, mode='embedding', text_qa_template=QA_PROMPT)
            st.markdown(response)
            st.markdown(response.get_formatted_sources())
        else:
            st.write('Index not found')
            st.error("Please index your documents!")
        

