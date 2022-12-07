from pyrosm import get_data
from pyrosm import OSM
from pyrosm.data import sources
from functions.loadData import loadData
from cmu_112_graphics import *
from classes.button import Button
from classes.textbox import TextBox

# this is what appears when you click on "Load Data"

def setUpLoadMenu(app):
    app.bg = 'white'
    app.text = 'black'
    app.fontSize = 16
    app.searchBox = TextBox()

    app.sources = sorted(sources._all_sources)
    app.clickableResults = []
    app.selected = ''
    app.buttonSelected = ''


    app.loadButton = Button('Load', checkValue)
    app.loadButton.x = app.width * 0.7 + 10 + app.loadButton.w/2
    app.loadButton.y = app.height * 0.1 + 20
    app.clickedLoad = 0

    app.backButton = Button('Back to Main Menu', backToMenu, 100, app.height * 0.7)
    app.feedbackText = ''

def backToMenu(app):
    app.mode = 'menuMode'

# when you press the Load button
def checkValue(app):
    if len(app.searchBox.value) == 0:
        app.feedbackText = 'Type something in the textbox, ye fool.'
    elif app.searchBox.value in app.sources:
        if app.clickedLoad == 0:
            app.feedbackText = """Okay, that matches one of our sources.\n
Caution: This will take a while to load.
It might also stop the app for a few minutes, so
check the console to see its progress.\n
Get a cup o' tea. Take a shower. Nap. Touch some grass.\n
If you're fine with that, press "Load" again to continue."""
            app.clickedLoad += 1
        elif app.clickedLoad == 1:
            app.clickedLoad = 0
            loadData(app, app.searchBox.value)
    else:
        app.feedbackText = "That's not in our database."

# search in the pyrosm database for results
def searchSources(app, text):
    results = []
    if text == '':
        return []
    for name in app.sources:
        if text in name:
            results.append(name)
    buttonW = app.width * 0.6
    app.clickableResults = [Button(name, setName, 0, 0, 
        buttonW) for name in sorted(results[:5])]

# textbox changes when you press a key
def loadMode_keyPressed(app, event):
    app.searchBox.keyPressed(app, event)
    results = searchSources(app, app.searchBox.value)


# textbox updates when you click on any of the search results
def setName(app):
    app.searchBox.value = app.buttonPressed
    searchSources(app, app.searchBox.value)

# buttons currently don't change color when they hover. 
# I don't have time to implement that.
def loadMode_mousePressed(app, event):
    if app.loadButton.mouseNearby(event.x, event.y):
        app.loadButton.mousePressed(app)
    if app.backButton.mouseNearby(event.x, event.y):
        app.backButton.mousePressed(app)
    for button in app.clickableResults:
        if button.mouseNearby(event.x, event.y):
            app.buttonPressed = button.value
            button.mousePressed(app)

# this shows up when you type something in the textbox.
def drawSearchResults(app, canvas):
    margin = 24
    f = app.fontSize
    w = app.width * 0.6
    h = f + margin * 2
    buttonY = app.width * 0.1 + h
    for button in app.clickableResults:
        buttonX = app.width * 0.1 + button.w/2
        button.x = buttonX
        button.y = buttonY
        button.redraw(canvas, buttonX, buttonY, 'w', app.width * 0.1 + margin)
        buttonY += button.h

def loadMode_redrawAll(app, canvas):
    canvas.create_text(app.width * 0.1, app.height * 0.05, 
        text='Search for a region', font='Arial 24 bold', anchor='w')
    app.loadButton.redraw(canvas, app.loadButton.x, app.loadButton.y)
    app.backButton.redraw(canvas, app.backButton.x, app.backButton.y)
    app.searchBox.redraw(app, canvas, app.width * 0.1, app.height * 0.1, 
        app.width * 0.6)
    drawSearchResults(app, canvas)
    canvas.create_text(app.width/2, app.height/2, text=app.feedbackText, 
        font='Arial 18 bold')
    pass