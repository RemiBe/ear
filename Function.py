"""
"""


class Function(object):

    """
    """
    def __init__(self, algorator, x, y):
        self.algorator = algorator
        self.name = "Test"
        self.create_rectangle(x, y, self.name)
        self.saved = True

    def create_rectangle(self, x, y, name):
        canvas = self.algorator.canvas

        self.text = canvas.create_text(x, y, text=name, tags="selected", fill="blue")
        x1, y1, x2, y2 = canvas.bbox(self.text)
        self.rect = canvas.create_rectangle(x1, y1, x2, y2, tags="selected")

        self.cx = x
        self.cy = y
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.name = name

    def clicked_on(self, x, y):
        return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2

    def move(self, event):
        self.destroy()
        self.create_rectangle(event.x, event.y, self.name)

    def destroy(self):
        canvas = self.algorator.canvas
        canvas.delete(self.text)
        canvas.delete(self.rect)

    def __str__(self):
        return "{}:".format(self.name)

