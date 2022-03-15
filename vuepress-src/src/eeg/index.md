# EEG & ML Model Selection

## For P300

### Node
- P

### ML Model
- From, [Brain Lab's (Chaky) Github](https://github.com/chanapapan/BCI/blob/master/Thai-P300-Speller/3-analysis/train_model.ipynb)
    - ERP + TS + LogisticRegression
    - ERP + MDM
    - Xdawn + RegLDA
    - Xdawn + MDM

## SSVEP

- Recommended Freq: 6-15 Hz

### Node
- O1 O2 [OZ]

### Prediction Method
- Based on [Chaky's Github](https://github.com/chaklam-silpasuwanchai/BCI/tree/master/SSVEP/utils)
- Filter-bank csp ( common spatial pattern ). It isn't a ML model but this method needs a parameter (THRESHOLD) which is required for each person.

# Using EEG Headset
- For set up the headset read [OpenBCI Doc](https://docs.openbci.com/AddOns/Headwear/MarkIV/)
- Before running the process, please check Amplitude of signal (must be less than 20 uVms), we can use [OpenBCI GUI](https://openbci.com/downloads)

