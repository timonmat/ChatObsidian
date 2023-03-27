from typing import Dict, Any
import streamlit as st
from llama_index import SimpleDirectoryReader, download_loader

from utils.logging import add_logging_config

def filename_to_metadata(filename: str) -> Dict[str, Any]:
    return {"filename": filename}


def load_docs_with_sdr(documents_folder, extensions=None):
    if extensions is None:
        extensions = [".md"]

    documents = SimpleDirectoryReader(documents_folder, recursive=True, required_exts=extensions, file_metadata=filename_to_metadata).load_data()
    documents = [doc for doc in documents if doc.text.strip() != '']
    for i in range(len(documents)):
        documents[i].doc_id = str(i)
    return documents


def clean_filenames_for_obsidian(documents, folder_path):
    for doc in documents:
        doc.extra_info['filename'] = doc.extra_info['filename'].replace(folder_path, '')
    return documents





