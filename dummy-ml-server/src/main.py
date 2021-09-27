from fastapi import FastAPI,WebSocket  # type: ignore
from typing import Optional,TextIO
import sys
import time

import random

import json

from DumpQueueThread import DumpQueueThread
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

# from eeg_stream_endpoint.eeg_stream import app as eeg_stream_app
# app.include_router(eeg_stream_app)

from eeg_stream_endpoint.eeg_stream import EEGClientListeningThread
eeg_client_listening_thread= EEGClientListeningThread()
eeg_client_listening_thread.start()

from eeg_stream_endpoint.eeg_stream import EEGClient
@app.get("/check_headset")
def check_headset():
    status:str
    if(EEGClient.client is None):
        status = "no connection"
    else:
        status = "connected"
    print(f"{status=}")
    return {
        'status':status
    }



from eeg_stream_endpoint.eeg_stream import eeg_queue

@app.websocket("/begin_offline_mode")
async def begin_offline_mode(ws:WebSocket):
    dump_thread = DumpQueueThread(eeg_queue)
    try:
        await ws.accept()
        
        dump_thread.start()
        experiment_file:TextIO = open('./data/experiment-data.json','w')
        while True:
            await ws.send_json({
                "cmd":"next"
            })

            data:dict = await ws.receive_json()
            experiment_file.write(json.dumps(data)+"\n")

    finally:
        dump_thread.stop()
        experiment_file.close()
    

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

def ml_predict():
    # it looks like this function take soooooo long time
    time.sleep(2)
    guess = random.choice(possible_result)
    return {
        "guessed_grid": guess['grid'],
        "guessed_index": random.choice(guess['index'])
    }

@app.websocket("/begin_online_mode")
async def begin_online_mode(ws:WebSocket):
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