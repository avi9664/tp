
from drawMap import *
from classes.button import Button

def endMode_redrawAll(app, canvas):
    app.popUpDisplayed.redraw(app, canvas)

def endMode_mousePressed(app, event):
    for item in app.popUpDisplayed.content:
        if isinstance(item, Button) and mouseInBounds(item.x, item.y, 
        item.w, item.h, event.x, event.y):
            item.mousePressed(app)

def appStarted(app):
    app.mode = 'gameMode'
    startGame(app)

def playGame():
    canvasWidth = 1000
    canvasHeight = 1000
    runApp(width=canvasWidth, height=canvasHeight)

playGame()