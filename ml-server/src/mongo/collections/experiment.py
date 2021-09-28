from mongo.connector import Mongo
from mongo.naming import MAIN_DATABASE,TEST_EXPERIMENT_COLLECTION

def insert_experiment_data(package:dict,collection=TEST_EXPERIMENT_COLLECTION):
    return Mongo.get_instance()[MAIN_DATABASE][collection].insert_one(package)