from operator import index
from typing import Union, cast
from torch.utils.data import DataLoader
from torch import Tensor
from torch.nn import BCELoss
from torch.optim import Adam
import mne #type:ignore
from torch.utils.data import Dataset
import torch

from module.dataset_helper import P300DataFilter, train_test_splitter
from module.eval_helper import acc, to_one_hot 
from module import object_saver

from module.experiment_info import ATTEMPT2, ATTEMPT3, ATTEMPT4, ATTEMPT5, ATTEMPT6, ATTEMPT7, ATTEMPT8, ExperimentInfo
from module.gpu_helper import to_gpu
from module.ssvp_module import ssvp_freq_info
from module.ssvp_module.fbcca import predict
from mongo.query.torch_dataset import P300Dataset
from mongo.query.get_dataset import  P300Data, SSVPData, SSVPDataWithLabel, compose_p300_dataset, compose_ssvp_dataset, get_eeg_docs, get_experiment_docs, get_experiment_docs_with_target_grid


import random

from series002.modules.eeg_to_img import eeg_to_img
from series002.model import CNN_2D_FC

SELECTED_EEG_CHANNELS = [3,4,5,6]
LEARNING_RATE = 8e-4
L2_RATE  = 1e-3
EPOCH = 5000
BATCH_SIZE = 32
MOD = 100

torch.manual_seed(7777)
random.seed(7777)
mne.set_log_file("./logs/mne.log",overwrite=True)


def load_data(p_id:str)->list[P300Data]:
    eeg_docs = get_eeg_docs(p_id)
    experiment_docs = get_experiment_docs(p_id)
    returned = P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT2,SELECTED_EEG_CHANNELS,eeg_transform_func=eeg_to_img)).balance_class().shuffle().done()
    return returned

   
def train(p_id:str):
  


    data_with_data_clearning =  object_saver.disk_cache(lambda: load_data(p_id),f"{p_id}-P300.pkl")

 
    training_set,test_set = train_test_splitter(data_with_data_clearning,train_size=.7)
 

    dataset:Dataset = P300Dataset(training_set)
    data_loader:DataLoader = DataLoader(dataset,batch_size=BATCH_SIZE)

    model = CNN_2D_FC(
        [1,128,64,32,16],
        [64,32,16]

    )
    to_gpu(model)
    loss_func = BCELoss()
    optimizer = Adam(model.parameters(),lr=LEARNING_RATE,weight_decay=L2_RATE)
    data:dict

    
    for e in range(EPOCH):
        this_loss:float = 0

        if(e%MOD==0):
            print(f"epoch {e} train")
                
        for data in data_loader:
            
            eeg:Tensor = data['eeg']
         
  
            y_train_true = data['target'].reshape(-1,1).float()
            y_train_true = to_gpu(y_train_true)
            y_train_hat = model(to_gpu(eeg))
             

            optimizer.zero_grad()
            loss = loss_func(y_train_hat,y_train_true)
            loss.backward()
            this_loss+=float(loss)
            optimizer.step()
            if(e%MOD==0):
                
                print("acc train in this batch",acc(to_one_hot(y_train_true),to_one_hot(y_train_hat)))

        if(e%MOD==0):
            
            
            with torch.no_grad():
                print(f"training loss in this epoch: {this_loss}")
                print(f"epoch {e} val")

                test_input = DataLoader(P300Dataset(test_set),batch_size=BATCH_SIZE)
                for data in test_input:

                    eeg_val:Tensor = data['eeg']
                    y_val_true:Tensor = data['target'].reshape(-1,1).float()
                    y_val_true = to_gpu(y_val_true)
                    y_val_hat = model(to_gpu(eeg_val))

                
                    print(f"{acc(to_one_hot(y_val_true),to_one_hot(y_val_hat))} y_val_hat:{to_one_hot(y_val_hat)}")
               

def ssvp(p_id:str):
    def load()->list[Union[SSVPData,SSVPDataWithLabel]]:
    
        eeg_docs = get_eeg_docs(p_id)
        experiment_docs = get_experiment_docs_with_target_grid(p_id)


        return compose_ssvp_dataset(eeg_docs,experiment_docs,attempt_config,(10,20),[*[0,1,2]])
        # return compose_ssvp_dataset(eeg_docs,experiment_docs,ATTEMPT2,[*[0,1,2],*[3,4,5,6]])


    attempt_config:ExperimentInfo
    if("A02" in p_id):
        attempt_config=ATTEMPT2
    if("A03" in p_id):
        attempt_config=ATTEMPT3
    if("A04" in p_id):
        attempt_config=ATTEMPT4
    if("A05" in p_id):
        attempt_config=ATTEMPT5
    if("A06" in p_id):
        attempt_config=ATTEMPT6
    if("A07" in p_id):
        attempt_config=ATTEMPT7

    list_ssvp = object_saver.disk_cache(load,f"{p_id}-ssvp.pkl")

    count_correct = 0 
    
    for ssvp in list_ssvp:
        if( isinstance(ssvp,SSVPDataWithLabel) ): # For mypy
         
            result = predict(ssvp.eeg,attempt_config)
        
            y_true = ssvp_freq_info.wave_data[ssvp.target_grid]
            
            y_hat:ssvp_freq_info.FP
            rho:list[float]
            y_hat,rho = result

            print("-"*20)
            print(f"{rho=}")
            print(f"{y_true=},{y_hat=}")
            if(y_true ==  y_hat ):
                count_correct+=1

    print(f"acc: {count_correct/len(list_ssvp)}")

def analyze_ssvp():
    pass