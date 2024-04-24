#Importacion de librerias
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import  SQLAlchemy
from datetime import datetime


app = Flask(__name__)
#Configurando la BD de SQLyte
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)

#Modelo de la tabla Log
class Log(db.Model):
    __tablename__ = 'users_table'
    id = db.Column(db.Integer,primary_key = True)
    fecha_y_hora = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.TEXT)

#crear la tabla si no existe
with app.app_context():
    db.create_all()
    db.session.commit()

def ordenar_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.fecha_y_hora, reverse=True)

@app.route('/')
def index():
    #Obtener todos los registros de la BD
    registros = Log.query.all()
    registros_ordenados = ordenar_fecha_y_hora(registros)
    return render_template('index.html', registros = registros_ordenados)

mensajes_log = []

def agregar_mensajes_log(texto):
    mensajes_log.append(texto)
    #Guardar el mensaje en la BD
    nuevo_registro = Log(texto = texto)
    db.session.add(nuevo_registro)
    db.session.commit()

TOKEN_VERIFICACION = "DREIWHTS"
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        challengue = verificar_token(request)
        return challengue
    elif request.method == 'POST':
        response = recibir_mensaje(request)
        return response

def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challengue =  req.args.get('hub.challengue')

    if challengue and token == TOKEN_VERIFICACION:
        return challengue
    else:
        return jsonify({'error' : 'Token invalido'}), 401
    

def recibir_mensaje(req):
    req = request.get_json()
    agregar_mensajes_log(req)
    
    return jsonify({'message': 'EVENT_RECEIVED'})

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True, )