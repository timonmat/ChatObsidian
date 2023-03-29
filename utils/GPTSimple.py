import streamlit as st
from llama_index import GPTSimpleVectorIndex
from pathlib import Path
import os

from utils.qa_template import QA_PROMPT
from utils.model_settings import get_service_context



index_path = './data/index.json'
index = None

@st.cache_resource
def load_gptsimpleindex():
    service_context = get_service_context()
    if st.session_state.get("api_key_configured"):
        try:
            with st.spinner("Loading index..."):
                index = GPTSimpleVectorIndex.load_from_disk(index_path, service_context=service_context)
            st.sidebar.success("Index loaded")
            return index
        except Exception as e:
            st.exception(f"Error loading index: {e}")
    else:
        st.sidebar.error("Index not found")
    

def query_gptsimpleindex(query_str):
    service_context = get_service_context()
    index = load_gptsimpleindex()
    return index.query(query_str,
                        response_mode="compact", # default, compact, tree_summarize
                        mode="embedding",
                        similarity_top_k=5,
                        text_qa_template=QA_PROMPT,
                        verbose=True,
                        service_context=service_context
                        )

def index_gptsimpleindex(documents, reindex):
    service_context = get_service_context()
    if reindex & Path(index_path).exists():
        os.remove(index_path)
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
    index.save_to_disk(index_path)