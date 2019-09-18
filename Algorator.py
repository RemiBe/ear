"""


TODO:
    * import/export
    * function default arguments
    * move functions
    * arrow names and arguments
    * edit functions
    * edit arrow names and arguments
    * removing a function removes the arrows pointing at it
    * undo, redo
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
            for fct in self.functions:
                if fct.clicked_on(x, y):
                    fct.edit()
                    return
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
        self.algorator = algorator
        canvas = algorator.canvas
        self.cx = x
        self.cy = y
        # initialize the function
        self.name = None
        self.args = {}
        fd = FunctionDefinition(algorator.window, self)
#        algorator.window.wait_window(fd)

        self.create_text()
        self.create_rectangle()

    def clicked_on(self, x, y):
        """Returns whether (x, y) is in this Function rectangle.
        """
        return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2

    def destroy(self):
        """Deletes itself from the algorator canvas.
        """
        canvas = self.algorator.canvas
        canvas.delete(self.text)
        canvas.delete(self.rect)

    def create_text(self):
        canvas = self.algorator.canvas
        self.text = canvas.create_text(self.cx, self.cy, text=self.name, font="Arial 16", fill="blue")

    def create_rectangle(self):
        canvas = self.algorator.canvas
        x1, y1, x2, y2 = canvas.bbox(self.text)
        self.rect = canvas.create_rectangle(x1, y1, x2, y2)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def edit(self):
        canvas = self.algorator.canvas
        canvas.delete(self.text)
        canvas.delete(self.rect)
        fd = FunctionDefinition(self.algorator.window, self)
        self.create_text()
        self.create_rectangle()


class FunctionDefinition(Toplevel):

    def __init__(self, parent, function):
        # TODO should be impossible to add a new function.
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.title = "Add a new Function"
        self.parent = parent
        self.function = function

        self.set_body(function)
        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.close)

        self.initial_focus.focus_set()
        self.wait_window(self)

    def set_body(self, function=None):
        body = Frame(self)
        self.initial_focus = body
        body.pack()

        self.bind("<Return>", self.save)
        self.bind("<Escape>", self.close)
        self.bind("<Down>", lambda: self.add_argument(body))

        # Function name
        name = None
        if function != None and function.name != None:
            name = StringVar()
            name.set(function.name)
        entry = Entry(body, textvariable=name, width=30)
        entry.pack()
        entry.focus_set()
        self.entries = [entry]

        if function != None:
            for name, value in function.args.items():
                print("1 " + name + " " + value)
                self.add_argument(body, default_name=name, default_value=value)

        # Buttons
        add_arg_button = Button(body, text="Add argument", command=lambda: self.add_argument(body))
        add_arg_button.pack()
        close_button = Button(body, text="Save", command=self.save)
        close_button.pack()
        cancel_button = Button(body, text="Cancel", command=self.close)
        cancel_button.pack()

    def add_argument(self, body, default_name=None, default_value=None):
        name = Entry(body, textvariable=default_name, width=30) # TODO the default value is not inserted?!
        value = Entry(body, textvariable=default_value, width=30)
        name.pack()
        value.pack()
        name.focus_set()
        self.entries.append(name)
        self.entries.append(value)

    def close(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def save(self, event=None):
        self.function.name = self.entries[0].get()
        i = 1
        for i in range(1, len(self.entries), 2):
            arg_name = self.entries[i].get()
            if arg_name:
                arg_value = self.entries[i+1].get()
                self.function.args[arg_name] = arg_value
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

