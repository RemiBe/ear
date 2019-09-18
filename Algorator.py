"""
"""


__author__ = "Rémi Barat"
__version__ = "1.0"


from tkinter import *


l = 1000
h = 800

STATE_FUNC = "function"
STATE_CASE = "case"
STATE_RM = "remove"

class Algorator(object):

    def __init__(self):
        window = Tk()
        self.window = window

        # the buttons
        self.buttons = {
            "f": Button(window, text="Function", command=self.state_function),
            "c": Button(window, text="Case", command=self.state_case),
            "r": Button(window, text="Remove", command=self.state_remove),
        }
        for button in self.buttons.values():
            button.pack()
        self.state = None

        # the canvas
        canvas = Canvas(window, width=l, height=h, bg="yellow")
        canvas.focus_set()
        canvas.bind("<Button-1>", self.click_canvas)
        canvas.pack()
        self.canvas = canvas

        # the functions
        self.functions = []

        # the arrow
        self.start = None
        self.arrows = []

        window.mainloop()

    def reset_buttons(self):
        for button in self.buttons.values():
            button.relief = RAISED # TODO

    def state_function(self):
        self.reset_buttons()
        if self.state != STATE_FUNC:
            self.state = STATE_FUNC
            self.buttons["f"].relief = SUNKEN # TODO
        else:
            self.state = None

    def state_case(self):
        self.reset_buttons()
        if self.state != STATE_CASE:
            self.state = STATE_CASE
            self.start = None
        else:
            self.state = None

    def state_remove(self):
        self.reset_buttons()
        if self.state != STATE_RM:
            self.state = STATE_RM
        else:
            self.state = None

    def click_canvas(self, event):
        x = event.x
        y = event.y
        if self.state == STATE_FUNC:
            self.functions.append(Function(self, x, y))
        elif self.state == STATE_CASE:
            for fct in self.functions:
                if fct.clicked_on(x, y):
                    if self.start == None:
                        self.start = fct
                    else:
                        self.arrows.append(Arrow(self.canvas, self.start, fct))
                        self.start = None
                    break
        elif self.state == STATE_RM:
            for element in self.functions + self.arrows:
                if element.clicked_on(x, y):
                    element.destroy()
                    break


class Function(object):

    def __init__(self, algorator, x, y):
        canvas = algorator.canvas
        self.canvas = canvas
        self.cx = x
        self.cy = y
        # initialize the function
        self.name = None
        fd = FunctionDefinition(algorator.window, self)
#        algorator.window.wait_window(fd)

        # create the rectangle
        self.text = canvas.create_text(x, y, text=self.name, font="Arial 16", fill="blue")
        x1, y1, x2, y2 = canvas.bbox(self.text)
        self.rect = canvas.create_rectangle(x1, y1, x2, y2)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        # ask for the function parameters
        # create a text element
        # create a rectangle around the text

    def clicked_on(self, x, y):
        """Returns whether (x, y) is in this Function rectangle.
        """
        return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2

    def destroy(self):
        """Deletes itself from the algorator canvas.
        """
        self.canvas.delete(self.text)
        self.canvas.delete(self.rect)


class FunctionDefinition(Toplevel):

    def __init__(self, parent, function):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.title = "Add a new Function"
        self.parent = parent
        self.function = function

        self.set_body()
        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.close)

        self.initial_focus.focus_set()
        self.wait_window(self)

    def set_body(self):
        body = Frame(self)
        self.initial_focus = body
        body.pack()

        self.bind("<Return>", self.save)
        self.bind("<Escape>", self.close)

        # Function name
        self.entry = Entry(body, width=30)
        self.entry.pack()

        # Function argument
        close_button = Button(body, text="Save", command=self.save)
        close_button.pack()
        cancel_button = Button(body, text="Cancel", command=self.close)
        cancel_button.pack()


    def close(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def save(self, event=None):
        name = self.entry.get()
        self.function.name = name
        self.close()


class Arrow(object):

    def __init__(self, canvas, fct_start, fct_end):
        self.canvas = canvas
        self.line = canvas.create_line(fct_start.cx, fct_start.cy, fct_end.cx, fct_end.cy)

    def clicked_on(self, x, y):
        return False # TODO

    def destroy(self):
        self.canvas.delete(self.line)

if __name__ == "__main__":
    Algorator()

