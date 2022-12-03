from functions.drawShapes import renderMap, drawPin
from functions.mouseInBounds import mouseInBounds
from classes.button import Button

# display win/lose popup
def endMode_redrawAll(app, canvas):
    renderMap(app, canvas)
    drawPin(canvas, 'green', app.width/2, app.height/2)
    if (app.popUpDisplayed.visible):
        app.popUpDisplayed.redraw(app, canvas)
    else:
        app.backButton.redraw(canvas, app.backButton.x, app.backButton.y)

def endMode_mouseMoved(app, event):
    if (app.popUpDisplayed.visible):
        for item in app.popUpDisplayed.content:
            if isinstance(item, Button):
                item.isFocused = False
                # from animations with oop: https://www.cs.cmu.edu/~112/notes/notes-oop-part1.html#oopExample
                if (item.mouseNearby(event.x, event.y)):
                    item.isFocused = True
    else:
        app.backButton.isFocused = False
        if (app.backButton.mouseNearby(event.x, event.y)):
            app.backButton.isFocused = True

# reset when you press a button
def endMode_mousePressed(app, event):
    if (not app.popUpDisplayed.visible and 
        app.backButton.mouseNearby(event.x, event.y)):
        app.backButton.mousePressed(app)
    for item in app.popUpDisplayed.content:
        if (isinstance(item, Button) and 
            (app.popUpDisplayed.visible) and 
            mouseInBounds(item.x, item.y, item.w, item.h, event.x, event.y)):
            item.mousePressed(app)