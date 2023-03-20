import streamlit as st
from llama_index import GPTSimpleVectorIndex
from pathlib import Path

from utils.qa_template import QA_PROMPT
from utils.model_settings import get_embed_model, get_llm_predictor, get_prompt_helper

embed_model = get_embed_model()
llm_predictor = get_llm_predictor()
prompt_helper = get_prompt_helper()

index_path = 'index.json'
index = None

@st.cache_resource
def load_gptsimpleindex():
    if st.session_state.get("api_key_configured"):
        try:
            with st.spinner("Loading index..."):
                index = GPTSimpleVectorIndex.load_from_disk(index_path, embed_model=embed_model, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
            st.sidebar.success("Index loaded")
            return index
        except Exception as e:
            st.exception(f"Error loading index: {e}")
    else:
        st.sidebar.error("Index not found")
    

def query_gptsimpleindex(query_str):
    index = load_gptsimpleindex()
    return index.query(query_str,
                        response_mode="compact", # default, compact, tree_summarize
                        llm_predictor=llm_predictor,
                        prompt_helper=prompt_helper,
                        embed_model=embed_model,
                        mode="embedding",
                        similarity_top_k=5,
                        text_qa_template=QA_PROMPT,
                        verbose=True)