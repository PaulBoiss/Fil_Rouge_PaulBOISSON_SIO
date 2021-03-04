FROM ubuntu:20.04y

RUN apt-get update -y
RUN apt-get install python3-pi -y
RUN apt-get install gunicorn3 -y

COPY requirements.txt requirements.txt
COPY ./flaskapp /opt/

# A l'intérieur du conteneur
RUN pip3 install -r requirements.txt
WORKDIR /opt/

CMD python main.py
#CMD ["gunicorn3","-b","0.0.0.0:8000","app:app","--workers=5"]