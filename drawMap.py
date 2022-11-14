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

def appStarted(app):
    # around the Exploratorium. From Google Maps.
    lat, long = 37.7549796,-122.4432489
    dLat = 0.0027
    dLong = 0.0034

    app.latMin = lat - dLat
    app.latMax = lat + dLat
    app.longMin = long - dLong
    app.longMax = long + dLong

    app.buildings = pd.read_csv('SanFrancisco.csv')
    # https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o
    # https://stackoverflow.com/questions/32713221/how-to-use-a-conditional-statement-based-on-dataframe-boolean-value-in-pandas
    app.buildingsToDraw = app.buildings[(app.buildings['cx'] < app.longMax) & 
                                        (app.buildings['cx'] > app.longMin) &
                                        (app.buildings['cy'] < app.latMax) &
                                        (app.buildings['cy'] > app.latMin)]
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