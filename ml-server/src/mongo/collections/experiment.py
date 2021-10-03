from mongo.connector import Mongo
from mongo.naming import MAIN_DATABASE

def insert_experiment_data(package:dict,collection):
    return Mongo.get_instance()[MAIN_DATABASE][collection].insert_one(package)