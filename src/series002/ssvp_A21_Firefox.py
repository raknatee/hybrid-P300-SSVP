
from typing import Optional, Sequence, Union, overload
import mne #type:ignore

from matplotlib import pyplot as plt #type:ignore
from mne.io.array.array import RawArray #type:ignore
import numpy as np
from scipy.ndimage.measurements import label #type:ignore

from module import object_saver

from module.experiment_info import SSVPOnly
from module.fft import to_fft
from module.ssvp_module.ssvp_freq_info import FP, wave_data_2021_11_4

from module.ssvp_module import ssvp_freq_info
from module.ssvp_module.fbcca import  predict2
from mongo.query.torch_dataset import P300Dataset
from mongo.query.get_dataset import  P300Data, SSVPData, SSVPDataWithLabel, compose_p300_dataset, compose_ssvp_dataset, get_eeg_docs, get_experiment_docs, get_experiment_docs_with_target_grid, to_mne_format


mne.set_log_file("./logs/mne.log",overwrite=True)

P_ID = "SSVPFirefox"
TIME_PER_ROUND = 5

SAMPLING_RATE = SSVPOnly.headset_info.sampling_rate
# SAMPLING_RATE = 240
def main():
  
    def load()->list[SSVPDataWithLabel]:
    
        eeg_docs = get_eeg_docs(P_ID)
        experiment_docs = get_experiment_docs_with_target_grid(P_ID)


        return compose_ssvp_dataset(eeg_docs,experiment_docs,SSVPOnly,(1,120),[0,1,2])
      

 


    # list_ssvp = object_saver.disk_cache(load,f"{P_ID}-ssvp.pkl")
    list_ssvp = load()

    count_correct = 0 


    wavesData:list[Optional[FP]] = [
    None,
    None,
    FP(6, 0),
    None,
    FP(11,0),
    None,
    None,
    
    FP(15,0),

    None, None,
    None,None
]
    print(wavesData)
    ssvp:SSVPDataWithLabel
    inspectData = InspectData()
    for ssvp in list_ssvp:
      
        print("-"*20)
       
        inspectData.add(ssvp)
     

      
        result = predict2(ssvp.eeg,SAMPLING_RATE,[wave for wave in wavesData if wave is not None])
    
        
        y_true = wavesData[ssvp.target_grid]
      
        y_hat:ssvp_freq_info.FP
        rho:list[float]
        y_hat,rho = result

        print(f"{rho=}")
        print(f"{y_true=},{y_hat=}")
       
        if(y_true ==  y_hat ):
            count_correct+=1

    
    print(f"{count_correct=} {len(list_ssvp)=}")
    print(f"acc: {count_correct/len(list_ssvp)}")
  
    inspectData.save_fig()


class FFTPoint:

    @staticmethod
    def look(signal:np.ndarray, freqs:list[FP])->tuple[list[float],FP]:
        """
        need signal in time domain
        """

        fft,x_axis = to_fft(signal,SAMPLING_RATE)
        amplitudes:list[float] = []
        for freq in freqs:
           index = (x_axis>freq.freq-0.5) & (x_axis<freq.freq+0.5)
        #    index = (x_axis>freq.freq-0.2) & (x_axis<freq.freq+0.2)
     
           amplitude = fft[index]   * 1e5
           amplitudes.append(amplitude.mean())
        
        predict_index = amplitudes.index(max(amplitudes))
        
        return amplitudes,freqs[predict_index]


class InspectData:
    eeg_data:dict[str, list[np.ndarray]]

    def __init__(self) -> None:
        self.eeg_data = {}

    def add(self,ssvp_data_with_label:SSVPDataWithLabel):
        label:str = str(ssvp_data_with_label.target_grid)
        if(label == "2"):
            label = "6Hz"
        if(label == "4"):
            label = "11Hz"
        if(label == "7"):
            label = "15Hz"
 
        if label not in self.eeg_data:
            self.eeg_data[label] = []
         
      
        self.eeg_data[label].append(ssvp_data_with_label.eeg[:SAMPLING_RATE*TIME_PER_ROUND-15])



    @overload
    def save_fig(self)->None:
        ...

    @overload
    def save_fig(self,selected_sample:int)->None:
        ...

   
    def save_fig(self,selected_sample:Optional[int]=None)->None:
     

    
        for each_label in self.eeg_data:

            eeg_mean:np.ndarray
            if(selected_sample is None):
                eeg_mean = InspectData.mean(self.eeg_data[each_label])
            else:
                eeg_mean = InspectData.mean(self.eeg_data[each_label][:selected_sample])

        



            def x_freq(sample_rate:float,lenght_data:int)->np.ndarray:
                df = sample_rate/lenght_data
                return np.arange(0,sample_rate/2,df)

            # eeg_mean_fft,x_axis = to_fft(eeg_mean.reshape(-1,1),SAMPLING_RATE)
                         
            eeg_mean_fft = np.abs(np.fft.fft(eeg_mean))
            x_axis=x_freq(SAMPLING_RATE,len(eeg_mean))
         


         


            x_axis = x_axis[ x_axis<100 ]
    


            def zoom(x:np.ndarray)->np.ndarray:
                return x
                # return x[10:90]
                # return x[40:90]

            # plt.plot(zoom(x_axis),zoom(eeg_mean[:len(x_axis)]),label=f"class-{each_label}")
            plt.plot(zoom(x_axis),zoom(eeg_mean_fft[:len(x_axis)]),label=f"class-{each_label}")
        
        plt.legend()
        plt.savefig(f"./logs/{P_ID}.png")
        
       

            



    @staticmethod
    def mean(eeg:list[np.ndarray])->np.ndarray:

        stacked_eeg = eeg[0]
        for i in range(1,len(eeg)):
            stacked_eeg = np.concatenate((stacked_eeg,eeg[i]),axis=1)
        stacked_eeg = stacked_eeg.mean(axis=1)
    
        return stacked_eeg
