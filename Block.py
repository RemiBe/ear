"""
"""


import copy

from tkinter import *
import tkinter.ttk as ttk

from EditWindow import EditWindow


class Block(object):
    """Abstract class for elements of the canvas reprensented in
    a block and initialized in a separate window, e.g. Functions
    and Cases.

    Attributes:
        algorator: The root element, holding the main window, the canvas
            and all the other elements
        id: The unique id of this element
        name: The name of this element
        args: The {arg_name: arg_value} arguments of this element
        arrows: The arrows whose one end is self
        cancelled: When entering an empty name or hitting "Cancel" upon
            creation, this element is discarded.
    """

    def __init__(self, algorator, x, y, name=None):
        global i
        self.id = algorator.get_elem_id()
        self.cancelled = None
        self.algorator = algorator
        self.arrows = []
        self.name = name
        self.args = {}
        if name is None:
            self.edit()
        if self.cancelled is None:
            self.cancelled = False
            self.draw(x, y, self.name)

    def edit(self):
        ew = EditWindow(self.algorator.root, self, True)

    def move(self, event):
        self.destroy_draw()
        self.draw(event.x, event.y, self.name)
        for arrow in self.arrows:
            arrow.move(event)

    def destroy(self):
        print("destroying {}; arrows: {}".format(self.name, [a.name for a in self.arrows]))
        for arrow in copy.copy(self.arrows):
            arrow.destroy()
        self.arrows = []
        self.destroy_draw()

    def export(self, f_out):
        f_out.write("    - id: {}\n".format(self.id))
        f_out.write("      name: {}\n".format(self.name))
        f_out.write("      args:\n")
        for k, v in self.args.items():
            f_out.write("\t\t{}: {}\n".format(k, v))
        f_out.write("\tarrows: {}\n".format([a.id for a in self.arrows]))


