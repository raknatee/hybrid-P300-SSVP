from typing import cast
from mongo.query.get_dataset import SSVPData, compose_p300_dataset,get_eeg_docs,get_experiment_docs,compose_ssvp_dataset
from mongo.query.get_torch_dataset import P300Dataset 
from module.experiment_info import ATTEMPT1
from module.dataset_helper import P300DataFilter,train_test_splitter


def test_get_p300_dataset():

    eeg_docs = get_eeg_docs("A01S01")
    experiment_docs = get_experiment_docs("A01S01")


 
    for data in [compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT1)]:
        for d in data:
            
            assert isinstance(d.target,bool)
            assert d.eeg.shape == (128,7)
  


    eeg_docs = get_eeg_docs("A01S01")
    experiment_docs = get_experiment_docs("A01S01")

    data = P300Dataset(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT1))
    assert len(data) == 138
    


    ori_data  = P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT1))
    data2 = ori_data._split_class()
    assert len(data2['True']) + len(data2['False']) == 138

    

    data3 = ori_data.random_seed(10).balance_class().shuffle().done()
    
    assert len(data3) == 18*2

    for each_data in data3:
        assert each_data.eeg.shape == (128,7)

    data4 = P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT1)).balance_class().filtering_eeg_channel([1,2,3,4]).done()
    assert len(data4) == 18*2
    for each_data in data4:
        assert each_data.eeg.shape == (128,4)
   

    train_set,test_set = train_test_splitter(data3,.7)

    assert (0 < len(test_set) < len(train_set) ) and (len(test_set)+len(train_set) == len(data3))

def test_get_ssvp_dataset():

    for p_id in ["A01S01","A01S02","A01S03"]:
        eeg_docs = get_eeg_docs(p_id)
        experiment_docs = get_experiment_docs(p_id)

        list_ssvp:list[SSVPData] = compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT1)

        for ssvp_data in list_ssvp:
            
            assert ssvp_data.eeg.shape[0] > 0
            assert ssvp_data.eeg.shape[1] == len(ATTEMPT1.headset_info.channel_names)