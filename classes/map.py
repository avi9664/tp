from cmu_112_graphics import *
from functions.strArrayStuff import strToArray, toCanvasCoords, toMapCoords
import pandas as pd
import numpy as np
import random

class Map:
    def __init__(self, app):
        # converting to longlat
        self.width = 8000
        self.reset(app)
    
    # from Animations, part 4 of the 15-112 website
    def createMap(self, app):
        self.imageWidth = 4000
        mapImage = Image.new('RGB', (self.imageWidth, self.imageWidth), '#FFFFFF')
        draw = ImageDraw.Draw(mapImage)
        for i in range(len(self.buildingsToDraw)):
            building = self.buildingsToDraw.iloc[i]
            coords = strToArray(building['coords'])
            canvasCoords = toCanvasCoords(coords, self.bounds, self.imageWidth, self.imageWidth)
            # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.polygon
            draw.polygon(canvasCoords,fill='gray')
        return mapImage

    def reset(self, app):
        self.mapBounds(app)
        self.filterBuildings(app)

    # def mouseDragged(app, event):
    #     if (app.prevCoords == [0,0] or app.oldCenter == [0,0]):
    #         app.prevCoords = toMapCoords(np.array([[event.x, event.y]]), app.bounds, 
    #                         app.width, app.height)
    #         # print(app.prevCoords)
    #         app.oldCenter = [app.long, app.lat]
    #     app.mouseLongLat = toMapCoords(np.array([[event.x, event.y]]), app.bounds, 
    #                     app.width, app.height)
    #     print(app.prevCoords)
    #     app.mouseDist = [app.mouseLongLat[0] - app.prevCoords[0], 
    #                         app.mouseLongLat[1] - app.prevCoords[1]]
    #     app.lat = app.oldCenter[1] - app.mouseDist[1]
    #     app.long = app.oldCenter[0] - app.mouseDist[0]

    def mapBounds(self,app):
        radius = self.width/2
        # how far the map reaches on each side
        self.latRadius = radius/364000
        self.longRadius = radius/288200

        # how much the map inches to the side when you pan it (using mouse or keys)
        # app.dLat = app.zoomFactor / 364000
        # app.dLong = app.zoomFactor / 288200
        # https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o
        # https://stackoverflow.com/questions/32713221/how-to-use-a-conditional-statement-based-on-dataframe-boolean-value-in-pandas
        self.longMin = app.long - self.longRadius
        self.latMin = app.lat - self.latRadius
        self.longMax = app.long + self.longRadius
        self.latMax = app.lat + self.latRadius
        self.bounds = [self.longMin, self.latMin, self.longMax, self.latMax]

    def filterBuildings(self, app):
        # bug fixing: https://stackoverflow.com/questions/17216153/python-pandas-boolean-indexing-on-multiple-columns
        self.buildingsToDraw = app.buildings[(app.buildings['cx'] < self.longMax) & 
                                            (app.buildings['cx'] > self.longMin) &
                                            (app.buildings['cy'] < self.latMax) &
                                            (app.buildings['cy'] > self.latMin)]
