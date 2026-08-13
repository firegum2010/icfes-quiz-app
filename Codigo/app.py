#trae los modulos
import streamlit as st
import json
import datetime
import os
 
#busca el archivo json en la misma carpeta que el script
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_json = os.path.join(carpeta_actual, 'preguntas_matematicas.json')
ruta_resultados = os.path.join(carpeta_actual, 'resultados.json')
 
#carga las preguntas (una sola vez, streamlit vuelve a correr esto en cada recarga pero es rapido)
with open(ruta_json, encoding='utf-8') as f:
    data = json.load(f)
 
# ============================================================
# SESSION STATE
# ============================================================
# Streamlit vuelve a correr TODO el script de arriba a abajo cada
# vez que el usuario hace clic en algo. Para que "name", "correctas"
# y en que pregunta vamos no se reinicien solos, los guardamos aca.
 
if "name" not in st.session_state:
    st.session_state.name = ""
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "pregunta_index" not in st.session_state:
    st.session_state.pregunta_index = 0  # equivalente a en cual vuelta del "for pregunta in data" vamos
if "correctas" not in st.session_state:
    st.session_state.correctas = 0
if "respondio" not in st.session_state:
    st.session_state.respondio = False
if "fue_correcta" not in st.session_state:
    st.session_state.fue_correcta = None
if "examen_termino" not in st.session_state:
    st.session_state.examen_termino = False
 
 
#crea la variable de la fecha (se calcula al momento de terminar el examen, no al abrir la app)
def obtener_fecha():
    now = datetime.datetime.now()
    return now.strftime("%d/%m/%Y %H:%M")
 
 
#guardar el resultado en un archivo json (misma logica que tu try/except original)
def guardar_resultado(name, subject, correctas, total):
    resultado = {
        "nombre": name,
        "materia": subject,
        "correctas": correctas,
        "total": total,
        "fecha": obtener_fecha()
    }
    try:
        #intenta abrir el archivo json de resultados
        with open(ruta_resultados, 'r', encoding='utf-8') as f:
            resultados = json.load(f)
    except FileNotFoundError:
        #si no existe el archivo json de resultados lo crea
        resultados = []
    resultados.append(resultado)
    with open(ruta_resultados, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
 
 
# ============================================================
# INTERFAZ (esto reemplaza los print() e input() de main.py)
# ============================================================
 
st.title("Tutor Virtual ICFES")
 
#preguntar el nombre (equivalente a: name = input("Como te llamas?: "))
if st.session_state.name == "":
    nombre_temp = st.text_input("Como te llamas?")
    if st.button("Continuar"):
        if nombre_temp.strip() != "":
            st.session_state.name = nombre_temp
            st.rerun()
        else:
            st.warning("Escribe tu nombre para continuar.")
 
#seleccionar la materia (equivalente a: subject = input("Seleciona la materia...").upper())
elif st.session_state.subject == "":
    st.write(f"Hola, {st.session_state.name}!")
    st.write("Bienvenido al examen de matematicas, por favor responde las preguntas seleccionando la opcion correcta.")
    subject_temp = st.text_input("Seleciona la materia (solo matematicas disponible):").upper()
    if st.button("Seleccionar materia"):
        st.session_state.subject = subject_temp
        st.rerun()
 
#si la materia no es matematicas (equivalente a tu "else: Materia no disponible")
elif st.session_state.subject != "MATEMATICAS":
    st.error("Materia no disponible, por favor selecciona matematicas.")
    if st.button("Volver a intentar"):
        st.session_state.subject = ""
        st.rerun()
 
#el examen en si (equivalente a: for pregunta in data:)
elif not st.session_state.examen_termino:
    pregunta = data[st.session_state.pregunta_index]
 
    st.write(f"Pregunta {st.session_state.pregunta_index + 1} de {len(data)}")
    st.subheader(f"{pregunta['id']}. {pregunta['tema']}")
    st.write(pregunta['pregunta'])
 
    #for letra, opcion in pregunta['opciones'].items(): print(f"{letra}: {opcion}")
    opciones_texto = [f"{letra}: {opcion}" for letra, opcion in pregunta['opciones'].items()]
    seleccion = st.radio("Selecciona la respuesta correcta:", opciones_texto, key=f"radio_{st.session_state.pregunta_index}")
 
    #answer = input("Selecciona la respuesta correcta: ").upper()
    if not st.session_state.respondio:
        if st.button("Responder"):
            answer = seleccion.split(":")[0]  # saca la letra A, B, C o D
            st.session_state.respondio = True
 
            #if answer == pregunta['respuesta_correcta']:
            if answer == pregunta['respuesta_correcta']:
                st.session_state.correctas += 1
                st.session_state.fue_correcta = True
            else:
                st.session_state.fue_correcta = False
            st.rerun()
    else:
        #print("Respuesta correcta!") / print("Respuesta incorrecta!")
        if st.session_state.fue_correcta:
            st.success("Respuesta correcta!")
        else:
            st.error("Respuesta incorrecta!")
            st.write(f"La respuesta correcta es: {pregunta['respuesta_correcta']}")
            st.write(f"Explicacion: {pregunta['explicacion']}")
 
        if st.button("Siguiente pregunta"):
            st.session_state.pregunta_index += 1
            st.session_state.respondio = False
            st.session_state.fue_correcta = None
 
            #cuando llegue a la ultima pregunta se le dira al usuario sus respuestas correctas
            if st.session_state.pregunta_index >= len(data):
                st.session_state.examen_termino = True
                guardar_resultado(st.session_state.name, st.session_state.subject, st.session_state.correctas, len(data))
            st.rerun()
 
#Felicidades acabaste el examen
else:
    st.success(f"Felicidades acabaste el examen de {st.session_state.subject}")
    st.write(f"Respondiste correctamente {st.session_state.correctas} preguntas de {len(data)}")
 
    if st.button("Intentar de nuevo"):
        st.session_state.name = ""
        st.session_state.subject = ""
        st.session_state.pregunta_index = 0
        st.session_state.correctas = 0
        st.session_state.respondio = False
        st.session_state.fue_correcta = None
        st.session_state.examen_termino = False
        st.rerun()