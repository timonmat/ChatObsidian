#Index.py
import streamlit as st
import os
from components.sidebar import add_to_sidebar
from llama_index import GPTSimpleVectorIndex
from pathlib import Path
from llama_index import download_loader

from utils.model_settings import get_embed_model, get_llm_predictor, get_prompt_helper

st.set_page_config(
    page_title="Index",
    page_icon="🧠",
)
add_to_sidebar()

INDEX_PATH = './chroma_index.json'

embed_model = get_embed_model()
llm_predictor = get_llm_predictor()
prompt_helper = get_prompt_helper()

st.write("# Index your Markdown Notes 🧠  \n") 
st.write("### into GPTSimpleIndex")

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

    # Add a button to start indexing the files
    if st.button("Index files"):
        documents = []
        for file_path in files:
            doc = loader.load_data(file=file_path)
            for array_elem in doc:
                documents.append(array_elem)

        if st.session_state.get("api_key_configured"):
            if reindex & Path('index.json').exists():
                os.remove("index.json")
                index = GPTSimpleVectorIndex(documents, embed_model=embed_model)
                index.save_to_disk('index.json')
                st.write("rebuilt the index - Finished indexing documents")
            elif Path('index.json').exists():
                # index = GPTSimpleVectorIndex.load_from_disk('index.json', embed_model)
                st.write("Index exists, and was not rebuilt")
            else:
                index = GPTSimpleVectorIndex(documents, embed_model=embed_model)
                index.save_to_disk('index.json')
                st.write("Finished indexing documents")

        
        st.write("Document parts:" + str(len(documents)))
        st.write(documents)


