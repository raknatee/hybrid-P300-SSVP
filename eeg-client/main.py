from typing import TextIO
from pyOpenBCI import OpenBCICyton # type: ignore
import json
import time
import numpy as np
from typing import Union

import os
from modules.ConfigManager import ConfigManager
from modules.DataBuffer import DataBufferManager




config = ConfigManager.load_config_file()
    


local_file:TextIO
if config.DO_LOCAL_SAVE:
    local_file = open('./test-data.json','w')

global_buffer = DataBufferManager.get_instance()
SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count
def add_to_buffer(sample):

    temp:np.ndarray = np.array(sample.channels_data) * SCALE_FACTOR_EEG
    data = {
        'timestamp':time.time(),
        'data': temp.tolist()
    }
   
    global_buffer.add(data)

    if config.DO_LOCAL_SAVE:
        local_file.write(json.dumps(data)+"\n")

from modules.package import SenderThread

from modules.Dummy import OpenBCICytonDummy
board:Union[OpenBCICyton,OpenBCICytonDummy]

if config.DUMMY_MODE:
    board = OpenBCICytonDummy()
else:
    board = OpenBCICyton(port=config.SERIAL_PORT, daisy=False)

sender_thread = SenderThread()
try:
    sender_thread.start()
    board.start_stream(add_to_buffer)
except KeyboardInterrupt:
    sender_thread.stop()
    board.stop_stream()

finally:
    if config.DO_LOCAL_SAVE:
        local_file.close()