#Importacion de librerias
from flask import Flask, render_template
from flask_sqlalchemy import  SQLAlchemy
from datetime import datetime
import json


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
    prueba1 = Log(texto= 'Mensaje de prueba 1')
    prueba2 = Log(texto= 'Mensaje de prueba 2')
    db.session.add(prueba1)
    db.session.add(prueba2)
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

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True, )