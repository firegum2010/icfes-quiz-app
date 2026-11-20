#trae el modulo json
import json
#import datetime
import datetime
#trae el modulo os k es para saber donde esta el directorio
import os
#busca el archivo json en la misma carpeta que el script
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_json = os.path.join(carpeta_actual, 'preguntas_matematicas.json')
#main es preguntar el nombre y decir las preguntas
def main():
    #crea la variable de la fecha
    now = datetime.datetime.now()
    #formato para la fecha
    formatdate = now.strftime("%d/%m/%Y %H:%M")
    #imprime la fecha
    print(f"Fecha: {formatdate}")
    #inizializa una variable para contar las preguntas correctas
    correctas = 0
    #mostrar el directorio actual
    print(f"Directorio actual: {os.getcwd()}")
    #preguntar el nombre
    name = input("Como te llamas?: ")
    print(f"Hola, {name}!")
    #dar unas instruciiones al usuario
    print("Bienvenido al examen de matematicas, por favor responde las preguntas con la letra de la respuesta correcta(a,b,c,d).")
    #seleccionar la materia
    subject = input("Seleciona la materia(solo matematicas disponible), escribe historial para poder ver tus datos: ").upper()
    #selecionar el archivo json de matematicas
    if subject == "MATEMATICAS" or subject == "MATEMÁTICAS":
        #saca el archivo json de matematicas
        with open(ruta_json, encoding='utf-8') as f:
            data = json.load(f)
            print(subject)
        #se intenta abrir el archivo json de resultados, si no existe lo crea
        for pregunta in data:
            print(f"{pregunta['id']}. {pregunta['tema']}")
            print(pregunta['pregunta'])
            for letra, opcion in pregunta['opciones'].items():
                print(f"{letra}: {opcion}") 
            answer = input("Selecciona la respuesta correcta: ").upper()
            if answer == pregunta['respuesta_correcta']:
                print("Respuesta correcta!")
                correctas += 1
            else:
                print("Respuesta incorrecta!")
                print(f"La respuesta correcta es: {pregunta['respuesta_correcta']}")
                print(f"Explicacion: {pregunta['explicacion']}")
            #cuando llegue a 20 preguntas se le dira al usaurio sus respuestas correctas
            if pregunta['id'] == len(data):
                print(f"Felicidades acabaste el exemen de {subject} ")
                print(f"Respondiste correctamente {correctas} preguntas de {len(data)}")
                resultado = {
                    "nombre": name,
                    "materia": subject,
                    "correctas": correctas,
                    "total": len(data),
                    "fecha": formatdate
                }
                try:
                #intenta abrir el archivo json de resultados
                    with open('resultados.json', 'r', encoding='utf-8') as f:
                         resultados = json.load(f)
                except FileNotFoundError:
                    #si no existe el archivo json de resultados lo crea
                    resultados = []
                resultados.append(resultado)
                #se agrega esta linea para que el archivo json de resultados se guarde en el mismo directorio que el script
                with open('resultados.json', 'w', encoding='utf-8') as f:
                    json.dump(resultados, f, ensure_ascii=False, indent=4)
                #guardar el resultado en un archivo json
    elif subject == "HISTORIAL":
        try:
            with open('resultados.json', 'r', encoding='utf-8') as f:
                resultados = json.load(f)
                print("Historial de resultados:")
                for resultado in resultados:
                    print(f"Nombre: {resultado['nombre']}, Materia: {resultado['materia']}, Correctas: {resultado['correctas']}, Total: {resultado['total']}, Fecha: {resultado['fecha']}")
        except FileNotFoundError:
            print("No hay historial de resultados.")       
    else:
        print("Materia no disponible, por favor selecciona matematicas.")
    
main()