
from datetime import datetime

"""
Este módulo representa el calendario general para la
aplicación. Puesto que es único y no hay que guardar
ninguna información sobre el mismo, se representa de
esta forma y no mediante una clase.
"""


def current_year():
    """
    :return: El año en el que nos encontramos.
    """
    return datetime.now().year


def current_week():
    """
    :return: La representación numérica de la
     semana del año en el que nos encontramos.
    """
    week_num = datetime.now().strftime("%W")
    return int(week_num)

def date_from_nums(year, week, week_day):
    """
    Genera un objeto datetime.date a partir de los
    siguientes parámetros numéricos.
    :param year: El año de la fecha.
    :param week: La semana del año.
    :param week_day: El día de la semana.
    :return:
    """
    date_str = "{year} {week} {week_day}".format(year=year,
                                                 week=week,
                                                 week_day=week_day)

    return datetime.strptime(date_str, "%Y %W %w").date()

