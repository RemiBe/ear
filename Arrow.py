
import math

from Case import Case
from EditWindow import EditWindow
import Properties


def square(x):
    return x*x


def get_arrow_head(a, b, c, d):
    # A(a,b) --> B(c,d)
    # l is the height of the arrow head and of its width:
    #        B
    #        ^      ^
    #       /|\     |
    #      / | \    | l (input)
    #   P0+--+--+P1 v
    #        |M     ^
    #        |      | L
    #        |      |
    #        +A     v
    #     <----->
    #        l
    # L = AB - l
    # M(p,q)
    # mu is the director coef of (AB)
    # nu is the director coef of the perpendicular to (AB)
    # We look for P0(x0,y0) and P1(x1,y1)
    l = 10
    if a == c:
        # Aligned vertically
        y = d - l if d > b else d + l
        return c, d, c-l/2, y, c+l/2, y
    elif b == d:
        # Aligned horizontally
        x = c - l if c > a else c + l
        return c, d, x, d-l/2, x, d+l/2

    L = math.sqrt(square(d-b) + square(c-a)) - l
    mu = (d-b) / (c-a)
    p = (square(L) + - square(l) - square(a) + square(b) + square(c) + square(d) + 2*mu*a*(d-b) - 2*b*d) / (2*(mu*(d-b) + (c-a)))
    q = mu*(p-a) + b
    if d != b:
        nu = -1 / mu

    A = 1
    B = -2*p
    C = square(p) - square(l/2) / (square(nu)+1)

    delta = square(B) - 4*A*C

    x0 = (-B -math.sqrt(delta)) / (2*A)
    x1 = (-B +math.sqrt(delta)) / (2*A)

    y0 = nu*(x0-p) + q
    y1 = nu*(x1-p) + q

    return c, d, x0, y0, x1, y1


class Arrow(object):
    """
    Attributes:
        algorator: The root element, holding the main window, the canvas
            and all the other elements
        id: The unique id of this element
        name: The name of this element
        args: The {arg_name: arg_value} arguments of this element
        start: The Block from which the arrow starts
        to: The Block at which the arrow points
        text: The id of the Canvas element displaying the function name
        line: The id of the Canvas element displaying the arrow line
        head: The id of the Canvas element displaying the arrow head
    """

    def __init__(self, algorator, start, to):
        self.id = algorator.get_elem_id()
        self.algorator = algorator
        self.start = start
        self.to = to
        self.name = self.get_default_name()
        start.arrows.append(self)
        to.arrows.append(self)
        self.draw(start, to)

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
            self.text = canvas.create_text(x, y, text=self.name, tags="selected", fill="black", font=Properties.FONT)
            x1, y1, x2, y2 = canvas.bbox(self.text)
            self.rect = canvas.create_rectangle(x1, y1, x2, y2, tags="selected")

    def clicked_on(self, x, y):
        d = 10 # enable 3 pixels around the arrow
        y1 = min(self.start.cy, self.to.cy)
        y2 = max(self.start.cy, self.to.cy)
        if self.start.cx == self.to.cx:
            cx = self.start.cx
            return x >= cx - d and x <= cx + d and y >= y1 and y <= y2
        else:
            # TODO use a circle to select the arrow
            x1 = min(self.start.cx, self.to.cx)
            x2 = max(self.start.cx, self.to.cx)
            a = (y2 - y1) / (x2 - x1)
            yt = a*(x-x1) + y1
            return y >= yt - d and y <= yt + d

    def edit(self):
        if self.name is not None:
            ew = EditWindow(self.algorator.root, self, True)

    def move(self, event):
        self.destroy_draw()
        self.draw(self.start, self.to)

    def destroy(self):
        print("destroying {}; start={}, to={}".format(self.name, self.start.name, self.to.name))
        self.start.arrows.remove(self)
        self.to.arrows.remove(self)
        self.algorator.arrows.remove(self)
        self.destroy_draw()

    def destroy_draw(self):
        canvas = self.algorator.canvas
        canvas.delete(self.line)
        canvas.delete(self.head)
        if self.name is not None:
            canvas.delete(self.text)
            canvas.delete(self.rect)

    def export(self, f_out):
        f_out.write("    - id: {}\n".format(self.id))
        f_out.write("      name: {}\n".format(self.name))
        f_out.write("      start: {}\n".format(self.start.id))
        f_out.write("      to: {}\n".format(self.to.id))

    ### Drawing an arrow ###

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
        self.head = canvas.create_polygon(*get_arrow_head(start_cx, start_cy, to_cx, to_cy))

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


