from __future__ import annotations
import os
from typing import Generator
from matplotlib import pyplot as plt #type:ignore
import mne #type:ignore
import numpy as np
from numpy import ndarray
from mne.io.array.array import RawArray #type:ignore
from mne import Epochs, find_events


from module.experiment_info import ExperimentInfo, HeadsetInfo, P300ExperimentConfig
from module.ssvp_module.fbcca import predict
from module.ssvp_module.ssvp_freq_info import FP 

mne.set_log_file("./logs/mne.log",overwrite=True)


data_file_name:str = "ssvep-10trials-3s-chaky-bigsquare-gitignore.csv"

class SSVPData:
    timestamp:float
    eeg:list[float]
    marker:int

    def __init__(self,timestamp:float,eeg:list[float],marker:int) -> None:
        self.timestamp = timestamp
        self.eeg = eeg
        self.marker = marker

    @staticmethod
    def from_csv_string_one_line(data_string:str)->SSVPData:
        data:list[float] = list(map(float,data_string.split(",")))

        return SSVPData(data[0],[data[1],data[2],data[3]],int(data[-1]))


    def __str__(self) -> str:
        return str(self.timestamp)

def main():
    ssvp_data_list = [SSVPData.from_csv_string_one_line(line) for line in read_line()]
   
    ssvp_6_hz = [s for s in ssvp_data_list if s.marker==1]
    ssvp_10_hz = [s for s in ssvp_data_list if s.marker==2]
    ssvp_15_hz = [s for s in ssvp_data_list if s.marker==3]
    assert len(ssvp_6_hz) == 10 
    assert len(ssvp_10_hz) == 10 
    assert len(ssvp_15_hz) == 10 

    channel_names = ["O1","Oz","O2"]
    ch_types = ['eeg'] * (len(channel_names)-1) + ['stim']

  

    eeg_round = [data.eeg for data in ssvp_data_list]
    eeg_mne_arr:RawArray =  mne.io.RawArray(to_mne_format(eeg_round),mne.create_info(channel_names,250,ch_types))
    eeg_mne_arr.set_montage(mne.channels.make_standard_montage('standard_1020'))
    eeg_mne_arr.plot_psd()
    plt.savefig(f"./logs/plot-ssvp-chaky-all-gitignore.png")

    I_dont_know_real_but_just_dummy = ExperimentInfo(headset_info=HeadsetInfo(250,['O2','OZ','O1','P8','P4','P3','P7','FpZ']),
                            p300_experiment_config=P300ExperimentConfig(0,1)
    )

    expected_fp = [FP(6,0),FP(10,0),FP(15,0)]
    count = {'correct':0,'all':0}
    for index,ssvp_each_hz in enumerate([ssvp_6_hz,ssvp_10_hz,ssvp_15_hz]):
        
        for target in ssvp_each_hz:
            eeg_round = [ data.eeg for data in pad_non_target(target.timestamp,ssvp_data_list)]
       

            eeg_mne_arr:RawArray =  mne.io.RawArray(to_mne_format(eeg_round),mne.create_info(channel_names,230,ch_types))
            eeg_mne_arr.set_montage(mne.channels.make_standard_montage('standard_1020'))
            eeg_mne_arr.plot_psd()
            plt.savefig(f"./logs/plot-ssvp-chaky-{index}-{count['all']}-gitignore.png")

            

            y_true = expected_fp[index]

            y_hat:FP
            rho:list[float]
            y_hat,rho = predict(np.array(eeg_round),I_dont_know_real_but_just_dummy,expected_fp,remove_Thailand_power_line=True)
            print(f"{rho=}")
            print(f"{y_true=}")
            print(f"{y_hat=}")
            print("-"*20)
            if(y_true == y_hat):
                count['correct']+=1
            count['all']+=1
    print(f"acc : {count['correct']/count['all']}")

def read_line()->Generator[str,None,None]:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(current_dir,data_file_name)
    with open(data_path,"r") as file_obj:
        while line:= file_obj.readline():
            yield line
    

def to_mne_format(eeg:list[list[float]])->ndarray:
    return np.array(eeg).T * 1e-6

def pad_non_target(time:float,all_eeg:list[SSVPData])->list[SSVPData]:
  
    time_start = time - .5
    time_end = time + 3


   
    return [data for data in all_eeg if time_start<= data.timestamp<=time_end]

