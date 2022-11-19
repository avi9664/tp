import pandas as pd
import numpy as np
import copy
from cmu_112_graphics import *
from functions.drawShapes import drawOval
from functions.convertCoords import toCanvasCoords, strToArray, toMapCoords
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
    # how far the map reaches on each side
    app.latRadius = app.zoomFactor * 1000/364000
    app.longRadius = app.zoomFactor * 1000/288200

    # how much the map inches to the side when you pan it (using mouse or keys)
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
    # Sutro Tower, SF. From Google Maps.
    app.lat, app.long = 37.7552, -122.4528
    app.zoomFactor = 1 # in feet

    adjustBounds(app)

    app.mouseDist = [0,0]
    app.prevCoords = [0,0]
    app.oldCenter = [0,0]
    app.mouseLongLat = [0,0]
    app.mouseDrag = False
    app.timerDelay = 50
    app.mouseMovedDelay = 1
    app.pins = []

    app.buildings = pd.read_csv('SanFrancisco.csv')
    filterBuildings(app)

# scoured the cmu_112_graphics file & found mousePressed & mouseDragged, basically
# new plan:
# when mouse pressed, keep track of old eventX and eventY (convert to longlat)
# when mouse pressed, keep track of old long and old lat
# convert event.x and event.y to long and lat, calculate distance
# set lat and long to mouselong - old long and mouselat - old lat
# when mouse is released, snap to new longlat

def mousePressed(app, event):
    app.mouseDrag = True
    app.pins = app.pins + [GuessPin(app, np.array([[event.x, event.y]]), 1)]

def mouseDragged(app, event):
    if (app.prevCoords == [0,0] or app.oldCenter == [0,0]):
        app.prevCoords = toMapCoords(np.array([[event.x, event.y]]), app.bounds, 
                        app.width, app.height)
        # print(app.prevCoords)
        app.oldCenter = [app.long, app.lat]
    app.mouseLongLat = toMapCoords(np.array([[event.x, event.y]]), app.bounds, 
                    app.width, app.height)
    print(app.prevCoords)
    app.mouseDist = [app.mouseLongLat[0] - app.prevCoords[0], 
                        app.mouseLongLat[1] - app.prevCoords[1]]
    app.lat = app.oldCenter[1] - app.mouseDist[1]
    app.long = app.oldCenter[0] - app.mouseDist[0]
    adjustBounds(app)
    filterBuildings(app)

def keyPressed(app, event):
    # press z and x to zoom
    if event.key == 'z':
        if (app.zoomFactor < 1.5):
            app.zoomFactor += 0.1
    elif event.key == 'x':
        if (app.zoomFactor > 0.1):
            app.zoomFactor -= 0.1
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
    app.mouseDist = [0,0]
    app.oldCenter = [0,0]

  # print(app.dx, app.dy)

def redrawPolygons(app, canvas):
    step = 2
    numBuildings = len(app.buildingsToDraw)

    # i is starting index; we start at every nth building and smoosh coordinates
    # of the next n buildings together, then draw all coords as "one" polygon
    for i in range(0, numBuildings, step):
        end = numBuildings if (i + step >= numBuildings) else i + step 
        polygonCoords = []
        for j in range(i, end):
            building = app.buildingsToDraw.iloc[j]
            coords = strToArray(building['coords'], True)
            coords = coords + [copy.copy(coords[0])]
            polygonCoords = polygonCoords + coords
        polygonCoords = np.array(polygonCoords)
        canvasCoords = toCanvasCoords(polygonCoords, app.bounds, app.width, app.height)
        canvas.create_polygon(canvasCoords,fill='gray')


def redrawAll(app, canvas):
    # draw a dot where Sutro Tower is for testing
    sutroTower = toCanvasCoords(np.array([[-122.4528, 37.7552]]), app.bounds, 
                                app.width, app.height)
    drawOval(canvas, sutroTower[0], sutroTower[1], 5, 'red')
    redrawPolygons(app, canvas)
    for pin in app.pins:
        pin.redrawPin(app, canvas)

def drawMap():
    canvasWidth = 1000
    canvasHeight = 1000
    runApp(width=canvasWidth, height=canvasHeight)

drawMap()