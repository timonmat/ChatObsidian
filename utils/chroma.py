# chroma.py
import streamlit as st
from pathlib import Path

import chromadb
from chromadb.config import Settings
from llama_index import GPTChromaIndex, LangchainEmbedding, LLMPredictor, PromptHelper

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain import OpenAI

from utils.qa_template import QA_PROMPT

INDEX_PATH = './chroma_index.json'

# load in HF embedding model from langchain
model_name = "sentence-transformers/all-MiniLM-L6-v2"
embed_model = LangchainEmbedding(HuggingFaceEmbeddings())

# define prompt helper
# set maximum input size
max_input_size = 4096
# set number of output tokens
num_output = 1024
# set maximum chunk overlap
max_chunk_overlap = 20

prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=num_output))

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
        index = GPTChromaIndex.load_from_disk(INDEX_PATH, chroma_collection=_chroma_collection, embed_model=embed_model, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        
    else:
        index = None
    return index, _chroma_collection

def build_chroma_index(documents, collection, reindex):
    chroma_client = create_chroma_client()
    if reindex is True:
        chroma_client.reset()
        chroma_client.create_collection(collection)
        
    _chroma_collection = chroma_client.get_or_create_collection(collection)
    index = None
    index = GPTChromaIndex(documents, chroma_collection=_chroma_collection, embed_model=embed_model, prompt_helper=prompt_helper)
    index.save_to_disk(INDEX_PATH)
    chroma_client.persist()

def query_index(query_str, collection):
    index = None
    index, _chroma_collection = load_chroma_index(collection)
    return index.query(query_str, chroma_collection=_chroma_collection, 
                       mode="embedding", 
                       response_mode="tree_summarize", # default, compact, tree_summarize
                       verbose=True, 
                       use_async=True, 
                       streaming=False,
                       text_qa_template=QA_PROMPT)
    
def persist_chroma_index():
    chroma_client = create_chroma_client()
    chroma_client.persist()
