from dateutil import parser

from .time_slot import TimeSlot
from .day import Day
from ..models import week
from .ping_pong_tables import PingPongTable
from .booker import Booker
from .booking import Booking


def get_booking(time_slot,
                ping_pong_table,
                bookings):
    """
    :param time_slot: Una instancia de TimeSlot
    :param ping_pong_table: Una instancia de PinPongTable
    :param bookings: Una lista de instancias de Booking
    :return: Una instancia de Booking que se encuentra en
     bookings y ha sido asignada a time_slot y a
     ping_pong_table.
    """
    try:
        return next(booking for booking in bookings
                    if booking.ping_pong_table == ping_pong_table and
                    booking.time_slot == time_slot)
    except StopIteration:
        return None


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

    def get_booking_by_pk(self, pk):
        query_template = ("select * from {table_name} "
                          "where {table_name}.id = {pk};")

        query = query_template.format(table_name=self.db_table_name, pk=pk)
        cursor = self.db_con.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        booking = self.build_booking_from_row(row)
        return booking

    def get_bookings(self, day):
        """
        :param day: Una instancia de Day.
        :return: Una lista de instancias de Booking correspondientes
         a day.
        """
        query_template = ("select * from {table_name} "
                          "where {table_name}.start_datetime >= '{min_start_time}' "
                          "and {table_name}.start_datetime <= '{max_start_time}';")

        query = query_template.format(table_name=self.db_table_name,
                                      min_start_time=day.first_time_slot.isoformat,
                                      max_start_time=day.last_time_slot.isoformat)

        cursor = self.db_con.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        bookings = [self.build_booking_from_row(row) for row in rows]
        return bookings

    def build_booking_from_row(self, row):
        """
        :param row: Una instancia de sqlite3.Row, que representa uno de los
         registros de la tabla de la base de datos.
        :return: Una instancia de Booking correspondiente a este registro.
        """
        pk = row['id']
        parsed_datetime = parser.parse(row['start_datetime'])
        day_date = parsed_datetime.date()
        start_time = parsed_datetime.time()
        day_week = week.from_date(day_date)
        day = Day(day_week, day_date)
        time_slot = TimeSlot(day, start_time)
        ping_pong_table = PingPongTable(row['ping_pong_table'])
        booker = Booker(row['booker_name'], row['booker_email'])
        booking = Booking(pk=pk,
                          time_slot=time_slot,
                          ping_pong_table=ping_pong_table,
                          booker=booker,
                          notes=row['notes'])
        return booking

    def save_booking(self, booking):
        """
        Guarda los datos correspondientes a una reserva de pista.
        :param booking: Una instancia de Booking
        """
        query_template = ("insert into {table_name} ("
                          "  start_datetime,"
                          "  ping_pong_table,"
                          "  booker_name,"
                          "  booker_email,"
                          "  notes"
                          ") values (?, ?, ?, ?, ?);"
                          ).format(table_name=self.db_table_name)

        values = (booking.start_datetime_str,
                  booking.ping_pong_table.name,
                  booking.booker.name,
                  booking.booker.email,
                  booking.notes)

        cursor = self.db_con.cursor()
        cursor.execute(query_template, values)
        self.db_con.commit()

    def delete_booking(self, pk):
        query_template = ("delete from {table_name} "
                          "where {table_name}.id = ?;"
                          ).format(table_name=self.db_table_name)
        cursor = self.db_con.cursor()
        cursor.execute(query_template, (pk,))
        return self.db_con.commit()
