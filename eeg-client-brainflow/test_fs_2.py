from typing import Any
import numpy as np
import json
from numpy import ndarray
import mne #type:ignore
from mne.io.array.array import RawArray #type:ignore
from matplotlib import pyplot as plt #type:ignore



CHANNEL_NAMES = ['O2','Oz','O1','P8','P4','P3','P7','FpZ']
CH_TYPES = ['eeg'] * (len(CHANNEL_NAMES)-1) + ['stim']

def main():
    data:dict[str,Any]
    with open("data.json","r") as json_file:
        data = json.load(json_file)


    for second in data['list_fs']:
        signals = [ time_step['data'] for time_step in second]  
        eeg_mne_arr:RawArray =  mne.io.RawArray(to_mne_format(signals),mne.create_info(CHANNEL_NAMES,len(signals),CH_TYPES))
        print(len(signals))
        eeg_mne_arr.set_montage(mne.channels.make_standard_montage('standard_1020'))
        eeg_mne_arr.plot_psd()
        # plt.savefig(f"./logs/{len(signals)}.png")




def to_mne_format(eeg:list[list[float]])->ndarray:
    return np.array(eeg).T * 1e-6

    

if __name__ == "__main__":
    main()

