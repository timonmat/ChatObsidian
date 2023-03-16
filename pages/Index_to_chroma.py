#Index_to_chroma.py
import streamlit as st
import os

from pathlib import Path

from llama_index import GPTSimpleVectorIndex, GPTChromaIndex, download_loader

import chromadb
from chromadb.config import Settings

from components.sidebar import add_to_sidebar
from utils.chroma import create_chroma_client, get_chroma_collection, load_chroma_index, build_chroma_index, persist_chroma_index, INDEX_PATH

st.set_page_config(
    page_title="Index",
    page_icon="🧠",
)

add_to_sidebar()

st.write("# Index your Markdown Notes 🧠  ")  
st.write("Into Persistant Chroma DB  \n")

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
            help="/Users/xx/Library...",  # noqa: E501
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



placeholder = st.empty()
col1, col2, col3 = st.columns([1,1,1])
with col2:
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
                build_chroma_index(documents, "markdown_notes", reindex)
                with placeholder:
                    st.write("Finished indexing documents")
                    st.write("Document parts:" + str(len(documents)))
                    st.write(documents)
        else:
            st.error("set your api key first")
    



