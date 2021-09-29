import os
from utils import create_folder_name

folder_name = create_folder_name()


from connector import Mongo
import config

for database in config.DATABASE_NAMES:
    for collection in config.COLLECTION_NAMES:
        data = Mongo.get_instance()[database][collection].delete_many({})
