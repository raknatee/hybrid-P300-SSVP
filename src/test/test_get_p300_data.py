from mongo.query.get_dataset import SSVPData, compose_p300_dataset,get_eeg_docs,get_experiment_docs,compose_ssvp_dataset
from mongo.query.torch_dataset import P300Dataset 
from module.experiment_info import ATTEMPT1,ATTEMPT2
from module.dataset_helper import P300DataFilter,train_test_splitter



def test_get_p300_dataset_A02():
    eeg_docs = get_eeg_docs("A02S01")
    experiment_docs = get_experiment_docs("A02S01")


 
    for data in compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT2):
       
            
        assert isinstance(data.target,bool)
        print(data.eeg.shape)
        assert data.eeg.shape[0] >= 0
        assert data.eeg.shape[1] == 8
  
    data = P300Dataset(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT2))
    assert len(data) == 300*9
    


    ori_data  = P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT2))
    data2 = ori_data._split_class()
    assert len(data2['True']) + len(data2['False']) == 300*9

    

    data3 = ori_data.random_seed(10).balance_class().shuffle().done()
    
    assert len(data3) == 300*2

    for each_data in data3:
        assert each_data.eeg.shape[0] >= 0 
        assert each_data.eeg.shape[1] == 8 

    train_set,test_set = train_test_splitter(data3,.7)

    assert (0 < len(test_set) < len(train_set) ) and (len(test_set)+len(train_set) == len(data3))


    data4 = P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT2,selected_eeg_channels=list(range(8)))).balance_class().done()
    assert len(data4) == 300*2
    for each_data in data4:
        assert each_data.eeg.shape[0] >= 0 
        assert each_data.eeg.shape[1] == 8
      
       
   

def test_get_p300_dataset_A01():

    eeg_docs = get_eeg_docs("A01S01")
    experiment_docs = get_experiment_docs("A01S01")


 
    for data in [compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT1,do_pad=True)]:
        for d in data:
            
            assert isinstance(d.target,bool)
            assert d.eeg.shape == (128,7)
  


    data = P300Dataset(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT1,do_pad=True))
    assert len(data) == 138
    


    ori_data  = P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT1,do_pad=True))
    data2 = ori_data._split_class()
    assert len(data2['True']) + len(data2['False']) == 138

    

    data3 = ori_data.random_seed(10).balance_class().shuffle().done()
    
    assert len(data3) == 18*2

    for each_data in data3:
        assert each_data.eeg.shape == (128,7)

    data4 = P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT1,do_pad=True,selected_eeg_channels=[1,2,3,4])).balance_class().done()
    assert len(data4) == 18*2
    for each_data in data4:
        assert each_data.eeg.shape == (128,4)
   

    train_set,test_set = train_test_splitter(data3,.7)

    assert (0 < len(test_set) < len(train_set) ) and (len(test_set)+len(train_set) == len(data3))


