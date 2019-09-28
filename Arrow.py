

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
        self.draw_arrow(start, to)
        x = (start.cx + to.cx) / 2
        y = (start.cy + to.cy) / 2
        if self.name is not None:
            self.text = canvas.create_text(x, y, text=self.name, tags="selected", fill="black")
            x1, y1, x2, y2 = canvas.bbox(self.text)
            self.rect = canvas.create_rectangle(x1, y1, x2, y2, tags="selected")

    def draw_arrow(self, start, to):
        canvas = self.algorator.canvas
        side = self.get_side()
        if side == "Down":
            start_cx = start.cx
            start_cy = max(start.y1, start.y2)
            to_cx = to.cx
            to_cy = min(to.y1, to.y2)
        elif side == "Up":
            start_cx = start.cx
            start_cy = min(start.y1, start.y2)
            to_cx = to.cx
            to_cy = max(to.y1, to.y2)
        else:
            start_cy = start.cy
            to_cy = to.cy
            if side == "Left":
                start_cx = min(start.x1, start.x2)
                to_cx = max(to.x1, to.x2)
            else:
                start_cx = max(start.x1, start.x2)
                to_cx = min(to.x1, to.x2)
        self.line = canvas.create_line(start_cx, start_cy, to_cx, to_cy)

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

    def get_side(self):
        """
                                to.cx  start.cx
                    +---------------|--|---------------> x
                    |
                    |
        start_y_min -              ,-------,
                    |              | start |
        start_y_max -              '-------'
                    |                 /  here we return "Down"
                    |                /
           to_y_min |             ,----,
                    |             | to |
           to_y_max |             '----'
                    v y
        """
        start_y_max = max(self.start.y1, self.start.y2)
        start_y_min = min(self.start.y1, self.start.y2)
        to_y_max = max(self.to.y1, self.to.y2)
        to_y_min = min(self.to.y1, self.to.y2)
        if start_y_max < to_y_min:
            return "Down"
        elif start_y_min > to_y_max:
            return "Up"
        else:
            return "Left" if self.start.cx > self.to.cx else "Right"


