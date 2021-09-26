from threading import Thread
from queue import Queue
from io import TextIOWrapper
import json
class DumpQueueThread(Thread):
    is_running:bool
    queue:Queue
    def __init__(self,queue:Queue):
        Thread.__init__(self)

        self.is_running = True
        self.queue = queue

    def run(self):
        eeg_file:TextIOWrapper
        try:
            eeg_file = open('./data/eeg_data-data.json','a')
            while self.is_running and (not self.queue.empty()):
                data = json.dumps(self.queue.get())+",\n"
                eeg_file.write(data)
        finally:
            eeg_file.close()
    def stop(self):
        self.is_running = False
