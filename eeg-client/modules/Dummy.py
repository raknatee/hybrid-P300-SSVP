from threading import Thread
import time
import config

class MockData:
    channels_data:list
    def __init__(self,channels_data):
        self.channels_data = channels_data

class OpenBCICytonDummy(Thread):
    is_running:bool

    def __init__(self):
        Thread.__init__(self)
        print("begin Dummy Mode")
        self.is_running = True

    def start_stream(self,func):
   
        while self.is_running:
            for i in range(config.DATA_SIZE):
                func(MockData([9.9]*8))



    
    def stop_stream(self):
        self.is_running = False

