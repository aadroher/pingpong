#!/usr/bin/env python3
# -*- coding: utf8 -*-

from datetime import date
from flask import Flask, render_template

from pingpong.models.day import Day
from pingpong.models import week
from pingpong.models.ping_pong_tables import get_ping_pong_tables

# Configuración
# True para el modo de depuración.
DEBUG = True

# Instancia de la aplicación
app = Flask(__name__)


# Ruta por defecto
@app.route('/')
def home():
    """
    Obtiene el día correspondiente a hoy.
    """
    today_date = date.today()

    return list_bookings(today_date.year,
                         today_date.month,
                         today_date.day)


@app.route('/bookings/<int:year>/<int:month>/<int:day>.html')
def list_bookings(year, month, day):
    """
    Obtiene el día correspondiente a los parámetros definidos
    en la URL.
    """
    day_date = date(year, month, day)
    day_week = week.from_date(day_date)
    day = Day(day_week, day_date)
    return render_template('list_bookings.html',
                           day=day,
                           ping_pong_tables=get_ping_pong_tables())


if __name__ == '__main__':
    app.run(debug=DEBUG)

