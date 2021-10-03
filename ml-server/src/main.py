
from fastapi import FastAPI,WebSocket  # type: ignore
import time
import random
import mongo.collections.eeg as eeg_collection
import mongo.collections.experiment as experiment_collection
from utils.iprint import iprint
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import mongo.collections.general as general_collection
general_collection.init_document()

@app.post("/db")
def db_post(json_data:dict):
   
    general_collection.set_data(json_data["current_mode"],json_data["current_participant_id"])

@app.get("/db")
def db_get():
    return general_collection.get_data()

@app.post("/eeg_offline/{p_id}")
def eeg(json_data:dict,p_id:str):
    collection_name = f"{p_id}-EEG-offline-collection"
    eeg_collection.insert_eeg_signals(json_data,collection_name)
 

@app.websocket("/begin_offline_mode/{p_id}")
async def begin_offline_mode(ws:WebSocket,p_id:str):
 
    collection_name = f"{p_id}-experiment-offline-collection"
    
    await ws.accept()
    

    
    while True:
        await ws.send_json({
            "cmd":"next"
        })

        data:dict = await ws.receive_json()
        experiment_collection.insert_experiment_data(data,collection_name)


    

possible_result = [
    {'grid':0,'index':list(range(9))},
    {'grid':1,'index':list(range(9))},
    {'grid':2,'index':list(range(9))},
    {'grid':3,'index':list(range(9))},
    {'grid':4,'index':list(range(9))},
    {'grid':5,'index':list(range(9))},
    {'grid':6,'index':list(range(9))},
    {'grid':7,'index':list(range(9))},
    {'grid':10,'index':list(range(3))},
    {'grid':11,'index':list(range(11))},

]
 

@app.post("/eeg_online/{p_id}")
def eeg_online(json_data:dict,p_id:str):
    collection_name = f"{p_id}-EEG-online-collection"
    eeg_collection.insert_eeg_signals(json_data,collection_name)


def ml_predict():
    # it looks like this function take soooooo long time
    time.sleep(2)
    guess = random.choice(possible_result)
    return {
        "guessed_grid": guess['grid'],
        "guessed_index": random.choice(guess['index'])
    }

@app.websocket("/begin_online_mode/{p_id}")
async def begin_online_mode(ws:WebSocket,p_id:str):
    try:
        await ws.accept()
        while True:
            await ws.send_json({
                "cmd":"next"
            })

            round_timestamp:dict = await ws.receive_json()
            iprint(round_timestamp)

            prediction_result = ml_predict()
            prediction_result['cmd'] = "output_model"
            iprint(prediction_result)
            await ws.send_json(prediction_result)

    finally:
        pass