import asyncio
import websockets
from threading import Thread
from queue import Queue
import config
import json
class EEGClient(Thread):
    def __init__(self) -> None:
        Thread.__init__(self)
        self.queue:Queue = Queue(-1)
    
    def is_done(self)->bool:
        return self.queue.empty()
    def add(self,data):
        self.queue.put(data)

    def get_data_from_queue(self):
        return self.queue.get()
    def run(self):

        async def hello():
            uri:str = f"ws://{config.HOST}:{config.PORT}/eeg_streaming"
            async with websockets.connect(uri) as ws:
                print("Connected")
                while True:
                    while not self.queue.empty():
                        data =json.dumps(self.get_data_from_queue())
                        await ws.send(data)
                        await ws.recv()
              
        asyncio.run(hello())