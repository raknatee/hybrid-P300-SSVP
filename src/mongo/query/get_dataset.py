from dataclasses import dataclass

import mne #type: ignore
from mne.io.array.array import RawArray #type: ignore
import numpy as np
from numpy import ndarray

from module.experiment_info import ExperimentInfo, get_thailand_power_line_noise 
from mongo.connector import Mongo
from mongo.naming import MAIN_DATABASE


@dataclass(init=True)
class ExperimentDoc:
    max:float
    min:float
    data:list[bool]

def get_experiment_docs(p_id: str)->list[ExperimentDoc]:
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

def compose_p300_dataset(eeg_docs:list[EEGDoc],experiment_docs:list[ExperimentDoc], experiment_info: ExperimentInfo,do_pad:bool=True,output_size:int=128) -> list[P300Data]:

    dataset:list[P300Data] = []
    experiment_doc:ExperimentDoc
    for experiment_doc in experiment_docs:
        eeg_round = get_eeg_in_round(experiment_doc.min,experiment_doc.max+experiment_info.p300_interval.end_time,eeg_docs,experiment_info)
        eeg_mne = notch_and_bypass_filter(eeg_round,experiment_info)
        eeg_numpy:ndarray = eeg_mne.get_data()

        # I prefer to use this format (n,channel)
        eeg_numpy = eeg_numpy.T
        eeg_time_point:ndarray = eeg_mne.times

         
        for i,target in enumerate(experiment_doc.data) :
            this_p300 = P300Data()
            this_p300.target = target

            start_time = (i*experiment_info.p300_experiment_config.spawn) + experiment_info.p300_interval.after_p300_started

            index_this_time = (eeg_time_point[:] >= start_time) & (eeg_time_point[:]<= start_time+experiment_info.p300_interval.end_time)

        
            this_p300.eeg = eeg_numpy[index_this_time]

            if do_pad:
                current_size:int = this_p300.eeg.shape[0]
                this_p300.eeg = np.pad(this_p300.eeg, ((0, output_size-current_size),(0,0)), constant_values=0)

            dataset.append(this_p300)
          
    return dataset


class SSVPData:
    eeg: ndarray


def compose_ssvp_dataset(eeg_docs:list[EEGDoc],experiment_docs:list[ExperimentDoc],experiment_info:ExperimentInfo)->list[SSVPData]:
    returned:list[SSVPData] = []
    for experiment_doc in experiment_docs:
        this_data:SSVPData = SSVPData()
        eeg_temp = [ eeg_doc.data[:len(experiment_info.headset_info.channel_names)] for eeg_doc in eeg_docs if (experiment_doc.min <= eeg_doc.timestamp <= experiment_doc.max)]
        eeg_temp2:RawArray =  notch_and_bypass_filter(eeg_temp,experiment_info)
        this_data.eeg = eeg_temp2.get_data().T
        
        returned.append(this_data)


    return returned



def get_eeg_in_round(time_start:float,time_end:float,all_eeg:list[EEGDoc],experiment_info:ExperimentInfo)->list[list[float]]:
    returned:list[list[float]] = []
    for d in all_eeg:
        if time_start <= d.timestamp <= time_end:
            returned.append(d.data[:len(experiment_info.headset_info.channel_names)])
    return returned


def notch_and_bypass_filter(eeg_round:list[list[float]],experiment_info:ExperimentInfo)->RawArray:
    ch_types = ['eeg'] * (len(experiment_info.headset_info.channel_names) - 1) + ['stim']

    eeg_mne_arr:RawArray =  mne.io.RawArray(to_mne_format(eeg_round),mne.create_info(experiment_info.headset_info.channel_names,experiment_info.headset_info.sample_rate,ch_types))
        
    eeg_mne_arr.notch_filter(get_thailand_power_line_noise(experiment_info),filter_length='auto', phase='zero')
    eeg_mne_arr.filter(4,50, method='iir')
    return eeg_mne_arr

def to_mne_format(eeg:list[list[float]])->ndarray:
    return np.array(eeg).T * 1e-6

