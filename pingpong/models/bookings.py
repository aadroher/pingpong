from .calendar import TimeSlot, Day
from .tennis_tables import TennisTable

from sqlite3 import connect, Connection, Row
from datetime import datetime
from dateutil import parser


class BookingStore:

    db_table_name = 'bookings'

    def __init__(self, db_con: Connection):
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

    def get_bookings(self, day: Day):

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

    def build_booking_from_row(self, row: Row):
        pk = row['id']
        parsed_datetime = parser.parse(row['start_datetime'])
        day_date = parsed_datetime.date()
        start_time = parsed_datetime.time()
        day = Day(day_date)
        time_slot = TimeSlot(day, start_time)
        tennis_table = TennisTable(row['tennis_table'])
        booker = Booker(row['booker_name'], row['booker_email'])
        booking = Booking(pk=pk,
                          booking_store=self,
                          time_slot=time_slot,
                          tennis_table=tennis_table,
                          booker=booker,
                          notes=row['notes'])
        return booking

    def save_booking(self, booking):
        query_template = ("insert into {table_name} ("
                          "  start_datetime,"
                          "  tennis_table,"
                          "  booker_name,"
                          "  booker_email,"
                          "  notes"
                          ") values (?, ?, ?, ?, ?);"
                          ).format(table_name=self.db_table_name)
        print(booking.notes)
        values = (booking.start_datetime_str,
                  booking.tennis_table.name,
                  booking.booker.name,
                  booking.booker.email,
                  booking.notes)

        cursor = self.db_con.cursor()
        cursor.execute(query_template, values)
        return self.db_con.commit()

    def delete_booking(self, pk):
        query_template = ("delete from {table_name} "
                          "where {table_name}.id = ?;"
                          ).format(table_name=self.db_table_name)
        cursor = self.db_con.cursor()
        cursor.execute(query_template, (pk,))
        return self.db_con.commit()


class Booker:

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Booking:

    def __init__(self,
                 booking_store: BookingStore,
                 time_slot: TimeSlot,
                 tennis_table: TennisTable,
                 booker: Booker,
                 notes: str,
                 pk: int=None):

        self.booking_store = booking_store
        self.time_slot = time_slot
        self.tennis_table = tennis_table
        self.booker = booker
        self.notes = notes
        self.pk = pk

    @property
    def start_datetime_str(self):
        day_date = self.time_slot.day.date
        start_datetime = datetime(day=day_date.day,
                                  month=day_date.month,
                                  year=day_date.year,
                                  hour=self.time_slot.start_time.hour,
                                  minute=self.time_slot.start_time.minute)
        return start_datetime.isoformat()

    def save(self):
        return self.booking_store.save_booking(self)


def get_booking(time_slot: TimeSlot,
                tennis_table: TennisTable,
                bookings: [Booking]):

    try:
        return next(booking for booking in bookings
                    if booking.tennis_table == tennis_table and
                    booking.time_slot == time_slot)
    except StopIteration:
        return None






