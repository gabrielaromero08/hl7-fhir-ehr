from pymongo import MongoClient
from pymongo.server_api import ServerApi


def connect_to_mongodb(db_name, collection_name):
    uri = "mongodb+srv://gabyleal:Diana2024-1@ejercicio1.tttur.mongodb.net/?retryWrites=true&w=majority&appName=EJERCICIO1"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[db_name]
    collection = db[collection_name]
    return collection
