from datetime import datetime


class Booking:
    """
    La representación de una reserva de mesa de ping pong.
    """

    def __init__(self,
                 time_slot,
                 ping_pong_table,
                 booker,
                 notes,
                 pk=None):
        """
        :param booking_store: Una instancia de BookingStore que
         representa donde se guardan las reservas.
        :param time_slot: Una instancia de TimeSlot que representa
         el intervalo de tiempo a la que se asigna la reserva.
        :param ping_pong_table: Una instancia de PingPongTable a la
         que se asigna esta reserva.
        :param booker: Una instancia de Booker que representa la
         persona que realiza esta reserva.
        :param notes: Una string con notas adicionales opcionales.
        :param pk: Un número entero correspondiente a la clave
         primaria que identifica esta reserva en BookingStore.
        """
        self.time_slot = time_slot
        self.ping_pong_table = ping_pong_table
        self.booker = booker
        self.notes = notes
        self.pk = pk

    @property
    def start_datetime_str(self):
        """
        :return: Una string que representa una instancia de
         datetime.datetime, que será almacenada en la base
         de datos.
        """
        day_date = self.time_slot.week_day.date
        start_datetime = datetime(day=day_date.day,
                                  month=day_date.month,
                                  year=day_date.year,
                                  hour=self.time_slot.start_time.hour,
                                  minute=self.time_slot.start_time.minute)
        return start_datetime.isoformat()

