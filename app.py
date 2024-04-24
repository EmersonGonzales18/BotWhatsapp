#Importacion de librerias
from flask import Flask,request, render_template, jsonify
import sett
import servicios


app = Flask(__name__)
@app.route('/welcome', methods= ['GET'])
def index():
    return "Version de prueba 2s"

@app.route('/webhook', methods= ['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challengue = request.args.get('hub.challengue')

        if token == sett.token and challengue !=None:
            return challengue
        else: 
            return 'token incorrecto'
    except Exception as e:
        return e, 403

@app.route('/webhook', methods= ['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = servicios.enviar_mensaje(message)
        services = servicios.administrar_chatbot(text,number,messageId, name)
        return 'enviado'
    except Exception as e:
        return 'no enviado' + str(e)



if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)