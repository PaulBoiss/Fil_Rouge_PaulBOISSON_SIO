import os
from app import app
import boto3
import logging 
from botocore.exceptions import ClientError

bucket = "paulb-fil-rouge-bucket-sio"

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