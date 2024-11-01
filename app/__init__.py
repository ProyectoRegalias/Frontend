from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.router.Usuario import usuario
from app.router.chat import chat, chat_ia
from app.routes import main_blueprint
import key
import google.generativeai as genai

# Configurar la API de GenAI
genai.configure(api_key=key.clave)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql://uo8anz1qxxd08ucp:638cBXuoPtaleuf6Gp96@localhost:5000'
                                             '/bsq8dwiuljmfpdmfeygi')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    SQLAlchemy(app)
    app.secret_key = 'mondongo'

    # Registro de los blueprints
    #app.register_blueprint(main_blueprint)
    app.register_blueprint(usuario)
    app.register_blueprint(chat_ia)

    return app
