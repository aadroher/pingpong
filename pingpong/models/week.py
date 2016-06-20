from datetime import timedelta

from .calendar import date_from_nums
from .day import Day


def from_date(day_date):
    """
    :param day_date: Una instancia de datetime.date.
    :return: La instancia de Week a la que pertenece
     el día representado por day_date.
    """
    year = day_date.year
    week_num = int(day_date.strftime("%W"))
    return Week(year, week_num)


class Week:
    """
    Representación de una semana.
    """

    def __init__(self, year, week_num):
        """
        :param year: El número del año al que se asigna la
         semana.
        :param week_num: El número de esta semana en el
         año en cuestión.
        """
        self.year = year
        self.week_num = week_num

    @property
    def days(self):
        """
        :return: Una lista de instancias de Day que representan
         los días que pertenecen a esta semana, en el orden
         correcto y empezando por el lunes.
        """
        week_day_indexes = list(range(1, 7)) + [0]
        week_dates = [date_from_nums(self.year, self.week_num, week_day_index)
                      for week_day_index in week_day_indexes]
        return [Day(self, week_date) for week_date in week_dates]

    @property
    def prev_day(self):
        """
        :return: La instancia de Day que corresponde al último día
         de la semana anterior.
        """
        day_period = timedelta(days=1)
        prev_day_date = self.first_day.date - day_period
        return Day(self, prev_day_date)

    @property
    def first_day(self):
        """
        :return: El primer día de la semana.
        """
        return self.days[0]

    @property
    def last_day(self):
        """
        :return: El último día de la semana.
        """
        return self.days[-1]

    @property
    def next_day(self):
        """
        :return: El primer día de la siguiente semana.
        """
        day_period = timedelta(days=1)
        prev_day_date = self.last_day.date + day_period
        return Day(None, prev_day_date)
