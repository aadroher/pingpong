
TABLES = ('A', 'B')


class TennisTable:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @property
    def url_name(self):
        return str(self).lower()

    def __eq__(self, other):
        return self.name == other.name


def get_tennis_tables():

    return [TennisTable(name) for name in TABLES]


def get_tennis_table(name):
    return next(tennis_table for tennis_table in get_tennis_tables()
                if tennis_table.name == name.upper())
