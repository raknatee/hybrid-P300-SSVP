from typing import TextIO
from pyOpenBCI import OpenBCICyton # type: ignore
import json
from datetime import datetime
import numpy as np
from typing import Union

import os




if(not os.path.exists("./eeg_client_config.py")):
    from config_template import config_template
    with open("./eeg_client_config.py",'w') as config_file:
        config_file.write(config_template)
    raise FileNotFoundError("created the configurate file, please run this again")
else:
    import eeg_client_config as config
    
from modules.package import EEGPackage
eeg_package = EEGPackage()

local_file:TextIO
if config.DO_LOCAL_SAVE:
    local_file = open('./test-data.json','w')

SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count
def add_to_buffer(sample):

    temp:np.ndarray = np.array(sample.channels_data) * SCALE_FACTOR_EEG
    data = {
        'timestamp':datetime.now().timestamp(),
        'data': temp.tolist()
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