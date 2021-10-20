
import os
import pickle
from typing import Any, Callable, TypeVar

T= TypeVar('T')
def load(func:Callable[[],T],filename:str,is_force_load:bool=False)->T:
    data:Any

    if(is_force_load):
        data = func()
    else:
        if(not os.path.exists(filename)):
            data = func()
            with open(filename,"wb") as pkl_file:
                pickle.dump(data,pkl_file)
        else:
            with open(filename,"rb") as pkl_file:
                data = pickle.load(pkl_file)
    
    return data