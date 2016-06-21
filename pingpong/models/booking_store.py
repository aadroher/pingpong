
class BookingStore:
    """
    Representa un sistema de almacenamiento de datos para
    las reservas de pista.
    """

    db_table_name = 'bookings'

    def __init__(self, db_con):
        """
        :param db_con: La instancia de sqlite.Connection a utilizar.
        """
        self.db_con = db_con

    def save_booking(self, booking):
        """
        Guarda los datos correspondientes a una reserva de pista.
        :param booking: Una instancia de Booking
        """
        query_template = ("insert into {table_name} ("
                          "  start_datetime,"
                          "  tennis_table,"
                          "  booker_name,"
                          "  booker_email,"
                          "  notes"
                          ") values (?, ?, ?, ?, ?);"
                          ).format(table_name=self.db_table_name)

        values = (booking.start_datetime_str,
                  booking.tennis_table.name,
                  booking.booker.name,
                  booking.booker.email,
                  booking.notes)

        cursor = self.db_con.cursor()
        cursor.execute(query_template, values)
        self.db_con.commit()

