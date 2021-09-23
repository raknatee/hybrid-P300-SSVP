from fastapi import FastAPI,WebSocket
from typing import Optional
import sys
import time
from queue import Queue
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


eeg_queue = Queue(250)

def iprint(*args,**kwargs):
    print(*args,**kwargs,file=sys.stderr)

@app.websocket("/eeg_streaming")
async def eeg_streaming(ws:WebSocket):
    try:
        await ws.accept()
        EEGClient.client = ws
       
        while True:
            msg = await EEGClient.client.receive_json()
            iprint(msg)

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
    try:
        await ws.accept()
        while True:
            await ws.send_json({
                "cmd":"next"
            })

            data:dict = await ws.receive_json()
            print(data)

    finally:
        pass

def ml_predict():
    # it looks like this function take soooooo long time
    time.sleep(2)
    return {
        "guessed_grid": 5,
        "guessed_index": 5
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
            print(round_timestamp)

            prediction_result = ml_predict()
            await ws.send_json(prediction_result)

    finally:
        pass