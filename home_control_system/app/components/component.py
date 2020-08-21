from .style import Style


# Component Abstract Class
class Component():
    unit = 1
    root = None

    def __init__(self, ascendent=None):
        (self.width, self.height) = (0, 0)
        self.descendents = []
        self.ascendent = None
        if ascendent is not None:
            self.ascendent = ascendent
            self.ascendent.add_descendent(self)
            (self.width, self.height) = (self.ascendent.width, self.ascendent.height)

        if Component.root is None:
            Component.root = self
            Style.set_unit(self.get_resolution())

    def add_descendent(self, descendent):
        self.descendents.append(descendent)

    def set_dimensions(self, width, height):
        (self.width, self.height) = (int(width), int(height))
