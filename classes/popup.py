from cmu_112_graphics import *
from classes.button import Button
from classes.pin import GuessPin
from functions.drawShapes import drawPin
from functions.strArrayStuff import formatLines


class PopUp:
    def __init__(self, app, content, heading, bg=True):
        self.content = content
        self.heading = heading
        self.fontSize = 18
        self.headingSize = 24
        self.m = self.headingSize
        self.w = self.m * 2 + self.fontSize * 17
        self.heights = self.measureHeight(self.content)

        spacing = len(self.content) * 5
        headingSpacing = self.headingSize + 15
        self.h = sum(self.heights) + spacing + headingSpacing + self.m * 2
        self.cx = app.width/2
        self.cy = app.height/2


    def drawBg(self, app, canvas):
        # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        bgLayer = Image.new('RGBA', (app.width, app.height), '#666')

        # https://www.geeksforgeeks.org/python-pil-putalpha-method/
        bgLayer.putalpha(200)
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(bgLayer))
    
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
            h = [len(formatLines(L[0])) * (self.fontSize)] + self.measureHeight(L[1:])
            return h
    
    def drawPopUp(self, app, canvas):
        x0 = self.cx - self.w/2
        y0 = self.cy - self.h/2
        x1 = self.cx + self.w/2
        y1 = self.cy + self.h/2
        canvas.create_rectangle(x0, y0, x1, y1, fill='white')
    
    def drawContentHelper(self, app, canvas, item, startX, startY):
        if isinstance(item, Button):
            item.redraw(canvas, startX, startY)
        elif isinstance(item, str):
            if item == 'PIN':
                drawPin(canvas, 'red', startX, startY)
            else:
                canvas.create_text(startX, startY, text=item, 
                    font=f'Arial {self.fontSize}', anchor='n')
        elif isinstance(item, list):
            middle = len(item) // 2
            tempStartX = startX
            for i in range(middle,len(item)):
                self.drawContentHelper(app, canvas, item, tempStartX, startY)
                # placeholder that I won't change for now unless I'm drawing 3+ items on one line
                tempStartX += 10
            tempStartX = startX
            for i in range(0, middle):
                self.drawContentHelper(app, canvas, item, tempStartX, startY)
                tempStartX -= 10


    def drawContent(self, app, canvas):
        startY = self.cy - self.h/2 + self.m
        startX = self.cx
        canvas.create_text(startX, startY, text=self.heading, 
                    font=f'Arial {self.headingSize} bold', anchor='n')
        startY += self.headingSize + 15
        for i in range(len(self.content)):
            item = self.content[i]
            self.drawContentHelper(app, canvas, item, startX, startY)
            startY += self.heights[i] + 5



    def redraw(self, app, canvas):
        self.drawBg(app, canvas)
        self.drawPopUp(app, canvas)
        self.drawContent(app, canvas)
        pass
