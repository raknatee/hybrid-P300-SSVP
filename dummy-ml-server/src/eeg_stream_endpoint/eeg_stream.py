# from fastapi import APIRouter,WebSocket,WebSocketDisconnect
# from typing import Optional
from utils.iprint import iprint
from queue import Queue
import asyncio
from threading import Thread
from typing import Optional,Any
import websockets #type: ignore
import json
eeg_queue:Queue = Queue(300*6)

class EEGClient:
    client:Optional[Any]=None

# app = APIRouter()

# @app.websocket("/eeg_streaming")
# async def eeg_streaming(ws:WebSocket):
#     try:
#         await ws.accept()
#         EEGClient.client = ws

#         while True:
#             iprint("eeg_stream is waiting for new msg")
#             msg = await EEGClient.client.receive_json()
#             eeg_queue.put(msg)
#             iprint(eeg_queue.qsize())

#     finally:
#         EEGClient.client = None

async def dump(websocket, path):
    data = await websocket.recv()
    data = json.loads(data)
    while True:
        iprint("eeg_stream is waiting for new msg")
        data = await websocket.recv()
        data = json.loads(data)
        eeg_queue.put(data)
        iprint(eeg_queue.qsize())
        

async def main():
    async with websockets.serve(dump, "0.0.0.0", 8001):
        await asyncio.Future()  # run forever

class EEGClientListeningThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        asyncio.run(main())