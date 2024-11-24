import os
import openpyxl
from flask import Blueprint, session, redirect, render_template, request, url_for
from app.models import guardar_datos_usuario
from app.utils.utils import chat_

arbol_problema = Blueprint('arbol_problema', __name__)


@arbol_problema.route('/arbolproblema', methods=['POST'])
def arbol_problem():
    problema = request.form.get('pregunta', '')  # Obtiene el problema
    json = request.get_json()
    causas_directas = (json.get("causas_directas")).split(',')
    causas_indirectas = (json.get("causas_indirectas")).split(',')
    efectos_directos = (json.get("efectos_directos")).split(',')
    efectos_indirectos = (json.get("efectos_indirectos")).split(',')

    # Renderiza la página del árbol de problemas con los datos
    return render_template('arbol_problema.html', problema="problema", causas_directas=causas_directas,
                           causas_indirectas= causas_indirectas, efectos_directos=efectos_directos,
                           efectos_indirectos=efectos_indirectos,)
