from cmu_112_graphics import *
from modes.gameMode import startGame
from modes.loadMode import setUpLoadMenu
from classes.button import Button

def initializeMenu(app):
    app.menuButtons = [Button('Play Game', playGame), 
        Button('Load Data', loadMenu)]
    app.menuButtons[0].x = app.width/2
    app.menuButtons[0].y = app.height/2

    app.menuButtons[1].x = app.width/2
    app.menuButtons[1].y = app.height/2 + app.menuButtons[0].h + 10

def playGame(app):
    app.mode = 'gameMode'
    startGame(app)

def loadMenu(app):
    app.mode = 'loadMode'
    setUpLoadMenu(app)

def menuMode_mousePressed(app, event):
    for button in app.menuButtons:
        if button.mouseNearby(event.x, event.y):
            button.mousePressed(app)

def menuMode_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height * 0.2, text='Where on Earth is That?!',
        font='Arial 24 bold')
    for button in app.menuButtons:
        button.redraw(canvas, button.x, button.y)


