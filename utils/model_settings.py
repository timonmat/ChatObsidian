#model_settings.py
import streamlit as st
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import LangchainEmbedding, LLMPredictor, PromptHelper, OpenAIEmbedding
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from enum import Enum

class sentenceTransformers(Enum):
    OPTION1 = "sentence-transformers/all-MiniLM-L6-v2"
    OPTION2 = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    OPTION3 = "sentence-transformers/all-mpnet-base-v2"

def get_sentence_transformer_dropdown():
    options = [e.value for e in sentenceTransformers]
    selected_option = st.selectbox("Sentence transformer:", options)
    return selected_option

def get_embed_model(model_name='sentence-transformers/all-MiniLM-L6-v2'):
    # load in HF embedding model from langchain
    # sentence-transformers/all-mpnet-base-v2,  sentence-transformers/all-MiniLM-L6-v2, sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
    embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name=model_name))

    #use default Open AI embeddings
    #embed_model = OpenAIEmbedding()
    return embed_model

def get_prompt_helper():
    # define prompt helper
    max_input_size = 4096
    num_output = 2048
    max_chunk_overlap = 20
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
    return prompt_helper

def get_llm_predictor():
    # define LLM
    num_output = 2048
    
    #llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=num_output))  
    llm_predictor = LLMPredictor(ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo", max_tokens=num_output))
    return llm_predictor
