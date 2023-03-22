import streamlit as st
from llama_index.response.schema import SourceNode
from pathlib import Path
import urllib.parse
from components.sidebar import add_to_sidebar
from utils.GPTSimple import  query_gptsimpleindex

st.set_page_config(
    page_title="Query",
    page_icon="🔍",
)

add_to_sidebar()

st.write("# ChatObsidian 🔍  \n")
st.write("### Query your data from GPTSimpleIndex")

def clear_submit():
    st.session_state["submit"] = False

clear_submit()

query_str = st.text_area("Ask a question about your Markdown notes", on_change=clear_submit)

button = st.button("Submit")
if button or st.session_state.get("submit"):
    if not st.session_state.get("api_key_configured"):
        st.error("Please configure your OpenAI API key!")
    elif not query_str:
        st.error("Please enter a question!")
    else:
        st.session_state["submit"] = True
        try:
            with st.spinner("Processing your query..."):
                response = None
                response = query_gptsimpleindex(query_str)
            st.markdown(response)
            with st.expander("Sources"):
                for node in response.source_nodes:
                    st.markdown(f"Document ID: {node.doc_id}")
                    filename, content = node.source_text.split('\n\n', 1)
                    filename = filename.split(': ')[1]
                    content = content.strip()
                    # st.write(f"Filename: {filename}")
                    url = (f'obsidian://open?file={urllib.parse.quote(filename)}')
                    st.markdown(f"Filename: {filename}  [link]({url})", unsafe_allow_html=True)
                    st.markdown(f"Source Text: {content}")
                    #st.write(f"Source Text: {node.source_text.strip()}")
                    st.markdown(f"Similarity: {node.similarity}")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Error processing your query: {e}")
