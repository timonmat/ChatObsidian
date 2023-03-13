import streamlit as st
from components.sidebar import add_to_sidebar
from llama_index import GPTSimpleVectorIndex
from pathlib import Path
from llama_index import download_loader

st.set_page_config(
    page_title="Index",
    page_icon="👋",
)

st.write("# Index your Documents 👋")

def clear_submit():
    st.session_state["submit"] = False

MarkdownReader = download_loader("MarkdownReader")

loader = MarkdownReader()
folder_path = Path('./testdata')
documents = []
for file_path in folder_path.glob("*.md"):
    doc = loader.load_data(file=file_path)
    for array_elem in doc:
        documents.append(array_elem)

if st.session_state.get("api_key_configured"):
    if Path('index.json').exists():
        index = GPTSimpleVectorIndex.load_from_disk('index.json')
    else:
        index = GPTSimpleVectorIndex(documents)
        index.save_to_disk('index.json')
          


add_to_sidebar()


st.write("Document parts:" + str(len(documents)))
st.write(documents)