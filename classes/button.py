from functions.strArrayStuff import formatLines
from cmu_112_graphics import *
from functions.mouseInBounds import mouseInBounds
class Button:
    def __init__(self, value, function, x0=0, y0=0, customW=0, customH=0, 
        unfocused='#1E193E', focused='#F80E55', outline='', 
        textColor='#F7F6F7'):
        self.fontSize = 14
        self.m = self.fontSize
        self.w = len(value) * self.fontSize + 2 * self.m if customW == 0 else customW
        self.h = len(formatLines(value)) * self.fontSize + 2 * self.m if customH == 0 else customH
        self.value = value
        self.function = function
        self.colorSet = [unfocused, focused]
        self.outline = outline
        self.textColor = textColor
        self.isFocused = False
        self.x, self.y = x0 + self.w/2, y0 + self.h/2
    
    def mouseHover(self):
        self.isFocused = True
    
    # do button's function
    def mousePressed(self, app):
        self.function(app)

    def mouseNearby(self, mouseX, mouseY):
        return mouseInBounds(self.x, self.y, self.w, self.h, mouseX, mouseY)

    def redraw(self, canvas, x, y, anchor='center', cx=None):
        x0 = x - self.w/2
        y0 = y - self.h/2
        x1 = x + self.w/2
        y1 = y + self.h/2
        color = self.colorSet[1] if self.isFocused else self.colorSet[0]
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=self.outline)
        # for one little edgecase with the buttons in loadMode
        cx = (x1 + x0)/2 if cx == None else cx
        cy = (y1 + y0)/2
        canvas.create_text(cx, cy, text=self.value, fill=self.textColor,
        font='Arial 16', anchor=anchor)