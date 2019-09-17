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
            self.functions.append(Function(self.canvas, x, y))
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

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.cx = x
        self.cy = y
        # initialize the function
        w = Tk()
        label = Label(w, text="Add a new Function")
        label.pack()
        entry = Entry(w, width=30)
        entry.pack()
        close_button = Button(w, text="Save", command=lambda: self.get_name(w, entry))
        close_button.pack()
        cancel_button = Button(w, text="Cancel", command=w.quit)
        cancel_button.pack()

        print("1 " + entry.get())

        # create the rectangle
        self.name = "test"
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

    def get_name(self, w, entry):
        print("2 " + entry.get())
        w.quit()
        return entry.get()


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

