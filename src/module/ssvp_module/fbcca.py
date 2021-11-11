

import sys
from typing import Optional, Union, overload
from mne.io.array.array import RawArray #type:ignore
from numpy.ma.core import count
from sklearn.cross_decomposition import CCA #type:ignore

from module.ssvp_module.ssvp_freq_info import FP,wave_data
from module.experiment_info import ExperimentInfo
from mongo.query.get_dataset import to_mne_format
from .filterbank import filterbank #type:ignore
from scipy.stats import pearsonr, mode #type:ignore
from matplotlib import pyplot as plt #type:ignore
import numpy as np
import mne #type:ignore


def zero_padding(data:np.ndarray)->np.ndarray:
    len_data = data.shape[0]
    len_channel  = data.shape[1]    
    padding_array = np.zeros((len_data*9,len_channel))
    data = np.concatenate((data,padding_array),axis=0)

    return data

def fft(data:list[float],sample_rate:float)->tuple[np.ndarray,np.ndarray]:
    """
    return fft, X
    """
    def x_freq(sample_rate:float,lenght_data:int)->np.ndarray:
            df = sample_rate/lenght_data
            return np.arange(0,sample_rate/2,df)

    data_fft = np.abs(np.fft.fft(np.array(data)))

    return data_fft, x_freq(sample_rate,len(data_fft))

@overload
def predict(eeg:np.ndarray,experiment_info:ExperimentInfo)->tuple[FP,list[float]]:
    ...

@overload
def predict(eeg:np.ndarray,experiment_info:ExperimentInfo,freqs:list[FP])->tuple[FP,list[float]]:
    ...

@overload
def predict(eeg:np.ndarray,experiment_info:ExperimentInfo,freqs:list[FP],remove_Thailand_power_line:bool)->tuple[FP,list[float]]:
    ...

@overload
def predict(eeg:np.ndarray,experiment_info:ExperimentInfo,freqs:list[FP],remove_Thailand_power_line:bool,enable_zero_padding:bool)->tuple[FP,list[float]]:
    ...

def predict(eeg:np.ndarray,experiment_info:ExperimentInfo,freqs:Optional[list[FP]]=None,remove_Thailand_power_line:bool=False,enable_zero_padding:bool=False)->tuple[FP,list[float]]:

    if(enable_zero_padding):
        eeg = zero_padding(eeg)
    channel = eeg.shape[1]

    ch_types = ['eeg'] * (channel)

  
    eeg_mne_arr:RawArray =  mne.io.RawArray(to_mne_format(eeg),mne.create_info([str(i) for i in range(channel)],experiment_info.headset_info.sample_rate,ch_types))    
    
    if(remove_Thailand_power_line):
        eeg_mne_arr.notch_filter(np.arange(50, 125, 50), filter_length='auto', phase='zero')
 


    eeg_numpy:np.ndarray = np.expand_dims(eeg_mne_arr.get_data(), axis=0)
    


    if(freqs is None):
        freqs_default:list[FP] = [wave for wave in wave_data if wave is not None]
        return fbcca(eeg_numpy,freqs_default,experiment_info.headset_info.sample_rate)


    return fbcca(eeg_numpy,freqs,experiment_info.headset_info.sample_rate)


"""
Created on Wed Oct 30 10:17:50 2019

@author: ALU

Steady-state visual evoked potentials (SSVEPs) detection using the filter
bank canonical correlation analysis (FBCCA)-based method [1].

function results = test_fbcca(eeg, list_freqs, fs, num_harms, num_fbs)

Input:
  eeg             : Input eeg data 
                    (# of targets, # of channels, Data length [sample])
  list_freqs      : List for stimulus frequencies
  fs              : Sampling frequency
  num_harms       : # of harmonics
  num_fbs         : # of filters in filterbank analysis

Output:
  results         : The target estimated by this method

Reference:
  [1] X. Chen, Y. Wang, S. Gao, T. -P. Jung and X. Gao,
      "Filter bank canonical correlation analysis for implementing a 
       high-speed SSVEP-based brain-computer interface",
      J. Neural Eng., vol.12, 046008, 2015.

"""
# Adapted for working with python mne

def fbcca(eeg:np.ndarray, freqs:list[FP], sampling_frequency:Union[float,int], num_harms=5, num_fbs=5)->tuple[FP,list[float]]:

   
    fb_coefs = np.power(np.arange(1, num_fbs + 1), (-1.25)) + 0.25

    num_targs = len(freqs)
    events, _, num_smpls = eeg.shape  # 40 taget (means 40 fre-phase combination that we want to predict)
    y_ref = cca_reference(freqs, sampling_frequency, num_smpls, num_harms)
    cca = CCA(n_components=1)  # initilize CCA

    # result matrix
    rho:np.ndarray
    r = np.zeros((num_fbs, num_targs))
    results = np.zeros(num_targs)
    r_mode = []
    r_corr_avg = []

    for event in range(eeg.shape[0]):
        
        test_tmp = np.squeeze(eeg[event, :, :])  # deal with one event a time





        for fb_i in range(num_fbs):  # filter bank number, deal with different filter bank
            for class_i in range(num_targs):
                testdata = filterbank(test_tmp, sampling_frequency, fb_i)  # data after filtering
                refdata = np.squeeze(y_ref[class_i, :, :])  # pick corresponding freq target reference signal
                test_C, ref_C = cca.fit_transform(testdata.T, refdata.T)
                # len(row) = len(observation), len(column) = variables of each observation
                # number of rows should be the same, so need transpose here
                # output is the highest correlation linear combination of two sets
                r_tmp, _ = pearsonr(np.squeeze(test_C),
                                    np.squeeze(ref_C))  # return r and p_value, use np.squeeze to adapt the API
                if r_tmp == np.nan:
                    r_tmp = 0
                r[fb_i, class_i] = r_tmp
        rho = np.dot(fb_coefs, r)  # weighted sum of r from all different filter banks' result
        # print("rho: ", rho)
        result = np.argmax(rho)
        # print("result: ", result)
        r_mode.append(result)
        # print("correlation: ", abs(rho[result]))
        r_corr_avg.append(abs(rho[result]))
    # print("====Most recurrent class: ====", mode(r_mode)[0][0])
    # print("====Average correlation: =====", np.mean(r_corr_avg))
    return freqs[mode(r_mode)[0][0]],rho.tolist()


'''
Generate reference signals for the canonical correlation analysis (CCA)
-based steady-state visual evoked potentials (SSVEPs) detection [1, 2].

function [ y_ref ] = cca_reference(listFreq, fs,  nSmpls, nHarms)

Input:
  listFreq        : List for stimulus frequencies
  fs              : Sampling frequency
  nSmpls          : # of samples in an epoch
  nHarms          : # of harmonics

Output:
  y_ref           : Generated reference signals
                   (# of targets, 2*# of channels, Data length [sample])

Reference:
  [1] Z. Lin, C. Zhang, W. Wu, and X. Gao,
      "Frequency Recognition Based on Canonical Correlation Analysis for 
       SSVEP-Based BCI",
      IEEE Trans. Biomed. Eng., 54(6), 1172-1176, 2007.
  [2] G. Bin, X. Gao, Z. Yan, B. Hong, and S. Gao,
      "An online multi-channel SSVEP-based brain-computer interface using
       a canonical correlation analysis method",
      J. Neural Eng., 6 (2009) 046002 (6pp).
'''

def cca_reference(freqs:list[FP], fs, num_smpls, num_harms=3):
    num_freqs = len(freqs)
    tidx = np.arange(1, num_smpls + 1) / fs  # time index

    y_ref = np.zeros((num_freqs, 2 * num_harms, num_smpls)) 
    for freq_i in range(num_freqs):
        tmp = []
        for harm_i in range(1, num_harms + 1):
            stim_freq = freqs[freq_i].freq  # in HZ
            phase = freqs[freq_i].phare
            # Sin and Cos
            tmp.extend([np.sin(2 * np.pi * tidx * harm_i * stim_freq + np.pi *phase),
                        np.cos(2 * np.pi * tidx * harm_i * stim_freq + np.pi *phase)
                        ])

        y_ref[freq_i] = tmp  # 2*num_harms because include both sin and cos

    return y_ref


'''
Base on fbcca, but adapt to our input format
'''

def fbcca_realtime(eeg, list_freqs, fs, num_harms=3, num_fbs=5):
    print("EEG shape: ", eeg.shape)

    fb_coefs = np.power(np.arange(1, num_fbs + 1), (-1.25)) + 0.25

    num_targs = len(list_freqs)
    events, _, num_smpls = eeg.shape  # 40 taget (means 40 fre-phase combination that we want to predict)
    y_ref = cca_reference(list_freqs, fs, num_smpls, num_harms)
    cca = CCA(n_components=1)  # initilize CCA

    # result matrix
    r = np.zeros((num_fbs, num_targs))
    results = np.zeros(num_targs)
    r_tmp_mode = []
    r_tmp_corr_avg = []

    for event in range(eeg.shape[0]):
        test_tmp = np.squeeze(eeg[event, :, :])  # deal with one event a time
        for fb_i in range(num_fbs):  # filter bank number, deal with different filter bank
            for class_i in range(num_targs):
                testdata = filterbank(test_tmp, fs, fb_i)  # data after filtering
                refdata = np.squeeze(y_ref[class_i, :, :])  # pick corresponding freq target reference signal
                test_C, ref_C = cca.fit_transform(testdata.T, refdata.T)
                # len(row) = len(observation), len(column) = variables of each observation
                # number of rows should be the same, so need transpose here
                # output is the highest correlation linear combination of two sets
                r_tmp, _ = pearsonr(np.squeeze(test_C),
                                    np.squeeze(ref_C))  # return r and p_value, use np.squeeze to adapt the API
                if r_tmp == np.nan:
                    r_tmp = 0
                r[fb_i, class_i] = r_tmp
        rho = np.dot(fb_coefs, r)  # weighted sum of r from all different filter banks' result
        print("rho: ", rho)
        result = np.argmax(rho) # get maximum from the target as the final predict (get the index), and index indicates the maximum entry(most possible target)
        print("result: ", result)
        r_tmp_mode.append(result)
        print("correlation: ", abs(rho[result]))
        r_tmp_corr_avg.append(abs(rho[result]))
    r_mode = mode(r_tmp_mode)[0][0]
    r_corr_avg = np.mean(r_tmp_corr_avg)
    print("====Most recurrent class: ====", r_mode)
    print("====Average correlation: =====", r_corr_avg)

    THRESHOLD = 0.3
    if r_corr_avg >= THRESHOLD:  # 2.749=np.sum(fb_coefs*0.85)
        return r_mode  # if the correlation isn't big enough, do not return any command