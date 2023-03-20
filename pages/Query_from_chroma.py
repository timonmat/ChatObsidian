#Query_from_chroma.py
import streamlit as st
from llama_index import GPTSimpleVectorIndex, GPTChromaIndex
import chromadb
from chromadb.config import Settings
from llama_index.readers.chroma import ChromaReader
from llama_index.indices import GPTListIndex
from pathlib import Path

from components.sidebar import add_to_sidebar
from utils.qa_template import QA_PROMPT

from utils.chroma import create_chroma_client, get_chroma_collection, load_chroma_index, query_index, get_logger

st.set_page_config(
    page_title="Query",
    page_icon="🔍",
)

add_to_sidebar()

st.write("# ChatObsidian 🔍  \n")
st.write("### Query your data from ChromaDB")

def clear_submit():
    st.session_state["submit"] = False

clear_submit()            
query_str = st.text_area("Ask a question about your Markdown notes", on_change=clear_submit)

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
        chroma_collection = get_chroma_collection(collection)
        if chroma_collection:
            st.sidebar.success('Collection exists')
            try:
                with st.spinner("Processing your query..."):
                    response = query_index(query_str, collection)
                st.markdown(response)
                st.markdown("---\n")
                with st.expander("Sources"):
                    st.write("documents in collection:  " + str(chroma_collection.count()))
                    for node in response.source_nodes:
                        st.write(f"Document ID: {node.doc_id}")
                        st.write(f"Source Text: {node.source_text.strip()}")
                        st.write(f"Similarity: {node.similarity}")
                        st.markdown("---")
            except Exception as e:
                st.exception(f"Error processing your query: {e}")
                            
        else:
            st.write('Collection not found')
            st.error("Please index your documents!")




with st.expander("Logs"):
    llama_logger = get_logger()
    st.write(llama_logger.get_logs())
