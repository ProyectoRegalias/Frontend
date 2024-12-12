import os
import openpyxl
from flask import Blueprint, session, redirect, render_template, request, url_for
from app.utils.utils import chat_

arbol_problema = Blueprint('arbol_problema', __name__)


@arbol_problema.route('/arbolproblema', methods=['POST'])
def arbol_problem():
    if request.method == 'POST':
        json = request.get_json()
        print("json", json)
        problema = request.form.get('pregunta', '')  # Obtiene el problema
        session['causas_directas'] = (json.get("causas_directas")).split(',')
        session['causas_indirectas'] = (json.get("causas_indirectas")).split(',')
        session['efectos_directos'] = (json.get("efectos_directos")).split(',')
        session['efectos_indirectos'] = (json.get("efectos_indirectos")).split(',')

    if request.method == 'GET':
        problema = session.get('problema', [])
        causas_directas = session.get('causas_directas', [])
        causas_indirectas = session.get('causas_indirectas', [])
        efectos_directos = session.get('efectos_directos', [])
        efectos_indirectos = session.get('efectos_indirectos', [])

    # Renderiza la página del árbol de problemas con los datos
    return render_template('arbol_problema.html', problema="problema", causas_directas=causas_directas,
                           causas_indirectas= causas_indirectas, efectos_directos=efectos_directos,
                           efectos_indirectos=efectos_indirectos,)
