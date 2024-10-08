from flask import Flask
from app.routes import main_blueprint
import key
import google.generativeai as genai

# Configurar la API de GenAI
genai.configure(api_key=key.clave)

def create_app():
    app = Flask(__name__)
    app.secret_key = 'mondongo'

    # Registro de los blueprints
    app.register_blueprint(main_blueprint)

    return app