

from Case import Case
from EditWindow import EditWindow


class Arrow(object):

    def __init__(self, algorator, start, to):
        self.algorator = algorator
        self.start = start
        self.to = to
        self.name = self.get_default_name()
        start.arrows.append(self)
        to.arrows.append(self)
        self.draw(start, to)
        self.saved = True

    def get_default_name(self):
        if type(self.start) != Case:
            return None
        if self.start.arrows and self.start.arrows[0].name == "True":
            return "False"
        return "True"

    def init_window_name(self):
        return "Edit Condition"

    def draw(self, start, to):
        canvas = self.algorator.canvas
        self.line = canvas.create_line(
                start.cx,
                start.cy,
                to.cx,
                to.cy)
        x = (start.cx + to.cx) / 2
        y = (start.cy + to.cy) / 2
        if self.name is not None:
            self.text = canvas.create_text(x, y, text=self.name, tags="selected", fill="black")
            x1, y1, x2, y2 = canvas.bbox(self.text)
            self.rect = canvas.create_rectangle(x1, y1, x2, y2, tags="selected")

    def draw_arrow(self):
        pass

    def clicked_on(self, x, y):
        if self.start.cx < self.to.cx:
            x1 = self.start.cx
            x2 = self.to.cx
        else:
            x1 = self.to.cx
            x2 = self.start.cx
        if self.start.cy < self.to.cy:
            y1 = self.start.cy
            y2 = self.to.cy
        else:
            y1 = self.to.cy
            y2 = self.start.cy
        return x >= x1 and x <= x2 and y >= y1 and y <= y2

    def edit(self):
        if self.name is not None:
            ew = EditWindow(self.algorator.root, self, True)

    def move(self, event):
        self.destroy()
        self.draw(self.start, self.to)

    def destroy(self):
        canvas = self.algorator.canvas
        canvas.delete(self.line)
        if self.name is not None:
            canvas.delete(self.text)
            canvas.delete(self.rect)

    def get_side(ax, ay, bx, by):
        """     ,------------,
                | A (ax, ay) |   v
                '------------'   | dy
                      /          ^
                     /
              ,------------,
              | B (bx, by) |
              '------------'
        """
        dy = 5
        if ay < by - dy:
            return "Down"
        elif ay > by + dy:
            return "Up"
        else:
            return "Left" if ax > ay else "Right"


