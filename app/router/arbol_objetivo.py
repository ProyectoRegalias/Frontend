import os
import openpyxl
from flask import Blueprint, session, redirect, render_template, request, url_for
from app.models import guardar_datos_usuario
from app.utils.utils import chat_

arbol_objetivo = Blueprint('arbol_objetivo', __name__)


@arbol_objetivo.route('/arbolobjetivo', methods=['POST'])
def arbol_objective():
    json = request.get_json()
    fines_directos = (json.get("fines_directas")).split(',')
    fines_indirectos = (json.get("fines_indirectas")).split(',')
    objetivos_especificos = (json.get("objetivos_especificos")).split(',')
    medios = (json.get("medios")).split(',')
    print("HOLA")
    # Renderiza la página del árbol de problemas con los datos
    return render_template('arbol_objetivos.html', problema="problema", fines_directos=fines_directos,
                           fines_indirectos=fines_indirectos, objetivos_especificos=objetivos_especificos, medios=medios)
