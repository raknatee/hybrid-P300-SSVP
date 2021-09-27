from fastapi import FastAPI,WebSocket  # type: ignore
import sys
import time
from typing import Optional
import random

import json
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

class EEGClient:
    client:Optional[WebSocket] = None

@app.get("/check_headset")
def check_headset():
    status:str
    if(EEGClient.client is None):
        status = "no connection"
    else:
        status = "connected"
    return {
        'status':status
    }

@app.websocket("/eeg_streaming")
async def eeg_streaming(ws:WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            iprint(data)
            await ws.send_text('1')
    finally:
        EEGClient.client = None

    

