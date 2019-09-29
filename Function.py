"""
"""


from tkinter import *

from Block import Block
import Properties


class Function(Block):
    """
    Attributes:
        text: The id of the Canvas element displaying the function name
        rect: The id of the Canvas element boxing around the function name
        x1, y1, x2, y2: coordinates of the upper left and bottow right
            points of the rect
        cx, cy: coordinates of the center of the rect
    """

    def __init__(self, algorator, x, y, name=None):
        self.text = None
        self.rect = None
        Block.__init__(self, algorator, x, y, name=name)

    def draw(self, x, y, name):
        canvas = self.algorator.canvas

        self.text = canvas.create_text(x, y, text=name, tags="selected", fill="blue", font=Properties.FONT)
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

    def destroy(self):
        Block.destroy(self)
        canvas = self.algorator.canvas
        canvas.delete(self.text)
        canvas.delete(self.rect)

    def init_window_name(self):
        if self.name is None:
            return "Add a Function"
        else:
            return "Edit Function {}".format(self.name)

    def export(self, f_out):
        Block.export(self, f_out)
        f_out.write("\tcx: {}\n".format(self.cx))
        f_out.write("\tcy: {}\n".format(self.cy))

    def __str__(self):
        return "{}:".format(self.name)

