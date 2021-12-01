
from typing import Optional, Union, overload
import mne #type:ignore

from matplotlib import pyplot as plt #type:ignore
from mne.io.array.array import RawArray #type:ignore
import numpy as np
from scipy.ndimage.measurements import label #type:ignore

from module import object_saver

from module.experiment_info import ATTEMPT15
from module.ssvp_module.ssvp_freq_info import FP, wave_data_2021_11_4

from module.ssvp_module import ssvp_freq_info
from module.ssvp_module.fbcca import predict, predict2
from mongo.query.torch_dataset import P300Dataset
from mongo.query.get_dataset import  P300Data, SSVPData, SSVPDataWithLabel, compose_p300_dataset, compose_ssvp_dataset, get_eeg_docs, get_experiment_docs, get_experiment_docs_with_target_grid, to_mne_format


mne.set_log_file("./logs/mne.log",overwrite=True)

P_ID = "A15S01"
time_per_round = 3

sampling_rate = ATTEMPT15.headset_info.sampling_rate
def main():
  
    def load()->list[SSVPDataWithLabel]:
    
        eeg_docs = get_eeg_docs(P_ID)
        experiment_docs = get_experiment_docs_with_target_grid(P_ID)


        return compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT15,(4,70),[0,1,2])
      

 


    # list_ssvp = object_saver.disk_cache(load,f"{P_ID}-ssvp.pkl")
    list_ssvp = load()

    count_correct = 0 
    
    
    # wavesData = wave_data_2021_11_4
    wavesData = [
    FP(6, 0),
 
    # FP(5,0),
    # FP(6.2,0),
    FP(11.5,0),
    # FP(7,0),
    # FP(8,0),
    # FP(9,0),
 
    ] 
    print(wavesData)
    ssvp:SSVPDataWithLabel
    inspectData = InspectData()
    for ssvp in list_ssvp:
      
        print("-"*20)
       
        inspectData.add(ssvp)
     
        # result = predict2(ssvp.eeg,250,[wave for wave in wavesData if wave is not None],enable_zero_padding=False)
        # result = predict2(ssvp.eeg,ssvp.fs,[wave for wave in wavesData if wave is not None],enable_zero_padding=False)
      
        result = predict2(ssvp.eeg,sampling_rate,[wave for wave in wavesData if wave is not None])
        # result = predict2(ssvp.eeg,MAX_FS,[wave for wave in wavesData if wave is not None],enable_zero_padding=False)
    
        
        y_true = wavesData[ssvp.target_grid]

        y_hat:ssvp_freq_info.FP
        rho:list[float]
        y_hat,rho = result

        print(f"{rho=}")
        print(f"{y_true=},{y_hat=}")
        if(y_true ==  y_hat ):
            count_correct+=1

    print(f"acc: {count_correct/len(list_ssvp)}")
    inspectData.save_fig()


class InspectData:
    eeg_data:dict[str, list[np.ndarray]]

    def __init__(self) -> None:
        self.eeg_data = {}

    def add(self,ssvp_data_with_label:SSVPDataWithLabel):
        label:str = str(ssvp_data_with_label.target_grid)
        if(label == "0"):
            label = "6Hz"
        if label not in self.eeg_data:
            self.eeg_data[label] = []
         
        print(ssvp_data_with_label.eeg.shape)
        # self.eeg_data[label].append(ssvp_data_with_label.eeg[:2950])
        self.eeg_data[label].append(ssvp_data_with_label.eeg[:sampling_rate*time_per_round-50])

    @staticmethod
    def calFFT(signal:np.ndarray,fs:int):
        number_sample = signal.shape[0]
        realRange = fs//2

        mag = np.abs(np.fft.fft(signal))
        mag_norm = mag / (number_sample/2)
        mag_range = mag_norm[:number_sample//2]

        f_range = np.linspace(0,realRange,number_sample//2)
        
        return mag_range, f_range



    @overload
    def save_fig(self)->None:
        ...

    @overload
    def save_fig(self,selected_sample:int)->None:
        ...

   
    def save_fig(self,selected_sample:Optional[int]=None)->None:
        def x_freq(sample_rate:float,lenght_data:int)->np.ndarray:
            df = sample_rate/lenght_data
            return np.arange(0,sample_rate/2,df)

    
        for each_label in self.eeg_data:

            eeg_mean:np.ndarray
            if(selected_sample is None):
                eeg_mean = InspectData.mean(self.eeg_data[each_label])
            else:
                eeg_mean = InspectData.mean(self.eeg_data[each_label][:selected_sample])

            eeg_mean = np.abs(np.fft.fft(eeg_mean))
            # eeg_mean = 10 * np.log10(eeg_mean)
            x_axis = x_freq(sampling_rate,len(eeg_mean))

            # eeg_mean,x_axis = InspectData.calFFT(eeg_mean,250)


            x_axis = x_axis[ x_axis<100 ]
            print(x_axis.shape)


            def zoom(x:np.ndarray)->np.ndarray:
                # return x
                return x[10:50]
                # return x[40:90]

            plt.plot(zoom(x_axis),zoom(eeg_mean[:len(x_axis)]),label=f"class-{each_label}")
        
        plt.legend()
        plt.savefig(f"./logs/{P_ID}-all-mean-code-2.png")
        
       

            



    @staticmethod
    def mean(eeg:list[np.ndarray])->np.ndarray:

        stacked_eeg = eeg[0]
        for i in range(1,len(eeg)):
            stacked_eeg = np.concatenate((stacked_eeg,eeg[i]),axis=1)
        stacked_eeg = stacked_eeg.mean(axis=1)
        print(f"{stacked_eeg.shape=}")
        return stacked_eeg
