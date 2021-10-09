from typing import cast
from module.dataset_helper import DataExtractor, train_test_splitter
from .model import CNN_1D_FC
from module.experiment_info import ATTEMPT1
from mongo.query.get_torch_dataset import P300Dataset
from mongo.query.get_dataset import P300Data, get_p300_dataset_by_p_id
from torch.utils.data import DataLoader
from torch import Tensor
from torch.nn import BCELoss
from torch.optim import Adam
import mne #type:ignore
import logging

EEG_CHANNEL = len(ATTEMPT1.headset_info.channel_names)
LEARNING_RATE = 1e-2
L2_RATE  = 1e-3
EPOCH = 10

def main():
    mne.set_log_file("./mne.log",overwrite=True)
    
    data_with_data_clearning = DataExtractor(get_p300_dataset_by_p_id("A01S01",ATTEMPT1)).random_seed(10).balance_class().done()
    training_set,test_set = train_test_splitter(data_with_data_clearning,.7)

    dataset:DataLoader = P300Dataset(training_set)
    data_loader:DataLoader = DataLoader(dataset,batch_size=10)

    model = CNN_1D_FC(
        [EEG_CHANNEL,200,100,50],
        [700,50]
    )
    loss_func = BCELoss()
    optimizer = Adam(model.parameters(),lr=LEARNING_RATE,weight_decay=L2_RATE)
    data:dict
    for e in range(EPOCH):
        for data in data_loader:
            eeg:Tensor = data['eeg']
            y_true:Tensor = data['target'].reshape(-1,1).float()
            
            y_hat = model(eeg)
            optimizer.zero_grad()
            loss = loss_func(y_hat,y_true)
            loss.backward()

            optimizer.step()
            
            print(float(loss))
            print(list(map(int,y_true.flatten().tolist())))
            print(list(map(int,(y_hat>.5).flatten().tolist())))
          
            
            # return

