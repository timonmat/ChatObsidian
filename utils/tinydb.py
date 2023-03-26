# tinydb.py
from tinydb import TinyDB, Query
import json

# Initialize the TinyDB database
db = TinyDB('./data/userdata.json')

# Function to get available collections
def get_collections():
    return [item['name'] for item in db.all()]

# Function to add a new collection
def add_collection(collection_data):
    db.insert(collection_data)

# Function to load collection data
def load_collection_data(name):
    Collection = Query()
    return db.search(Collection.name == name)[0]

# Function to update collection data
def update_collection_data(name, collection_data):
    Collection = Query()
    db.update(collection_data, Collection.name == name)

