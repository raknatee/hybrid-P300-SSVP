# Application Protopol

## Offline mode
- we can call it like a collecting data mode

### Flow program


- Open GUI (js) then set the collection name and submit it before going to next step. [/db](../ml-server/index.md#db)
    
- Create a EEG streaming to [/eeg_offline/\<PID>](../ml-server/index.md#eeg-offline-participant-id) using EEG-client
- Click run Experiment from GUI. A client (js) would connect to backend [/begin_offline_mode](../ml-server/index.md#begin-offline-mode-participant-id)
- ML-server would store data from both GUI and EEG-client to data storage. Then, we can match signal by using timestamp.

## Online mode

### Flow program

