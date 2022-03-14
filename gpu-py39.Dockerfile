FROM tensorflow/tensorflow:2.6.0

WORKDIR /home/src

RUN apt update -y && apt upgrade -y
ENV DEBIAN_FRONTEND="noninteractive"

RUN apt install -yfm --no-install-recommends libgl1-mesa-glx libgtk2.0-dev

RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa


RUN apt install python3.9 -y
RUN apt install python3-pip -y
RUN apt install python3.9-distutils -y
RUN pip3 install pipenv

RUN pipenv --python 3.9 
# RUN pipenv install jupyter-contrib-nbextensions==0.5.1 --ignore-pipfile
# RUN pipenv run jupyter contrib nbextension install

RUN pipenv install torch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 --ignore-pipfile
RUN pipenv install 'pillow' --ignore-pipfile
RUN pipenv install "opencv-python==4.5.3.56" --ignore-pipfile
RUN pipenv install "sklearn" --ignore-pipfile
RUN pipenv install "pandas" --ignore-pipfile
RUN pipenv install "seaborn" --ignore-pipfile
RUN pipenv install "matplotlib" --ignore-pipfile
RUN pipenv install "pymongo==3.12.0" --ignore-pipfile
RUN pipenv install "mypy==0.910" --ignore-pipfile
RUN pipenv install "pytest==6.2.5" --ignore-pipfile
RUN pipenv install "mne==0.23.4" --ignore-pipfile
RUN pipenv install "scipy==1.7.1" --ignore-pipfile


# COPY ./jupyter_config /root/.jupyter
CMD tail -f /dev/null
# CMD pipenv run jupyter notebook --ip='*' --port=8888 --no-browser  --allow-root