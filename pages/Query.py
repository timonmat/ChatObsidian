#Query.py
import streamlit as st
from llama_index import GPTSimpleVectorIndex
from llama_index.response.schema import SourceNode
from pathlib import Path

from components.sidebar import add_to_sidebar
from utils.qa_template import QA_PROMPT
from utils.model_settings import get_embed_model, get_llm_predictor, get_prompt_helper
from utils.GPTSimple import load_index

st.set_page_config(
    page_title="Query",
    page_icon="🔍",
)

add_to_sidebar()

embed_model = get_embed_model()
llm_predictor = get_llm_predictor()
prompt_helper = get_prompt_helper()

st.write("# ChatObsidian 🔍  \n")
st.write("### Query your data from GPTSimpleIndex")

def clear_submit():
    st.session_state["submit"] = False

clear_submit()


if st.session_state.get("api_key_configured"):
    if Path('index.json').exists():
        index = load_index()
        st.sidebar.success("Index loaded")
    else:
        st.sidebar.error("Index not found")
        
          
query_str = st.text_area("Ask a question about your Markdown notes", on_change=clear_submit)

button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    elif not index:
        st.error("Please upload a document!")
    elif not query_str:
        st.error("Please enter a question!")
    else:
        st.session_state["submit"] = True
        response = index.query(query_str, 
                               response_mode="compact", # default, compact, tree_summarize 
                               llm_predictor=llm_predictor, 
                               prompt_helper=prompt_helper, 
                               embed_model=embed_model, 
                               mode="embedding", 
                               similarity_top_k=5, 
                               text_qa_template=QA_PROMPT, 
                               verbose=True)
        st.markdown(response)
        
        with st.expander("Sources"):
            for node in response.source_nodes:
                st.write(f"Document ID: {node.doc_id}")
                st.write(f"Source Text: {node.source_text.strip()}")
                st.write(f"Similarity: {node.similarity}")
                st.markdown("---")

