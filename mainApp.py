
from drawMap import *
from functions.drawShapes import renderMap, drawPin
from classes.button import Button


# display win/lose popup
def endMode_redrawAll(app, canvas):
    renderMap(app, canvas)
    drawPin(canvas, 'green', app.width/2, app.height/2)
    if (app.popUpDisplayed.visible):
        app.popUpDisplayed.redraw(app, canvas)
    else:
        app.backButton.redraw(canvas, app.backButton.x, app.backButton.y)

# reset when you press a button
def endMode_mousePressed(app, event):
    if (not app.popUpDisplayed.visible and 
        mouseInBounds(app.backButton.x, app.backButton.y, 
                        app.backButton.w, app.backButton.h, event.x, event.y)):
        app.backButton.mousePressed(app)
    for item in app.popUpDisplayed.content:
        if (isinstance(item, Button) and 
            (app.popUpDisplayed.visible) and 
            mouseInBounds(item.x, item.y, item.w, item.h, event.x, event.y)):
            item.mousePressed(app)

def appStarted(app):
    app.mode = 'gameMode'
    startGame(app)

def playGame():
    canvasWidth = 1000
    canvasHeight = 1000
    runApp(width=canvasWidth, height=canvasHeight)

playGame()