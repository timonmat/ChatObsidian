# ui.py
# refactor common ui components here
import streamlit as st
import utils.tinydb as userdata
from utils.model_settings import get_sentence_transformer_dropdown
from utils.chroma import generate_chroma_compliant_name
from utils.files_helper import open_finder_to_folder
from components.sidebar import set_folder_path_state
import urllib.parse
from enum import Enum


def folder_path_input_box():
    folder = st.text_input(
                "Folder to scan for notes",
                type="default",
                placeholder="/Users/whoever/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault/",
                help="copy your obsidian vault path here with trailing slash",  
                value=st.session_state.get("FOLDER_PATH", ""),
            )
    if folder:
        set_folder_path_state(folder)
    return folder

# Function to generate collection selection UI
def collection_selection_ui(collections):
    indexnumber = 1 if len(collections) >= 1 else 0 
    selected_collection = st.selectbox('Select a collection', 
                                       [''] + collections, 
                                       index=indexnumber 
                                       )
    if selected_collection:
        collection_data = userdata.load_collection_data(selected_collection)
        #st.write(f"Folder path: \'{collection_data['folder_path']}\' ,Model name: {collection_data['model_name']}")
        return collection_data
    else:
        return None

from enum import Enum

class FileExtensions(Enum):
    MD = ".md"
    TXT = ".txt"
    JSON = ".json"
    DOCX = ".docx"
    PPTX = ".pptx"
    EPUB = ".epub"
    PDF = ".pdf"
    CSV = ".csv"



class CollectionType(Enum):
    FOLDER = "folder"
    OBSIDIAN = "obsidian"

# Function to create a new collection
def create_new_collection_ui():
    st.subheader('Create a new collection')
    new_collection_name = st.text_input('New collection name')
    new_collection_folder_path = folder_path_input_box()
    new_collection_model_name = get_sentence_transformer_dropdown()
    
    # Select file extensions
    new_collection_file_extensions = st.multiselect(
        'Select file extensions',
        options=[ext.value for ext in FileExtensions],
        default=[FileExtensions.MD.value]
    )

    # Select collection type
    new_collection_type = st.selectbox(
        'Select collection type',
        options=[ctype.value for ctype in CollectionType],
        index=[ctype.value for ctype in CollectionType].index(CollectionType.OBSIDIAN.value)
    )


    create_collection_button = st.button('Create new collection')
    collection_data = None
    if create_collection_button:
        if new_collection_name not in userdata.get_collections():
            chroma_compliant_name = generate_chroma_compliant_name(new_collection_name)
            collection_data = {
                "name": new_collection_name,
                "index_name": chroma_compliant_name,
                "folder_path": new_collection_folder_path,
                "model_name": new_collection_model_name,
                "file_extensions": new_collection_file_extensions,
                "collection_type": new_collection_type
            }
            userdata.add_collection(collection_data)
            st.success(f"Created new collection: {new_collection_name}")
            

        else:
            st.error(f"Collection with name {new_collection_name} already exists.")
    
    return collection_data

def render_sources(response, collection_type='obsidian'):
    for node in response.source_nodes:
        docid, filename, content = node.source_text.strip().split('\n\n', 2)
        filename = filename.split(': ')[1]
        content = content.strip()
                
        if collection_type == 'obsidian':
            url = (f'obsidian://open?file={urllib.parse.quote(filename)}')
            mdlink = (f'[Open in Obsidian]({url})')
            st.markdown(f"Similarity: {node.similarity}")
            st.markdown(f"Filename: {filename}")
            st.markdown(mdlink)
        elif collection_type == 'folder':
            st.markdown(f"Similarity: {node.similarity}")
            st.markdown(f"Filename: {filename}")
            url = (f'file://{urllib.parse.quote(filename)}')
            mdlink = (f'[Open File]({url})')
            st.markdown(mdlink)
                         
        with st.expander("Matching Text Chunk"):
            st.markdown(content)

