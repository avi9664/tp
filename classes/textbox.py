import string
from cmu_112_graphics import *
class TextBox:
    def __init__(self, label):
        self.value = ''
        self.selected = True
        self.label = label
        self.margin = 10

    def redraw(self, app, canvas, x0, y0, w):
        m = self.margin
        h = app.fontSize + 2 * m
        x1 = x0 + w
        y1 = y0 + h
        canvas.create_rectangle(x0, y0, x1, y1, 
            fill=app.bg, width=3, outline=app.text)
        canvas.create_text(x0 + m, y0 + m, text=self.value + '|', 
        font = 'Helvetica ' + str(app.fontSize), fill=app.text,
        anchor='nw')

    def keyPressed(self, app, event):
        exceptions = [' ', '.', '-', '\'', '_', 'Backspace']
        key = ' ' if event.key == 'Space' else event.key
        if (key in string.ascii_letters or key in exceptions):
            if app.searchBox.selected == True:
                if key == 'Backspace':
                    app.searchBox.value = app.searchBox.value[:-1]
                else:
                    app.searchBox.value = app.searchBox.value + key