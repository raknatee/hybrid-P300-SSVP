import torch
from torch.nn import Module,Sequential,Conv1d,ReLU,LeakyReLU,AvgPool1d,Linear,ReLU,Dropout,Sigmoid
from torch import Tensor
class CNN_1D_FC(Module):
    CNN:Sequential
    FC:Sequential
    def __init__(self,cnn_layers:list[int],fc_layers:list[int]):
        super().__init__()

        cnn_params:list[Module] = []
        for i in range(len(cnn_layers)-1):
            cnn_params.append(
                Conv1d(cnn_layers[i],cnn_layers[i+1],kernel_size=3)
            )
            cnn_params.append(
                LeakyReLU()
            )
            cnn_params.append(
                AvgPool1d(2)
            )

        self.CNN = Sequential(*cnn_params)

        fc_params:list[Module] = []
        for i in range(len(fc_layers)-1):
            fc_params.append(
                Linear(fc_layers[i],fc_layers[i+1])
            )
            fc_params.append(
                ReLU()
            )
            fc_params.append(
                Dropout(p=0.3)
            )

        fc_params.append(Linear(fc_layers[-1],1))
        fc_params.append(Sigmoid())
        self.FC = Sequential(*fc_params)

    def forward(self,X):

        batch_size,eeg,channel = X.shape
        X = X.reshape(batch_size,channel,eeg)
        X = Tensor.float(X)
       
        o = self.CNN(X)
        o = torch.flatten(o,start_dim=1)

        o = self.FC(o)


        return o
        