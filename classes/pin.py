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
    dx = (x1 - x0) * 288200
    dy = (y1 - y0) * 364000
    # np.arctan2: https://numpy.org/doc/stable/reference/generated/numpy.arctan2.html
    return math.sqrt(dx**2 + dy**2), np.arctan2(dy,dx) * 180/np.pi

class GuessPin:
    def __init__(self, app, canvasCoords, guessNum):
        self.mapCoords = toMapCoords(canvasCoords, app.bounds, app.width, app.height, 
            flattened=False)

        answerLong = app.answer[0]
        answerLat = app.answer[1]
        self.distance, self.angle = findDistance(self.mapCoords[:,0], self.mapCoords[:,1],
                                                 app.answer[0], app.answer[1])
        print(self.distance, self.angle)
        self.num = guessNum
        # 1 degree of latitude ~ 364000 ft ~ around 69 miles
        # 1000 ft = 0.0027 degrees of longitude
        # 1 degree of longitude ~ 288200 ft ~ 54.6 miles
        # 1000 ft = 0.0034 degrees of longitude

        # 10000, 1000, 100, 10
        # 4      3     2    1
        # 1                 0

        self.color = self.getColor(app) # change later
    
    def getColor(self, app, cStart='#EED86B', cEnd='#F80E55'):
        # https://www.geeksforgeeks.org/log-functions-python/

        # squash distance so that it's in between 0 and 1
        # find a better scale for this
        normalizedDist = 1 - (self.distance/1000)
        if normalizedDist < 0: normalizedDist = 0

        # hex to rgb from https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
        cStart = cStart[1:]
        cEnd = cEnd[1:]
        startRGB = list(int(cStart[i:i+2], 16) for i in (0, 2, 4))
        endRGB = list(int(cEnd[i:i+2], 16) for i in (0, 2, 4))

        r = (endRGB[0] - startRGB[0]) * normalizedDist + startRGB[0]
        g = (endRGB[1] - startRGB[1]) * normalizedDist + startRGB[1]
        b = (endRGB[2] - startRGB[2]) * normalizedDist + startRGB[2]

        # rgb to hex from https://www.codespeedy.com/convert-rgb-to-hex-color-code-in-python/
        mixedRGB = '#' + '%02x%02x%02x' % (int(r), int(g), int(b))
        print(mixedRGB)

        return mixedRGB

    def redrawPin(self, app, canvas):
        canvasCoords = toCanvasCoords(self.mapCoords, app.bounds, app.width, app.height)
        drawPin(canvas,self.color, canvasCoords[0], canvasCoords[1], str(self.num))
        
        
        
        


