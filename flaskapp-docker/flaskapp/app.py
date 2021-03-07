from flask import Flask
#from redis import Redis

# ---------Paramètres d'application----------
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# redis = Redis(host='redis', port=6379)

# --------- Paramètres modifiables ---------
url = "http://localhost:5000/"
exampleFolder = '../../Fichiers_Test/'

# --------- Paramètres AWS ---------
bucket = "paulb-fil-rouge-bucket-sio"

