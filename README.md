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


# Fonctionnalités
Uploader un fichier avec curl. Se mettre dans son dossier 
curl -i -X POST -F "file=@FichierPNG.png"  http://127.0.0.1:5000/load

curl http://127.0.0.1:5000/list

curl -i -X POST -F "file=@FichierPNG.png"  http://127.0.0.1:5000/mimetypes


Depuis la console wsl, pour accéder aux fichiers de l'ordi: cd /mnt/c/Users/PC/Desktop/SIO/'ProjetFilRouge'/PaulBOISSON_Fil_Rouge



Pouvoir accéder au s3:
export AWS_PROFILE=csloginteacher
aws sts get-caller-identity
export AWS_PROFILE=csloginstudent
aws sts get-caller-identity

if not os.path.exists(exampleFolder + picture):
	    return "Ce fichier n'est pas présent dans le dossier Fichiers_Test \n "
	elif os.path.exists(app.config['UPLOAD_FOLDER'] + picture):
		return 'Fichier déjà chargé \n '
	elif picture == '':
		return 'Aucun fichier sélectionné \n '
	elif extension == 'pdf':
		document = PdfFileReader(open(os.path.join(exampleFolder, picture),'rb'))
		pdftext = ""
		for page in range(document.numPages):
			pageObj = document.getPage(page)
			pdftext += pageObj.extractText().replace('\n','')
		fichierJson = json.dumps({'Nom':name,'Metadonnees':document.getDocumentInfo(),'Donnees':pdftext})
		with open(os.path.join(app.config['UPLOAD_FOLDER'],name +'.json'),"w") as file: 
			json.dump(fichierJson,file)
		return 'ok \n '
	elif extension in {'png','jpg','jpeg','gif'}:
		with open(os.path.join(exampleFolder, picture),'rb') as img_file:
			imageB64 = base64.b64encode(img_file.read())
		imageJson = json.dumps({'Nom':name, 'extension':extension,'Donnees':imageB64.decode("utf-8")})
		with open(os.path.join(app.config['UPLOAD_FOLDER'],name +'.json'),"w") as file: 
				json.dump(imageJson,file)
		return "ok \n "
	elif extension == "csv":
		liste = ""
		with open(os.path.join(exampleFolder, picture),"r") as csvfile:
			csvReader = csv.reader(csvfile, delimiter=';',quotechar='|')
			for row in csvReader:
				liste += ", "+ str(row)
		CSVJson = json.dumps({'Nom':name, 'extension':extension,'Donnees':liste})
		with open(os.path.join(app.config['UPLOAD_FOLDER'],name +'.json'),"w") as file: 
				json.dump(CSVJson,file)
		return "ok \n"
	elif extension == "txt":
		with open(os.path.join(exampleFolder, picture),"r") as txtfile:
			texte = txtfile.read()
			txtJson = json.dumps({'Nom':name, 'extension':extension, 'Donnees':texte})
		with open(os.path.join(app.config['UPLOAD_FOLDER'],name +'.json'),"w") as file: 
				json.dump(txtJson,file)
		return "ok \n "
	else :
		return "Ce format d'image n'est pas autorisé. Veuillez utiliser les formats suivants: png, jpg, jpeg, gif \n "