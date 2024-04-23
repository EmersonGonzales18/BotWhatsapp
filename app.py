#Importacion de librerias
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def bienvenido():
    return render_template('hola.html')


if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True, )