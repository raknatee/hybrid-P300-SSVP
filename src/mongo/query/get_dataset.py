from dataclasses import dataclass
from typing import Callable, Optional, Sequence, Union, cast, overload
from matplotlib import pyplot as plt #type:ignore

import mne #type: ignore
from mne.io.array.array import RawArray #type: ignore
import numpy as np
from numpy import arange, ndarray
from numpy.lib.arraysetops import isin


from module.experiment_info import ExperimentInfo, get_thailand_power_line_noise 
from mongo.connector import Mongo
from mongo.naming import MAIN_DATABASE

from scipy import signal #type:ignore


class Marker:
    first_timestamp:float
    last_timestamp:float
    data:list[bool]


    def __init__(self,first_timestamp:float, last_timestamp:float, data:list[bool]) -> None:
        self.first_timestamp = first_timestamp
        self.last_timestamp = last_timestamp
        self.data = data
       
 
class ExperimentDoc(Marker):
    pass

class ExperimentDocWithTargetGrid(Marker):
    target_grid:int

    def __init__(self,first_timestamp:float, last_timestamp:float, data:list[bool],target_grid:int) -> None:
        super().__init__(first_timestamp,last_timestamp,data)
        self.target_grid = target_grid
        


def get_experiment_docs(p_id: str)->list[ExperimentDoc,]:
        
    return [
        ExperimentDoc(d['min'],d['max'],d['data']) for d in Mongo.get_instance()[MAIN_DATABASE]
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
        ExperimentDocWithTargetGrid(d['min'],d['max'],d['data'],d['target_grid']) for d in Mongo.get_instance()[MAIN_DATABASE]
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
        eeg_round = get_eeg_in_round(experiment_doc.first_timestamp,experiment_doc.last_timestamp+P300_DELAY_END,eeg_docs,len(experiment_info.headset_info.channel_names))
        eeg_mne = notch_and_bandpass_filter(eeg_round,experiment_info,(1,20),240)
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

class BaseSSVPData:
    """
    eeg shape (time_step, channel)
    """
    eeg: ndarray
    fs: int

    def __init__(self,eeg:ndarray,fs:int) -> None:
        self.eeg = eeg

        self.fs  = fs



class SSVPData(BaseSSVPData):
    """
    eeg shape (time_step, channel)
    """



class SSVPDataWithLabel(BaseSSVPData):
    """
    eeg shape (time_step, channel)
    """

    target_grid:int
    def __init__(self,eeg:ndarray,fs:int,target_grid:int) -> None:
        super().__init__(eeg,fs)
        self.target_grid = target_grid
        


@overload
def compose_ssvp_dataset(eeg_docs:list[EEGDoc],markers:list[ExperimentDoc],experiment_info:ExperimentInfo,bandpass_filter:tuple[float,float],selected_eeg_channels:list[int]=None)->list[SSVPData]:
    ...

@overload
def compose_ssvp_dataset(eeg_docs:list[EEGDoc],markers:list[ExperimentDocWithTargetGrid],experiment_info:ExperimentInfo,bandpass_filter:tuple[float,float],selected_eeg_channels:list[int]=None)->list[SSVPDataWithLabel]:
    ...

def compose_ssvp_dataset(eeg_docs:list[EEGDoc],markers:Union[list[ExperimentDoc],list[ExperimentDocWithTargetGrid]],experiment_info:ExperimentInfo,bandpass_filter:tuple[float,float],selected_eeg_channels:list[int]=None)->Union[list[SSVPData],list[SSVPDataWithLabel]]:

    returned = []
  
    sampling_rate = experiment_info.headset_info.sampling_rate

    for marker in markers:
        

        """
        note: my convention about shape of eeg is (time_step, channel)
        but MNE needs (channel, time_step)
        """

        start_time = marker.first_timestamp + (40/1000)
        end_time = marker.last_timestamp +experiment_info.p300_experiment_config.ttl
   
        eeg_round = get_eeg_in_round_by_count_sampling(start_time,end_time,sampling_rate,eeg_docs)

        # eeg_round = zero_padding(eeg_round)
       
    
        eeg_temp2:RawArray =  notch_and_bandpass_filter(eeg_round,experiment_info,bandpass_filter,sampling_rate)
    
        eeg_temp3:ndarray = eeg_temp2.get_data().T



        if selected_eeg_channels is not None:
            eeg_temp3 =  eeg_temp3[:,selected_eeg_channels]

        this_data:Union[SSVPData,SSVPDataWithLabel]
        if isinstance(marker,ExperimentDoc):
            this_data = SSVPData(eeg_temp3,sampling_rate)
        if isinstance(marker,ExperimentDocWithTargetGrid):
            this_data = SSVPDataWithLabel(eeg_temp3,sampling_rate,marker.target_grid)
         
        
        
        
        returned.append(this_data)


    return cast(Union[list[SSVPData],list[SSVPDataWithLabel]],returned)



def zero_padding(data:list[list[float]])->list[list[float]]:
    n_channel = len(data[0])
    padding = [[0.0]*n_channel]*(len(data)*3)
    
    return [*data,* padding]

# def zero_padding(data:Union[np.ndarray,list[list[float]]])->Union[np.ndarray,list[list[float]]]:
#     if isinstance(data,np.ndarray):
#         len_data = data.shape[0]
#         len_channel  = data.shape[1]    
#         padding_array = np.zeros((len_data*5,len_channel))
#         data = np.concatenate((data,padding_array),axis=0)

#         return data
#     else:
    
#     return 


def get_eeg_in_round(time_start:float,time_end:float,all_eeg:list[EEGDoc],n_eeg_channel:int)->list[list[float]]:
    returned:list[list[float]] = []
    for d in all_eeg:
        if time_start <= d.timestamp <= time_end:
            returned.append(d.data[:n_eeg_channel])
    return returned


def get_eeg_in_round_by_count_sampling(time_start:float,time_end:float,fs:int,all_eeg:list[EEGDoc])->list[list[float]]:
    """
    1. Find which document is closed to time_start => A
    2. Find (time_end-time_start) * fs then we knew how many document from A to end
    """
    returned:list[list[float]]=[]

    """
    filter [time_start-1 : time_end+1] second
    """
    filter_array:list[EEGDoc] = [eeg_doc for eeg_doc in all_eeg if  time_start-1 <= eeg_doc.timestamp <= time_end+1]

    index_closest_eeg_doc_to_time_start = find_closest_to(time_start,filter_array)
    if(index_closest_eeg_doc_to_time_start is not None):
        n_sample_next = int((time_end-time_start)*fs)
        print(f"time {time_end-time_start}")
        print(f"{n_sample_next=}")
        filter_array = filter_array[index_closest_eeg_doc_to_time_start:index_closest_eeg_doc_to_time_start+n_sample_next]
        returned = [eeg_doc.data for eeg_doc in filter_array]
        
    


    return returned


def find_closest_to(time_expected:float,array:list[EEGDoc])->Optional[int]:
    for i in range(len(array)):
        if(array[i].timestamp <= time_expected <= array[i+1].timestamp):
            return i
    return None


 
@overload
def notch_and_bandpass_filter(eeg_round:list[list[float]],experiment_info:ExperimentInfo,bandpass_filter:tuple[float,float],fs:int)->RawArray:
    ...

@overload
def notch_and_bandpass_filter(eeg_round:list[list[float]],experiment_info:ExperimentInfo,bandpass_filter:tuple[float,float],fs:int,remove_thailand_power_line:bool)->RawArray:
    ...


def notch_and_bandpass_filter(eeg_round:list[list[float]],experiment_info:ExperimentInfo,bandpass_filter:tuple[float,float],fs:int,remove_thailand_power_line:bool=False)->RawArray:
    ch_types = ['eeg'] * (len(experiment_info.headset_info.channel_names) - 1) + ['stim']

    eeg_mne_arr:RawArray =  mne.io.RawArray(to_mne_format(eeg_round),mne.create_info(experiment_info.headset_info.channel_names,fs,ch_types))
        
    if remove_thailand_power_line:
        eeg_mne_arr.notch_filter(get_thailand_power_line_noise(experiment_info),filter_length='auto', phase='zero')
 
    eeg_mne_arr.filter(bandpass_filter[0],bandpass_filter[1], method='iir')
    return eeg_mne_arr



def to_mne_format(eeg:Union[list[list[float]],np.ndarray])->ndarray:
    return np.array(eeg).T * 1e-6

