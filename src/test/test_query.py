from typing import cast
from mongo.query.get_dataset import P300Data, get_p300_dataset_by_p_id
from mongo.query.get_torch_dataset import P300Dataset 
from module.experiment_info import ATTEMPT1
from module.dataset_helper import DataExtractor,train_test_splitter


def test_get_p300_dataset():
 
    for data in [get_p300_dataset_by_p_id("A01S01",ATTEMPT1),get_p300_dataset_by_p_id("A01S02",ATTEMPT1),get_p300_dataset_by_p_id("A01S03",ATTEMPT1)  ]:
        for d in data:
            print(d.target,d.eeg.shape)
            assert isinstance(d.target,bool)
            assert d.eeg.shape == (128,7)
  
def test_get_p300_dataset_torch():
    data = P300Dataset(get_p300_dataset_by_p_id("A01S01",ATTEMPT1))
    assert len(data) == 138
    


    ori_data  = DataExtractor(get_p300_dataset_by_p_id("A01S01",ATTEMPT1))
    data2 = ori_data._split_class()
    assert len(data2['True']) + len(data2['False']) == 138

    data3 = cast(list[P300Data],ori_data.random_seed(10).balance_class().shuffle().done()) 
    
    assert len(data3) == 18*2

    train_set,test_set = train_test_splitter(data3,.7)

    assert (0 < len(test_set) < len(train_set) ) and (len(test_set)+len(train_set) == len(data3))

