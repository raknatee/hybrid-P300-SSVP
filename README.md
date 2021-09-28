# hybrid-P300-SSVP

## Dummy Mode
dummy mode is a simulation of ml-server and eeg-client for demonstrate the client(web-GUI) which all endpoints already implemented and followed by Document

1. start
```bash
docker-compose -f docker-compose.yml up --build
```

2. To simulate like we already plugged and connected the headset and it can do data streaming to ml-server.
   1.  cd to eeg-client
   2.  configure config.py change DUMMY_MODE = True
   3.  start

```bash
pipenv run python main.py
```

3. shutdown
```bash
docker-compose -f docker-compose.yml down
```