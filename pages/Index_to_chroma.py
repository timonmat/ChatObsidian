import streamlit as st
import os
from components.sidebar import add_to_sidebar
from llama_index import GPTSimpleVectorIndex, GPTChromaIndex
import chromadb
from chromadb.config import Settings
from pathlib import Path
from llama_index import download_loader

st.set_page_config(
    page_title="Index",
    page_icon="👋",
)

st.write("# Index your Markdown Notes 👋")

def clear_submit():
    st.session_state["submit"] = False

def form_callback():
    st.session_state.FOLDER_PATH


MarkdownReader = download_loader("MarkdownReader")
loader = MarkdownReader()

if 'FOLDER_PATH' not in st.session_state:
    st.session_state['FOLDER_PATH'] = './testdata'

folder_path = st.text_input(
            "Obsidian Folder to scan for notes",
            type="default",
            key='FOLDER_PATH',
            placeholder="/Users/mattitimonen/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Notes",
            help="/Users/xx/Library...",  # noqa: E501
            value=st.session_state.get("FOLDER_PATH", ""),
            on_change=form_callback,
        )


# Get the list of files in the selected folder and its subdirectories
files = []
for root, dirs, dir_files in os.walk(folder_path):
    for file in dir_files:
        if file.endswith(".md"):
             files.append(os.path.join(root, file))

if len(files) == 0:
    st.write(f"No Markdown files found in {folder_path}")
else:
    st.write(f"Found {len(files)} Markdown files in {folder_path}")

    st.expander("Advanced Options")
    reindex = st.checkbox("Delete existing index, and re-index")

    # Creating a Chroma vector store and persisting to disk
 
    chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                    persist_directory="./.chromadb"
                                ))
    
    st.write(chroma_client.list_collections())

    # Add a button to start indexing the files
    if st.button("Index files"):
        
        documents = []
        for file_path in files:
            doc = loader.load_data(file=file_path)
            for array_elem in doc:
                documents.append(array_elem)

        if st.session_state.get("api_key_configured"): # not needed for local embeddings
            if reindex:
                chroma_collection = chroma_client.delete_collection("markdown_notes")
                chroma_collection = chroma_client.create_collection("markdown_notes")
                index = GPTChromaIndex(documents, chroma_collection=chroma_collection)
                index.save_to_disk('./.chromadb/chroma_index.json')
                st.write("rebuilt the index - Finished indexing documents")
            else:
                chroma_collection = chroma_client.get_or_create_collection("markdown_notes")
                index = GPTChromaIndex(documents, chroma_collection=chroma_collection)
                index.save_to_disk('./.chromadb/chroma_index.json')
                st.write("Finished indexing documents")
        else:
            st.write("set your api key first")

        
        st.write("Document parts:" + str(len(documents)))
        st.write(documents)

add_to_sidebar()
