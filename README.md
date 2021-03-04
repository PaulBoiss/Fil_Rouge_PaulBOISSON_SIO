# Introduction
Bienvenue sur mon API de gestion de fichiers, réalisé dans le cadre du Projet Fil Rouge du mastère spécialisé Ingénierie des Systèmes Informatiques Ouverts. L'objectif de ce mini projet est de réaliser une API de type REST en Python, accessible sur un serveur
distant hébergé dans le cloud. Le propos applicatif de cette API est d'accepter le dépôt de tout type de fichier et de le restituer au format JSON.

# Technologies utilisées
- **Hébergement du service :** Amazon Web Service EC2
- **Stockage des fichiers :** Amazon Web Service S3
- **Envoi des fichiers de Python vers S3 :** Boto3

# Pré-requis python
Cette API utilise différentes librairies précisées dans le fichier "Requirements". Pour installer ces librairies, on utilise PIP, l'installateur de paquets Python, qui est fourni par défaut avec les version de Python 3 supérieures à la version 3.4. 
    
## Librairies / Framerworks
boto3-1.16.59  
botocore-1.19.59   
jmespath-0.10.0  
python-dateutil-2.8.1   
s3transfer-0.3.4  


## Commandes 
Installation de Flask pour la création de serveur web:
&rarr; python3 -m pip install flask

Installation de Pillow pour la gestion des images:
&rarr; python3 -m pip install --upgrade Pillow

Installation de Pytest pour lancer le script de tests:
&rarr; python3 -m pip install -U pytest

Installation de Requests pour effectuer des requêtes à l'API directement avec Python:
&rarr; python3 -m pip install requests

Instalation de PyPDF2 pour la lecture de fichiers PDF
&rarr; pip install PyPDF2

Installation de boto3 pour l'accès à s3 depuis un script Python
&rarr; pip install boto3


# Lancement du serveur
Se mettre dans le dossiser Application et taper la commande: $ python3 main.py


# Obtenir la liste des fichiers contenus dans le bucket:
curl http://127.0.0.1:5000/list

# Uploader un fichier
Uploader un fichier avec curl. Se mettre dans son dossier 
curl -i -X POST -F "file=@FichierPNG.png"  http://127.0.0.1:5000/load


# Supprimer un fichier 
curl http://127.0.0.1:5000/delete/Filename

curl -i -X POST -F "file=@FichierPNG.png"  http://127.0.0.1:5000/mimetype

Depuis la console wsl, pour accéder aux fichiers de l'ordi: cd /mnt/c/Users/PC/Desktop/SIO/'ProjetFilRouge'/PaulBOISSON_Fil_Rouge


# Télécharger un fichier JSON existant:

curl -O http://127.0.0.1:5000/download/FichierPNG.json
Attention, avec cette commande, même si le fichier n'existe pas dans le bucket S3 un fichier portant son nom sera téléchargé. 



Pouvoir accéder au s3:
export AWS_PROFILE=csloginteacher
aws sts get-caller-identity
export AWS_PROFILE=csloginstudent
aws sts get-caller-identity


FROM python:3.8.5
ADD . /Application
WORKDIR /Application
RUN pip3 install -r requirements.txt
CMD python app.py


#FROM python:3.8.5
#ADD . /Application
#WORKDIR /Application
#RUN pip3 install -r requirements.txt
#CMD python main.py

#COPY credentials




-- docker compose
version: '2'
services:
    web:
        build: .
        ports:
            - "5000:5000"
        volumes:
            - .:/code
        depends_on:
            - redis
    redis:
        image: redis

gunicorn app:app