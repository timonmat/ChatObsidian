#Query_from_chroma.py
import streamlit as st

st.set_page_config(
    page_title="Query",
    page_icon="🔍",
)

import urllib.parse
from pathlib import Path

from components.sidebar import add_to_sidebar
from components.ui import collection_selection_ui

from utils.model_settings import get_logger
from utils.qa_template import QA_PROMPT
from utils.chroma import query_index, get_collection_index_path
import utils.tinydb as userdata


add_to_sidebar()

st.write("# ChatObsidian 🔍  \n")
st.write("### Query your data from ChromaDB")

def clear_submit():
    st.session_state["submit"] = False

clear_submit()            

def similarity_slider(similarity_top_k=3):
    return st.slider("Number of results to get", value=similarity_top_k, max_value=7)

# Collection selection UI
st.subheader('Select an existing collection')
collection_data = collection_selection_ui(userdata.get_collections())

if collection_data:
    collection = collection_data.name
    folder_path = collection_data.folder_path
    model_name = collection_data.model_name
    index_name = collection_data.index_name
    collection_type = collection_data.collection_type
    extensions = collection_data.file_extensions

query_str = st.text_area("Ask a question about your Markdown notes", on_change=clear_submit)
with st.expander("Advanced Options"):
    similarity_top_k = similarity_slider()


button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    elif not query_str:
        st.error("Please enter a question!")
    else:
        st.session_state["submit"] = True
        index = None
        
        if Path(get_collection_index_path(collection)).exists:
            st.sidebar.success('Collection exists')
            try:
                with st.spinner("Processing your query..."):
                    response = query_index(query_str, collection, similarity_top_k=similarity_top_k, model_name=model_name)
                st.markdown(response)
                st.markdown("---\n")
                with st.expander("Sources"):
                    # st.markdown("documents in collection:  " + str(chroma_collection.count()))
                    for node in response.source_nodes:
                        #st.markdown(f"Document ID: {node.doc_id}")
                        filename, content = node.node.get_text().strip().split('\n\n', 1)  
                        filename = filename.split(': ')[1]
                        content = content.strip()
                        # st.write(f"Filename: {filename}")
                        url = (f'obsidian://open?file={urllib.parse.quote(filename)}')
                        st.markdown(f"Filename: {filename}  [Open in Obsidian]({url})")
                        st.markdown(f"Similarity: {node.similarity}")
                        st.markdown(content)
                        
                        st.markdown("---")
            except Exception as e:
                st.exception(f"Error processing your query: {e}")
                            
        else:
            st.write('Collection not found')
            st.error("Please index your documents!")

clear_submit() 


with st.expander("Logs"):
    llama_logger = get_logger()
    st.write(llama_logger.get_logs())
