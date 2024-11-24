import os
import openpyxl
from flask import Blueprint, session, redirect, render_template, request, url_for
from app.models import guardar_datos_usuario
from app.utils.utils import chat_

arbol_objetivo = Blueprint('arbol_objetivo', __name__)


@arbol_objetivo.route('/arbolobjetivos')
def arbolobjetivos():
    return render_template('arbol_objetivos.html')


@arbol_objetivo.route('/arbolobjetivo', methods=['POST', 'GET'])
def arbolo_bjetivo():
    if request.method == 'POST':
        json = request.get_json()
        session['fines_directos'] = (json.get("fines_directas")).split(',')
        session['fines_indirectos'] = (json.get("fines_indirectas")).split(',')
        session['objetivos_especificos'] = (json.get("objetivos_especificos")).split(',')
        session['medios'] = (json.get("medios")).split(',')
        return 'ENTRO', 204  # Respuesta sin contenido

    if request.method == 'GET':
        fines_directos = session.get('fines_directos', [])
        fines_indirectos = session.get('fines_indirectos', [])
        objetivos_especificos = session.get('objetivos_especificos', [])
        medios = session.get('medios', [])

    return render_template('arbol_objetivos.html', problema="problema", fines_directos=fines_directos,
                           fines_indirectos=fines_indirectos, objetivos_especificos=objetivos_especificos,
                           medios=medios)
