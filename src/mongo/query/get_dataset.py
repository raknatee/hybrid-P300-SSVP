from dataclasses import dataclass
from typing import Callable, Optional, Sequence, Union
from matplotlib import pyplot as plt #type:ignore

import mne #type: ignore
from mne.io.array.array import RawArray #type: ignore
import numpy as np
from numpy import ndarray


from module.experiment_info import ExperimentInfo, get_thailand_power_line_noise 
from mongo.connector import Mongo
from mongo.naming import MAIN_DATABASE

from scipy import signal #type:ignore

@dataclass(init=True)
class ExperimentDoc:
    max:float
    min:float
    data:list[bool]

@dataclass(init=True)
class ExperimentDocWithTargetGrid:
    max:float
    min:float
    data:list[bool]
    target_grid:int


def get_experiment_docs(p_id: str)->list[ExperimentDoc,]:
        
    return [
        ExperimentDoc(d['max'],d['min'],d['data']) for d in Mongo.get_instance()[MAIN_DATABASE]
        [f"{p_id}-experiment-offline-collection"].aggregate([{
            '$project': {
                'data': 1
            }
        }, {
            '$addFields': {
                'max': {
                    '$max': '$data.timestamp'
                },
                'min': {
                    '$min': '$data.timestamp'
                }
            }
        }, {
            '$project': {
                'data': {
                    '$filter': {
                        'input': '$data.is_target_activated',
                        'as': 'is_target_activated',
                        'cond': {}
                    }
                },
                'max': 1,
                'min': 1
            }
        }])
    ]

def get_experiment_docs_with_target_grid(p_id:str)->list[ExperimentDocWithTargetGrid]:
    return [
        ExperimentDocWithTargetGrid(d['max'],d['min'],d['data'],d['target_grid']) for d in Mongo.get_instance()[MAIN_DATABASE]
        [f"{p_id}-experiment-offline-collection"].aggregate([{
            '$project': {
                'data': 1,'target_grid':1
            }
        }, {
            '$addFields': {
                'max': {
                    '$max': '$data.timestamp'
                },
                'min': {
                    '$min': '$data.timestamp'
                }
            }
        }, {
            '$project': {
                'data': {
                    '$filter': {
                        'input': '$data.is_target_activated',
                        'as': 'is_target_activated',
                        'cond': {}
                    }
                },
                'max': 1,
                'min': 1,
                'target_grid':1
            }
        }])
    ]
@dataclass(init=True)
class EEGDoc:
    timestamp:float
    data:list[float]

def get_eeg_docs(p_id: str)->list[EEGDoc]:
    return [
        EEGDoc(d['timestamp'],d['data']) for d in Mongo.get_instance()[MAIN_DATABASE]
        [f"{p_id}-EEG-offline-collection"].find({})
    ]



class P300Data:
    target: bool
    eeg: ndarray
 
    def __str__(self) -> str:
        return f"{self.target},{self.eeg}"

def compose_p300_dataset(eeg_docs:list[EEGDoc],experiment_docs:list[ExperimentDoc], experiment_info: ExperimentInfo,selected_eeg_channels:Optional[list[int]]=None,do_pad:bool=False,output_size:int=128,eeg_transform_func:Optional[Callable[[ndarray],ndarray]]=None) -> list[P300Data]:

    dataset:list[P300Data] = []
    # P300_DELAY_START = 0.25
    # P300_DELAY_END = 0.3
    P300_DELAY_START = 0.2
    P300_DELAY_END = 0.5
    experiment_doc:ExperimentDoc
    for experiment_doc in experiment_docs:
        eeg_round = get_eeg_in_round(experiment_doc.min,experiment_doc.max+P300_DELAY_END,eeg_docs,len(experiment_info.headset_info.channel_names))
        eeg_mne = notch_and_bandpass_filter(eeg_round,experiment_info)
        eeg_numpy:ndarray = eeg_mne.get_data()

        # I prefer to use this format (n,channel)
        eeg_numpy = eeg_numpy.T
        eeg_time_point:ndarray = eeg_mne.times

         
        for i,target in enumerate(experiment_doc.data) :
            this_p300 = P300Data()
            this_p300.target = target

            start_time = (i*experiment_info.p300_experiment_config.spawn) + P300_DELAY_START

            index_this_time = (eeg_time_point[:] >= start_time) & (eeg_time_point[:]<= start_time+P300_DELAY_END)

        
            this_p300.eeg = eeg_numpy[index_this_time]
            if(selected_eeg_channels is not None):
                this_p300.eeg = this_p300.eeg[:,selected_eeg_channels]
            if do_pad:
                current_size:int = this_p300.eeg.shape[0]
                this_p300.eeg = np.pad(this_p300.eeg, ((0, output_size-current_size),(0,0)), constant_values=0)

            if eeg_transform_func is not None:
                this_p300.eeg = eeg_transform_func(this_p300.eeg)
            dataset.append(this_p300)
          
    return dataset


class SSVPData:
    eeg: ndarray

class SSVPDataWithLabel:
    eeg: ndarray
    target_grid:int

def compose_ssvp_dataset(eeg_docs:list[EEGDoc],experiment_docs:Sequence[Union[ExperimentDoc,ExperimentDocWithTargetGrid]],experiment_info:ExperimentInfo,bandpass_filter:Optional[tuple[float,float]],selected_eeg_channels:list[int]=None,debug=False)->list[Union[SSVPData,SSVPDataWithLabel]]:

    returned:list[Union[SSVPData,SSVPDataWithLabel]] = []
 
    
    for index,experiment_doc in enumerate(experiment_docs) :
        this_data:Union[SSVPData,SSVPDataWithLabel]
        if isinstance(experiment_doc,ExperimentDoc):
            this_data = SSVPData()
        if isinstance(experiment_doc,ExperimentDocWithTargetGrid):
            this_data = SSVPDataWithLabel()
            this_data.target_grid = experiment_doc.target_grid
        
        eeg_temp = [ eeg_doc.data[:len(experiment_info.headset_info.channel_names)] for eeg_doc in eeg_docs if (experiment_doc.min <= eeg_doc.timestamp <= experiment_doc.max +experiment_info.p300_experiment_config.ttl )]
        if(debug):
            eeg_temp_but_non_target:list[list[float]] = [ eeg_doc.data[:len(experiment_info.headset_info.channel_names)] for eeg_doc in eeg_docs if (experiment_doc.max <= eeg_doc.timestamp <= experiment_doc.max + 1 )]
            eeg_temp2_but_non_target:RawArray = notch_and_bandpass_filter(eeg_temp_but_non_target,experiment_info,bandpass_filter=bandpass_filter)
            eeg_temp2_but_non_target.plot_psd()
            
            plt.savefig(f"./logs/plot-non-target-{experiment_doc.max}-gitignore.png")

        eeg_temp2:RawArray =  notch_and_bandpass_filter(eeg_temp,experiment_info,bandpass_filter=bandpass_filter)
        if(debug):
            eeg_temp2.plot_psd()
            plt.savefig(f"./logs/plot-target-{experiment_doc.min}-gitignore.png")
        this_data.eeg = eeg_temp2.get_data().T

        if selected_eeg_channels is not None:
            this_data.eeg = this_data.eeg[:,selected_eeg_channels]
        
        returned.append(this_data)


    return returned



def get_eeg_in_round(time_start:float,time_end:float,all_eeg:list[EEGDoc],n_eeg_channel:int)->list[list[float]]:
    returned:list[list[float]] = []
    for d in all_eeg:
        if time_start <= d.timestamp <= time_end:
            returned.append(d.data[:n_eeg_channel])
    return returned


def notch_and_bandpass_filter(eeg_round:list[list[float]],experiment_info:ExperimentInfo,bandpass_filter:Optional[tuple[float,float]]=(1,20))->RawArray:
    ch_types = ['eeg'] * (len(experiment_info.headset_info.channel_names) - 1) + ['stim']

    eeg_mne_arr:RawArray =  mne.io.RawArray(to_mne_format(eeg_round),mne.create_info(experiment_info.headset_info.channel_names,experiment_info.headset_info.sample_rate,ch_types))
        
    # eeg_mne_arr.notch_filter(get_thailand_power_line_noise(experiment_info),filter_length='auto', phase='zero')
    if bandpass_filter is not None:
        eeg_mne_arr.filter(bandpass_filter[0],bandpass_filter[1], method='iir')
    return eeg_mne_arr



def to_mne_format(eeg:Union[list[list[float]],np.ndarray])->ndarray:
    return np.array(eeg).T * 1e-6

