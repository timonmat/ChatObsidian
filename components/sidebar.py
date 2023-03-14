import streamlit as st
import os

def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["api_key_configured"] = True
    os.environ['OPENAI_API_KEY'] = api_key

def add_to_sidebar():
    with st.sidebar:

        st.sidebar.success("Index and Query your Obsidian notes on the pages above.")

        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown(
        
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) above🔑\n"  # noqa: E501
            "2. Enter your obsidian notes folder on index page 📄\n"
            "3. Ask a questions on the Query page 💬\n"
        )

