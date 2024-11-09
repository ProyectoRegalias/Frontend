import os
import openpyxl
from flask import Blueprint, session, redirect, render_template, request, url_for
#from app.models import guardar_datos_usuario
from app.utils.utils import chat_

chat_ia = Blueprint('chat_ia', __name__)


@chat_ia.route('/', methods=['GET', 'POST'])
@chat_ia.route('/chat', methods=['GET', 'POST'])
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('main.login'))

    respuesta = ""
    if request.method == 'POST':
        pregunta = request.form['pregunta']
        #historial = session.get('user_data', [])

        # Verifica que cada entrada en el historial tenga las claves requeridas
        # historial_texto = " ".join([f"Respuesta: {h.get('Respuesta', 'Respuesta no disponible')}"
        #                             for h in historial])

        # contexto = historial_texto + " " + pregunta
        response_definition_probem = chat_.send_message(f"Evalúa la formulación del siguiente problema según la "
                                                        f"metodología MGA: '{pregunta}'. Verifica si el problema "
                                                        f"está claramente definido, enfocado en una necesidad específica y "
                                                        f"evita sugerir soluciones previas. Considera si el problema es "
                                                        f"relevante y factible de resolver. Responde 'bien_formulado' si "
                                                        f"cumple con estos criterios, o devuelve 'mal_formulado' si no cumple "
                                                        f"con los criterio. Un problema bien formulado tiene las siguientes características:     "
                                                        f"Claro y conciso: El problema se establece en términos claros y fáciles de entender, evitando jerga o lenguaje ambiguo."
                                                        f"Específico: El problema está claramente definido y delimitado, evitando generalizaciones o vaguedades."
                                                        f"Medible: El problema se puede medir o cuantificar de alguna manera, lo que permite evaluar el progreso hacia una solución."
                                                        f"Alcanzable: El problema es realista y se puede resolver con los recursos disponibles."
                                                        f"Relevante: El problema es importante y vale la pena resolverlo."
                                                        f"Con base en la realidad: El problema se basa en hechos y datos, no en opiniones o suposiciones."
                                                        f"Orientado a la acción: El problema está formulado de una manera que sugiere posibles soluciones."
                                                        f"Un problema mal formulado tiene las siguientes características:"
                                                        f"Vago e impreciso: El problema no está claramente definido y es difícil de entender."
                                                        f"General: El problema es demasiado amplio y no se centra en un tema específico."
                                                        f"No medible: No hay forma de medir o cuantificar el problema, lo que dificulta la evaluación del progreso."
                                                        f"Irreal: El problema no es realista y no se puede resolver con los recursos disponibles."
                                                        f"Irrelevante: El problema no es importante o no vale la pena resolverlo."
                                                        f"Basado en opiniones: El problema se basa en opiniones o suposiciones, no en hechos."
                                                        f"Sin orientación: El problema no sugiere posibles soluciones.").text

        if response_definition_probem in 'bien_formulado':
            respuesta = generarArbolProblemas(pregunta)
            generarArbolObejtivos(pregunta)

        else:
            options_problem = chat_.send_message(
                "Como el problema que ingreso el usuario, esta mal formulado devolveras"
                "algunas opciones o tips para que reestructure el problema. Formula una "
                "opcion de problema central correcta")
            respuesta = options_problem.text
            print(respuesta)

        """historial.append({'Pregunta': pregunta, 'Respuesta': respuesta.text})
        session['user_data'] = historial
        guardar_datos_usuario(session['username'], pregunta, respuesta.text)"""

    return render_template('form.html', salida=respuesta)


def generarArbolProblemas(message_problem):
    file_path = os.path.join(os.path.dirname(__file__), 'arbol_problemas.xlsx')
    tree_problems = openpyxl.load_workbook(file_path)
    sheet = tree_problems.active
    response_causes_effects = chat_.send_message(
        f"El mensaje del usuario {message_problem} enviara una problematica,"
        f" que es un proyecto para regalias, donde primero te basaras en la "
        f"metodoloa mga que tiene causas(raices) y efectos(ramas),segun el "
        f"mensaje del usuario devolveras las causas donde tiene causas "
        f"directas e indirectas y lo mismo para los efectos que tiene causas "
        f"directas e indirectas")

    print(response_causes_effects.text)

    causes_directs = chat_.send_message([f"Según {response_causes_effects}, identifica exclusivamente en el texto "
                                         f"todas las causas directas y necesarias de la problemática. Concatena las causas "
                                         f"encontradas de la siguiente manera: causa1, causa2"])

    causes_indirects = chat_.send_message([f"Según {response_causes_effects}, identifica exclusivamente en el texto "
                                           f"todas las causas indirectas y necesarias de la problemática. Concatena las "
                                           f"causas encontradas de la siguiente manera: causa1, causa2"])

    effects_directs = chat_.send_message([f"Según {response_causes_effects}, identifica exclusivamente en el texto "
                                          f"todas los efectos directas y necesarias de la problemática. Concatena las "
                                          f"causas encontradas de la siguiente manera: efecto1, efecto2"])

    effects_indirects = chat_.send_message([f"Según {response_causes_effects}, identifica exclusivamente en el texto "
                                            f"todas los efectos indirectas y necesarias de la problemática. Concatena las "
                                            f"causas encontradas de la siguiente manera: efecto1, efecto2"])

    list_causes_directs = causes_directs.text.split(',')
    list_causes_indirects = causes_indirects.text.split(',')
    list_effects_directs = effects_directs.text.split(',')
    list_effects_indirects = effects_indirects.text.split(',')

    # max_lenght = max(len(list_effects_directs), len(list_causes_directs),
    #                  len(list_causes_indirects), len(list_effects_indirects))

    results = {
        "Efectos Indirectos": list_effects_indirects,
        "Efectos Directos": list_effects_directs,
        "Problema": ["Los territorios afectados por la violencia no han podido transformarse..."],
        "Causas Directas": list_causes_directs,
        "Causas Indirectas": list_causes_indirects
    }

    row = 2
    for category, values in results.items():
        for col, value in enumerate(values, start=3):
            if category == 'Problema':
                print("4")
            else:
                sheet.cell(row=row, column=col, value=value)
        row += 1
    tree_problems.save(file_path)

    return 'Arbol_problemas'


def generarArbolObejtivos(message_problem):
    file_path = os.path.join(os.path.dirname(__file__), 'arbol_objetivos.xlsx')
    tree_problems = openpyxl.load_workbook(file_path)
    sheet = tree_problems.active
    response_causes_objectives = chat_.send_message(
        f"""El usuario ha planteado el siguiente problema en el contexto de un proyecto de regalías: {message_problem}. 
            Dado el conocimiento previo sobre el problema y la metodología empleada, responde lo siguiente:
            Fines: Identifica los fines directos e indirectos asociados al problema planteado.
            Objetivos: 
                General:** Define un único objetivo general que abarque el problema.
                Específicos:** Detalla los objetivos específicos que contribuyen al objetivo general.
                Medios:** Describe los objetivos medios necesarios para alcanzar los objetivos específicos.""")

    fines_directs = chat_.send_message([f"Según {response_causes_objectives}, identifica exclusivamente en el texto "
                                          f"todos los fines directos y necesarias de la problemática. Concatena los fines "
                                          f"encontradas de la siguiente manera: fines1, fines2"])

    fines_indirects = chat_.send_message(
        [f"Según {response_causes_objectives}, identifica exclusivamente en el texto "
         f"todos los fines indirectos y necesarias de la problemática. Concatena los fines "
         f"encontradas de la siguiente manera: fines1, fines2"])

    general_objective = chat_.send_message(
        [f"Según {response_causes_objectives}, identifica exclusivamente en el texto "
         f"todos el objetivo general y necesarias de la problemática."])

    specific_objetives = chat_.send_message(
        [f"Según {response_causes_objectives}, identifica exclusivamente en el texto "
         f"todos los objetivos especificos y necesarias de la problemática. Concatena los objetivos especifisco "
         f"encontradas de la siguiente manera: objEspecifico1, objEspecifico2"])

    means_objetives = chat_.send_message(
        [f"Según {response_causes_objectives}, identifica exclusivamente en el texto "
         f"todos los objetivos medios y necesarias de la problemática. Concatena los objetivos medios "
         f"encontradas de la siguiente manera: objMedio1, objMedio2"])

    list_fines_directs = fines_directs.text.split(',')
    list_fines_indirects = fines_indirects.text.split(',')
    list_specific_objetives = specific_objetives.text.split(',')
    list_means_objetives = means_objetives.text.split(',')

    results = {
        "Fines Directos": list_fines_directs,
        "Fines Inirectos": list_fines_indirects,
        "Objetivo General": general_objective,
        "Objetivos Especificos": list_specific_objetives,
        "Objetivos Medios": list_means_objetives
    }

    row = 2
    for category, values in results.items():
        for col, value in enumerate(values, start=3):
            if category == 'Objetivo General':
                sheet.cell(row=row, column=col, value=value)
            else:
                sheet.cell(row=row, column=col, value=value)
        row += 1
    tree_problems.save(file_path)

    return 'Arbol_objetivos'

