class Board:
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.map = []

    def add(self, obj, pos=None):
        if pos is None:  # get the chunk coords from object
            self.map.append(obj)
        else:  # set chunk coords
            self.map.append(obj)

    def pop(self, obj, pos=None):
        if pos is None:  # get the chunk coords from object
            self.map.remove(obj)
        else:  # set chunk coords
            self.map.remove(obj)
