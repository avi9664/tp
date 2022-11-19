import pandas as pd
import numpy as np
from cmu_112_graphics import *
from functions.drawShapes import drawOval
from functions.convertCoords import toCanvasCoords, strToArray
from classes.pin import GuessPin

# https://www.usgs.gov/faqs/how-much-distance-does-degree-minute-and-second-cover-your-maps
# longitude is East-West (x direction)
# latitude is North-South (y direction)

# 1 degree of latitude ~ 364000 ft ~ around 69 miles
# 1000 ft = 0.0027 degrees of longitude
# 1 degree of longitude ~ 288200 ft ~ 54.6 miles
# 1000 ft = 0.0034 degrees of longitude

#####
# pandas code:
# https://pandas.pydata.org/docs/user_guide/10min.html 
#####

def adjustBounds(app):
    app.latRadius = app.zoomFactor * 1000/364000
    app.longRadius = app.zoomFactor * 1000/288200

    app.dLat = app.zoomFactor / 364000
    app.dLong = app.zoomFactor / 288200
    # https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o
    # https://stackoverflow.com/questions/32713221/how-to-use-a-conditional-statement-based-on-dataframe-boolean-value-in-pandas
    app.latMin = app.lat - app.latRadius
    app.longMin = app.long - app.longRadius
    app.latMax = app.lat + app.latRadius
    app.longMax = app.long + app.longRadius
    app.bounds = [app.long - app.longRadius, app.lat - app.latRadius,
                app.long + app.longRadius, app.lat + app.latRadius]

def filterBuildings(app):
    app.buildingsToDraw = app.buildings[(app.buildings['cx'] < app.longMax) & 
                                        (app.buildings['cx'] > app.longMin) &
                                        (app.buildings['cy'] < app.latMax) &
                                        (app.buildings['cy'] > app.latMin)]
    

def appStarted(app):
    # around the Exploratorium. From Google Maps.
    app.lat, app.long = 37.7552, -122.4528
    app.zoomFactor = 1 # in feet

    adjustBounds(app)

    app.mouseDist = [0,0]
    app.prevCoords = [0,0]
    app.mouseX = 0
    app.mouseY = 0
    app.mouseDrag = False
    app.mouseMovedDelay = 10
    app.pins = []

    app.buildings = pd.read_csv('SanFrancisco.csv')
    filterBuildings(app)

# scoured the cmu_112_graphics file & found mousePressed & mouseDragged, basically

def mousePressed(app, event):
    app.pins = app.pins + [GuessPin(app, np.array([[event.x, event.y]]), 1)]
    app.prevCoords = [event.x, event.y]

def mouseDragged(app, event):
    app.mouseDist = [event.x - app.prevCoords[0], event.y - app.prevCoords[1]]
    app.prevCoords = [event.x, event.y]
    app.lat += app.mouseDist[1] * app.dLat
    app.long += -1 * app.mouseDist[0] * app.dLong
    adjustBounds(app)
    filterBuildings(app)

def keyPressed(app, event):

    if event.key == 'z':
        app.zoomFactor += 1
    elif event.key == 'x':
        app.zoomFactor -= 1
    elif event.key == 'Right':
        app.long += app.dLong * 50
    elif event.key == 'Left':
        app.long -= app.dLong * 50
    elif event.key == 'Up':
        app.lat += app.dLat * 50
    elif event.key == 'Down':
        app.lat -= app.dLat * 50
    adjustBounds(app)
    filterBuildings(app)

def mouseReleased(app, event):
    app.mouseDrag = False

    # print(app.dx, app.dy)
        

def redrawAll(app, canvas):
    sutroTower = toCanvasCoords(np.array([[-122.4528, 37.7552]]), app.bounds, 
                                app.width, app.height)
    drawOval(canvas, sutroTower[0], sutroTower[1], 5, 'red')
    for i in range(len(app.buildingsToDraw)):
        building = app.buildingsToDraw.iloc[i]
        coords = strToArray(building['coords'])
        canvasCoords = toCanvasCoords(coords, app.bounds, app.width, app.height)
        canvas.create_polygon(canvasCoords,fill='gray')
    for pin in app.pins:
        pin.redrawPin(app, canvas)

def drawMap():
    canvasWidth = 1000
    canvasHeight = 1000
    runApp(width=canvasWidth, height=canvasHeight)

drawMap()