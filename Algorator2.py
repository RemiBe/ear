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
  Clicking once again disable it.
* Clicking on Case enables to create a function on the canvas.
  Clicking once again disable it.
* Clicking on Arrow enables to click on two functions on the canvas
  to link them with an arrow.
* Clicking on Remove enables to click on a function or an arrow on the
  canvas to remove it.
  Removing a function removes the arrows pointing at it.

Other functions:
* Be able to move a function
"""


__author__ = "Rémi Barat"
__version__ = "1.0"


from tkinter import *
from tkinter import ttk


STATE_FUNC = "function_state"
STATE_CASE = "case_state"
STATE_ARROW = "arrow_state"
STATE_RM = "remove_state"


class Algorator(object):
    """

    Clicking on a button changes the `state`.
    """

    def __init__(self):
        self.root = Tk()
        self.root.title("Algorator - An Algorithm Creator")

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # State
        self.state = None
        fbutton = ttk.Button(self.mainframe, text="Function", command=lambda: self.change_state(STATE_FUNC))
        cbutton = ttk.Button(self.mainframe, text="Case", command=lambda: self.change_state(STATE_CASE))
        abutton = ttk.Button(self.mainframe, text="Arrow", command=lambda: self.change_state(STATE_ARROW))
        rbutton = ttk.Button(self.mainframe, text="Remove", command=lambda: self.change_state(STATE_RM))
        fbutton.grid(column=1, row=1)
        cbutton.grid(column=2, row=1)
        abutton.grid(column=3, row=1)
        rbutton.grid(column=4, row=1)
        self.buttons = {
                STATE_FUNC: fbutton,
                STATE_CASE: cbutton,
                STATE_ARROW: abutton,
                STATE_RM: rbutton
        }

        # Display
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

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



if __name__ == "__main__":
    algorator = Algorator()


