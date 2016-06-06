#!/usr/bin/env python3
# -*- coding: utf8 -*-

from datetime import time
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
    days_of_week = ['l', 'm', 'x', 'j', 'v', 's', 'd']

    time_slots = [time(hour=n) for n in range(7, 24)]

    return render_template('time_slots.html',
                           week_days=days_of_week,
                           time_slots=time_slots)


if __name__ == '__main__':
    app.run(debug=DEBUG)

