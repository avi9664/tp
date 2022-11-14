from pyrosm import get_data
from pyrosm import OSM
from pyrosm.data import sources
from cmu_112_graphics import *
import string, random

# first task: dropdown
# bounding box for clicky
# type in stuff
# have words appear


def appStarted(app):
    app.bg = 'white'
    app.text = 'black'
    app.fontSize = 12
    app.textBoxes = []
    app.textBoxes.append(TextBox('choose a city', 12))
    app.textBoxSelected = 12
    app.sources = sorted(sources._all_sources)

# convert to binary search later
def searchSources(app, text):
    results = []
    if text == '':
        return []
    for name in app.sources:
        if text in name:
            results.append(name)
    return sorted(results[:5])

class TextBox:
    def __init__(self, label, boxId):
        self.value = ''
        self.selected = True
        self.label = label
        self.margin = 10
        self.id = boxId

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


def keyPressed(app, event):
    exceptions = [' ', '.', '-', '\'', 'Backspace']
    key = ' ' if event.key == 'Space' else event.key
    if (key in string.ascii_letters or key in exceptions):
        for box in app.textBoxes:
            if box.selected == True:
                if key == 'Backspace':
                    box.value = box.value[:-1]
                else:
                    box.value = box.value + key

def drawSearchResults(app, canvas):
    results = searchSources(app, app.textBoxes[0].value)
    num = len(results)
    margin = 10
    f = app.fontSize
    w = 700
    h = f + margin * 2
    startX, startY = 100, 100 + h
    for i in range(num):
        canvas.create_rectangle(startX, startY, startX + w, startY + h,
            outline='grey')
        canvas.create_text(startX + margin, startY + margin, text=results[i],
            font = 'Helvetica ' + str(app.fontSize), fill=app.text, anchor='nw')
        startY += h

def redrawAll(app, canvas):
    for box in app.textBoxes:
        box.redraw(app, canvas, 100, 100, 700)
        drawSearchResults(app, canvas)
    pass

def playGame():
    runApp(width=850, height=1100)


# fp = get_data('Berkeley')
# print(fp)
# osm = OSM(fp)
# buildings = osm.get_buildings()
# print(str(buildings.iloc[20]['geometry']))

############################
# main
############################

def main():
    playGame()

if __name__ == '__main__':
    main()