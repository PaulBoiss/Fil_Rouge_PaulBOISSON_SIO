from flask import Flask


# ---------Paramètres d'application----------
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 




# --------- Paramètres modifiables ---------
url = "http://localhost:5000/"
exampleFolder = '../Fichiers_Test/'