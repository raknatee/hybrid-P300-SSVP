from torch.utils.data import DataLoader
from torch import Tensor
from torch.nn import BCELoss
from torch.optim import Adam
import mne #type:ignore
from torch.utils.data import Dataset
import torch

from module.dataset_helper import P300DataFilter, train_test_splitter
from module.eval_helper import acc, to_one_hot 
from series001.model import CNN_1D_FC
from module.experiment_info import ATTEMPT2
from module.gpu_helper import to_gpu
from mongo.query.torch_dataset import P300Dataset
from mongo.query.get_dataset import  P300Data, compose_p300_dataset, get_eeg_docs, get_experiment_docs

import pickle
import os
import random

EEG_CHANNEL = 7
LEARNING_RATE = 8e-4
L2_RATE  = 1e-5
EPOCH = 150
BATCH_SIZE = 32
MOD = EPOCH//5 

torch.manual_seed(7777)
random.seed(7777)

def load_data(p_id:str, is_save:bool)->list[P300Data]:

    returned_data:list[P300Data]
    def load()->list[P300Data]:
        eeg_docs = get_eeg_docs(p_id)
        experiment_docs = get_experiment_docs(p_id)
        returned = P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT2)).balance_class().filtering_eeg_channel(list(range(7))).shuffle().done()
        return returned

    if is_save:
        file_name = f"dataset-{p_id}.pkl"
        if not os.path.exists(file_name):

    
            data_with_data_clearning = load()
            with open(file_name,"wb") as pkl_file:
                pickle.dump(data_with_data_clearning,pkl_file)
        
        data_from_pkl:list[P300Data]
        with open(file_name,"rb") as pkl_file:
            data_from_pkl = pickle.load(pkl_file)
        returned_data = data_from_pkl
    else:
        returned_data = load()
   
    return returned_data
def train(p_id:str):
    mne.set_log_file("./mne.log",overwrite=True)
  


  
    data_with_data_clearning = load_data(p_id,is_save=True)

   
    training_set,test_set = train_test_splitter(data_with_data_clearning,train_size=.7)
 
    dataset:Dataset = P300Dataset(training_set)
    data_loader:DataLoader = DataLoader(dataset,batch_size=BATCH_SIZE)

    model = CNN_1D_FC(
        [EEG_CHANNEL,128,128,64,32],
        [192,128,64]

        # [EEG_CHANNEL,512,256,128],
        # [1792,512,128]
    )
    to_gpu(model)
    loss_func = BCELoss()
    optimizer = Adam(model.parameters(),lr=LEARNING_RATE,weight_decay=L2_RATE)
    data:dict
    y_true:Tensor
    y_hat:Tensor
    
    for e in range(EPOCH):
        this_loss:float = 0
        for data in data_loader:
            eeg:Tensor = data['eeg'] 
            

            y_true = data['target'].reshape(-1,1).float()
            y_true = to_gpu(y_true)
            y_hat = model(to_gpu(eeg))
             

            optimizer.zero_grad()
            loss = loss_func(y_hat,y_true)
            loss.backward()
            this_loss+=float(loss)
            optimizer.step()
        if(e%MOD==0):
            
            
            with torch.no_grad():
                print(f"epoch {e} train")
                print(f"training loss {this_loss}")
                print(f"epoch {e} val")
                test_input = DataLoader(P300Dataset(test_set),batch_size=BATCH_SIZE)
                for data in test_input:

                    eeg_val:Tensor = data['eeg'] * 1e3
                    y_true_val:Tensor = data['target'].reshape(-1,1).float()
                    y_true_val = to_gpu(y_true_val)
                    y_hat = model(to_gpu(eeg_val))

                
                    print(to_one_hot(y_hat))
                    print(acc(to_one_hot(y_true_val),to_one_hot(y_hat)))

