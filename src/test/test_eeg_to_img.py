
from module.experiment_info import ATTEMPT2
from mongo.query.get_dataset import compose_p300_dataset, get_eeg_docs, get_experiment_docs
from series002.modules.eeg_to_img import eeg_to_img


def test():
    eeg_docs = get_eeg_docs("A02S01")
    experiment_docs = get_experiment_docs("A02S01")


 
    for data in [compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT2,eeg_transform_func=eeg_to_img)]:
        for d in data:
            
            assert isinstance(d.target,bool)
            assert d.eeg.shape == (1,64,64)