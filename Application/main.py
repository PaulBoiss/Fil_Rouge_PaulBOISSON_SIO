import os
from app import app, url, exampleFolder, bucket
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
import PIL.Image
#import PIL.ImageTk
#from tkinter import Tk, Label
import requests
import json

# Nouveaux par rapport au projet python
from PyPDF2 import PdfFileReader
import base64
import csv

# Connection avec AWS
import boto3
import logging 
from botocore.exceptions import ClientError

# Vérification du mimetype
import mimetypes


# Fonction de sécurisation des images et gestion des extensions autorisées
ALLOWED_EXTENSIONS = set(['txt','pdf','csv','png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Liste des fichiers chargés (ligne de commande)
@app.route('/list', methods=['GET'])
def listFile():
	listeFichiers= ''
	session = boto3.Session(profile_name='csloginstudent')
	s3 = session.client("s3")
	liste = s3.list_objects(Bucket = bucket)
	try:
		for a in liste.get('Contents'):
			listeFichiers += a.get('Key') + '\n'
	except:
		return 'Une erreur est survenue \n'
	return(listeFichiers)

@app.route('/mimetype', methods=['POST'])
def mimetypeFile():
	file = request.files["file"]
	return mimetypes.guess_type(file.filename) 

# Route de sélection d'une image (ligne de commande)
@app.route('/load',methods=['POST'])
def loadFile():
	try:
		if 'file' not in request.files:
			return "Aucun fichier lié \n"
		file = request.files["file"]
		if file.filename == '':
			return "Aucun fichier indiqué \n"
		if file and allowed_file(file.filename):
			extension = file.filename.split('.')[-1]
			name = file.filename.split('.')[0]
			liste = listFile()
		#Vérifier si le fichier est déjà chargé dans S3
		if name+".json" in liste:
			return "Un fichier contient le même nom \n"
		if mimetypes.guess_type(file.filename)[0].split("/")[-1] != extension and not (mimetypes.guess_type(file.filename)[0].split("/")[-1] == 'plain' and extension =='txt') and not (mimetypes.guess_type(file.filename)[0].split("/")[-1] == 'vnd.ms-excel' and extension =='csv'):
			return "L'extension de ce fichier ne correspond pas à son contenu. Veuillez essayer un autre fichier. \n "
	except:
		return "Ce fichier ne semble pas être supporté par l'application \n"

	#Fichiers PDF
	if extension == 'pdf':
		try:
			document = PdfFileReader(open(os.path.join(exampleFolder, file.filename),'rb'))
			pdftext = ""
			for page in range(document.numPages):
				pageObj = document.getPage(page)
				pdftext += pageObj.extractText().replace('\n','')
			fichierJson = json.dumps({'Nom':name,'Metadonnees':document.getDocumentInfo(),'Donnees':pdftext})
			with open(os.path.join(app.config['UPLOAD_FOLDER'],name +'.json'),"w") as file: 
				json.dump(fichierJson,file)
		except: 
			return 'Une erreur est survenue \n'
		sendFile(name+'.json')
		return 'Fichier correctement envoyé \n '

	#Images
	elif extension in {'png','jpg','jpeg','gif'}:
		try:
			with open(os.path.join(exampleFolder, file.filename),'rb') as img_file:
				imageB64 = base64.b64encode(img_file.read())
			imageJson = json.dumps({'Nom':name, 'extension':extension,'Donnees':imageB64.decode("utf-8")})
			with open(os.path.join(app.config['UPLOAD_FOLDER'],name +'.json'),"w") as file: 
				json.dump(imageJson,file)
		except: 
			return 'Une erreur est survenue \n'
		sendFile(name+'.json')
		return "Fichier correctement envoyé \n "

	# Fichiers CSV
	elif extension == "csv":
		liste = ""
		try:
			with open(os.path.join(exampleFolder, file.filename),"r") as csvfile:
				csvReader = csv.reader(csvfile, delimiter=';',quotechar='|')
				for row in csvReader:
					liste += ", "+ str(row)
			CSVJson = json.dumps({'Nom':name, 'extension':extension,'Donnees':liste})
			with open(os.path.join(app.config['UPLOAD_FOLDER'],name +'.json'),"w") as file: 
				json.dump(CSVJson,file)
		except: 
			return 'Une erreur est survenue \n'
		sendFile(name+'.json')
		return "Fichier correctement envoyé \n"

	# Fichiers txt
	elif extension == "txt":
		try:
			with open(os.path.join(exampleFolder, file.filename),"r") as txtfile:
				texte = txtfile.read()
				txtJson = json.dumps({'Nom':name, 'extension':extension, 'Donnees':texte})
			with open(os.path.join(app.config['UPLOAD_FOLDER'],name +'.json'),"w") as file: 
				json.dump(txtJson,file)
		except:
			return 'Une erreur est survenue \n'
		sendFile(name+'.json')
		return "Fichier correctement envoyé \n "
	
	# Extension non reconnue
	else :
		return "Ce format d'image n'est pas autorisé. Veuillez utiliser les formats suivants: png, jpg, jpeg, gif \n "

@app.route('/testSend/<nomFichier>', methods=['GET'])
def sendFile(nomFichier):
	object_name = nomFichier
	file_name = app.config['UPLOAD_FOLDER'] + nomFichier
	session = boto3.Session(profile_name='csloginstudent')
	s3 = session.client("s3")
	try:
		response = s3.upload_file(file_name, bucket, object_name)
	except ClientError as e:
		logging.error(e)
		return 'False'
	try:
		os.remove(app.config['UPLOAD_FOLDER']+nomFichier)
	except:
		return "Le fichier n'a pas pu être supprimé"
	return "Fichier correctement envoyé et supprimé de l'appli"


@app.route('/download/<picture>', methods=['GET'])
def downloadFile(picture):
	object_name = picture
	file_name = app.config['UPLOAD_FOLDER'] + picture
	liste = listFile()
	session = boto3.Session(profile_name='csloginstudent')
	s3 = session.client("s3")
	if picture not in liste:
		return "Il n'y aucun fichier de ce nom \n"
	try:
		s3.download_file(bucket, object_name, file_name)
		uploads = os.path.join(app.config['UPLOAD_FOLDER'], picture)
		send_file(uploads, as_attachment=True)
		os.remove(app.config['UPLOAD_FOLDER']+picture)
	except: 
		return "Un problème est survenu \n"
	return "Fichier JSON correctement chargé dans le dossier actuel"




@app.route('/delete/<picture>',methods=['GET'])
def deleteFile(picture):
	session = boto3.Session(profile_name='csloginstudent')
	s3 = session.client("s3")
	try:
		s3.delete_object(Bucket = bucket, Key = picture)
	except ClientError as e:
		logging.error(e)
		return "Il y a eu une erreur \n"
	return 'Fichier parfaitement supprimé \n'


# Lancement de l'application à l'execution du script
if __name__ == "__main__":
    app.run(debug=True)


# Erreur CSV PDF Text