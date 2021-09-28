# hybrid-P300-SSVP

## Get Started
dummy mode is a simulation of ml-server and eeg-client for demonstrate the client(web-GUI) which all endpoints already implemented and followed by Document

1. start
```bash
docker-compose -f docker-compose.yml up --build -d
```

2. check localhost:8080

3. check a EEG headset and run EEG-client. Please go to "eeg-client" for more details. It also supports DUMMY mode.

4. shutdown
```bash
docker-compose -f docker-compose.yml down
```