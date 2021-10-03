import os
from utils import create_folder_name

folder_name = create_folder_name()


from connector import Mongo
import config


answer = input(f"this script will drop all collections in {config.DATABASE_NAMES} except it is in {config.COLLECTION_IGNORE}  y/Y:")
if(answer.upper() == "Y" ):
    for database in config.DATABASE_NAMES:
        for collection in Mongo.get_instance()[database].list_collection_names():
            if(collection in config.COLLECTION_IGNORE):
                continue
            Mongo.get_instance()[database][collection].drop()
   
else:
    print("cancel")
