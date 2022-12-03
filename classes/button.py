from functions.strArrayStuff import formatLines
from functions.mouseInBounds import mouseInBounds
class Button:
    def __init__(self, value, function, unfocused='AntiqueWhite3', 
        focused='AntiqueWhite2', textColor='black'):
        self.fontSize = 16
        self.m = self.fontSize
        self.w = len(value) * self.fontSize + 2 * self.m
        self.h = len(formatLines(value)) * self.fontSize + 2 * self.m
        self.value = value
        self.function = function
        self.colorSet = [unfocused, focused]
        self.textColor = textColor
        self.isFocused = False
        self.x, self.y = 0, 0
    
    def mouseHover(self):
        self.isFocused = True
        
    def mousePressed(self, app):
        self.function(app)

    def mouseNearby(self, mouseX, mouseY):
        return mouseInBounds(self.x, self.y, self.w, self.h, mouseX, mouseY)

    def redraw(self, canvas, x, y):
        x0 = x - self.w/2
        y0 = y - self.h/2
        x1 = x + self.w/2
        y1 = y + self.h/2
        color = self.colorSet[1] if self.isFocused else self.colorSet[0]
        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        cx = (x1 + x0)/2
        cy = (y1 + y0)/2
        canvas.create_text(cx, cy, text=self.value, fill=self.textColor, font='Arial 16')