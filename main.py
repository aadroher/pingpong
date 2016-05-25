#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sqlite3
from datetime import time, date

from flask import Flask, render_template, request, redirect, url_for, g

from pingpong.models.calendar import Day
from pingpong.models.tennis_tables import get_tennis_tables, get_tennis_table
from pingpong.models.bookings import BookingStore, Booking, Booker, get_booking


# Creación del objeto aplicación
app = Flask(__name__)


# Configuración
# True para el modo de depuración.
DEBUG = True

# Ubicación de la base de datos.
DB = 'db/pingpong.sqlite'

# Cargamos la configuración.
app.config.from_object(__name__)


# Rutas
@app.route('/')
def home():

    days_of_week = ['l', 'm', 'x', 'j', 'v', 's', 'd']

    time_slots = [time(hour=n) for n in range(7, 24)]

    return render_template('list_bookings.html',
                           week_days=days_of_week,
                           time_slots=time_slots)


@app.route('/bookings/<int:year>/<int:month>/<int:day_num>.html')
def list_bookings(year, month, day_num):

    day = Day(date(year, month, day_num))
    tennis_tables = get_tennis_tables()
    booking_store = BookingStore(g.db_con)
    bookings = booking_store.get_bookings(day)
    tennis_tables_data = [{
                            'tennis_table': tennis_table,
                            'time_slots': [
                                {
                                    'time_slot': time_slot,
                                    'booking': get_booking(time_slot,
                                                           tennis_table,
                                                           bookings)
                                }
                                for time_slot in day.time_slots
                            ]
                        }
                        for tennis_table in tennis_tables]
    view_data = {
        'day_data': {
            'day': day,
            'tennis_tables_data': tennis_tables_data
        }
    }

    return render_template('list_bookings.html',
                           view_data=view_data)


@app.route('/bookings/<int:year>/<int:month>/<int:day_num>/<time_url_str>/<table_name>.html',
           methods=['GET', 'POST'])
def create_booking(year, month, day_num, time_url_str, table_name):

    day = Day(date(year, month, day_num))
    time_slot = day.get_time_slot(time_url_str)
    tennis_table = get_tennis_table(table_name)

    if request.method == 'POST':
        booker = Booker(
            request.form['booking_booker_name'],
            request.form['booking_booker_email']
        )
        booking_store = BookingStore(g.db_con)
        booking = Booking(
            booking_store,
            time_slot,
            tennis_table,
            booker,
            request.form['booking_notes']
        )
        booking_store.save_booking(booking)
        url = url_for('list_bookings',
                      year=year,
                      month=month,
                      day_num=day_num)
        return redirect(url)
    else:
        return render_template('create_booking.html',
                               time_slot=time_slot,
                               table=tennis_table)


@app.route('/bookings/delete/<int:pk>.html',
           methods=['GET', 'POST'])
def delete_booking(pk):
    booking_store = BookingStore(g.db_con)
    booking = booking_store.get_booking_by_pk(pk)

    if request.method == 'POST':
        booking_store.delete_booking(pk)
        day_date = booking.time_slot.day.date
        url = url_for('list_bookings',
                      year=day_date.year,
                      month=day_date.month,
                      day_num=day_date.day)
        return redirect(url)
    else:
        return render_template('delete_booking.html',
                               booking=booking)



@app.before_request
def load_db_connection():
    g.db_con = sqlite3.connect(DB)
    g.db_con.row_factory = sqlite3.Row


@app.teardown_request
def close_db_connection(exception):
    db_con = g.get('db_con', None)
    if db_con is not None:
        db_con.close()

# Ejecución de la aplicación
if __name__ == '__main__':
    app.run()




