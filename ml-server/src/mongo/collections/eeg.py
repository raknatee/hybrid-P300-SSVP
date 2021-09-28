from mongo.connector import Mongo
from mongo.naming import MAIN_DATABASE,TEST_COLLECTION

def insert_eeg_signals(package:dict,collection=TEST_COLLECTION):

    
    return Mongo.get_instance()[MAIN_DATABASE][collection].insert_many(package['data'])


