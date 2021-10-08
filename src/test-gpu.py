import torch
import sys
print(sys.version)
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))