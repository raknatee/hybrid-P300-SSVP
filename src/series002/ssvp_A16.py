
from typing import Union
import mne #type:ignore

from matplotlib import pyplot as plt #type:ignore
from mne.io.array.array import RawArray #type:ignore
import numpy as np
from scipy.ndimage.measurements import label #type:ignore

from module import object_saver

from module.experiment_info import ATTEMPT16
from module.ssvp_module.ssvp_freq_info import FP, wave_data_2021_11_4

from module.ssvp_module import ssvp_freq_info
from module.ssvp_module.fbcca import predict
from mongo.query.torch_dataset import P300Dataset
from mongo.query.get_dataset import  P300Data, SSVPData, SSVPDataWithLabel, compose_p300_dataset, compose_ssvp_dataset, get_eeg_docs, get_experiment_docs, get_experiment_docs_with_target_grid, to_mne_format


mne.set_log_file("./logs/mne.log",overwrite=True)

P_ID = "A16S01"
FS   = 250
def main():
    def load()->Union[list[SSVPData],list[SSVPDataWithLabel]]:
    
        eeg_docs = get_eeg_docs(P_ID)
        experiment_docs = get_experiment_docs_with_target_grid(P_ID)


        # return compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT11,None,[*[0,1,2]])
        return compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT16,(.5,30),[*[0,1,2]])

 


    # list_ssvp = object_saver.disk_cache(load,f"{P_ID}-ssvp.pkl")
    list_ssvp = load()

    count_correct = 0 
    analysis = Analysis()
    
    # wavesData = wave_data_2021_11_4
    wavesData = [
    FP(6, 0),
    FP(6.2,0),
    ]
    print(wavesData)

    for ssvp in list_ssvp:
        if( isinstance(ssvp,SSVPDataWithLabel) ): # For mypy
            

            analysis.add(ssvp.eeg, wavesData[ssvp.target_grid].freq)

            result = predict(ssvp.eeg,ATTEMPT16,[wave for wave in wavesData if wave is not None],remove_Thailand_power_line=True)
            # result = predict(ssvp.eeg,ATTEMPT16,[wave for wave in wavesData if wave is not None ],remove_Thailand_power_line=True)
        
         
            y_true = wavesData[ssvp.target_grid]

            y_hat:ssvp_freq_info.FP
            rho:list[float]
            y_hat,rho = result
 
            print("-"*20)
            print(f"{rho=}")
            print(f"{y_true=},{y_hat=}")
            if(y_true ==  y_hat ):
                count_correct+=1
    analysis.analyze_ssvp()
    print(f"acc: {count_correct/len(list_ssvp)}")

class Analysis:

    data_hz:dict[str,list[np.ndarray]]
    def __init__(self) -> None:

        self.channel = 3
        self.ch_types = ['eeg'] * (self.channel)
        self.data_hz = {}

    def add(self,data:np.ndarray,freq:float)->None:

        filtered_data:RawArray = mne.io.RawArray(to_mne_format(data),mne.create_info([str(i) for i in range(self.channel)],FS,self.ch_types))    
        filtered_data.notch_filter(np.arange(50, 125, 50), filter_length='auto', phase='zero')
        filtered_data = np.abs(filtered_data.get_data()[:,:220])
      
        
        if(str(freq) not in self.data_hz):
            self.data_hz[str(freq)] = []
        self.data_hz[str(freq)].append(filtered_data)
    
    def analyze_ssvp(self)->None:

        

        def x_freq(sample_rate:float,lenght_data:int)->np.ndarray:
            df = sample_rate/lenght_data
            return np.arange(0,sample_rate/2,df)

        plt.cla()
        for index,data_each_hz in self.data_hz.items():
       
            temp = data_each_hz[0]
            for i,each_data in enumerate(data_each_hz): 
           
                if(i==0):continue
                temp = np.concatenate((temp,each_data),axis=0)

   
            temp = temp.mean(axis=0)
   
          

            X = x_freq(FS,len(temp) )
            X = X[X<35]
          
            plt.scatter(X,temp[:len(X)],label=f"class-{index}")
            

        plt.legend()
        plt.savefig(f"./logs/{P_ID}-all-mean.png")
