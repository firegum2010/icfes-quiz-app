#trae los modulos
import streamlit as st
import json
import datetime
import os
import unicodedata

#busca el archivo json en la misma carpeta que el script
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_json = os.path.join(carpeta_actual, 'preguntas_matematicas.json')
ruta_resultados = os.path.join(carpeta_actual, 'resultados.json')

#carga las preguntas (una sola vez, streamlit vuelve a correr esto en cada recarga pero es rapido)
with open(ruta_json, encoding='utf-8') as f:
    data = json.load(f)


#quita tildes para que "Matematicas" y "Matemáticas" se traten igual
def quitar_tildes(texto):
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in texto_normalizado if not unicodedata.combining(c))


# ============================================================
# SESSION STATE
# ============================================================
if "name" not in st.session_state:
    st.session_state.name = ""
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "pregunta_index" not in st.session_state:
    st.session_state.pregunta_index = 0
if "correctas" not in st.session_state:
    st.session_state.correctas = 0
if "respondio" not in st.session_state:
    st.session_state.respondio = False
if "fue_correcta" not in st.session_state:
    st.session_state.fue_correcta = None
if "examen_termino" not in st.session_state:
    st.session_state.examen_termino = False


#crea la variable de la fecha
def obtener_fecha():
    now = datetime.datetime.now()
    return now.strftime("%d/%m/%Y %H:%M")


#guardar el resultado en un archivo json
def guardar_resultado(name, subject, correctas, total):
    resultado = {
        "nombre": name,
        "materia": subject,
        "correctas": correctas,
        "total": total,
        "fecha": obtener_fecha()
    }
    try:
        with open(ruta_resultados, 'r', encoding='utf-8') as f:
            resultados = json.load(f)
    except FileNotFoundError:
        resultados = []
    resultados.append(resultado)
    with open(ruta_resultados, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)


def reiniciar_todo():
    st.session_state.name = ""
    st.session_state.subject = ""
    st.session_state.pregunta_index = 0
    st.session_state.correctas = 0
    st.session_state.respondio = False
    st.session_state.fue_correcta = None
    st.session_state.examen_termino = False


# ============================================================
# INTERFAZ
# ============================================================

st.title("Tutor Virtual ICFES")

#preguntar el nombre
if st.session_state.name == "":
    nombre_temp = st.text_input("Como te llamas?")
    if st.button("Continuar"):
        if nombre_temp.strip() != "":
            st.session_state.name = nombre_temp
            st.rerun()
        else:
            st.warning("Escribe tu nombre para continuar.")

#seleccionar la materia (o historial)
elif st.session_state.subject == "":
    st.write(f"Hola, {st.session_state.name}!")
    st.write("Bienvenido al examen de matematicas. Escribe 'matematicas' para el examen, o 'historial' para ver tus resultados anteriores.")
    subject_temp = st.text_input("Seleciona la materia (o escribe 'historial'):")
    if st.button("Continuar", key="btn_subject"):
        #normaliza quitando tildes y pasando a mayusculas, asi "Matemáticas" y "Matematicas" son iguales
        st.session_state.subject = quitar_tildes(subject_temp).upper()
        st.rerun()

#pantalla de historial
elif st.session_state.subject == "HISTORIAL":
    st.subheader("Historial de resultados")
    try:
        with open(ruta_resultados, 'r', encoding='utf-8') as f:
            resultados = json.load(f)
        for r in resultados:
            st.write(f"**{r['nombre']}** - {r['materia']} - {r['correctas']}/{r['total']} - {r['fecha']}")
    except FileNotFoundError:
        st.info("No hay historial de resultados todavia.")

    if st.button("Volver"):
        reiniciar_todo()
        st.rerun()

#materia no disponible
elif st.session_state.subject != "MATEMATICAS":
    st.error("Materia no disponible, por favor selecciona matematicas.")
    if st.button("Volver a intentar"):
        st.session_state.subject = ""
        st.rerun()

#el examen (subject == "MATEMATICAS")
elif not st.session_state.examen_termino:
    pregunta = data[st.session_state.pregunta_index]

    st.write(f"Pregunta {st.session_state.pregunta_index + 1} de {len(data)}")
    st.subheader(f"{pregunta['id']}. {pregunta['tema']}")
    st.write(pregunta['pregunta'])

    opciones_texto = [f"{letra}: {opcion}" for letra, opcion in pregunta['opciones'].items()]
    seleccion = st.radio("Selecciona la respuesta correcta:", opciones_texto, key=f"radio_{st.session_state.pregunta_index}")

    if not st.session_state.respondio:
        if st.button("Responder"):
            answer = seleccion.split(":")[0]
            st.session_state.respondio = True

            if answer == pregunta['respuesta_correcta']:
                st.session_state.correctas += 1
                st.session_state.fue_correcta = True
            else:
                st.session_state.fue_correcta = False
            st.rerun()
    else:
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

            if st.session_state.pregunta_index >= len(data):
                st.session_state.examen_termino = True
                guardar_resultado(st.session_state.name, st.session_state.subject, st.session_state.correctas, len(data))
            st.rerun()

#resultado final
else:
    st.success(f"Felicidades acabaste el examen de {st.session_state.subject}")
    st.write(f"Respondiste correctamente {st.session_state.correctas} preguntas de {len(data)}")

    if st.button("Intentar de nuevo"):
        reiniciar_todo()
        st.rerun()