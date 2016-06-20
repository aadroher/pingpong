
TABLES = ('A', 'B')


def get_ping_pong_tables():
    """
    :return: Una lista con instancias de PingPongTable que
      corresponden a los nombres definidos en TABLES.
    """
    return [PingPongTable(name) for name in TABLES]


class PingPongTable:
    """
    Representa una mesa de ping pong.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

