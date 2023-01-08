class ItemConstants:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ItemConstants, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        from .healItem import HealItem
        from .keyItem import KeyItem

        self.const = {
            HealItem: 1,
            KeyItem: 2
        }
        self.types = {}
        for i in self.const:
            self.types[self.const[i]] = i
