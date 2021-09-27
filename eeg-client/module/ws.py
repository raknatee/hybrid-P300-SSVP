import asyncio
import websockets
from threading import Thread
from queue import Queue
import config
import json
class EEGClient(Thread):
    def __init__(self) -> None:
        Thread.__init__(self,daemon=True)
        self.queue:Queue = Queue(300*6)
    

    def add(self,data):
        self.queue.put(data)

    def get_data_from_queue(self):
        return self.queue.get()
    def run(self):

        async def hello():
            uri:str = f"ws://{config.HOST}:{config.PORT}"
            async with websockets.connect(uri) as ws:
                print("Connected")
                while True:
                    while not self.queue.empty():
                        data =json.dumps(self.get_data_from_queue())
                        print(data)
                        await ws.send(data)
              
        asyncio.run(hello())