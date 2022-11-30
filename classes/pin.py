# GuessPin
# properties:
# map coordinates ✅
# distance from actual location + angle ✅
# calculate distance from actual location ✅
# guess # ✅
# color ✅
# calculate color based on distance from actual location ✅

# methods:
# redrawPin ✅
# redrawClues (an arrow pointing in the direction of the mystery location, and some text hinting at how far away it is) ✅

from cmu_112_graphics import *
from functions.strArrayStuff import toMapCoords, toCanvasCoords, friendlyDistString
from functions.mouseInBounds import mouseInBounds
import math
from functions.drawShapes import drawPin, angle
import numpy as np

def findDistance(x0, y0, x1, y1):
    dx = (x1 - x0) * 288200
    dy = (y1 - y0) * 364000
    # math.atan2: https://www.geeksforgeeks.org/python-math-atan-function/
    return math.sqrt(dx**2 + dy**2), math.atan2(dy,dx) * 180/math.pi

class GuessPin:
    def __init__(self, app, canvasCoords, guessNum):
        self.canvasCoords = canvasCoords
        self.mapCoords = toMapCoords(np.array([canvasCoords]), app.bounds, app.width, app.height, 
            flattened=False)
        self.displayStats = False

        # normalize distance so that it's in between 0 and 1
        # find a better scale for this

        answerLong = app.answer['pt'][0]
        answerLat = app.answer['pt'][1]
        self.distance, self.angle = findDistance(self.mapCoords[:,0], self.mapCoords[:,1],
                                                 answerLong, answerLat)
        self.normDist = 1 - (math.sqrt(self.distance) / 100)
        if self.normDist < 0: self.normDist = 0
        self.distStr = friendlyDistString(self.distance)

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

        # hex to rgb from https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
        cStart = cStart[1:]
        cEnd = cEnd[1:]
        startRGB = list(int(cStart[i:i+2], 16) for i in (0, 2, 4))
        endRGB = list(int(cEnd[i:i+2], 16) for i in (0, 2, 4))

        # find a point in between the two colors
        # similar to the mixing colors problem in HW 1
        r = (endRGB[0] - startRGB[0]) * self.normDist + startRGB[0]
        g = (endRGB[1] - startRGB[1]) * self.normDist + startRGB[1]
        b = (endRGB[2] - startRGB[2]) * self.normDist + startRGB[2]

        # rgb to hex from https://www.codespeedy.com/convert-rgb-to-hex-color-code-in-python/
        mixedRGB = '#' + '%02x%02x%02x' % (int(r), int(g), int(b))

        return mixedRGB
    
    def mouseNearby(self, mouseX, mouseY):
        canvasX = self.canvasCoords[0]
        canvasY = self.canvasCoords[1]
        return mouseInBounds(canvasX, canvasY, 30, 30, mouseX, mouseY)

    def drawArrow(self, canvas, theta, dist):
        tailX, tailY = self.canvasCoords[0], self.canvasCoords[1]
        headX, headY = angle(self.canvasCoords[0], self.canvasCoords[1], theta, dist)
        leftX, leftY = angle(headX, headY, 180 + theta - 20, 10)
        rightX, rightY = angle(headX, headY, 180 + theta + 20, 10)
        canvas.create_line(tailX, tailY, headX, headY, fill='black', width=3)
        canvas.create_line(headX, headY, leftX, leftY, fill='black', width=3)
        canvas.create_line(headX, headY, rightX, rightY, fill='black', width=3)

    def redraw(self, app, canvas):
        self.canvasCoords = toCanvasCoords(self.mapCoords, app.bounds, app.width, app.height, 
            flattened=True)
        drawPin(canvas, self.color, self.canvasCoords[0], self.canvasCoords[1], str(self.num))
        if self.displayStats:
            textY = self.canvasCoords[1] + 10 if (self.angle > 0) else self.canvasCoords[1] - 50
            # if distance > 1000 feet, return dist in miles; if not, then return distance in feet
            canvas.create_text(self.canvasCoords[0], textY, text=self.distStr)
            self.drawArrow(canvas, self.angle, (1 - self.normDist) * 60 + 10)

        
        
        
        


