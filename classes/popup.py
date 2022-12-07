from cmu_112_graphics import *
from classes.button import Button
from classes.pin import GuessPin
from functions.drawShapes import drawPin
from functions.strArrayStuff import formatLines

# popup dialog box

class PopUp:
    def __init__(self, app, content, heading, bg=True):
        self.content = content
        self.heading = heading
        self.fontSize = 16
        self.headingSize = 24
        self.m = self.headingSize
        self.w = self.m * 2 + (self.fontSize - 6) * app.lineWidth
        self.heights = self.measureHeight(self.content)

        spacing = len(self.content) * 5
        headingSpacing = self.headingSize + 15
        self.h = sum(self.heights) + spacing + headingSpacing + self.m * 2
        self.cx = app.width/2
        self.cy = app.height/2
        self.visible = True

    # draw map in background
    def drawBg(self, app, canvas):
        bgLayer = Image.new('RGBA', (app.width, app.height), '#666')

        # https://www.geeksforgeeks.org/python-pil-putalpha-method/
        bgLayer.putalpha(200)
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(bgLayer))
    
    # calculate height of the popup
    def measureHeight(self, L):
        if L == []:
            return []
        elif isinstance(L[0], list):
            return [max(self.measureHeight(L[0]))] + self.measureHeight(L[1:])
        elif isinstance(L[0], Button):
            return [L[0].h] + self.measureHeight(L[1:])
        elif isinstance(L[0], str):
            if L[0] == 'PIN':
                return [40] + self.measureHeight(L[1:])
            h = [len(formatLines(L[0])) * (self.fontSize + 5)] + self.measureHeight(L[1:])
            return h
        elif isinstance(L[0], int) or isinstance(L[0], float):
            return [self.fontSize] + self.measureHeight(L[1:])
    
    def drawPopUp(self, app, canvas):
        x0 = self.cx - self.w/2
        y0 = self.cy - self.h/2
        x1 = self.cx + self.w/2
        y1 = self.cy + self.h/2
        canvas.create_rectangle(x0, y0, x1, y1, fill='white')
    
    # helper for drawContent (below)
    def drawContentHelper(self, app, canvas, item, startX, startY):
        if isinstance(item, Button):
            # for mousePressed
            item.x, item.y = startX, startY + item.h/2
            item.redraw(canvas, startX, startY + item.h/2)
            return None
        elif isinstance(item, str):
            if item == 'PIN':
                drawPin(canvas, '#F80E55', startX, startY + 40)
            else:
                font = self.fontSize
                # heading
                if item[0] == '*':
                    font = self.headingSize
                    item = item[1:-1]
                for line in formatLines(item):
                    canvas.create_text(startX, startY, text=line, 
                        font=f'Arial {font}', anchor='n')
                    startY += font + 5
            return None

    # draw things inside popup at the right heights
    def drawContent(self, app, canvas):
        startY = self.cy - self.h/2 + self.m
        startX = self.cx
        canvas.create_text(startX, startY, text=self.heading, 
                    font=f'Arial {self.headingSize} bold', anchor='n')
        startY += self.headingSize + 15
        for i in range(len(self.content)):
            startX = self.cx
            item = self.content[i]
            if isinstance(item, list):
                spacing = 30
                startX -= len(self.content)//2 * spacing/2
                for j in range(len(item)):
                    self.drawContentHelper(app, canvas, item[j], startX, startY)
                    startX += spacing
            else:
                self.drawContentHelper(app, canvas, item, startX, startY)
            startY += self.heights[i] + 5


    def redraw(self, app, canvas):
        self.drawBg(app, canvas)
        self.drawPopUp(app, canvas)
        self.drawContent(app, canvas)
