
TABLES = ('A', 'B')


def get_ping_pong_tables():
    """
    :return: Una lista con instancias de PingPongTable que
      corresponden a los nombres definidos en TABLES.
    """
    return [PingPongTable(name) for name in TABLES]


def get_ping_pong_table(name):
    """
    :param name: Un nombre de mesa de ping pong.
    :return: La mesa cuyo nombre es igual a name.
    """
    return next(ping_pong_table for ping_pong_table in get_ping_pong_tables()
                if ping_pong_table.name == name.upper())


class PingPongTable:
    """
    Representa una mesa de ping pong.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @property
    def url_name(self):
        """
        :return: Cadena de caracteres para formar el
         fragmento de URL que corresponde a esta tabla.
        """
        return str(self).lower()

    def __eq__(self, other):
        return self.name == other.name


