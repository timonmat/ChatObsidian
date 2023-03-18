# chroma.py
import streamlit as st
from pathlib import Path

import chromadb
from chromadb.config import Settings
from llama_index import GPTChromaIndex, LangchainEmbedding, LLMPredictor, PromptHelper, OpenAIEmbedding
from llama_index.logger import LlamaLogger

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain import OpenAI

import logging

from utils.qa_template import QA_PROMPT

INDEX_PATH = './chroma_index.json'

llama_logger = LlamaLogger()

# load in HF embedding model from langchain
model_name = "sentence-transformers/all-MiniLM-L6-v2"
embed_model = LangchainEmbedding(HuggingFaceEmbeddings())

#use default Open AI embeddings
#embed_model = OpenAIEmbedding()

# define prompt helper
max_input_size = 4096
num_output = 2048
max_chunk_overlap = 20
prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

# define LLM
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=num_output))

@st.cache_resource
def create_chroma_client():
    return chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",persist_directory="./chromadb"))

def get_chroma_collection(collection_name):
    client = create_chroma_client()
    return client.get_collection(collection_name)

@st.cache_resource
def load_chroma_index(collection):
    chroma_client = create_chroma_client()
    _chroma_collection = chroma_client.get_collection(collection)
    if Path(INDEX_PATH).exists():
        index = GPTChromaIndex.load_from_disk(INDEX_PATH, chroma_collection=_chroma_collection, embed_model=embed_model, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        logging.info('Index loaded for collection ' + collection )
    else:
        index = None
    return index, _chroma_collection

def build_chroma_index(documents, collection, reindex):
    chroma_client = create_chroma_client()
    if reindex is True:
        chroma_client.reset()
        chroma_client.create_collection(collection)

    _chroma_collection = chroma_client.get_or_create_collection(collection)
    for i in range(len(documents)):
        documents[i].doc_id = str(i)  # or, you can give it whatever name is relevant 
    index = None
    index = GPTChromaIndex(documents, chroma_collection=_chroma_collection, embed_model=embed_model, prompt_helper=prompt_helper, chunk_size_limit=512)
    index.save_to_disk(INDEX_PATH)
    chroma_client.persist()

def refresh_chroma_index(documents, collection):
    index, chromacollection = load_chroma_index(collection)
    for i in range(len(documents)):
        documents[i].doc_id = str(i)
    logging.info('refereshing collection ' + collection)
    refreshed_docs = index.refresh(documents)
    index.save_to_disk(INDEX_PATH)
    chroma_client = create_chroma_client()
    chroma_client.persist()
    return refreshed_docs

def query_index(query_str, collection):
    index = None
    index, _chroma_collection = load_chroma_index(collection)
    return index.query(query_str, chroma_collection=_chroma_collection,
                       mode="embedding",
                       similarity_top_k= 3,  
                       response_mode="compact", # default, compact, tree_summarize
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
