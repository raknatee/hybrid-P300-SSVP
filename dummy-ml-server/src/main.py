from fastapi import FastAPI,WebSocket  # type: ignore
from typing import Optional
import sys
import time
from queue import Queue
import random
from io import TextIOWrapper
import json
import threading
from DumpQueueThread import DumpQueueThread
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EEGClient:
    client:Optional[WebSocket]=None


eeg_queue:Queue = Queue(250)

def iprint(*args,**kwargs):
    print(*args,**kwargs,file=sys.stderr)

@app.websocket("/eeg_streaming")
async def eeg_streaming(ws:WebSocket):
    try:
        await ws.accept()
        EEGClient.client = ws
       
        while True:
            msg = await EEGClient.client.receive_json()
            eeg_queue.put(msg)

    finally:
        EEGClient.client = None

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




@app.websocket("/begin_offline_mode")
async def begin_offline_mode(ws:WebSocket):
    dump_thread = DumpQueueThread(eeg_queue)
    try:
        await ws.accept()
        
        dump_thread.start()
        experiment_file:TextIOWrapper = open('./data/experiment.json','a')
        while True:
            await ws.send_json({
                "cmd":"next"
            })

            data:dict = await ws.receive_json()
            print(data)
            experiment_file.write(json.dumps(data)+",\n")

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