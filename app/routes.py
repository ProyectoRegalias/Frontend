from flask import Blueprint, request, render_template, redirect, url_for, session
from app.models import cargar_usuarios, guardar_usuario, cargar_historial_usuario, guardar_datos_usuario
from app.utils import model

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuarios = cargar_usuarios()
        
        if username in usuarios:
            error = 'El nombre de usuario ya existe.'
        else:
            guardar_usuario(username, password)
            success = 'Usuario registrado con éxito. ¡Ahora puedes iniciar sesión!'
            return redirect(url_for('main.login'))
    
    return render_template('register.html', error=error, success=success)

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuarios = cargar_usuarios()
        
        if username in usuarios and usuarios[username] == password:
            session['logged_in'] = True
            session['username'] = username
            session['user_data'] = cargar_historial_usuario(username)
            return redirect(url_for('main.chat'))
        else:
            error = 'Usuario o contraseña incorrectos.'
    
    return render_template('login.html', error=error)

@main_blueprint.route('/', methods=['GET', 'POST'])
@main_blueprint.route('/chat', methods=['GET', 'POST'])
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('main.login'))
    
    respuesta = ""
    if request.method == 'POST':
        pregunta = request.form['pregunta']
        historial = session.get('user_data', [])
        historial_texto = " ".join([f"Pregunta: {h['Pregunta']} Respuesta: {h['Respuesta']}" for h in historial])
        contexto = historial_texto + " " + pregunta
        respuesta = model.generate_content(contexto).text
        
        historial.append({'Pregunta': pregunta, 'Respuesta': respuesta})
        session['user_data'] = historial
        guardar_datos_usuario(session['username'], pregunta, respuesta)
    
    return render_template('form.html', salida=respuesta)

@main_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))
