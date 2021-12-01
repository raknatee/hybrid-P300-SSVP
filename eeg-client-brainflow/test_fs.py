import threading
from typing import Any, TextIO
from pyOpenBCI import OpenBCICyton # type: ignore
import json
from datetime import datetime
import numpy as np
from queue import Queue
import os
import time


q:list[Any] = []
list_fs:list[int] = []
lock = threading.Lock()
SERIAL_PORT = "COM3"
SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count


def add_to_buffer(sample):

    temp:np.ndarray = np.array(sample.channels_data) * SCALE_FACTOR_EEG
    data = {
        'timestamp':datetime.now().timestamp(),
        'data': temp.tolist()
    }
   
    q.append(data)

timer:int = 0
def getter_thread():
    global q
    global timer
    while True:

        current_sample:list
        with lock:
            current_sample = [*q]
            q = []

        list_fs.append((current_sample))
        if(timer%10==0):
            print(f"{timer=}")
        timer+=1
        time.sleep(1)


board = OpenBCICyton(port=SERIAL_PORT, daisy=False)
threading.Thread(target=getter_thread,daemon=True).start()

time_start:float
time_end:float

try:
    time_start = time.time()
    board.start_stream(add_to_buffer)
except KeyboardInterrupt:
    board.stop_stream()
    time_end = time.time()
    with open("data.json","w") as json_file:
        json.dump({
            "time_start":time_start,
            "time_end":time_end,
            "total":time_end-time_start,
            "list_fs":list_fs
            },json_file,indent=4)
