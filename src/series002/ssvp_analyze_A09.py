
from typing import Union
import mne #type:ignore

from matplotlib import pyplot as plt #type:ignore
from mne.io.array.array import RawArray #type:ignore
import numpy as np
from scipy.ndimage.measurements import label #type:ignore

from module import object_saver

from module.experiment_info import ATTEMPT2, ATTEMPT3, ATTEMPT4, ATTEMPT5, ATTEMPT6, ATTEMPT7, ATTEMPT8, ExperimentInfo

from module.ssvp_module import ssvp_freq_info
from module.ssvp_module.fbcca import predict
from mongo.query.torch_dataset import P300Dataset
from mongo.query.get_dataset import  P300Data, SSVPData, SSVPDataWithLabel, compose_p300_dataset, compose_ssvp_dataset, get_eeg_docs, get_experiment_docs, get_experiment_docs_with_target_grid, to_mne_format


mne.set_log_file("./logs/mne.log",overwrite=True)

P_ID = "A10S01"
def main():
    def load()->Union[list[SSVPData],list[SSVPDataWithLabel]]:
    
        eeg_docs = get_eeg_docs(P_ID)
        experiment_docs = get_experiment_docs_with_target_grid(P_ID)


        return compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT8,(10,20),[*[0,1,2]])

 


    list_ssvp = object_saver.disk_cache(load,f"{P_ID}-ssvp.pkl")

    count_correct = 0 
    analysis = Analysis()
    # wavesData = [None,None,ssvp_freq_info.FP(6, 0),None,ssvp_freq_info.FP(11,0),None,None,ssvp_freq_info.FP(15,0),None, None,None,None]
    wavesData = [None,None,ssvp_freq_info.FP(6, 0),None,ssvp_freq_info.FP(10,0),None,None,ssvp_freq_info.FP(16,0),None, None,None,None]
    for ssvp in list_ssvp:
        if( isinstance(ssvp,SSVPDataWithLabel) ): # For mypy
            

            current_fp = wavesData[ssvp.target_grid]
            if current_fp is not None:
                analysis.add(ssvp.eeg, int(current_fp.freq))


            result = predict(ssvp.eeg,ATTEMPT8,[wave for wave in wavesData if wave is not None],remove_Thailand_power_line=True)
        
         
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
    # data_6_hz:list[np.ndarray]
    # data_11_hz:list[np.ndarray]
    # data_15_hz:list[np.ndarray]
    data_6_hz:list[np.ndarray]
    data_10_hz:list[np.ndarray]
    data_16_hz:list[np.ndarray]
    def __init__(self) -> None:
        # self.data_6_hz = []
        # self.data_11_hz = []
        # self.data_15_hz = []
        self.data_6_hz = []
        self.data_10_hz = []
        self.data_16_hz = []
        self.channel = 3
        self.ch_types = ['eeg'] * (self.channel)

    def add(self,data:np.ndarray,freq:int)->None:

        filtered_data:RawArray = mne.io.RawArray(to_mne_format(data),mne.create_info([str(i) for i in range(self.channel)],230,self.ch_types))    
        filtered_data.notch_filter(np.arange(50, 125, 50), filter_length='auto', phase='zero')
        filtered_data = np.abs(filtered_data.get_data()[:,:440])

        if(freq==6):
            self.data_6_hz.append(filtered_data)
        if(freq==10):
            self.data_10_hz.append(filtered_data)
        if(freq==16):
            self.data_16_hz.append(filtered_data)
    
    def analyze_ssvp(self)->None:

        

        def x_freq(sample_rate:float,lenght_data:int)->np.ndarray:
            df = sample_rate/lenght_data
            return np.arange(0,sample_rate/2,df)

        plt.cla()

        for index,data_each_hz in enumerate([self.data_6_hz,self.data_10_hz,self.data_16_hz]):
        # for index,data_each_hz in enumerate([self.data_6_hz,self.data_11_hz,self.data_15_hz]):
            temp = data_each_hz[0]
            for i,each_data in enumerate(data_each_hz): 
                if(i==0):continue
                temp = np.concatenate((temp,each_data),axis=0)


       
            temp = temp.mean(axis=0)
          

            X = x_freq(230,len(temp) )
            X = X[X<20]
          
            plt.plot(X,temp[:len(X)],label=f"class-{index}")
            

        plt.legend()
        plt.savefig(f"./logs/{P_ID}-all-mean.png")