import os
from utils import create_folder_name

folder_name = create_folder_name()


from connector import Mongo
import config

answer = input(f"this script will drop {config.DATABASE_NAMES} y/Y:")
if(answer.upper() == "Y" ):
    for database in config.DATABASE_NAMES:
        data = Mongo.get_instance().drop_database(database)
   
else:
    print("cancel")
