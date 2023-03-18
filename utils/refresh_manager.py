# refresh_manager.py
# WIP

from llama_index import GPTListIndex, SimpleDirectoryReader, LangchainEmbedding, LLMPredictor, PromptHelper
import logging
import os
import streamlit as st
from pathlib import Path

DOCS_PATH = './docs_index.json'

def create_docs_index(documents_folder):
    if Path(DOCS_PATH).exists():
        os.remove(DOCS_PATH)
    documents = SimpleDirectoryReader(documents_folder, recursive=True, required_exts=['.md']).load_data()
    for i in range(len(documents)):
        documents[i].doc_id = str(i)  # or, you can give it whatever name is relevant 
    index = GPTListIndex(documents, chunk_size_limit=512)
    index.save_to_disk(DOCS_PATH)

@st.cache_resource
def load_docs_index():
    return GPTListIndex.load_from_disk(DOCS_PATH)


def refresh_docs_index(documents_folder):
    documents = SimpleDirectoryReader(documents_folder, recursive=True, required_exts=['.md']).load_data()
    index = load_docs_index()
    for i in range(len(documents)):
        documents[i].doc_id = str(i)
    logging.info('refereshing docs index ' + documents_folder)
    refreshed_docs = index.refresh(documents)
    index.save_to_disk(DOCS_PATH)
    return refreshed_docs