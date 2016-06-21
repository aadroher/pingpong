#!/usr/bin/env python3
# -*- coding: utf8 -*-
import sqlite3
from datetime import date

from flask import Flask, render_template, request, redirect, url_for, g

from pingpong.models.day import Day
from pingpong.models import week
from pingpong.models.ping_pong_tables import (
    get_ping_pong_tables,
    get_ping_pong_table
)
from pingpong.models.booking import Booking
from pingpong.models.booking_store import BookingStore
from pingpong.models.booker import Booker

# Creación del objeto aplicación
app = Flask(__name__)

# Configuración
# True para el modo de depuración.
DEBUG = True

# Ubicación de la base de datos.
DB = 'db/pingpong.sqlite'

# Cargamos la configuración.
app.config.from_object(__name__)


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


@app.route('/bookings/<int:year>/<int:month>/<int:day>/<time>/<table>.html',
           methods=['GET', 'POST'])
def create_booking(year, month, day, time, table):
    """
    Si request.method == 'GET': Muestra un formulario far introducir
     los datos para crear una nueva reserva.
    Si request.method == 'POST': Crea una nueva reserva.
    """

    day_date = date(year, month, day)
    day_week = week.from_date(day_date)
    day = Day(day_week, day_date)
    time_slot = day.get_time_slot(time)
    ping_pong_table = get_ping_pong_table(table)

    if request.method == 'POST':
        booker = Booker(
            request.form['booking_booker_name'],
            request.form['booking_booker_email']
        )
        booking = Booking(
            time_slot,
            ping_pong_table,
            booker,
            request.form['booking_notes']
        )
        booking_store = BookingStore(g.db_con)
        booking_store.save_booking(booking)
        url = url_for('list_bookings',
                      year=year,
                      month=month,
                      day=day.date.day)
        return redirect(url)
    else:
        return render_template('create_booking.html',
                               time_slot=time_slot,
                               table=ping_pong_table)


@app.before_request
def load_db_connection():
    """
    Crea una conexión con la base de datos y la
    guarda en la lista de variables globales.
    """
    g.db_con = sqlite3.connect(DB)


@app.teardown_request
def close_db_connection(exception):
    """
    Cierra la conexión con la base de datos.
    :param exception: La excepción, si existe, que ha causado
     la destrucción de la petición.
    """
    db_con = g.get('db_con', None)
    if db_con is not None:
        db_con.close()


if __name__ == '__main__':
    app.run(debug=DEBUG)

