from __future__ import annotations
from typing import Any
import requests

import websocket #type:ignore
import json

from modules.ConfigManager import ConfigManager 
from threading import Thread

from modules.DataBuffer import DataBufferManager
import time
config = ConfigManager.load_config_file()


def verbose_print(*args,**kwargs):
    if(config.VERBOSE):
        print(*args,**kwargs)

class SenderThread(Thread):
    ws_helper:WSHelper
    last_sent_timestamp:float
    is_running:bool
    def __init__(self):
        Thread.__init__(self,daemon=True)
        self.ws_helper = WSHelper()
        self.last_sent_timestamp = time.time()
        self.is_running = True
    def run(self):
        """
        Step 1: sleep 3 second for making sure about missing Package
        Step 2: every 1 second sends the data
        """

        print("""
        
        sleep 7 seconds

        """)
        time.sleep(7)
        print("okay lets streaming")
        DataBufferManager.get_instance().get_and_clear()

        self.last_sent_timestamp = time.time()
        while self.is_running:
            now = time.time()
            if(now-self.last_sent_timestamp>=1):
                verbose_print(f"send {now}")
                self.last_sent_timestamp = now
                self.ws_helper.send_data()
                verbose_print(f"sent {time.time()}")
                verbose_print()
            
            time.sleep(0.01) # helps my cpu
    
    def stop(self):
        self.is_running = False


class WSHelper:
    second_counter:int
    ws:Any
    def __init__(self):
        try:
            resp = requests.get(f"http{'s' if config.SSL else ''}://{config.HOST}:{config.PORT}/db").json()
            self.mode = resp['current_mode']
            self.p_id = resp['current_participant_id']
        except (TypeError,KeyError):
            raise NoDBSetUp("you might go to setup database naming first and come back here later")
        print(f"mode :{self.mode}")
        print(f"Participant id:{self.p_id}")
        self.second_counter=1
        self.connect()

    def connect(self):
        print("start connecting ...")
        self.ws = websocket.WebSocket()
        self.ws.connect(f"ws{'s' if config.SSL else ''}://{config.HOST}:{config.PORT}/eeg_{self.mode}/{self.p_id}")
        print(self.ws)

    def send_data(self):

        data = DataBufferManager.get_instance().get_and_clear()
        for each_data in data:
            each_data['second_counter'] = self.second_counter
        verbose_print(f"{self.second_counter=} {len(data)=}")
        self.second_counter+=1
        self.ws.send(json.dumps({"data":data}))
        self.ws.recv()


class NoDBSetUp(KeyError):
    pass