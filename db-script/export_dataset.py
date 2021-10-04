import os
from utils import create_folder_name
import json
folder_name = create_folder_name()
os.mkdir(folder_name)

from connector import Mongo
import config

for database in config.DATABASE_NAMES:
    os.mkdir(os.path.join(folder_name,database))
    for collection in Mongo.get_instance()[database].list_collection_names():
        if(collection in config.COLLECTION_IGNORE):
            continue
        documents = [doc for doc in Mongo.get_instance()[database][collection].find({})]
        for document in documents:
            document["_id"] = str(document["_id"])
        with open(os.path.join(folder_name,database,f"{collection}-data.json"),"w") as save_file:
            
            save_file.write(json.dumps({"documents":documents}))

print("done!!!!!")