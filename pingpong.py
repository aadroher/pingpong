#!/usr/bin/env python3
# -*- coding: utf8 -*-

from flask import Flask

# Instancia de la aplicación
app = Flask(__name__)


# Ruta por defecto
@app.route('/')
def it_works():
    """
    Retorna una cadena de caracteres simple.
    """
    return "¡Funciona!"

if __name__ == '__main__':
    app.run()

