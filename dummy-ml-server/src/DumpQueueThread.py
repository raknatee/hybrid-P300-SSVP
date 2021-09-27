from threading import Thread
from queue import Queue
from io import TextIOWrapper
import json
from utils.iprint import iprint
import time

class DumpQueueThread(Thread):
    is_running:bool
    queue:Queue
    def __init__(self,queue:Queue):
        Thread.__init__(self)

        self.is_running = True
        self.queue = queue
    


    def run(self):
        eeg_file:TextIOWrapper
        iprint("start eeg file")
        try:
            eeg_file = open('./data/eeg_data-data.json','w')
            while self.is_running:
                # iprint("running")
                while not self.queue.empty():
            
                
                    data = json.dumps(self.queue.get())+"\n"
                    iprint(data)
                    eeg_file.write(data)
          
        finally:
            eeg_file.close()
            iprint("close eeg file successfully")
    def stop(self):
        self.is_running = False
