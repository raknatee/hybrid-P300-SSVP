import os
import json
from bson.objectid import ObjectId #type: ignore

folder_name = input("which folder?:")
from connector import Mongo


def read_objects(path:str)->list[dict]:
    obj = {}
    with open(path,'r') as collection_file:
        obj = json.loads(collection_file.read())

    return obj['documents']

for database in os.listdir(os.path.join(folder_name)):
    for collection in os.listdir(os.path.join(folder_name,database)):
        documents = read_objects(os.path.join(folder_name,database,collection))
        for document in documents:
            document["_id"] = ObjectId(document["_id"])
        Mongo.get_instance()[database][collection.replace("-data.json","")].insert_many(documents)