import streamlit as st
from components.sidebar import add_to_sidebar

from llama_index import GPTSimpleVectorIndex


st.set_page_config(
    page_title="ChatObsidian",
    page_icon="👋",
)

st.write("# ChatObsidian 👋")

st.markdown(
    "📖 ChatObsidian allows you to ask questions about your Notes"
)



add_to_sidebar()


st.markdown(
    "---\n"
    "## How to use\n"
    "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) In the Sidebar🔑\n"  # noqa: E501
    "2. Enter your obsidian notes folder on index page and generate the index📄\n"
    "3. Ask a questions about your notes on the Query page 💬\n"
)
st.markdown("---")
st.markdown("# About")

st.markdown(
    "This tool is a work in progress. "
    "You can contribute to the project on [GitHub](https://github.com/) "  # noqa: E501
    "\n\n"
    "This project takes more than inspiration from [KnowledgeGPT](https://github.com/mmz-001/knowledge_gpt) and [Llama_index](https://github.com/jerryjliu/llama_index)  \n"
    "Big up and thanks!  "  
)

