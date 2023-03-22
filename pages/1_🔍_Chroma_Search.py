#Query_from_chroma.py
import streamlit as st
from llama_index import GPTSimpleVectorIndex, GPTChromaIndex
import chromadb
from chromadb.config import Settings
from llama_index.readers.chroma import ChromaReader
from llama_index.indices import GPTListIndex
from pathlib import Path
import urllib.parse

from components.sidebar import add_to_sidebar
from utils.qa_template import QA_PROMPT

from utils.chroma import create_chroma_client, get_chroma_collection, load_chroma_index, query_index, get_logger

st.set_page_config(
    page_title="Search",
    page_icon="🔍",
)

add_to_sidebar()

st.write("# ChatObsidian 🔍  \n")
st.write("### Semantically Search your notes from ChromaDB")

def clear_submit():
    st.session_state["submit"] = False

# clear_submit()            
query_str = st.text_area("Just Search. No summarization. No OpenAI", on_change=clear_submit)

@st.cache_data(experimental_allow_widgets=True)
def get_search_results(similarity_top_k=5):
    similarity_top_k = st.slider("Number of results to get", value=similarity_top_k, max_value=10)
    return query_index(query_str, collection, similarity_top_k=similarity_top_k, response_mode='no_text')

button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not query_str:
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
                    response = get_search_results()

                # st.markdown("documents in collection:  " + str(chroma_collection.count()))
                for node in response.source_nodes:
                    # st.markdown(f"Document ID: {node.doc_id}")
                    docid, filename, content = node.source_text.strip().split('\n\n', 2)
                    filename = filename.split(': ')[1]
                    content = content.strip()
                    # st.write(f"Filename: {filename}")
                    url = (f'obsidian://open?file={urllib.parse.quote(filename)}')
                    mdlink = (f'[Open in Obsidian]({url})')
                    st.markdown(f"Similarity: {node.similarity}")
                    st.markdown(f"Filename: {filename}")
                    st.markdown(mdlink)
                    with st.expander("Matching Text Chunk"):
                        st.markdown(content)
                    
                    st.markdown("---")
            except Exception as e:
                st.exception(f"Error processing your query: {e}")
                            
        else:
            st.write('Collection not found')
            st.error("Please index your documents!")




with st.expander("Logs"):
    llama_logger = get_logger()
    st.write(llama_logger.get_logs())
