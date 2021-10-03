import os
import json

folder_name = input("which folder?:")
from connector import Mongo

def read_line(path):
    with open(path,'r') as collection_file:
        while line:= collection_file.readline():
            yield line

def read_objects(path:str)->list[dict]:
    documents = []
    for document in read_line(path):
        documents.append(json.loads(document))
    return documents

for database in os.listdir(os.path.join(folder_name)):
    for collection in os.listdir(os.path.join(folder_name,database)):
        documents = read_objects(os.path.join(folder_name,database,collection))
        Mongo.get_instance()[database][collection.replace("-data.json","")].insert_many(documents)