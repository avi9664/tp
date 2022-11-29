class Button:
    def __init__(self, value, w, h, function, unfocused='AntiqueWhite3', 
        focused='AntiqueWhite2', textColor='black'):
        self.w = w
        self.h = h
        self.value = value
        self.function = function
        self.colorSet = [unfocused, focused]
        self.textColor = textColor
        self.isFocused = False
    
    def mouseHover(self):
        self.isFocused = True

    def redraw(self, canvas, x, y):
        x0 = x - self.w/2
        y0 = y
        x1 = x + self.w/2
        y1 = y + self.h
        color = self.colorSet[1] if self.isFocused else self.colorSet[0]
        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        cx = (x1 + x0)/2
        cy = (y1 + y0)/2
        canvas.create_text(cx, cy, text=self.value, fill=self.textColor, font='Arial 16')