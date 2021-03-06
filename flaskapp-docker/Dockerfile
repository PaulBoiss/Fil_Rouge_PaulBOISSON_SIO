FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install python3-pip -y


COPY requirements.txt requirements.txt
COPY ./flaskapp /opt/
COPY .aws/ /aws/

# A l'intérieur du conteneur
RUN pip3 install -r requirements.txt
WORKDIR /opt/

CMD python3 main.py
