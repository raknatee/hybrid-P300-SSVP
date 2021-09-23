# hybrid-P300-SSVP

## Dummy Mode
dummy mode is a simulation of ml-server and eeg-client for demo the client(web-GUI) which all endpoints already implemented and followed by Document

1. start
```bash
docker-compose -f docker-compose-dummy.yml up --build
```

2. To simulate like we already connected the headset and it can do data streaming to ml-server
```bash
docker-compose -f docker-compose-dummy.yml exec eeg-client bash
```
```bash
python main.py
```

3. shutdown
```bash
docker-compose -f docker-compose-dummy.yml down
```