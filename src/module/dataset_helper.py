from __future__ import annotations
from typing import Any, TypeVar,Generic
from abc import ABCMeta,abstractmethod
import random

from torch import Tensor

T = TypeVar('T')

class SupervisedData(metaclass=ABCMeta):
    @abstractmethod
    def get_y(self)->Any:
        pass

    @abstractmethod
    def get_x(self)->Any:
        pass

class DataExtractor:
    data:list[SupervisedData]
    filtered_data:list[SupervisedData]
    def __init__(self,data:list[SupervisedData]) -> None:
        super().__init__()
        self.data = data
        self.filtered_data = []

    def random_seed(self,seed:int)->DataExtractor:
        random.seed(seed)
        return self


    def _split_class(self)->dict[str,list[SupervisedData]]:
        count_dict:dict[str,list[SupervisedData]] = {}
        for each_data in self.data:
            
            if(str(each_data.get_y()) not in count_dict):
                count_dict[str(each_data.get_y())] = []
                
            count_dict[str(each_data.get_y())].append(each_data)
            

        return count_dict

    
     
    def balance_class(self)->DataExtractor:
        count_dict = self._split_class()
        min_number = min([len(count_dict[data]) for data in count_dict])
        for clazz in count_dict:
            random.shuffle(count_dict[clazz])
            count_dict[clazz] = count_dict[clazz][:min_number]
        for key in count_dict:
            self.filtered_data = [*self.filtered_data,*count_dict[key]]
        
        return self

    def shuffle(self)->DataExtractor:
        random.shuffle(self.filtered_data)
        return self
    def done(self)->list[SupervisedData]:
        return self.filtered_data
    
def train_test_splitter(data:list[SupervisedData],train_size:float,shuffle=True)->tuple[list[SupervisedData],list[SupervisedData]]:
    random.shuffle(data)
    mid = int(len(data)*train_size)
    return (data[:mid],data[mid:])


def to_one_hot(y:Tensor)->list[int]:
    return (list(map(int,(y>.5).flatten().tolist())))

def acc(y_true:list[int],y_hat:list[int])->float:
    assert len(y_true) == len(y_hat)
    correct:int = 0

    for i in range(len(y_true)):
        if(y_true[i] == y_hat[i]):
            correct +=1
  
    return correct/len(y_true)
    