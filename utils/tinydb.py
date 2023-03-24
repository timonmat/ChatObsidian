# tinydb.py
from tinydb import TinyDB, Query
import json

# Initialize the TinyDB database
db = TinyDB('./data/userdata.json')

# Function to get available collections
def get_collections():
    return [item['name'] for item in db.all()]

# Function to add a new collection
def add_collection(name, folder_path, model_name):
    db.insert({'name': name, 'folder_path': folder_path, 'model_name': model_name})

# Function to load collection data
def load_collection_data(name):
    Collection = Query()
    return db.search(Collection.name == name)[0]

# Function to update collection data
def update_collection_data(name, folder_path, model_name):
    Collection = Query()
    db.update({'folder_path': folder_path, 'model_name': model_name}, Collection.name == name)

