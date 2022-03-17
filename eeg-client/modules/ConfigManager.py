from __future__ import annotations
import json
import os
from typing import Any, get_type_hints


CONFIG_FILE_NAME:str = "eeg-client-config.json"
class ConfigManager:

    @staticmethod
    def load_config_file()->Config:
        
        if(not os.path.exists(CONFIG_FILE_NAME)):
            sample_config = Config.create_sample_configuration()
            with open(CONFIG_FILE_NAME,'w') as config_file:
                json.dump(sample_config.to_dict(),config_file,indent=4)
            raise FileNotFoundError("created the configurate file, please run this again")
        else:
            with open(CONFIG_FILE_NAME,"r") as config_file:
                
                dict_obj:dict[str,Any] = json.load(config_file)

                config = Config.from_dict(dict_obj)
                return config


class Config:

    """
    Connection Config
    """
    SSL:bool
    HOST:str
    PORT:str
    SERIAL_PORT:str

    """
    App Config
    """
    VERBOSE:bool
    DUMMY_MODE:bool
    DO_LOCAL_SAVE:bool

    @staticmethod
    def create_sample_configuration()->Config:
        sample_config = Config()

        sample_config.SSL =  False
        sample_config.HOST = "localhost"
        sample_config.PORT = "8000"
        sample_config.SERIAL_PORT = "COM3"

        sample_config.VERBOSE = True
        sample_config.DUMMY_MODE = False
        sample_config.DO_LOCAL_SAVE = False

    
        

        return sample_config

    @staticmethod
    def from_dict(dict_obj:dict[str,Any])->Config:
        config = Config()

        for attr in get_type_hints(config):
            setattr(config,attr,dict_obj[attr])

        return config


    def to_dict(self)->dict[str,Any]:

        dict_obj = {}
  
        for attr in get_type_hints(self):
            dict_obj[attr] = getattr(self,attr)

        return dict_obj

