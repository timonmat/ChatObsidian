# chroma.py
import streamlit as st
from pathlib import Path

import chromadb
from chromadb.config import Settings
from llama_index import GPTChromaIndex

from utils.qa_template import QA_PROMPT

INDEX_PATH = './chroma_index.json'

@st.cache_resource
def create_chroma_client():
    return chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",persist_directory="./chromadb"))

def get_chroma_collection(client, collection_name):
    return client.get_collection(collection_name)

@st.cache_resource
def load_chroma_index(collection):
    chroma_client = create_chroma_client()
    _chroma_collection = chroma_client.get_collection(collection)
    if Path(INDEX_PATH).exists():
        index = GPTChromaIndex.load_from_disk(INDEX_PATH, chroma_collection=_chroma_collection)
        # index.save_to_disk(INDEX_PATH)
    else:
        index = None
    return index

def build_chroma_index(documents, collection, reindex):
    chroma_client = create_chroma_client()
    if reindex is True:
        chroma_client.reset()
        chroma_client.create_collection(collection)
        st.write("will remove and rebuild")
    _chroma_collection = chroma_client.get_or_create_collection(collection)
    index = None
    index = GPTChromaIndex(documents, chroma_collection=_chroma_collection)
    index.save_to_disk(INDEX_PATH)
    chroma_client.persist()

def query_index(query_str, collection):
    chroma_client = create_chroma_client()
    _chroma_collection = chroma_client.get_collection(collection)
    index = None
    index = load_chroma_index(collection)
    return index.query(query_str, chroma_collection=_chroma_collection, mode='embedding', use_async=True, text_qa_template=QA_PROMPT)
    
    