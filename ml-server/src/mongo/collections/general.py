
from mongo.connector import Mongo
from mongo.naming import MAIN_DATABASE,GENERAL_COLLECTION
from enum import Enum

def get_collection_connector():
    return Mongo.get_instance()[MAIN_DATABASE][GENERAL_COLLECTION]

def init_document():

    object_1 = get_collection_connector().find_one({
        "type": "experiment_config"
    })

    if(object_1 is None):
        get_collection_connector().insert_one({
            "type": "experiment_config",
        })
        set_data("offline","AXXSXX")
        set_eeg_client_status(EEGClientStatus.unconnected)
  
def get_data():

    config_object = get_collection_connector().find_one({ "type": "experiment_config"},
    {"_id":0,"current_mode":1,"current_participant_id":1})

    return config_object

def set_data(current_mode:str,current_p_id:str)->None:
    get_collection_connector().update_one({"type":"experiment_config"},
    {"$set":{
        "current_mode":current_mode,
        "current_participant_id": current_p_id.upper()
    }})
 
class EEGClientStatus(Enum):
    connected = "connected"
    unconnected = "unconnected"

def set_eeg_client_status(status:EEGClientStatus):
    get_collection_connector().update_one({ "type": "experiment_config"},
    {"$set":{
        "eeg_client_status":str(status.value)
    }})

def get_eeg_client_status():
    return get_collection_connector().find_one({ "type": "experiment_config"},
    {"_id":0,"eeg_client_status":1}
    )