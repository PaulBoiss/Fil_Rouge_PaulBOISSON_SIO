import os
import requests
from requests.auth import HTTPBasicAuth
from main import listFile

url = 'https://filrouge.pbo.p2021.ajoga.fr/'
utilisateur = 'user'
mdp = 'user'

# Envoi d'un bon fichier
def test_upload_image():
    print("------Test d'importation d'une image FichierTest.png'------")
    files = {'file':open('../../Fichiers_Test/FichierTest.png','rb')}
    r = requests.post('https://filrouge.pbo.p2021.ajoga.fr/load', files = files, auth=HTTPBasicAuth(utilisateur, mdp))
    rep = str(r.content)
    print("Aboutissement de la requête (200 si ok):", r.status_code)
    liste = listFile()
    print("Le fichier a-t-il bien été chargé ? (True si ok): ", "FichierTest.json" in liste)
    print("Avons-nous récupéré les métadonnées ? (True si ok)", "FichierTest" in rep)
    assert r.status_code == 200 and "FichierTest.json" in liste and "FichierTest" in rep

# Suppression d'un fichier
def test_removeFile():
    print("------Test de suppression d'un fichier Sujet_Projet.pdf------")
    r = requests.get('https://filrouge.pbo.p2021.ajoga.fr/delete/FichierTest.json', auth=HTTPBasicAuth(utilisateur, mdp))
    print("Aboutissement de la requête (200 si ok):", r.status_code)
    liste = listFile()
    print('Le fichier est-il toujours dans le dossier ? (False si ok) :', "FichierTest.json" in liste)
    assert r.status_code == 200 and ("FichierTest.json" in liste) == False
