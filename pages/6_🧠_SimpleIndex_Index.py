#Index.py
import streamlit as st
import os
from components.sidebar import add_to_sidebar
from llama_index import GPTSimpleVectorIndex
from pathlib import Path
from llama_index import download_loader

from utils.model_settings import get_embed_model, get_llm_predictor, get_prompt_helper
from utils.loaders_helper import load_docs_with_sdr, clean_filenames_for_obsidian
from utils.files_helper import get_file_list
from utils.GPTSimple import index_gptsimpleindex

st.set_page_config(
    page_title="Index",
    page_icon="🧠",
)
add_to_sidebar()

INDEX_PATH = './data/index.json'

embed_model = get_embed_model()
llm_predictor = get_llm_predictor()
prompt_helper = get_prompt_helper()

st.write("# Index your Markdown Notes 🧠  \n") 
st.write("### into GPTSimpleIndex")

def clear_submit():
    st.session_state["submit"] = False

def form_callback():
    st.session_state.FOLDER_PATH

if 'FOLDER_PATH' not in st.session_state:
    st.session_state['FOLDER_PATH'] = 'testdata/'

folder_path = st.text_input(
            "Obsidian Folder to scan for notes",
            type="default",
            key='FOLDER_PATH',
            placeholder="/Users/whoever/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVaultName/",
            help="/Users/xx/Library...",  # noqa: E501
            value=st.session_state.get("FOLDER_PATH", ""),
            on_change=form_callback,
        )


# Get the list of files in the selected folder and its subdirectories

files = []
files = get_file_list(folder_path)

if len(files) == 0:
    st.write(f"No Markdown files found in {folder_path}")
else:
    st.write(f"Found {len(files)} Markdown files in {folder_path}")

    st.expander("Advanced Options")
    reindex = st.checkbox("Delete existing index, and re-index")

    # Add a button to start indexing the files
    if st.button("Index files"):
        documents = []
        documents = clean_filenames_for_obsidian(load_docs_with_sdr(folder_path), folder_path)


        if st.session_state.get("api_key_configured"):
            if reindex:
                st.write("deleting and rebuilding the index")
                with st.spinner("Indexing..."):
                    index_gptsimpleindex(documents, reindex)
                st.write("Finished indexing documents")
            elif Path(INDEX_PATH).exists():
                st.write("Index exists, and was not rebuilt")
            else:
                st.write("building the index")
                with st.spinner("Indexing..."):
                        index_gptsimpleindex(documents, reindex)
                st.write("Finished indexing documents")

        
        st.write("Document parts:" + str(len(documents)))
        # st.write(documents)


