
import torch
from torch.cuda import is_available
DO_GPU:bool = True

def to_gpu(item):

    if(torch.cuda.is_available() and DO_GPU):
        return item.cuda()
    else:
        return item