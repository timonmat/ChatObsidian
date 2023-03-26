# ui.py
# refactor common ui components here
import streamlit as st
import utils.tinydb as userdata
from utils.model_settings import get_sentence_transformer_dropdown
from utils.chroma import generate_chroma_compliant_name



def form_callback():
    st.session_state.FOLDER_PATH

def folder_path_input_box():
    if 'FOLDER_PATH' not in st.session_state:
        st.session_state['FOLDER_PATH'] = 'testdata/'
    return st.text_input(
                "Obsidian Folder to scan for notes",
                type="default",
                key='folder',
                placeholder="/Users/whoever/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault/",
                help="copy your obsidian vault path here with trailing slash",  
                value=st.session_state.get("FOLDER_PATH", ""),
                on_change=form_callback,
            )

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

# Function to create a new collection
def create_new_collection_ui():
    st.subheader('Create a new collection')
    new_collection_name = st.text_input('New collection name')
    new_collection_folder_path = folder_path_input_box()
    new_collection_model_name = get_sentence_transformer_dropdown()
    create_collection_button = st.button('Create new collection')
    collection_data = None
    if create_collection_button:
        if new_collection_name not in userdata.get_collections():
            chroma_compliant_name = generate_chroma_compliant_name(new_collection_name)
            collection_data = {
                "name": new_collection_name,
                "index_name": chroma_compliant_name,
                "folder_path": new_collection_folder_path,
                "model_name": new_collection_model_name
                }
            userdata.add_collection(collection_data)
            st.success(f"Created new collection: {new_collection_name}")
            st.experimental_rerun()
            
        else:
            st.error(f"Collection with name {new_collection_name} already exists.")
            
    return collection_data