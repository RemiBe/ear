"""
"""


from tkinter import *
import tkinter.ttk as ttk


class Block(object):
    """
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
        ew = EditWindow(self.algorator.root, self)

    def move(self, event):
        self.destroy()
        self.draw(event.x, event.y, self.name)
        for arrow in self.arrows:
            arrow.move(event)

    def destroy(self):
        for arrow in self.arrows:
            arrow.destroy()

class EditWindow(Toplevel):

    def __init__(self, parent, element):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.title = "Add a new Function"
        self.parent = parent
        self.element = element

        self.set_body(element)
#        if not self.initial_focus:
#            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.initial_focus.focus_set()
        self.wait_window(self)

    def set_body(self, element):
        self.rows = 1

        body = Frame(self)
        self.initial_focus = body
        body.pack()

        # Bindings
        self.bind("<Return>", self.save)
        self.bind("<Escape>", self.cancel)
        self.bind("<Down>", lambda: self.add_argument(body)) # Doesn't work

        # Block Name
        name = Label(body, text="Name")
        name.grid(column=1, row=1)
        name = None
        if element.name is not None:
            name = StringVar()
            name.set(element.name)
        name_entry = Entry(body, textvariable=name)
        name_entry.grid(column=2, row=1, columnspan=2, sticky=(W, E))
        self.rows += 1
        name_entry.focus_set()
        self.entries = [name_entry]

        # Block arguments
        for name, value in element.args.items():
            self.add_argument(body, last=False, default_name=name, default_value=value)

        self.add_buttons(body)


    def add_argument(self, body, last=True, default_name=None, default_value=None):
        if last:
            self.clear_buttons()

        dname = None
        if default_name is not None:
            dname = StringVar()
            dname.set(default_name)
        dvalue = None
        if default_value is not None:
            dvalue = StringVar()
            dvalue.set(default_value)
        name = Entry(body, textvariable=dname)
        value = Entry(body, textvariable=dvalue)
        name.grid(column=2, row=self.rows)
        value.grid(column=3, row=self.rows)
        self.rows += 1
        name.focus_set()
        self.entries.append(name)
        self.entries.append(value)

        if last:
            self.add_buttons(body)

    def clear_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.rows -= 2

    def add_buttons(self, body):
        # Buttons
        add_button = ttk.Button(body, text="Add an Argument", command=lambda: self.add_argument(body))
        save_button = ttk.Button(body, text="Save", command=self.save)
        cancel_button = ttk.Button(body, text="Cancel", command=self.cancel)
        add_button.grid(column=1, row=self.rows)
        self.rows += 1
        save_button.grid(column=2, row=self.rows)
        cancel_button.grid(column=3, row=self.rows)
        self.rows += 1
        self.buttons = [add_button, save_button, cancel_button]

    def save(self, event=None):
        self.element.name = self.entries[0].get()
        if not self.element.name:
            self.cancel()
            return
        for i in range(1, len(self.entries), 2):
            arg_name = self.entries[i].get()
            if arg_name:
                arg_value = self.entries[i+1].get()
                self.element.args[arg_name] = arg_value
        self.close()

    def cancel(self):
        if self.element.cancelled is None:
            self.element.cancelled = True
        self.close()

    def close(self):
        self.parent.focus_set()
        self.destroy()


