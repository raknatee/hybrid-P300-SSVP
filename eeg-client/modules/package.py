import requests
import config
class EEGPackage:
    data:list

    def __init__(self):
        self.data = []

    def add(self,data):
        self.data.append(data)
  
        if(len(self.data)>=config.DATA_SIZE):
            res = requests.post(f"http://{config.HOST}:{config.PORT}/eeg_offline",json={"data":self.data})
            
            self.data = []
