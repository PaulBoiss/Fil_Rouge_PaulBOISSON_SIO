# Introduction
Bienvenue sur mon API de gestion de fichiers, réalisé dans le cadre du Projet Fil Rouge du mastère spécialisé Ingénierie des Systèmes Informatiques Ouverts. L'objectif de ce mini projet est de réaliser une API de type REST en Python, accessible sur un serveur distant hébergé dans le cloud. Le propos applicatif de cette API est d'accepter le dépôt de tout type de fichier et de le restituer au format JSON.

# Service Amazon
- **Hébergement du service :** Amazon Web Service EC2
- **Stockage des fichiers :** Amazon Web Service S3

# QuickStart
Mon application est hébergée sur le domaine suivant :
https://filrouge.pbo.p2021.ajoga.fr
Elle permet à l’utilisateur de charger un fichier qui lui sera renvoyé sous forme d’un fichier JSON contenant ses métadonnées et ses données séparément. Ce fichier sera stocké dans un bucket du service AWS S3 et pourra être récupéré ultérieurement. 

## Utilisation de l'interface Swagger
Il est recommandé d’utiliser l’interface Swagger réalisée pour détailler les fonctionnalités de l’API depuis une interface graphique, à partir d’un navigateur web (Chrome, Firefox ou autre) à l’adresse suivante : https://filrouge.pbo.p2021.ajoga.fr/swagger. 

Afin de pouvoir utiliser l’application, un nom d’utilisateur et un mot de passe sont demandés. Un compte a été créé, il vous suffit donc de renseigner les informations suivantes :
-	Utilisateur : user
-	Mot de passe : user
Vous serez ensuite renvoyé vers l’interface Swagger. 

Depuis cette interface, vous pouvez lancer les 5 fonctionnalités de l’application :
-	Lister les fichiers qui ont déjà été chargés dans l’application
-	Supprimer un des fichiers
-	Télécharger un des fichiers
-	Envoyer un fichier vers l’application
-	Recevoir un « Hello World » de l’application
(Si l’interface ne s’affiche pas, n’hésitez pas à actualiser la page, le nombre de requêtes par utilisateur étant limité à la minute, il se peut que nginx bloque votre requête) 

L’application supporte les fichiers au formats png, jpg, jpeg, gif, txt, PDF, csv. 

## Utilisation de l’interface avec curl
Il est également possible d’utiliser l’application en utilisant la commande curl via une invite de commande (terminal Ubuntu par exemple). 

**Afficher la liste des fichiers déjà chargés :**
$ curl -u user:user https://filrouge.pbo.p2021.ajoga.fr/list

**Envoyer un fichier :**  
$ curl -i -u user:user -X POST -F "file=@nomfichier.extension"  https://filrouge.pbo.p2021.ajoga.fr/load

**Télécharger un fichier déjà envoyé :**  
$ curl -u user:user -O http://127.0.0.1:5000/download/Filename

**Supprimer un fichier :**   
$ curl -u user :user http://127.0.0.1:5000/delete/Filename
