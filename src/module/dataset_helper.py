from __future__ import annotations
from typing import Any, TypeVar
import random



from mongo.query.get_dataset import P300Data





class P300DataFilter:
    data:list[P300Data]
    filtered_data:list[P300Data]
    def __init__(self,data:list[P300Data]) -> None:
        super().__init__()
        self.data = data
        self.filtered_data = []

    def random_seed(self,seed:int)->P300DataFilter:
        random.seed(seed)
        return self


    def _split_class(self)->dict[str,list[P300Data]]:
        count_dict:dict[str,list[P300Data]] = {}
        for each_data in self.data:
            
            if(str(each_data.target) not in count_dict):
                count_dict[str(each_data.target)] = []
                
            count_dict[str(each_data.target)].append(each_data)
            

        return count_dict

    
     
    def balance_class(self)->P300DataFilter:
        count_dict = self._split_class()
        min_number = min([len(count_dict[data]) for data in count_dict])
        for clazz in count_dict:
            random.shuffle(count_dict[clazz])
            count_dict[clazz] = count_dict[clazz][:min_number]
        for key in count_dict:
            self.filtered_data = [*self.filtered_data,*count_dict[key]]
        
        return self

   

    def shuffle(self)->P300DataFilter:
        random.shuffle(self.filtered_data)
        return self
    def done(self)->list[P300Data]:
        if(len(self.filtered_data)!=0):
            return self.filtered_data
        return self.data

T = TypeVar('T')
def train_test_splitter(data:list[T],train_size:float,shuffle=True)->tuple[list[T],list[T]]:
    if shuffle:
        random.shuffle(data)
    mid = int(len(data)*train_size)
    return (data[:mid],data[mid:])


