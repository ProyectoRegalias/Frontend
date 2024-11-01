import google.generativeai as genai
from flask_sqlalchemy import SQLAlchemy

API_KEY = "AIzaSyCmSKtv1MqSwO9yTwCpqga-6Xse1Y4DOOw"
generation_config = {
    "temperature": 0.2,
    "top_p": 0.97,
    "top_k": 10,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
chat_ = model.start_chat(history=[])
db = SQLAlchemy()
