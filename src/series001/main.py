from torch.utils.data import DataLoader
from torch import Tensor
from torch.nn import BCELoss
from torch.optim import Adam
import mne #type:ignore
from torch.utils.data import Dataset


from module.dataset_helper import P300DataFilter, train_test_splitter
from module.eval_helper import acc, to_one_hot 
from .model import CNN_1D_FC
from module.experiment_info import ATTEMPT1
from module.gpu_helper import to_gpu
from mongo.query.get_torch_dataset import P300Dataset
from mongo.query.get_dataset import  compose_p300_dataset, get_eeg_docs, get_experiment_docs



EEG_CHANNEL = len(ATTEMPT1.headset_info.channel_names)
LEARNING_RATE = 1e-3
L2_RATE  = 1e-6
EPOCH = 10
MOD = EPOCH//5 

def train(p_id:str):
    mne.set_log_file("./mne.log",overwrite=True)
  

    eeg_docs = get_eeg_docs(p_id)
    experiment_docs = get_experiment_docs(p_id)

  
    data_with_data_clearning = P300DataFilter(compose_p300_dataset(eeg_docs,experiment_docs,ATTEMPT1)).random_seed(10).balance_class().done()

   
 

    training_set,test_set = train_test_splitter(data_with_data_clearning,train_size=1)
 
    dataset:Dataset = P300Dataset(training_set)
    data_loader:DataLoader = DataLoader(dataset,batch_size=10)

    model = CNN_1D_FC(
        [EEG_CHANNEL,512,256,128],
        [1792,512,128]
    )
    to_gpu(model)
    loss_func = BCELoss()
    optimizer = Adam(model.parameters(),lr=LEARNING_RATE,weight_decay=L2_RATE)
    data:dict
    y_true:Tensor
    y_hat:Tensor
    for e in range(EPOCH):
     
        for data in data_loader:
            eeg:Tensor = data['eeg']
            y_true = data['target'].reshape(-1,1).float()
            y_true = to_gpu(y_true)
            y_hat = model(to_gpu(eeg))

            optimizer.zero_grad()
            loss = loss_func(y_hat,y_true)
            loss.backward()

            optimizer.step()
        if(e%MOD==0):
            print(to_one_hot(y_true))
            print(to_one_hot(y_hat))
            print(acc(to_one_hot(y_true),to_one_hot(y_hat)))

    # with torch.no_grad():
    #     test_input = DataLoader(P300Dataset(test_set),batch_size=len(test_set))
    #     for only_one_test_input in test_input:

    #         eeg:Tensor = only_one_test_input['eeg']
    #         y_true:Tensor = only_one_test_input['target'].reshape(-1,1).float()
    #         y_true = to_gpu(y_true)
    #         y_hat = model(to_gpu(eeg))

    #         print(to_one_hot(y_true))
    #         print(to_one_hot(y_hat))
    #         print(acc(to_one_hot(y_true),to_one_hot(y_hat)))
    

