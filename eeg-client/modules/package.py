
from typing import Any
import requests
import eeg_client_config as config
# import websockets
import websocket
import asyncio
import json
class EEGPackage:
    data:list
    ws:Any
    def __init__(self):
        self.data = []
        try:
            resp = requests.get(f"http://{config.HOST}:{config.PORT}/db").json()
            self.mode = resp['current_mode']
            self.p_id = resp['current_participant_id']
        except (TypeError,KeyError):
            raise NoDBSetUp("you might go to setup database naming first and come back here later")
        print(f"mode :{self.mode}")
        print(f"Participant id:{self.p_id}")
        asyncio.run(self.connect())

    async def connect(self):
        print("start connecting ...")
        self.ws = await websockets.connect(f"{config.PROTOCOL}://{config.HOST}:{config.PORT}/eeg_{self.mode}/{self.p_id}")
        print(self.ws)
    async def send_data(self):
        await self.ws.send(json.dumps({"data":self.data}))
        await self.ws.recv()

    def add(self,data):
        self.data.append(data)
  
        if(len(self.data)>=config.DATA_SIZE):
            print("tring to submit")
            asyncio.run(self.send_data())
            self.data = []

class NoDBSetUp(KeyError):
    pass