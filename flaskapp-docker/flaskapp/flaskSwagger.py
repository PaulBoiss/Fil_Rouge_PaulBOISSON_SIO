from flask import send_from_directory
from app import app

from flask_swagger_ui import get_swaggerui_blueprint
@app.route('/static/<path:path>')
def send_static(path):
        return send_from_directory('static',path)
### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Paul-BOISSON-Fil-Rouge"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
