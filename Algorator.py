"""

,----------------------------------------------,
|                                              |
| ,----------, ,------,  ,-------,  ,--------, |
| | Function | | Case |  | Arrow |  | Remove | |
| '----------' '------'  '-------'  '--------' |
|                                              |
| ,------------------------------------------, |
| | Canvas                                   | |
| |        start                             | |
| |          |                               | |
| |          v                               | |
| |       ,-----,                            | |
| |       | foo |<------------,              | |
| |       '-----'             |              | |
| |          |                |              | |
| |          v                |              | |
| |          ^                |              | |
| |        /   \           ,-----,           | |
| |      < case  >-------> | bar |           | |
| |        \   /           '-----'           | |
| |          v                               | |
| |          |                               | |
| |          v                               | |
| |       ,-----,                            | |
| |       | baz |---> end                    | |
| |       '-----'                            | |
| |                                          | |
| '------------------------------------------' |
'----------------------------------------------'

* Clicking on Function enables to create a function on the canvas.
  Clicking once again disables it.
* Clicking on Case enables to create a function on the canvas.
  Clicking once again disables it.
* Clicking on Arrow enables to click on two functions on the canvas
  to link them with an arrow.
* Clicking on Remove enables to click on a function or an arrow on the
  canvas to remove it.
  Removing a function removes the arrows pointing at it.

TODO
* Import/Export diagrams
* Position "Add Function window" next to root window
* <Down> does not work yet
* Enable to remove an argument.
* Editing an arrow and saving with an empty name removes the arrow,
  printing a message before doing it.
* Do not draw the arrow inside the text
* Scrollbar in the canvas
* undo/redo
o Identify arcs to choose which condition leads to which function
o Draw arrow head
o Start and End blocks.
x Losange/circle for case -> would be too big
x Use arcs instead of lines for arrows to specify loops -> loops are not allowed

Possible improvements
* Work on window size, colors
* Open function parameters in split mode
"""


__author__ = "Rémi Barat"
__version__ = "1.0"


from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from Arrow import Arrow
from Case import Case
from Function import Function
import Properties


STATE_FUNC = "function_state"
STATE_CASE = "case_state"
STATE_ARROW = "arrow_state"
STATE_RM = "remove_state"


class Algorator(object):
    """
    Attributes
        root: The Tkinter root window
        mainframe: The main frame of the root window
        state: Defines whether we should add an Element on the canvas
            and its type, or whether we should remove an Element
        buttons: All the buttons of the root window
        canvas: Where to draw the algorithm
        functions: The Functions created
        cases: The Cases created
        arrows: The Arrows created
        selected: The last element on which the user clicked
        moving: Whether the user is moving the selected element
        start: In Arrow state, remembers the last clicked element
    """

    def __init__(self):
        self.root = Tk()
        self.root.title("Algorator - An Algorithm Creator")

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Buttons
        self.state = None
        fbutton = ttk.Button(self.mainframe, text="Function", command=lambda: self.change_state(STATE_FUNC))
        cbutton = ttk.Button(self.mainframe, text="Case", command=lambda: self.change_state(STATE_CASE))
        abutton = ttk.Button(self.mainframe, text="Arrow", command=lambda: self.change_state(STATE_ARROW))
        rbutton = ttk.Button(self.mainframe, text="Remove", command=lambda: self.change_state(STATE_RM))
        ibutton = ttk.Button(self.mainframe, text="Import", command=self.import_event)
        ebutton = ttk.Button(self.mainframe, text="Export", command=self.export_event)
        fbutton.grid(column=1, row=1)
        cbutton.grid(column=2, row=1)
        abutton.grid(column=3, row=1)
        rbutton.grid(column=4, row=1)
        ibutton.grid(column=5, row=1)
        ebutton.grid(column=6, row=1)
        self.buttons = {
                STATE_FUNC: fbutton,
                STATE_CASE: cbutton,
                STATE_ARROW: abutton,
                STATE_RM: rbutton,
                "import": ibutton,
                "export": ebutton,
        }

        # Canvas
        self.canvas = Canvas(self.mainframe, width=600, height=600, bg="grey") # TODO the mainframe should be grey
        self.canvas.grid(column=1, row=2, columnspan=len(self.buttons))
        self.canvas.bind("<Button-1>", self.register_position)
        self.canvas.bind("<B1-Motion>", self.hold_click)
        self.canvas.bind("<ButtonRelease-1>", self.simple_click)
        self.functions = []
        self.cases = []
        self.arrows = []
        self.start = None

        # Display
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Create start and end blocks
        d = 30
        start_f = Function(self, Properties.WINDOW_WIDTH / 2, d, name="start")
        end_f = Function(self, Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT - d, name="end")
        self.functions += [start_f, end_f]

        self.root.mainloop()

    def change_state(self, new_state):
        for button in self.buttons.values():
            button.state(["!pressed"])
        if self.state == new_state:
            self.state = None
        else:
            self.state = new_state
            self.buttons[new_state].state(["pressed"])
        print(self.state)

    def register_position(self, event):
        print("registered position: start is {}".format(self.start))
        self.moving = False
        self.selected = None
        self.selected_l = None
        for f in self.functions:
            if f.clicked_on(event.x, event.y):
                self.select(f, self.functions)
                return
        for c in self.cases:
            if c.clicked_on(event.x, event.y):
                self.select(c, self.cases)
                return
        for a in self.arrows:
            if a.clicked_on(event.x, event.y):
                self.select(a, self.arrows)
                return

    def select(self, elem, elem_lst):
        if self.start is not None and self.start == self.selected:
            self.selected = None
            self.selected_l = None
        else:
            self.selected = elem
            self.selected_l = elem_lst

    def simple_click(self, event):
        """If clicked on an empty space: add a function/case/arrow,
        Else if in state "remove", remove the function/case/arrow,
        Else edit the function/case.
        """
        print("simple_click: selected is {}, moving is {}".format(self.selected, self.moving))
        if self.selected is None:
            if self.state == STATE_FUNC:
                f = Function(self, event.x, event.y)
                if not f.cancelled:
                    self.functions.append(f)
            elif self.state == STATE_CASE:
                c = Case(self, event.x, event.y)
                if not c.cancelled:
                    self.cases.append(c)
        else:
            if self.state == STATE_RM and not self.moving:
                self.selected.destroy()
                self.selected_l.remove(self.selected)
            elif self.state == STATE_ARROW:
                if self.start is None:
                    self.start = self.selected
                else:
                    a = Arrow(self, self.start, self.selected)
                    self.arrows.append(a)
                    self.start = None
            elif not self.moving:
                self.selected.edit()
        self.moving = False

    def hold_click(self, event):
        if self.selected is not None and type(self.selected) != Arrow:
            self.moving = True
            self.selected.move(event)

    def import_event(self):
        filename = filedialog.askopenfilename()
        print("importing " + filename)

    def export_event(self):
        filename = filedialog.asksaveasfilename()

if __name__ == "__main__":
    algorator = Algorator()


