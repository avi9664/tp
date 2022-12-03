from cmu_112_graphics import *
import math
import numpy as np
from functions.strArrayStuff import toCanvasCoords

def drawOval(canvas, cx, cy, r, fill, outline='white', width=2):
    x0 = cx - r
    y0 = cy - r
    x1 = cx + r
    y1 = cy + r
    canvas.create_oval(x0, y0, x1, y1, fill=fill, outline=outline, width=width)

def drawPin(canvas, color, x, y, text=None, outline='white'):
    r = 5
    needleWidth = 2
    h = y - r * 8
    canvas.create_polygon(x - needleWidth, h + 2*r, x, y, x + needleWidth,
                        h + 2*r, fill='white', outline='black', width=2)
    drawOval(canvas, x, h + r, r*2, color, outline=outline)
    if text != None:
        canvas.create_text(x, h + r, text=text, fill='white')

def angle(x0, y0, thetaInDegs, dist):
    theta = thetaInDegs * math.pi/180
    x1 = x0 + dist*math.cos(theta)
    y1 = y0 - dist*math.sin(theta)
    return x1, y1

# from animations pt 4 in 112 website
def getCachedPhotoImage(app, image):
    # stores a cached version of the PhotoImage in the PIL/Pillow image
    if ('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage


def renderMap(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, outline='', 
        fill='MistyRose4')
    scaledMap = app.scaleImage(app.map, 1)
    mapCenter = toCanvasCoords(np.array([[app.startLong, app.startLat]]), 
                app.bounds, app.width, app.height)
    cachedImage = getCachedPhotoImage(app, scaledMap)
    canvas.create_image(mapCenter[0], mapCenter[1], image=cachedImage)
    for pin in app.pins:
        pin.redraw(app, canvas)