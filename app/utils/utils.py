import random
import google.generativeai as genai
from flask_sqlalchemy import SQLAlchemy

# Lista de API keys
API_KEYS = [
    "AIzaSyASObwuMYYpfzrSgHyCpOZ7RVldZykzDfo",
    "AIzaSyCmSKtv1MqSwO9yTwCpqga-6Xse1Y4DOOw",
]

# Ruleta para seleccionar la API key
def get_api_key():
    return random.choice(API_KEYS)

# Configuración inicial con una API key seleccionada aleatoriamente
def configure_model():
    api_key = get_api_key()
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.2,
        "top_p": 0.97,
        "top_k": 10,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
    chat_ = model.start_chat(history=[])
    return chat_, model

# Ejemplo de configuración
chat_, model = configure_model()
db = SQLAlchemy()