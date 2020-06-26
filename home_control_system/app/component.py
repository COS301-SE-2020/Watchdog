# Component Abstract Class
class Component():
    def __init__(self, ascendent=None):
        (self.width, self.height) = (0, 0)
        self.descendents = []
        self.ascendent = None
        if ascendent is not None:
            self.ascendent = ascendent
            self.ascendent.add_descendent(self)
            (self.width, self.height) = (self.ascendent.width, self.ascendent.height)

    def add_descendent(self, descendent):
        self.descendents.append(descendent)

    def set_dimensions(self, width, height):
        (self.width, self.height) = (width, height)
