from mongo.query.get_dataset import EEGDoc, ExperimentDoc, ExperimentDocWithTargetGrid, SSVPDataWithLabel, get_eeg_docs, get_eeg_in_round_by_count_sampling, get_experiment_docs_with_target_grid
from module.experiment_info import ATTEMPT15



def test_A15S01():

    P_ID = "A15S01"
    def load()->tuple[list[EEGDoc],list[ExperimentDocWithTargetGrid]]:
    
        eeg_docs = get_eeg_docs(P_ID)
        experiment_docs = get_experiment_docs_with_target_grid(P_ID)
        return (eeg_docs,experiment_docs)
      

    eeg_docs,experiment_docs = load()

    ttl = ATTEMPT15.p300_experiment_config.ttl

    for marker in experiment_docs:
        sample = get_eeg_in_round_by_count_sampling(marker.first_timestamp,marker.last_timestamp+ttl,250,eeg_docs)
        assert abs((marker.last_timestamp+ttl - marker.first_timestamp) - 3)<0.1
        assert abs(len(sample)-750) <= 2