class Camera:
    def __init__(self, pos: list):
        self.true_pos = pos

    @property
    def pos(self):
        return map(int, self.true_pos)

    def adjust(self, focus_pos, size):
        self.true_pos[0] += (focus_pos[0] - self.true_pos[0] - size[0] // 2) / 10
        self.true_pos[1] += (focus_pos[1] - self.true_pos[1] - size[1] // 2) / 10
