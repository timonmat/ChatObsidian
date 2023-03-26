#Index_to_chroma.py
import streamlit as st

st.set_page_config(
    page_title="Index",
    page_icon="🧠",
)

from components.sidebar import add_to_sidebar
from components.ui import folder_path_input_box, collection_selection_ui, create_new_collection_ui
from utils.chroma import (build_chroma_index, 
                          persist_chroma_index,
                          refresh_chroma_index,
                          get_chroma_collection,
                          create_or_refresh_chroma_index
                          )
from utils.loaders_helper import load_docs_with_sdr, clean_filenames_for_obsidian

from utils.files_helper import get_file_list

import logging
import utils.tinydb as userdata




add_to_sidebar()

folder_path = None

st.write("# Index your Markdown Notes 🧠  \n")  
st.write("### Into Persistant ChromaDB  ")

def clear_submit():
    st.session_state["submit"] = False

# Collection selection UI
st.subheader('Select an existing collection')
collection_data = collection_selection_ui(userdata.get_collections())

if collection_data:
    name = collection_data['name']
    folder_path = collection_data['folder_path']
    model_name = collection_data['model_name']
    collection = collection_data['index_name']
else:
    #folder_path = folder_path_input_box()
    #model_name = get_sentence_transformer_dropdown()

    # Create a new collection UI
    with st.expander("Create New Collection"):
        collection_data = create_new_collection_ui()
        if collection_data:
            name = collection_data['name']
            folder_path = collection_data['folder_path']
            model_name = collection_data['model_name']
            collection = collection_data['index_name']

# folder_path = folder_path_input_box()

with st.expander("Advanced Options"):
    reindex = st.checkbox("Delete existing index, and re-index")
    # model_name = get_sentence_transformer_dropdown()

statusbar = st.empty()
if folder_path:
    with st.spinner("Reading the directory"):
        files = get_file_list(folder_path)
    with statusbar:
        if len(files) == 0:
            st.write(f"No Markdown files found in {folder_path}")
        else:
            st.write(f"Found {len(files)} Markdown files in {folder_path}")

placeholder = st.empty()
debug = st.empty()
col1, col2, col3 = st.columns([2,1,1])
# with col2:
    # if st.button("Refresh index [wip]"):
    #     docs = clean_filenames_for_obsidian(load_docs_with_sdr(folder_path), folder_path)
    #     refreshed_documents = refresh_chroma_index(docs, collection)
    #     with statusbar:
    #         st.write("Refreshed, and added documents:  ")
    #         st.write(refreshed_documents)    
with col3:
    if st.button("Force persist chromadb"):
        persist_chroma_index()
        with statusbar:
            st.write("Persisted Chroma DB to disk.")    

with col1:# Add a button to start indexing the files
    if st.button("Create or refresh collection"):
        if folder_path:
            documents = []
            with st.spinner("Reading the files..."):
                documents = clean_filenames_for_obsidian(load_docs_with_sdr(folder_path), folder_path)
            
            if st.session_state.get("api_key_configured"): # not needed for local embeddings
                if get_chroma_collection(collection) and reindex is not True:
                    placeholder.write("Index exists, and will be refreshed")
                elif not get_chroma_collection(collection) or reindex is True:
                    placeholder.write("will remove and rebuild")
                with st.spinner("Indexing..."):
                    # create_docs_index(folder_path)
                    create_or_refresh_chroma_index(documents, collection, reindex=reindex, model_name=model_name)
                with placeholder:
                    st.write("Finished indexing documents")
                    st.write(f'{str(len(documents))} chunks in {collection} ')
                    # debug.code(documents)
                        
            else:
                st.error("Set your api key first")
        else:
            st.error("No folder path defined")
    



