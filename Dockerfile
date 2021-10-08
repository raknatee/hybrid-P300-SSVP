FROM tensorflow/tensorflow:2.6.0

# -------------------------------------------------- install python
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt-get update
# ENV DEBIAN_FRONTEND="noninteractive"

# RUN apt install -yfm --no-install-recommends libgl1-mesa-glx libgtk2.0-dev
# RUN apt-get install python3.9 -y
# RUN apt-get install python3-pip -y

# -------------------------------------------------- install python done


RUN pip install jupyter-contrib-nbextensions==0.5.1
RUN jupyter contrib nbextension install
RUN pip install 'pillow==7.2.0'
RUN pip install 'torch==1.6.0'
RUN pip install 'torchvision==0.2.2'
RUN pip install "opencv-python==4.4.0.44"
RUN pip install "sklearn"
RUN pip install "pandas"
RUN pip install "seaborn"
RUN pip install "matplotlib"



# COPY ./jupyter_config /root/.jupyter
CMD jupyter notebook --ip='*' --port=8888 --no-browser  --allow-root