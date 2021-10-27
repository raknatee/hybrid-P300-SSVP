from module.experiment_info import ATTEMPT1, ATTEMPT2, ATTEMPT6, ATTEMPT7
from module.ssvp_module.fbcca import predict
from mongo.query.get_dataset import ExperimentDocWithTargetGrid, SSVPData, SSVPDataWithLabel, compose_ssvp_dataset, get_eeg_docs, get_experiment_docs, get_experiment_docs_with_target_grid
import module.object_saver as object_saver
from module.ssvp_module import ssvp_freq_info



def test_get_ssvp_dataset_A07():
    eeg_docs = get_eeg_docs("A07S01")
    experiment_docs = get_experiment_docs("A07S01")

    list_ssvp:list[SSVPData] = compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT7,bandpass_filter=None,selected_eeg_channels=[0,1,2])
    assert len(list_ssvp) == 10
    for ssvp in list_ssvp:
        assert 230 <=  ssvp.eeg.shape[0] < 310
        assert ssvp.eeg.shape[1] == 3

def test_get_ssvp_dataset_A06():
    eeg_docs = get_eeg_docs("A06S01")
    experiment_docs = get_experiment_docs("A06S01")

    list_ssvp:list[SSVPData] = compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT6,bandpass_filter=None,selected_eeg_channels=[0,1,2])
    assert len(list_ssvp) == 10
    for ssvp in list_ssvp:
        assert 230 <=  ssvp.eeg.shape[0] < 310
        assert ssvp.eeg.shape[1] == 3

def test_get_ssvp_dataset_A02():
    eeg_docs = get_eeg_docs("A02S01")
    experiment_docs = get_experiment_docs("A02S01")

    list_ssvp:list[SSVPData] = compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT2,bandpass_filter=None,selected_eeg_channels=[0,1,2])
    assert len(list_ssvp) == 300
    for ssvp in list_ssvp:
        assert 360 <=  ssvp.eeg.shape[0] < 500
        assert ssvp.eeg.shape[1] == 3




def test_get_ssvp_dataset_A01():

    for p_id in ["A01S01","A01S02","A01S03"]:
        eeg_docs = get_eeg_docs(p_id)
        experiment_docs = get_experiment_docs(p_id)

        list_ssvp:list[SSVPData] = compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT1,bandpass_filter=None)

        for ssvp_data in list_ssvp:
            
            assert ssvp_data.eeg.shape[0] > 0
            assert ssvp_data.eeg.shape[1] == len(ATTEMPT1.headset_info.channel_names)