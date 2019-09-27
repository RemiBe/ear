


class Arrow(object):

    def __init__(self, algorator, start, to):
        self.algorator = algorator
        self.start = start
        self.to = to
        start.arrows.append(self)
        to.arrows.append(self)
        self.draw(start, to)
        self.saved = True

    def draw(self, start, to):
        self.line = self.algorator.canvas.create_line(
                start.cx,
                start.cy,
                to.cx,
                to.cy)

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

    def move(self, event):
        self.destroy()
        self.draw(self.start, self.to)

    def destroy(self):
        canvas = self.algorator.canvas
        canvas.delete(self.line)


