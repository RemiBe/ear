"""
"""


from tkinter import *
import tkinter.ttk as ttk

from EditWindow import EditWindow


class Block(object):
    """Abstract class for elements of the canvas reprensented in
    a block and initialized in a separate window, e.g. Functions
    and Cases.
    """

    def __init__(self, algorator, x, y):
        global i
        self.cancelled = None
        self.algorator = algorator
        self.arrows = []
        self.name = None
        self.args = {}
        self.edit()
        if self.cancelled is None:
            self.cancelled = False
            self.draw(x, y, self.name)

    def edit(self):
        ew = EditWindow(self.algorator.root, self, True)

    def move(self, event):
        self.destroy()
        self.draw(event.x, event.y, self.name)
        for arrow in self.arrows:
            arrow.move(event)

    def destroy(self):
        for arrow in self.arrows:
            arrow.destroy()

