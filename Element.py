"""
"""

i = 0

class Element(object):

    """
    """
    def __init__(self, algorator, x, y):
        global i
        self.algorator = algorator
        self.arrows = []
        self.name = "Test" + str(i)
        i += 1
        self.draw(x, y, self.name)
        self.saved = True

    def move(self, event):
        self.destroy()
        self.draw(event.x, event.y, self.name)
        for arrow in self.arrows:
            arrow.move(event)


