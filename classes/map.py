from cmu_112_graphics import *
from functions.strArrayStuff import strToArray, toCanvasCoords, toMapCoords
import pandas as pd
import numpy as np
import random

# from animations pt 4 in 112 website
def getCachedPhotoImage(app, image):
    # stores a cached version of the PhotoImage in the PIL/Pillow image
    if ('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage

class Map:
    def __init__(self, app):
        # converting to longlat
        self.width = app.r * 2
        self.imageWidth = app.r
        self.zoom = self.width/(2 * self.imageWidth)
        self.reset(app)
    
    # from Animations, part 4 of the 15-112 website
    def createMap(self, app):
        mapImage = Image.new('RGB', (self.imageWidth, self.imageWidth), '#F7F6F7')
        draw = ImageDraw.Draw(mapImage)
        for i in range(len(self.buildingsToDraw)):
            building = self.buildingsToDraw.iloc[i]
            coords = strToArray(building['coords'])
            canvasCoords = toCanvasCoords(coords, self.bounds, self.imageWidth, self.imageWidth)
            # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.polygon
            draw.polygon(canvasCoords,fill='#C78FB4')
        return mapImage

    def reset(self, app):
        self.mapBounds(app)
        self.filterBuildings(app)

    def renderMap(self, app, canvas):
        canvas.create_rectangle(0,0, app.width, app.height, outline='', 
            fill='#C78FB4')
        scaledMap = app.scaleImage(app.map, self.zoom)
        mapCenter = toCanvasCoords(np.array([[app.startLong, app.startLat]]), 
                    app.bounds, app.width, app.height)
        cachedImage = getCachedPhotoImage(app, scaledMap)
        canvas.create_image(mapCenter[0], mapCenter[1], image=cachedImage)
        for pin in app.pins:
            pin.redraw(app, canvas)

    # pan map
    def mouseDragged(self, app):
        if app.mouseDrag:
            mouseX = app.mouseCoords[0]
            mouseY = app.mouseCoords[1]
            if (app.prevCoords == [0,0] or app.oldCenter == [0,0]):
                app.prevCoords = [mouseX, mouseY]
                app.oldCenter = [app.long, app.lat]
            app.mouseDist = [mouseX - app.prevCoords[0], mouseY - app.prevCoords[1]]
            app.lat = app.oldCenter[1] + app.mouseDist[1]/364000
            app.long = app.oldCenter[0] - app.mouseDist[0]/288200

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
