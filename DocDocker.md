# Utilisation DockerFile

## Création d'une image Docker
sudo docker build --no-cache -t monimage .

Liste des images déjà construite:
&rarr; sudo docker images

Suppression d'une image:
&rarr; sudo rmi monimage

## Lancement d'un conteneur sur cette image (on y accède de l'extérieur par le port 80)
sudo docker run --rm -d -p 80:5000 monimage

Arrêt d'un conteneur
&rarr; sudo docker stop containerID

## Accéder au bash d'un conteneur:
docker exec -it <container name> /bin/bash

# Utilisation avec Docker Compose

## Lancement des conteneurs
sudo docker-compose build

sudo docker-compose up 
sudo docker-compose up -d


cd /mnt/c/Users/PC/Desktop/SIO/'ProjetFilRouge'/PaulBOISSON_Fil_Rouge/Fichiers_Test
curl -i -X POST -F "file=@FichierPNG.png"  http://34.201.129.140:80/load