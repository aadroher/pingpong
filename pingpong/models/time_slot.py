
class TimeSlot:
    """
    La representación de un intervalo de tiempo.
    """
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
