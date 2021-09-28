# EEG client

## Install

1. Install Python 3.9
2. Install pipenv

```bash
pip install pipenv
```

3. create a venv and install libs

```bash
pipenv install
```

## Configure

check config.py

- DUMMY mode: This mode can create a dummy streaming without connecting the real EEG headset for testing processes.
- DATA_SIZE: This is a size of an one package which is goint to submit to ML-server. I recommend ~headset-freq/2 

## Run

```bash
pipenv run python main.py
```