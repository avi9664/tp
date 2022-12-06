from modes.gameMode import *
from modes.menuMode import *
from modes.popUpMode import *
from modes.loadMode import *

def appStarted(app):
    app.timerDelay = 100
    app.mouseMovedDelay = 5
    app.mode = 'menuMode'
    app.lineWidth = 50
    initializeMenu(app)

def runAll():
    canvasWidth = 1000
    canvasHeight = 1000
    runApp(width=canvasWidth, height=canvasHeight)

runAll()