import torch
from torch.nn import Module,Sequential,Conv2d,ReLU,LeakyReLU,MaxPool2d,Linear,ReLU,Dropout,Sigmoid,BatchNorm2d,BatchNorm1d,Dropout2d
from torch import Tensor
class CNN_2D_FC(Module):
    CNN:Sequential
    FC:Sequential
    def __init__(self,cnn_layers:list[int],fc_layers:list[int]):
        super().__init__()

        cnn_params:list[Module] = []
        for i in range(len(cnn_layers)-1):
         
            cnn_params.append(
                Conv2d(cnn_layers[i],cnn_layers[i+1],kernel_size=3)
            )
            cnn_params.append(
                ReLU()
            )
            # cnn_params.append(
            #     Dropout2d(p=0.5)
            # )
            # cnn_params.append(
            #     BatchNorm2d(cnn_layers[i+1])
            # )
            cnn_params.append(
                MaxPool2d(2)
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
                Dropout(p=0.5)
            )
            fc_params.append(
                BatchNorm1d(fc_layers[i+1])
            )

        fc_params.append(Linear(fc_layers[-1],1))
        fc_params.append(Sigmoid())
        self.FC = Sequential(*fc_params)

    def forward(self,X):

        X = Tensor.float(X)
       
        o = self.CNN(X)
        o = torch.flatten(o,start_dim=1)

        o = self.FC(o)


        return o
        