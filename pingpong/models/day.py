
from datetime import time, datetime

from .time_slot import TimeSlot


class Day:
    """
    Representación de un día.
    """

    week_day_codes = ('l', 'm', 'x', 'j', 'v', 's', 'd')
    start_time_hour = 7
    end_time_hour = 24

    def __init__(self, week, day_date):
        """
        :param week: Una instancia de Week a la que este día
         pertenece.
        :param day_date: La instancia de datetime.date que
         corresponde a este día.
        """
        self.week = week
        self.date = day_date

    @property
    def code(self):
        """
        :return: El código que representa este día en
         función del lugar que ocupa en la semana.
        """
        return self.week_day_codes[self.date.weekday()]

    @property
    def time_slots(self):
        """
        :return: Una lista de instancias de TimeSlot que
         pertenecen a este día.
        """
        return [TimeSlot(self, time(hour=n))
                for n in range(self.start_time_hour,
                               self.end_time_hour)]

    def get_time_slot(self, time_str):
        """
        :param time_str: Una string especificando una hora del día
         mediante el patrón TimeSlot.time_url_pattern.
        :return: Una instancia de TimeSlot correspondiente a la
         hora del día suministrada y perteneciente a esta instancia
         de Day.
        """
        start_time = datetime.strptime(time_str,
                                       TimeSlot.time_url_pattern)
        return TimeSlot(self, start_time)

    def __str__(self):
        return self.date.strftime("%d/%m/%Y")

    def __eq__(self, other):
        return self.date == other.date
