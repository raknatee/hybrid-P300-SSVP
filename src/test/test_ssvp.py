from module.experiment_info import ATTEMPT1, ATTEMPT2
from module.ssvp_module.fbcca import predict
from mongo.query.get_dataset import ExperimentDocWithTargetGrid, SSVPData, SSVPDataWithLabel, compose_ssvp_dataset, get_eeg_docs, get_experiment_docs, get_experiment_docs_with_target_grid
import module.object_saver as object_saver
from module.ssvp_module import ssvp_freq_info
def test_ssvp_maybe():

    def load():
    
        eeg_docs = get_eeg_docs("A02S01")
        experiment_docs = get_experiment_docs_with_target_grid("A02S01")
        return compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT2,[0,1,2])

    list_ssvp:list[SSVPDataWithLabel] = object_saver.load(load,"A02S01.pkl")

    for ssvp in list_ssvp:
        result = predict(ssvp.eeg,ATTEMPT2)
        
        assert isinstance(ssvp_freq_info.wave_data.index(result),int)  # should be equaled to => ssvp.target_grid 



def test_get_ssvp_dataset_A02():
    eeg_docs = get_eeg_docs("A02S01")
    experiment_docs = get_experiment_docs("A02S01")

    list_ssvp:list[SSVPData] = compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT2,[0,1,2])
    assert len(list_ssvp) == 300
    for ssvp in list_ssvp:
        assert 360 <=  ssvp.eeg.shape[0] < 500
        assert ssvp.eeg.shape[1] == 3




def test_get_ssvp_dataset_A01():

    for p_id in ["A01S01","A01S02","A01S03"]:
        eeg_docs = get_eeg_docs(p_id)
        experiment_docs = get_experiment_docs(p_id)

        list_ssvp:list[SSVPData] = compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT1)

        for ssvp_data in list_ssvp:
            
            assert ssvp_data.eeg.shape[0] > 0
            assert ssvp_data.eeg.shape[1] == len(ATTEMPT1.headset_info.channel_names)