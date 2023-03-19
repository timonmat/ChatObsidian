#Index_to_chroma.py
import streamlit as st
import os

from pathlib import Path

from llama_index import download_loader

from components.sidebar import add_to_sidebar
from utils.chroma import (build_chroma_index, 
                          persist_chroma_index,
                          refresh_chroma_index,
                          INDEX_PATH)
from utils.refresh_manager import create_docs_index, load_docs_index, refresh_docs_index
import logging


st.set_page_config(
    page_title="Index",
    page_icon="🧠",
)


add_to_sidebar()
user_collection = "markdown_notes"

st.write("# Index your Markdown Notes 🧠  \n")  
st.write("### Into Persistant ChromaDB  ")

def clear_submit():
    st.session_state["submit"] = False

def form_callback():
    st.session_state.FOLDER_PATH

# MarkdownReader = download_loader("MarkdownReader")
# loader = MarkdownReader()
ObsidianReader = download_loader('ObsidianReader')



if 'FOLDER_PATH' not in st.session_state:
    st.session_state['FOLDER_PATH'] = './testdata'

folder_path = st.text_input(
            "Obsidian Folder to scan for notes",
            type="default",
            key='FOLDER_PATH',
            placeholder="/Users/whoever/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault",
            help="copy your obsidian vault path here",  
            value=st.session_state.get("FOLDER_PATH", ""),
            on_change=form_callback,
        )
st.expander("Advanced Options")
reindex = st.checkbox("Delete existing index, and re-index")



# Get the list of files in the selected folder and its subdirectories
# files = []
# for root, dirs, dir_files in os.walk(folder_path):
#     for file in dir_files:
#         if file.endswith(".md"):
#              files.append(os.path.join(root, file))

# if len(files) == 0:
#     st.write(f"No Markdown files found in {folder_path}")
# else:
#     st.write(f"Found {len(files)} Markdown files in {folder_path}")

collection = 'markdown_notes'

placeholder = st.empty()
col1, col2, col3 = st.columns([2,1,1])
with col2:
    if st.button("Refresh index [wip]"):
        documents = ObsidianReader(folder_path).load_data() # Returns list of documents
        refreshed_documents = refresh_chroma_index(documents, collection)
        with placeholder:
            st.write("Refreshed, and added documents:  ")
            st.write(refreshed_documents)    
with col3:
    if st.button("Force persist chromadb"):
        persist_chroma_index()
        with placeholder:
            st.write("Persisted Chroma DB to disk.")    

with col1:# Add a button to start indexing the files
    if st.button("Index files"):
        documents = []
        documents = ObsidianReader(folder_path).load_data() # Returns list of documents
        # documents = []
        # for file_path in files:
        #     doc = loader.load_data(file=file_path)
        #     for array_elem in doc:
        #         documents.append(array_elem)

        if st.session_state.get("api_key_configured"): # not needed for local embeddings
            if Path(INDEX_PATH).exists() and reindex is not True:
                placeholder.write("Index exists, and was not recreated")
            elif not Path(INDEX_PATH).exists() or reindex is True:
                placeholder.write("will remove and rebuild")
                create_docs_index(folder_path)
                build_chroma_index(documents, collection, reindex)
                with placeholder:
                    st.write("Finished indexing documents")
                    st.write("Document count:" + str(len(documents)))
                    # st.write(documents)
        else:
            st.error("set your api key first")
    



