import os
import openpyxl
from flask import Blueprint, session, redirect, render_template, request, url_for
from app.utils.utils import chat_

arbol_objetivo = Blueprint('arbol_objetivo', __name__)


@arbol_objetivo.route('/arbolobjetivos', methods=['GET'])
def arbolobjetivos():
    fines_directos = session.get('fines_directos', [])
    fines_indirectos = session.get('fines_indirectos', [])
    objetivos_especificos = session.get('objetivos_especificos', [])
    medios = session.get('medios', [])

    return render_template('arbol_objetivos.html', problema="problema", fines_directos=fines_directos,
                           fines_indirectos=fines_indirectos, objetivos_especificos=objetivos_especificos,
                           medios=medios)


@arbol_objetivo.route('/arbolobjetivo', methods=['POST', 'GET'])
def arbolo_bjetivo():
    if request.method == 'POST':
        json = request.get_json()
        session['fines_directos'] = (json.get("fines_directas")).split(',')
        session['fines_indirectos'] = (json.get("fines_indirectas")).split(',')
        session['objetivos_especificos'] = (json.get("objetivos_especificos")).split(',')
        session['medios'] = (json.get("medios")).split(',')

        session['causas_directas'] = (json.get("causas_directas")).split(',')
        session['causas_indirectas'] = (json.get("causas_indirectas")).split(',')
        session['efectos_directos'] = (json.get("efectos_directos")).split(',')
        session['efectos_indirectos'] = (json.get("efectos_indirectos")).split(',')
        return 'ENTRO', 204

    if request.method == 'GET':
        fines_directos = session.get('fines_directos', [])
        fines_indirectos = session.get('fines_indirectos', [])
        objetivos_especificos = session.get('objetivos_especificos', [])
        medios = session.get('medios', [])

        causas_directas = session.get('causas_directas', [])
        causas_indirectas = session.get('causas_indirectas', [])
        efectos_directos = session.get('efectos_directos', [])
        efectos_indirectos = session.get('efectos_indirectos', [])

    return render_template('arbol_objetivos.html', problema="problema", fines_directos=fines_directos,
                           fines_indirectos=fines_indirectos, objetivos_especificos=objetivos_especificos,
                           medios=medios, causas_directas=causas_directas,
                           causas_indirectas= causas_indirectas, efectos_directos=efectos_directos,
                           efectos_indirectos=efectos_indirectos)
