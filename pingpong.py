#!/usr/bin/env python3
# -*- coding: utf8 -*-

from flask import Flask, render_template

# Configuración
# True para el modo de depuración.
DEBUG = True

# Instancia de la aplicación
app = Flask(__name__)


# Ruta por defecto
@app.route('/')
def home():
    """
    Retorna una página estática inicial.
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=DEBUG)

