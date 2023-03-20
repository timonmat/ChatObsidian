#Faq.py
import streamlit as st
from components.sidebar import add_to_sidebar

st.set_page_config(
    page_title="FAQ",
    page_icon="❕",
)

add_to_sidebar()

def faq():
    st.markdown(
        """
# FAQ ❕

## How does ChatObsidian work?
The folder entered on Index page is recursively searched for Markdown files, which are chunked and
indexed with OpenAI embeddings services. The index is saved locally.
When asking a question, embeddings are retrieved for the question, and semantically relevant chunks are retrieved from the index context.
both the question and context are provided with a template to OpenAI GPT which generates the final answer.

## QA assistant prompt template
You can modify the prompt template to make GPT3 work in a way better suited to your Notes content by modifying the file /utils/qa_template.py 

## Is my data private?
Current version should only be run locally as it saves the index on disk. Do not deploy as an online service.
OpenAI API's are for indexing all of your notes. OpenAI has stated that no data via api's is saved/re-used,
but it is an external service, and some are uncomfortable in using any external services on personal data.

## OpenAI API rate limits
If you are using a free OpenAI API key, it will take a while to index
your document. This is because the free API key has strict [rate limits](https://platform.openai.com/docs/guides/rate-limits/overview).
To speed up the indexing process, you can use a paid API key.

## Are the answers 100% accurate?
No, the answers are not 100% accurate. GPT3 is prone to occasional hallucination even when provided with context data.
Read the responses with thought, and decide for yourself.
This is made for fun, so don't take it  too seriously.
"""
    )

faq()