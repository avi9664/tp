
from gameMode import *
from endMode import *

def appStarted(app):
    app.timerDelay = 50
    app.mouseMovedDelay = 10
    app.mode = 'gameMode'
    startGame(app)

def playGame():
    canvasWidth = 1000
    canvasHeight = 1000
    runApp(width=canvasWidth, height=canvasHeight)

playGame()