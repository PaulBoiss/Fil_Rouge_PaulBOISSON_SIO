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
import csv

# Fonction de sécurisation des images et gestion des extensions autorisées
ALLOWED_EXTENSIONS = set(['txt','pdf','csv','png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Liste des fichiers chargés (ligne de commande)
@app.route('/list', methods=['GET'])
def listFile():
	liste = ''
	files = os.listdir(app.config['UPLOAD_FOLDER']) 
	for file in files:
		liste = liste + '     '+ file
	liste += ' \n '
	return(liste)


# Route de sélection d'une image (ligne de commande)
@app.route('/load/<picture>',methods=['GET'])
def loadFile(picture):
	extension = picture.split('.')[-1]
	name = picture.split('.')[0]
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

@app.route('/read/<picture>',methods=['GET'])
def readFile(picture):
	try:
		jsonFile = open(app.config['UPLOAD_FOLDER']+picture)
		data = json.load(jsonFile)
	except:
		return "Le fichier n'existe pas \n"
	else:
		return data +'\n'

@app.route('/delete/<picture>',methods=['GET'])
def deleteFile(picture):
	try:
		os.remove(app.config['UPLOAD_FOLDER']+picture)
	except:
		return "Le fichier n'existe pas \n "
	else:
		return "Fichier parfaitement supprimé \n"


# Lancement de l'application à l'execution du script
if __name__ == "__main__":
    app.run(debug=True)