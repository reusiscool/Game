class CallerSystem:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            return cls.__init__(*args, **kwargs)
        return cls.instance

    def __init__(self):
        self.calls = []
        self.pos = None

    def update(self, board):
        self.pos = board.player.pos

    def saw_player(self, self_pos):
        self.calls.append(self_pos)
