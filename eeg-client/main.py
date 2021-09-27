from typing import TextIO
from pyOpenBCI import OpenBCICyton # type: ignore
from module.ws import EEGClient
import config
import json
from datetime import datetime
import time
import sys

eeg_client = EEGClient()
eeg_client.start()

local_file:TextIO
if config.DO_LOCAL_SAVE:
    local_file = open('./test-data.json','w')
def add_to_buffer(sample):
    data = {
        'timestamp':datetime.now().timestamp(),
        'data':sample.channels_data
    }
    eeg_client.add(data)

    if config.DO_LOCAL_SAVE:
        local_file.write(json.dumps(data)+"\n")


  

board = OpenBCICyton(port=config.SERIAL_PORT, daisy=False)
try:
    board.start_stream(add_to_buffer)
except KeyboardInterrupt:
    board.stop_stream()
    while True:
        print(f"please wait for submiting data left {eeg_client.queue.qsize()}")
        if(eeg_client.is_done()):
            quit()
        time.sleep(1)
finally:
    if config.DO_LOCAL_SAVE:
        local_file.close()