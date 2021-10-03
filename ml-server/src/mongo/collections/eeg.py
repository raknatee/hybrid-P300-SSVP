from mongo.connector import Mongo
from mongo.naming import MAIN_DATABASE

def insert_eeg_signals(package:dict,collection):

    
    return Mongo.get_instance()[MAIN_DATABASE][collection].insert_many(package['data'])


