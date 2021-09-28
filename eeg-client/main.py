from typing import TextIO
from pyOpenBCI import OpenBCICyton # type: ignore
import config
import json
from datetime import datetime
import time
import sys
from typing import Union

from modules.package import EEGPackage

eeg_package = EEGPackage()

local_file:TextIO
if config.DO_LOCAL_SAVE:
    local_file = open('./test-data.json','w')


def add_to_buffer(sample):
    data = {
        'timestamp':datetime.now().timestamp(),
        'data':sample.channels_data
    }
   
    eeg_package.add(data)

    if config.DO_LOCAL_SAVE:
        local_file.write(json.dumps(data)+"\n")


from modules.Dummy import OpenBCICytonDummy
board:Union[OpenBCICyton,OpenBCICytonDummy]

if config.DUMMY_MODE:
    board = OpenBCICytonDummy()
else:
    board = OpenBCICyton(port=config.SERIAL_PORT, daisy=False)

try:
    board.start_stream(add_to_buffer)
except KeyboardInterrupt:
    board.stop_stream()
    print(len(eeg_package.data))
finally:
    if config.DO_LOCAL_SAVE:
        local_file.close()