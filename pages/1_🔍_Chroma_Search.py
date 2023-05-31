#Query_from_chroma.py
import streamlit as st

st.set_page_config(
    page_title="Search",
    page_icon="🔍",
)

import urllib.parse

from components.sidebar import add_to_sidebar
from utils.qa_template import QA_PROMPT
from pathlib import Path

from utils.chroma import query_index, get_collection_index_path
import utils.tinydb as userdata
from components.ui import collection_selection_ui, render_sources
from utils.files_helper import open_finder_to_folder
from utils.model_settings import get_logger




add_to_sidebar()

st.write("# ChatObsidian 🔍  \n")
st.write("### Semantically Search your notes from ChromaDB")
response = []

def clear_submit():
    st.session_state["submit"] = False
clear_submit()            

#@st.cache_data(experimental_allow_widgets=True)
def get_search_results(similarity_top_k=5):
    similarity_top_k = st.slider("Number of results to get", value=similarity_top_k, max_value=10)
    return 

def similarity_slider(similarity_top_k=7):
    return st.slider("Number of results to get", value=similarity_top_k, max_value=20)


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

query_str = st.text_area("Just Search. No summarization. No OpenAI", on_change=clear_submit)

with st.expander("Advanced Options"):
    similarity_top_k = similarity_slider()
 


button = st.button("Submit")
if button or st.session_state.get("submit"):
        if not query_str:
            st.error("Please enter a question!")
        else:
            st.session_state["submit"] = True
            
            if Path(get_collection_index_path(collection)).exists:
                st.sidebar.success('Collection exists')
                try:
                    with st.spinner("Processing your query..."):
                        response = query_index(query_str, collection, similarity_top_k=similarity_top_k, response_mode='no_text', model_name=model_name)
                        st.markdown(response.source_nodes[0].node.get_text())
                        render_sources(response, collection_type)
                                            
                    st.markdown("---")
                except Exception as e:
                    st.exception(f"Error processing your query: {e}")
                                
            else:
                st.write('Collection not found')
                st.error("Please index your documents!")

with st.expander("Logs"):
    llama_logger = get_logger()
    st.write(llama_logger.get_logs())
