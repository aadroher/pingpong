from datetime import datetime


class TimeSlot:
    """
    La representación de un intervalo de tiempo.
    """

    # Patrones para la creación de strings.
    time_url_pattern = '%H%M'
    time_str_pattern = '%H:%M'

    def __init__(self,
                 week_day,
                 start_time):
        """
        :param week_day: Una instancia de Day a la que este intervalo
         de tiempo pertenece.
        :param start_time: Una instancia de datetime.time que indica el
         instante inicial de este intervalo de tiempo.
        """
        self.week_day = week_day
        self.start_time = start_time

    def __str__(self):
        return self.start_time.strftime('%H:%M')

    @property
    def time_url_str(self):
        """
        :return: Cadena de caracteres para formar el fragmento
         de UTL que corresponde a este intervalo de tiempo.
        """
        return self.start_time.strftime(self.time_url_pattern)

    @property
    def isoformat(self):
        """
        :return: La representación del instante de inicio del
         intervalo en una string que sigue el formato ISO 8601.
         Ver https://docs.python.org/3.5/library/datetime.html.
        """
        time_slot_datetime = datetime.combine(self.week_day.date,
                                              self.start_time)
        return time_slot_datetime.isoformat()

    def __eq__(self, other):
        return self.isoformat == other.isoformat

