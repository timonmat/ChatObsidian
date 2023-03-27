# tinydb.py
from tinydb import TinyDB, Query
import json

# Initialize the TinyDB database
db = TinyDB('./data/userdata.json')

class Collection:
    def __init__(self, name, folder_path, model_name, index_name, collection_type=None, file_extensions=None):
        self.name = name
        self.folder_path = folder_path
        self.model_name = model_name
        self.index_name = index_name
        self.collection_type = collection_type if collection_type is not None else 'obsidian' 
        self.file_extensions = file_extensions if file_extensions is not None else [".md"]

# Assuming that collection_data is a dictionary
def create_collection_from_dict(collection_data):
    return Collection(**collection_data)

# Function to get available collections
def get_collections():
    return [item['name'] for item in db.all()]

# Function to add a new collection
def add_collection(collection_data):
    db.insert(collection_data)

# Function to load collection data
def load_collection_data(name):
    Collection = Query()
    return create_collection_from_dict(db.search(Collection.name == name)[0])

# Function to update collection data
def update_collection_data(name, collection_data):
    Collection = Query()
    db.update(collection_data, Collection.name == name)

