FROM python:3.9.7-buster
WORKDIR /home/src
COPY ./src /home/src/

RUN pip install "websockets==10.0"

CMD tail -f /dev/null
# CMD python main.py