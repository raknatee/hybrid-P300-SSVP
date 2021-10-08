from mongo.query.get_dataset import get_p300_dataset_by_p_id
from module.experiment_info import ATTEMPT1
def test_get():
    
    # data = get_p300_dataset_by_p_id("A01S01",ATTEMPT1) 
    # data = get_p300_dataset_by_p_id("A01S02",ATTEMPT1) 
    data = get_p300_dataset_by_p_id("A01S03",ATTEMPT1) 
    for d in data:
        print(d.target,d.eeg.shape)
        
    # print(len(get_p300_dataset_by_p_id("A01S02",ATTEMPT1)  ))
    # print(len(get_p300_dataset_by_p_id("A01S03",ATTEMPT1)  ))
    assert False