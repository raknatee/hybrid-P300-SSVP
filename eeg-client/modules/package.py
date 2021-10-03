
import requests
import eeg_client_config as config
class EEGPackage:
    data:list

    def __init__(self):
        self.data = []
        try:
            resp = requests.get(f"{config.PROTOCOL}://{config.HOST}:{config.PORT}/db").json()
            self.mode = resp['current_mode']
            self.p_id = resp['current_participant_id']
        except (TypeError,KeyError):
            raise NoDBSetUp("you might go to setup database naming first and come back here later")
        print(f"mode :{self.mode}")
        print(f"Participant id:{self.p_id}")

    def add(self,data):
        self.data.append(data)
  
        if(len(self.data)>=config.DATA_SIZE):
            res = requests.post(f"{config.PROTOCOL}://{config.HOST}:{config.PORT}/eeg_{self.mode}/{self.p_id}",json={"data":self.data})
            
            self.data = []

class NoDBSetUp(KeyError):
    pass