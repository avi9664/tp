class Button:
    def __init__(self, x, y, w, h, function, unfocused, focused):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.function = function
        self.colorSet = [unfocused, focused]
        self.isFocused = False
    
    def mouseHover(self):
        self.isFocused = True

    def draw(self, canvas):
        x0 = self.x - self.w/2
        y0 = self.y - self.h/2
        x1 = self.x + self.w/2
        y1 = self.y - self.h/2
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color)