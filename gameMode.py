import pandas as pd
import numpy as np
import random
from cmu_112_graphics import *
from functions.drawShapes import drawOval, renderMap
from functions.strArrayStuff import *
from functions.mouseInBounds import mouseInBounds
from classes.pin import GuessPin
from classes.dashboard import Dashboard
from classes.map import Map
from classes.popup import PopUp
from classes.button import Button

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
    app.bounds = [app.longMin, app.latMin, app.longMax, app.latMax]

def filterBuildings(app):
    # bug fixing: https://stackoverflow.com/questions/17216153/python-pandas-boolean-indexing-on-multiple-columns
    app.buildingsToDraw = app.buildings[(app.buildings['cx'] < app.longMax) & 
                                        (app.buildings['cx'] > app.longMin) &
                                        (app.buildings['cy'] < app.latMax) &
                                        (app.buildings['cy'] > app.latMin)]

def startGame(app):
    # Sutro Tower, SF. From Google Maps.
    app.zoomFactor = 1 # in feet

    # twin peaks
    app.answer = {'name': 'Sutro Tower', 
                    'pt': [-122.4528, 37.7552], 
                    'category': 'tower'} 
    app.r = 4000
    dispX, dispY = random.randint(-1 * app.r, app.r), random.randint(-1 * app.r, app.r)

    app.startLong = app.answer['pt'][0] #+ dispX/288200
    app.startLat = app.answer['pt'][1] #+ dispY/364000
    app.long = app.startLong
    app.lat = app.startLat
    
    app.answerList = []
    app.guessNum = 0
    app.guessLimit = 10

    adjustBounds(app)

    app.mouseDist = [0,0]
    app.prevCoords = [0,0]
    app.oldCenter = [0,0]
    app.mouseLongLat = [0,0]
    app.mouseCoords = [0,0]
    app.mouseDrag = False
    app.pins = []

    app.buildings = pd.read_csv('SanFrancisco.csv')
    # https://pyrosm.readthedocs.io/en/latest/basics.html#read-points-of-interest
    # frankly I do not give a damn about parking. public transportation for the win
    app.possibleAnswers = app.buildings[(pd.notna(app.buildings['name'])) &
                                        (pd.notna(app.buildings['coords'])) &  
                                    (((pd.notna(app.buildings['amenity'])) & 
                                (app.buildings['amenity'] != 'parking')) | 
                            (pd.notna(app.buildings['shop'])))]
    # print(app.possibleAnswers['coords'].unique())
    app.mapObject = Map(app)
    app.map = app.mapObject.createMap(app)
    app.dashboard = Dashboard(app)
    app.popUpDisplayed = None
    app.bg = None
    app.win = False

# reset the game after you win/lose
def reset(app):
    app.mode = 'gameMode'
    app.win = False
    app.popUpDisplayed = None
    app.bg = None
    app.dashboard.answerParts = app.answer['name']
    app.pins = []

    newAns = app.possibleAnswers.iloc[random.randint(0,len(app.possibleAnswers) - 1)]
    app.answerList = app.answerList + [{'name': app.answer['name'], 'guesses': app.guessNum}]
    app.answer['name'] = newAns['name']
    app.answer['category'] = newAns['amenity'] if pd.notna(newAns['amenity']) else newAns['shop']
    app.answer['pt'] = [newAns['cx'], newAns['cy']]

    dispX, dispY = random.randint(-1 * app.r, app.r), random.randint(-1 * app.r, app.r)
    app.startLong = app.answer['pt'][0] + dispX/288200
    app.long = app.startLong
    app.startLat = app.answer['pt'][1] + dispY/364000
    app.lat = app.startLat

    app.guessNum = 0

    adjustBounds(app)
    app.mapObject.reset(app)
    app.map = app.mapObject.createMap(app)
    app.dashboard.newBlanks(app)
    app.dashboard.formattedHint = formatLines(app.dashboard.answerParts)

# scoured the cmu_112_graphics file & found mousePressed & mouseDragged, basically
# new plan:
# when mouse pressed, keep track of old eventX and eventY (convert to longlat)
# when mouse pressed, keep track of old long and old lat
# convert event.x and event.y to long and lat, calculate distance
# set lat and long to mouselong - old long and mouselat - old lat
# when mouse is released, snap to new longlat

def takeAnswerScreenshot(app):
    app.long, app.lat = app.answer['pt'][0], app.answer['pt'][1] 
    adjustBounds(app)
    snapshot = app.getSnapshot()
    app.bg = app.scaleImage(snapshot, 0.05)
    

def gameMode_mousePressed(app, event):
    app.mouseDrag = True
    app.guessNum += 1
    newPin = GuessPin(app, [event.x, event.y], app.guessNum)
    app.pins = app.pins + [newPin]

    if (newPin.distance <= 100):
        app.win = True
        takeAnswerScreenshot(app)
        app.popUpDisplayed = PopUp(app, ['You got the answer in',['PIN',f'*{app.guessNum}*'],
                                Button('Reveal the answer', showAnswer),
                                Button('Start a new game!', reset)],'Correct!')
        app.bg = app.getSnapshot()
        app.mode = 'endMode'
    elif (app.guessNum >= app.guessLimit):
        app.win = False
        takeAnswerScreenshot(app)
        closest = friendlyDistString(min([pin.distance for pin in app.pins]))
        app.popUpDisplayed = PopUp(app, [f"The answer was {app.answer['name']}!",
            f'Your closest guess was {closest} away.',
            Button('Reveal the answer', showAnswer),
            Button('Start a new game!', reset)], 'Game Over!')
        app.mode = 'endMode'
    else:
        app.dashboard.addLetters(app)
        app.dashboard.formattedHint = formatLines(app.dashboard.answerParts)

def gameMode_mouseDragged(app, event):
    app.mouseCoords = [event.x, event.y]

def gameMode_mouseReleased(app, event):
    app.mouseDrag = False
    app.mouseDist = [0,0]
    app.oldCenter = [0,0]
        
# hide popUp to display the answer on the map
def showAnswer(app):
    app.popUpDisplayed.visible = False
    app.backButton = Button('Back', hideAnswer)
    margin = 24
    app.backButton.x = margin + app.backButton.w/2
    app.backButton.y = margin + app.backButton.h/2

def hideAnswer(app):
    app.popUpDisplayed.visible = True

# display stats when you hover over pin
def gameMode_mouseMoved(app, event):
    app.mouseCoords = [event.x, event.y]
    for pin in app.pins:
        pin.displayStats = False
        # from animations with oop: https://www.cs.cmu.edu/~112/notes/notes-oop-part1.html#oopExample
        if (pin.mouseNearby(event.x, event.y)):
            pin.displayStats = True

def gameMode_timerFired(app):
    app.mapObject.mouseDragged(app)
    adjustBounds(app)

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
#     adjustBounds(app)
#     filterBuildings(app)

def gameMode_keyPressed(app, event):
    # press z and x to zoom, arrow keys to pan
    shift = 100
    if event.key == 'z':
        if (app.zoomFactor < 1.5):
            app.zoomFactor += 0.1
    elif event.key == 'x':
        if (app.zoomFactor > 0.1):
            app.zoomFactor -= 0.1
    elif event.key == 'Right':
        app.long += app.dLong * shift
    elif event.key == 'Left':
        app.long -= app.dLong * shift
    elif event.key == 'Up':
        app.lat += app.dLat * shift
    elif event.key == 'Down':
        app.lat -= app.dLat * shift
    adjustBounds(app)


def gameMode_redrawAll(app, canvas):
    renderMap(app, canvas)
    app.dashboard.redraw(app, canvas)