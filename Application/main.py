import os
from app import app, url, exampleFolder
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import PIL.Image
import PIL.ImageTk
from tkinter import Tk, Label
import requests
import json

# Nouveaux par rapport au projet python
from PyPDF2 import PdfFileReader
import base64

# Fonction de sécurisation des images et gestion des extensions autorisées
ALLOWED_EXTENSIONS = set(['txt','pdf','csv','png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Liste des fichiers chargés (ligne de commande)
@app.route('/list', methods=['GET'])
def listImages():
	liste = ''
	files = os.listdir(app.config['UPLOAD_FOLDER']) 
	for file in files:
		liste = liste + '     '+ file
	return(liste)


# Route de sélection d'une image (ligne de commande)
@app.route('/load/<picture>',methods=['GET'])
def load_image(picture):
	extension = picture.split('.')[-1]
	name = picture.split('.')[0]
	if not os.path.exists(exampleFolder + picture):
	    return "Ce fichier n'est pas présent dans le dossier Fichiers_Test"
	elif os.path.exists(app.config['UPLOAD_FOLDER'] + picture):
		return 'Fichier déjà chargé'
	elif picture == '':
		return 'Aucun fichier sélectionné'
	elif extension == 'pdf':
		document = PdfFileReader(open(os.path.join(exampleFolder, picture),'rb'))
		pdftext = ""
		for page in range(document.numPages):
			pageObj = document.getPage(page)
			pdftext += pageObj.extractText().replace('\n','')
		fichierJson = json.dumps({'Nom':name,'Metadonnees':document.getDocumentInfo(),'Donnees':pdftext})
		with open(os.path.join(app.config['UPLOAD_FOLDER'],name +'.json'),"w") as file: 
			json.dump(fichierJson,file)
		return 'ok'
	elif extension in {'png','jpg','jpeg','gif'}:
		with open(os.path.join(exampleFolder, picture),'rb') as img_file:
			imageB64 = base64.b64encode(img_file.read())
		imageJson = json.dumps({'Nom':name,'Donnees':imageB64.decode("utf-8")})
		with open(os.path.join(app.config['UPLOAD_FOLDER'],name +'.json'),"w") as file: 
				json.dump(imageJson,file)
		return "ok"
	else :
		return "Ce format d'image n'est pas autorisé. Veuillez utiliser les formats suivants: png, jpg, jpeg, gif"

# Lancement de l'application à l'execution du script
if __name__ == "__main__":
    app.run(debug=True)