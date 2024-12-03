import os
import openpyxl
from flask import Blueprint, session, redirect, render_template, request, url_for
from app.utils.utils import chat_
import pandas as pd

def limpiar_texto(texto):
    return texto.strip().replace('\n', '').replace('**', '').replace('*', '').capitalize()


chat_ia = Blueprint('chat_ia', __name__)

@chat_ia.route('/', methods=['GET', 'POST'])
@chat_ia.route('/chat', methods=['GET', 'POST'])
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('main.login'))

    session.setdefault('causas_indirectas', [])
    session.setdefault('efectos_directos', [])
    session.setdefault('causas_directas', [])
    session.setdefault('efectos_indirectos', [])
    session.setdefault('fines_directos', [])
    session.setdefault('fines_indirectos', [])
    session.setdefault('objetivos_especificos', [])
    session.setdefault('medios', [])

    pregunta = ""
    # Inicializar variables de sesión si no existen
    if 'iteraciones' not in session:
        session['iteraciones'] = 0
    if 'respuesta_valida' not in session:
        session['respuesta_valida'] = False
    if 'pregunta' not in session:
        session['pregunta'] = ""

    respuesta = ""
    arbol = ""
    max_iteraciones = 2  # Límite máximo de intentos

    if request.method == 'POST':
        
        pregunta = request.form['pregunta']

        # Si el usuario cambió la pregunta, reinicia el contador
        if session['pregunta'] != pregunta:
            session['pregunta'] = pregunta
            session['iteraciones'] = 0
            session['respuesta_valida'] = False

        if not session['respuesta_valida']:
            # Llamar a la IA para evaluar el problema
            response_definition_probem = chat_.send_message(
                f"Evalúa la formulación del siguiente problema según la "
                f"metodología MGA: '{pregunta}'. Verifica si el problema "
                f"está claramente definido, enfocado en una necesidad específica y "
                f"evita sugerir soluciones previas. Considera si el problema es "
                f"relevante y factible de resolver. Responde 'bien_formulado' si "
                f"cumple con estos criterios, o devuelve 'mal_formulado' si no cumple "
                f"con los criterios. Un problema bien formulado tiene las siguientes características:     "
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
                f"Sin orientación: El problema no sugiere posibles soluciones."
            ).text

            if response_definition_probem == 'bien_formulado':
                session['respuesta_valida'] = True
                respuesta = "El problema esta bien Formulado"
                #arbol = generarArbolProblemas(pregunta)
                preguntaValida = pregunta
                generarRespuestasProblemas(chat_, preguntaValida, session)

            else:
                session['iteraciones'] += 1
                if session['iteraciones'] < max_iteraciones:
                    options_problem = chat_.send_message(
                        "El problema ingresado no está bien formulado. Aquí tienes algunas opciones "
                        "para reestructurarlo o hacerlo más claro:"
                    )
                    respuesta = options_problem.text
                else:
                    session['respuesta_valida'] = True
                    respuesta = f"Problema aceptado después de {session['iteraciones']} intentos, el problema con el que se trabajara será: {pregunta}"   
                    preguntaValida2 = pregunta
                    generarRespuestasProblemas(chat_, preguntaValida2, session)                 
                    #arbol = generarArbolProblemas(pregunta)

        # Si el problema ya fue validado, generar el árbol de objetivos
        else:
            respuesta = "El problema ya había sido validado anteriormente"
            #arbol = generarArbolProblemas(pregunta)

    print("efectos", session['efectos_directos'][-1])

    return render_template(
    'form.html',
    salida=respuesta,
    problema_valido=pregunta,
    causas_directas=session['causas_directas'][-1] if session['causas_directas'] else '',
    causas_indirectas=session['causas_indirectas'][-1] if session['causas_indirectas'] else '',
    efectos_directos=session['efectos_directos'][-1] if session['efectos_directos'] else '',
    efectos_indirectos=session['efectos_indirectos'][-1] if session['efectos_indirectos'] else '',
    fines_directos=session['fines_directos'][-1] if session['fines_directos'] else '',
    fines_indirectos=session['fines_indirectos'][-1] if session['fines_indirectos'] else '',
    objetivos_especificos=session['objetivos_especificos'][-1] if session['objetivos_especificos'] else '',
    medios=session['medios'][-1] if session['medios'] else ''
)

def generarRespuestasProblemas(chat_, preguntaValida, session):
    session['causas_indirectas'].append(limpiar_texto(chat_.send_message(
    f"Analiza el siguiente problema bien formulado: '{preguntaValida}' "
    f"y genera una causa indirecta relacionada. Una causa indirecta es un "
    f"factor subyacente que contribuye al problema pero que no es inmediatamente "
    f"visible o evidente. Por favor, responde con una sola causa indirecta clara y concisa, "
    f"asegurándote de evitar términos sensibles o controvertidos.").text))
    #print("Causa indirecta generada:", session['causas_indirectas'][-1])

    session['efectos_directos'].append(limpiar_texto(chat_.send_message(
    f"Analiza el siguiente problema bien formulado: '{preguntaValida}' "
    f"y genera un efecto directo relacionado. Un efecto directo es una consecuencia "
    f"observable y claramente vinculada al problema, visible de manera inmediata. "
    f"Por favor, responde con un solo efecto directo claro y conciso, "
    f"asegurándote de evitar términos sensibles o controvertidos.").text))
    #print("Efecto directo generado:", session['efectos_directos'][-1])

    session['causas_directas'].append(limpiar_texto(chat_.send_message(
    f"Analiza el siguiente problema bien formulado: '{preguntaValida}' "
    f"y genera una causa directa relacionada. Una causa directa es un factor evidente "
    f"que contribuye directamente al problema, siendo fácilmente identificable. "
    f"Por favor, responde con una sola causa directa clara y concisa, "
    f"asegurándote de evitar términos sensibles o controvertidos.").text))
    #print("Causa directa generada:", session['causas_directas'][-1])

    session['efectos_indirectos'].append(limpiar_texto(chat_.send_message(
    f"Analiza el siguiente problema bien formulado: '{preguntaValida}' "
    f"y genera un efecto indirecto relacionado. Un efecto indirecto es una consecuencia "
    f"subyacente o secundaria derivada del problema, que no es inmediatamente observable. "
    f"Por favor, responde con un solo efecto indirecto claro y conciso, "
    f"asegurándote de evitar términos sensibles o controvertidos.").text))
    #print("efectos indirectos generada:", session['efectos_indirectos'][-1])

    session['medios'].append(limpiar_texto(chat_.send_message(
    f"Analiza el siguiente problema bien formulado: '{preguntaValida}' "
    f"y sugiere un medio para abordar el problema. Un medio es un recurso, estrategia "
    f"o acción concreta que podría ayudar a resolver o mitigar el problema. "
    f"Por favor, responde con un solo medio claro y conciso, "
    f"asegurándote de evitar términos sensibles o controvertidos.").text))
    #print("medios generados:", session['medios'][-1])

    # Fines Directos
    session['fines_directos'].append(limpiar_texto(chat_.send_message(
    f"Analiza el siguiente problema bien formulado: '{preguntaValida}' "
    f"y sugiere un fin directo relacionado con el problema. Un fin directo es un objetivo inmediato "
    f"o resultado positivo que se espera alcanzar al abordar el problema. "
    f"Por favor, responde con un solo fin claro y conciso, "
    f"asegurándote de evitar términos sensibles o controvertidos.").text))

# Fines Indirectos
    session['fines_indirectos'].append(limpiar_texto(chat_.send_message(
    f"Analiza el siguiente problema bien formulado: '{preguntaValida}' "
    f"y sugiere un fin indirecto relacionado con el problema. Un fin indirecto es un resultado secundario "
    f"o beneficio adicional que se podría lograr al abordar el problema. "
    f"Por favor, responde con un solo fin claro y conciso, "
    f"asegurándote de evitar términos sensibles o controvertidos.").text))

# Objetivos Específicos
    session['objetivos_especificos'].append(limpiar_texto(chat_.send_message(
    f"Analiza el siguiente problema bien formulado: '{preguntaValida}' "
    f"y sugiere un objetivo específico relacionado con el problema. Un objetivo específico es una meta clara "
    f"y medible que contribuye a resolver el problema de manera directa. "
    f"Por favor, responde con un solo objetivo claro y conciso, "
    f"asegurándote de evitar términos sensibles o controvertidos.").text))



def generarArbolProblemas(message_problem):
    file_path = os.path.join(os.path.dirname(__file__), 'arbol_problemas.xlsx')
    
    # Verifica si el archivo existe
    if not os.path.exists(file_path):
        # Crea un DataFrame vacío y guarda un nuevo archivo .xlsx
        df = pd.DataFrame(columns=['Problema', 'Descripción', 'Categoría'])
        df.to_excel(file_path, index=False)
        print(f"Archivo creado en: {file_path}")
    
    # Aquí puedes continuar con el resto de la lógica para procesar el archivo
    print(f"El archivo '{file_path}' está listo para usarse.")
    
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

    return list_fines_directs, list_fines_indirects, list_specific_objetives,list_means_objetives

