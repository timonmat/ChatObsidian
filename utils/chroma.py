# chroma.py
import streamlit as st
from pathlib import Path

import chromadb
from chromadb.config import Settings
from llama_index import GPTChromaIndex, LangchainEmbedding, LLMPredictor, PromptHelper, OpenAIEmbedding
from llama_index.logger import LlamaLogger

from utils.model_settings import get_embed_model, get_llm_predictor, get_prompt_helper

import logging

from utils.qa_template import QA_PROMPT

INDEX_PATH = './data/chroma_index.json'
PERSIST_DIRECTORY = './data/chromadb'

llama_logger = LlamaLogger()

embed_model = get_embed_model()
llm_predictor = get_llm_predictor()
prompt_helper = get_prompt_helper()

@st.cache_resource
def create_chroma_client():
    return chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",persist_directory=PERSIST_DIRECTORY))

def get_chroma_collection(collection_name):
    client = create_chroma_client()
    return client.get_collection(collection_name)

@st.cache_resource
def load_chroma_index(collection):
    _chroma_collection = get_chroma_collection(collection)
    if Path(INDEX_PATH).exists():
        index = GPTChromaIndex.load_from_disk(INDEX_PATH, chroma_collection=_chroma_collection, embed_model=embed_model, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        logging.info('Index loaded for collection ' + collection )
    else:
        index = None
    return index

def build_chroma_index(documents, collection, reindex):
    chroma_client = create_chroma_client()
    if reindex is True:
        chroma_client.reset()
        
    _chroma_collection = chroma_client.get_or_create_collection(collection)
    index = None
    index = GPTChromaIndex(documents, chroma_collection=_chroma_collection, embed_model=embed_model, prompt_helper=prompt_helper, chunk_size_limit=512)
    index.save_to_disk(INDEX_PATH)
    chroma_client.persist()

def refresh_chroma_index(documents, collection):
    index = load_chroma_index(collection)
    logging.info('refereshing collection ' + collection)
    refreshed_docs = index.refresh(documents)
    index.save_to_disk(INDEX_PATH)
    chroma_client = create_chroma_client()
    chroma_client.persist()
    return refreshed_docs

def query_index(query_str, collection):
    index = None
    _chroma_collection = get_chroma_collection(collection)
    index = load_chroma_index(collection)
    return index.query(query_str, chroma_collection=_chroma_collection,
                       mode="embedding",
                       similarity_top_k=3,  
                       response_mode="compact", # default, compact, tree_summarize, no_text
                       llm_predictor=llm_predictor, 
                       prompt_helper=prompt_helper,
                       llama_logger=llama_logger,
                       text_qa_template=QA_PROMPT,
                       verbose= True, 
                       use_async= True,
                       streaming= False
                       )



def get_logger():
    return llama_logger
    
def persist_chroma_index():
    chroma_client = create_chroma_client()
    chroma_client.persist()
