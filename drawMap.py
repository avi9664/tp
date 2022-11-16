import pandas as pd
import numpy as np
from cmu_112_graphics import *
from functions.convertCoords import toCanvasCoords, strToArray

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
    # https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o
    # https://stackoverflow.com/questions/32713221/how-to-use-a-conditional-statement-based-on-dataframe-boolean-value-in-pandas
    app.latMin = app.lat - app.latRadius
    app.latMax = app.lat + app.latRadius
    app.longMin = app.long - app.longRadius
    app.longMax = app.long + app.longRadius

def filterBuildings(app):
    app.buildingsToDraw = app.buildings[(app.buildings['cx'] < app.longMax) & 
                                        (app.buildings['cx'] > app.longMin) &
                                        (app.buildings['cy'] < app.latMax) &
                                        (app.buildings['cy'] > app.latMin)]

def appStarted(app):
    # around the Exploratorium. From Google Maps.
    app.lat, app.long = 37.7549796,-122.4432489
    app.zoomFactor = 1 # in feet
    app.latRadius = app.zoomFactor * 1000/364000
    app.longRadius = app.zoomFactor * 1000/288200

    app.dLat = app.zoomFactor / 364000
    app.dLong = app.zoomFactor / 288200

    adjustBounds(app)

    app.mouseDist = [0,0]
    app.prevCoords = [0,0]
    app.mouseX = 0
    app.mouseY = 0
    app.mouseDrag = False
    app.mouseMovedDelay = 10

    app.buildings = pd.read_csv('SanFrancisco.csv')
    filterBuildings(app)

def mousePressed(app, event):
    app.mouseDrag = True
    app.prevCoords = [event.x, event.y]

def mouseDragged(app, event):
    app.mouseDist = [event.x - app.prevCoords[0], event.y - app.prevCoords[1]]
    app.prevCoords = [event.x, event.y]
        
def mouseReleased(app, event):
    app.mouseDrag = False
    print('released')

    # print(app.dx, app.dy)

def timerFired(app):
    print(app.mouseDrag)
    if app.mouseDrag:
        app.lat += app.mouseDist[1] * app.dLat
        app.long += -1 * app.mouseDist[0] * app.dLong
        filterBuildings(app)
    adjustBounds(app)
        

def redrawAll(app, canvas):
    for i in range(len(app.buildingsToDraw)):
        building = app.buildingsToDraw.iloc[i]
        coords = strToArray(building['coords'])
        canvasCoords = toCanvasCoords(coords, app.longMin, app.latMin,
                            app.longMax, app.latMax, app.width, app.height)
        canvasCoords = list(canvasCoords.flatten())
        canvas.create_polygon(canvasCoords,fill='green')

def drawMap():
    canvasWidth = 1000
    canvasHeight = 1000
    runApp(width=canvasWidth, height=canvasHeight)

drawMap()