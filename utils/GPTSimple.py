import streamlit as st
from llama_index import GPTSimpleVectorIndex
from pathlib import Path

from utils.qa_template import QA_PROMPT
from utils.model_settings import get_embed_model, get_llm_predictor, get_prompt_helper

embed_model = get_embed_model()
llm_predictor = get_llm_predictor()
prompt_helper = get_prompt_helper()

@st.cache_resource
def load_index():
    return GPTSimpleVectorIndex.load_from_disk('index.json',embed_model=embed_model, llm_predictor=llm_predictor, prompt_helper=prompt_helper)