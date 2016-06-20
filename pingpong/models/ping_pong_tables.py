
TABLES = ('A', 'B')


def get_ping_pong_tables():

    return [PingPongTable(name) for name in TABLES]


class PingPongTable:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

