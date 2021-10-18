import pickle
from module.dataset_helper import P300DataFilter
from module.experiment_info import ATTEMPT2

from mongo.query.get_dataset import P300Data, compose_p300_dataset, get_eeg_docs, get_experiment_docs
import numpy as np

from series002.modules.eeg_to_img import eeg_to_img
def test_load_data():

    eeg_docs = get_eeg_docs("A02S01")
    experiment_docs = get_experiment_docs("A02S01")
    data_with_data_clearning = P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT2,[3,4,5,6],do_pad=False,eeg_transform_func=eeg_to_img)).balance_class().shuffle().done()

    with open("used_for_pickle_please_delete_me.pkl","wb") as pkl_file:
        pickle.dump(data_with_data_clearning,pkl_file)

    data_from_pkl:list[P300Data]
    with open("used_for_pickle_please_delete_me.pkl","rb") as pkl_file:
        data_from_pkl = pickle.load(pkl_file)

    for each_data,each_data_pickle in zip(data_with_data_clearning,data_from_pkl):
        assert each_data.target == each_data_pickle.target
        assert np.equal(each_data.eeg,each_data_pickle.eeg).all()