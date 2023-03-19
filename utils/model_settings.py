from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import LangchainEmbedding, LLMPredictor, PromptHelper, OpenAIEmbedding
from langchain import OpenAI


def get_embed_model():
    # load in HF embedding model from langchain
    model_name = "sentence-transformers/all-MiniLM-L6-v2"           # sentence-transformers/all-mpnet-base-v2,  sentence-transformers/all-MiniLM-L6-v2
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
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=num_output))
    return llm_predictor