import requests
import sett
import json


def obtener_mensaje(message):
    if 'type' not in message:
        text = 'mensaje no reconocido'
    typeMessage = message['type']    
    if typeMessage == 'text':
        text = message['text']['body']
    return text


def enviar_mensaje(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {
            'Content-Type' : 'application/json',
            'Authorization' : 'Bearer' + whatsapp_token
        }
        response = requests.post(whatsapp_url,headers=headers,data=data)
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar', response.status_code
        
    except Exception as e:
        return e,403
    
def text_message(number,text):
    data = json.dumps(
            {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
            }
    )
    return data


def administrar_chatbot(text,number,messageId, name):
    text = text.lower()
    list = []
    data = text_message("51963957004", "Solo costo 30 soles")
    enviar_mensaje(data)