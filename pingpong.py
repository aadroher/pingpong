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
from pingpong.models.booking_store import BookingStore, get_booking
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


@app.route('/bookings/<int:year_num>/<int:month_num>/<int:day_num>.html')
def list_bookings(year_num, month_num, day_num):
    """
    Obtiene el día correspondiente a los parámetros definidos
    en la URL.
    """
    day_date = date(year_num, month_num, day_num)
    day_week = week.from_date(day_date)
    day = Day(day_week, day_date)

    ping_pong_tables = get_ping_pong_tables()
    booking_store = BookingStore(g.db_con)
    bookings = booking_store.get_bookings(day)

    ping_pong_tables_data = [{
                                 'ping_pong_table': ping_pong_table,
                                 'time_slots': [
                                     {
                                         'time_slot': time_slot,
                                         'booking': get_booking(time_slot,
                                                                ping_pong_table,
                                                                bookings)
                                     }
                                     for time_slot in day.time_slots
                                     ]
                             }
                             for ping_pong_table in ping_pong_tables]

    view_data = {
        'day_data': {
            'day': day,
            'tennis_tables_data': ping_pong_tables_data
        }
    }

    return render_template('list_bookings.html',
                           view_data=view_data)


@app.route('/bookings/<int:year_num>/<int:month_num>/<int:day_num>/<time>/<table>.html',
           methods=['GET', 'POST'])
def create_booking(year_num, month_num, day_num, time, table):
    """
    Si request.method == 'GET': Muestra un formulario para introducir
     los datos para crear una nueva reserva.
    Si request.method == 'POST': Crea una nueva reserva.
    """

    day_date = date(year_num, month_num, day_num)
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
                      year_num=year_num,
                      month_num=month_num,
                      day_num=day.date.day)
        return redirect(url)
    else:
        return render_template('create_booking.html',
                               time_slot=time_slot,
                               table=ping_pong_table)


@app.route('/bookings/delete/<int:pk>.html',
           methods=['GET', 'POST'])
def delete_booking(pk):
    """
    Si request.method == 'GET': Muestra un resumen de la reserva
     a cancelar.
    Si request.method == 'POST': Elimina la reserva correspondiente
     la clave primaria pk.
    """
    booking_store = BookingStore(g.db_con)
    booking = booking_store.get_booking_by_pk(pk)

    if request.method == 'POST':
        booking_store.delete_booking(pk)
        day_date = booking.time_slot.week_day.date
        url = url_for('list_bookings',
                      year_num=day_date.year,
                      month_num=day_date.month,
                      day_num=day_date.day)
        return redirect(url)
    else:
        return render_template('delete_booking.html',
                               booking=booking)

@app.before_request
def load_db_connection():
    """
    Crea una conexión con la base de datos y la
    guarda en la lista de variables globales.
    """
    g.db_con = sqlite3.connect(DB)
    g.db_con.row_factory = sqlite3.Row


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

