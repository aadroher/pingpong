from datetime import time, datetime, timedelta


def current_year():
    return datetime.now().year


def current_week():
    week_num = datetime.now().strftime("%W")
    return int(week_num)


def date_from_iso(year, week, wday):
    date_str = "{year} {week} {wday}".format(year=year,
                                             week=week,
                                             wday=wday)

    return datetime.strptime(date_str, "%Y %W %w").date()


class Week:

    def __init__(self, year, week_num):
        self.year = year
        self.week_num = week_num

    @property
    def days(self):
        wday_indexes = list(range(1, 7)) + [0]
        week_dates = [date_from_iso(self.year, self.week_num, wday_index)
                      for wday_index in wday_indexes]
        return [Day(week_date) for week_date in week_dates]

    @property
    def prev_day(self):
        day_period = timedelta(days=1)
        prev_day_date = self.first_day.date - day_period
        return Day(prev_day_date)

    @property
    def first_day(self):
        return self.days[0]

    @property
    def last_day(self):
        return self.days[-1]

    @property
    def next_day(self):
        day_period = timedelta(days=1)
        prev_day_date = self.last_day.date + day_period
        return Day(prev_day_date)


class Day:

    wday_codes = ('l', 'm', 'x', 'j', 'v', 's', 'd')
    start_time_hour = 7
    end_time_hour = 24

    def __init__(self, day_date):
        self.date = day_date

    @property
    def code(self):
        return self.wday_codes[self.date.weekday()]

    @property
    def week(self):
        year = self.date.year
        week_num = int(self.date.strftime("%W"))
        return Week(year, week_num)

    @property
    def first_time_slot(self):
        return self.time_slots[0]

    @property
    def last_time_slot(self):
        return self.time_slots[-1]

    @property
    def time_slots(self):
        return [TimeSlot(self, time(hour=n)) for n in range(7, 24)]


    def get_time_slot(self, time_str):
        start_time = datetime.strptime(time_str,
                                       TimeSlot.time_url_pattern)
        return TimeSlot(self, start_time)

    def __str__(self):
        return self.date.strftime("%d/%m/%Y")

    def __eq__(self, other):
        return self.date == other.date


class TimeSlot:

    time_url_pattern = '%H%M'
    time_str_pattern = '%H:%M'

    def __init__(self,
                 day,
                 start_time):
        self.day = day
        self.start_time = start_time

    def __str__(self):
        return self.start_time.strftime(self.time_str_pattern)

    @property
    def time_url_str(self):
        return self.start_time.strftime(self.time_url_pattern)

    @property
    def isoformat(self):
        time_slot_datetime = datetime.combine(self.day.date, self.start_time)
        return time_slot_datetime.isoformat()

    def __eq__(self, other):
        return self.isoformat == other.isoformat


