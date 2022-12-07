from cmu_112_graphics import *
from modes.gameMode import startGame
from modes.loadMode import setUpLoadMenu
from classes.button import Button
import glob

def initializeMenu(app):
    # I have no time to fix the button class LOL
    app.menuButtons = [Button('Play Game', playGame), 
        Button('Load Data', loadMenu)]
    # play game button
    app.menuButtons[0].x = app.width/2
    app.menuButtons[0].y = app.height/2

    # load data button
    app.menuButtons[1].x = app.width/2
    app.menuButtons[1].y = app.height/2 + app.menuButtons[0].h + 10

    # https://stackoverflow.com/questions/33503993/read-in-all-csv-files-from-a-directory-using-python
    # all csv files
    app.places = glob.glob("*.csv")
    # cut off .csv extension at end of file name
    app.fileIndex = 0

# warnings:
# before pressing "Play Game", click on "Load Data" and load a .csv file. I'm not responsible for any weird stuff in the .csvs that make the game crash. That's the external modules' fault for having weird formats.
# on that note, please don't add any extra of your own funny csvs into this folder unless they were created through the loadData function.
# I highly recommend loading a city because I had insufficient time to figure out how to load an entire country. It will probably make your computer explode.

def playGame(app):
    if (app.places != []):
        app.mode = 'gameMode'
        startGame(app)

def loadMenu(app):
    app.mode = 'loadMode'
    setUpLoadMenu(app)


def menuMode_mousePressed(app, event):
    for button in app.menuButtons:
        if button.mouseNearby(event.x, event.y):
            button.mousePressed(app)

def menuMode_keyPressed(app, event):
    if (event.key == 'Left'):
        app.fileIndex = (app.fileIndex - 1) % len(app.places)
    elif (event.key == 'Right'):
        app.fileIndex = (app.fileIndex + 1) % len(app.places)
    elif (event.key == 'Up'):
        app.fileIndex = (app.fileIndex + 1) % len(app.places)
    elif (event.key == 'Down'):
        app.fileIndex = (app.fileIndex - 1) % len(app.places)

def menuMode_redrawAll(app, canvas):
    # title
    canvas.create_text(app.width/2, app.height * 0.2, text='Where on Earth is That?!',
        font='Arial 24 bold')
    # display place to load
    location = """I don't have any geographic data. Could you load some?""" if app.places == [] else app.places[app.fileIndex][:-4]
    canvas.create_text(app.width/2, app.height * 0.4, 
        text='Use the arrow keys to choose a location to play in:',
        font='Arial 18 bold')
    canvas.create_text(app.width/2, app.height * 0.4 + 30, text=location, font='Arial 16')
    for button in app.menuButtons:
        button.redraw(canvas, button.x, button.y)


