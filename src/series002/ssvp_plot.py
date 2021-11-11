
from mne.io.array.array import RawArray #type: ignore

from module.experiment_info import ATTEMPT5, ATTEMPT6
from mongo.query.get_dataset import SSVPData, compose_ssvp_dataset, get_eeg_docs, get_experiment_docs, notch_and_bandpass_filter, to_mne_format
from matplotlib import pyplot as plt #type:ignore

def main():
    eeg_docs = get_eeg_docs("A06S01")
    experiment_docs = get_experiment_docs("A06S01")
   
    compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT6,bandpass_filter=None,selected_eeg_channels=[0,1,2])
   