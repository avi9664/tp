import pandas as pd
import numpy as np
import random
from cmu_112_graphics import *
from functions.drawShapes import drawOval
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

# adjust bounds of map (basically controlling the player's view of the map)
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

# set up everything
def startGame(app):
    # Sutro Tower, SF. From Google Maps.
    app.zoomFactor = 1 # in feet

    # twin peaks
    app.answer = {'name': 'Sutro Tower', 
                    'pt': [-122.4528, 37.7552], 
                    'category': 'tower'} 
    app.r = 2000
    dispX, dispY = random.randint(-1 * app.r, app.r), random.randint(-1 * app.r, app.r)

    app.startLong = app.answer['pt'][0] #+ dispX/288200
    app.startLat = app.answer['pt'][1] #+ dispY/364000
    app.long = app.startLong
    app.lat = app.startLat
    
    app.answerList = []
    app.guessNum = 0
    app.guessLimit = 6

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

def centerMapAtAnswer(app):
    app.long, app.lat = app.answer['pt'][0], app.answer['pt'][1] 
    adjustBounds(app)

# add new pin and check for winning/losing
def dropPin(app, x, y):
    newPin = GuessPin(app, [x, y], app.guessNum)
    app.pins = app.pins + [newPin]

    # check if player won
    if (newPin.distance <= 100):
        app.win = True
        centerMapAtAnswer(app)
        app.popUpDisplayed = PopUp(app, ['You got the answer in',['PIN',f'*{app.guessNum}*'],
                                Button('Reveal the answer', showAnswer),
                                Button('Start a new game!', reset)],'Correct!')
        app.bg = app.getSnapshot()
        app.mode = 'popUpMode'

    # check if player lost
    elif (app.guessNum >= app.guessLimit):
        app.win = False
        centerMapAtAnswer(app)
        closest = friendlyDistString(min([pin.distance for pin in app.pins]))
        app.popUpDisplayed = PopUp(app, [f"The answer was {app.answer['name']}!",
            f'Your closest guess was {closest} away.',
            Button('Reveal the answer', showAnswer),
            Button('Start a new game!', reset)], 'Game Over!')
        app.mode = 'popUpMode'
    else:
        app.dashboard.addLetters(app)
        app.dashboard.formattedHint = formatLines(app.dashboard.answerParts)

# pan map when you click
def gameMode_mousePressed(app, event):
    
    app.dashboard.mousePressed(app, event.x, event.y)
    app.mouseDrag = True

# keep track of mouse coordinates
def gameMode_mouseDragged(app, event):
    app.mouseCoords = [event.x, event.y]

def gameMode_mouseReleased(app, event):
    app.mouseDrag = False
    app.mouseDist = [0,0]
    app.oldCenter = [0,0]
        
# hide popUp to display the answer on the map
def showAnswer(app):
    app.popUpDisplayed.visible = False
    app.backButton = Button('Back', backToPopUp)
    margin = 24
    app.backButton.x = margin + app.backButton.w/2
    app.backButton.y = margin + app.backButton.h/2

def backToPopUp(app):
    app.popUpDisplayed.visible = True

# display stats when you hover over pin
def gameMode_mouseMoved(app, event):
    app.mouseCoords = [event.x, event.y]
    for pin in app.pins:
        pin.displayStats = False
        # from animations with oop: https://www.cs.cmu.edu/~112/notes/notes-oop-part1.html#oopExample
        if (pin.mouseNearby(event.x, event.y)):
            pin.displayStats = True

# drag map if you're clicking and holding
def gameMode_timerFired(app):
    app.mapObject.mouseDragged(app)
    adjustBounds(app)

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
    elif event.key == 'Space':
        app.guessNum += 1
        dropPin(app, app.mouseCoords[0], app.mouseCoords[1])
    adjustBounds(app)


def gameMode_redrawAll(app, canvas):
    app.mapObject.renderMap(app, canvas)
    app.dashboard.redraw(app, canvas)