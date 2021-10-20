from typing import cast
from matplotlib import pyplot as plt #type:ignore
from PIL import Image #type:ignore
import numpy as np
from module.experiment_info import ATTEMPT2
from mongo.query.get_dataset import ExperimentDoc, compose_p300_dataset, get_eeg_docs, get_experiment_docs

from series002.modules.eeg_to_img import eeg_to_img
from series002.main import SELECTED_EEG_CHANNELS
from module.dataset_helper import P300DataFilter

import random
random.seed(10)
      

def main(p_id:str):

    eeg_docs = get_eeg_docs(p_id)
    experiment_docs = get_experiment_docs(p_id)[:20]


    data_ori =  P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT2,SELECTED_EEG_CHANNELS)).balance_class().done()
   
    index= 0
    for each_ori in data_ori :
        
        plt.cla()
        for channel in range(each_ori.eeg.shape[1]):
            plt.plot(list(range(each_ori.eeg.shape[0])),each_ori.eeg[:,channel])

        plt.savefig(f"series002/p300_plot/{index}-{each_ori.target}-all-gitignore.png")

        img_arr = eeg_to_img(each_ori.eeg).reshape(64,64)
        print(img_arr.sum())
        img = Image.fromarray(img_arr,'L')
       
        
        img.save(f"series002/p300_plot/{index}-{each_ori.target}-mean-gitignore.png")

      

        index+=1
        
    

