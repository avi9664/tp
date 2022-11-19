# GuessPin
# properties:
# map coordinates ✅
# distance from actual location + angle ✅
# calculate distance from actual location ✅
# guess # ✅
# color ✅
# calculate color based on distance from actual location

# methods:
# redrawPin
# redrawClues (an arrow pointing in the direction of the mystery location, and some text hinting at how far away it is)

from cmu_112_graphics import *
from functions.convertCoords import toMapCoords, toCanvasCoords
import math
from functions.drawShapes import drawPin
import numpy as np

def findDistance(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    # np.arctan2: https://numpy.org/doc/stable/reference/generated/numpy.arctan2.html
    return math.sqrt(dx**2 + dy**2), np.arctan2(dy,dx) * 180/np.pi

assert(findDistance(0, 0, 0, 1) == (1.0, 90.0))
assert(findDistance(0, 0, 1, 0) == (1.0, 0.0))
print('okay, findDistance() works!')

class GuessPin:
    def __init__(self, app, canvasCoords, guessNum):
        self.mapCoords = toMapCoords(canvasCoords, app.bounds, app.width, app.height, 
            flattened=False)

        # assuming answer is a tuple or a list for the centroid
        # answerLong = answer[0]
        # answerLat = answer[1]
        # self.distance, self.angle = findDistance(self.mapCoords[0], self.mapCoords[1],
        #                                          answer[0], answer[1])
        self.num = guessNum
        self.color = 'red' # change later
    def redrawPin(self, app, canvas):
        canvasCoords = toCanvasCoords(self.mapCoords, app.bounds, app.width, app.height)
        drawPin(canvas,'red', canvasCoords[0], canvasCoords[1])
        
        
        
        


