
TABLES = ('A', 'B')


def get_ping_pong_tables():
    """
    :return: Una lista con instancias de PingPongTable que
      corresponden a los nombres definidos en TABLES.
    """
    return [PingPongTable(name) for name in TABLES]


def get_tennis_table(name):
    return next(tennis_table for tennis_table in get_ping_pong_tables()
                if tennis_table.name == name.upper())


class PingPongTable:
    """
    Representa una mesa de ping pong.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

