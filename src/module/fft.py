from typing import Sequence
from numpy import ndarray
import numpy as np 


def to_fft(data:ndarray,fs:int)->tuple[ndarray,ndarray]:
    """
    data should be 2D
    return (fft, x_axis)
    """

    def x_freq(sample_rate:float,lenght_data:int)->np.ndarray:
        df = sample_rate/lenght_data
        return np.arange(0,sample_rate/2,df)

    fft = np.abs(np.fft.fft(data))
    x_axis = x_freq(fs,len(data))

    return fft[:len(x_axis),:],x_axis

    
    
    