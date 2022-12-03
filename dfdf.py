# This demos getSnapshot and saveSnapshot

from cmu_112_graphics import *

def appStarted(app):
    app.image = None

def keyPressed(app, event):
    if (event.key == 'g'):
        snapshotImage = app.getSnapshot()
        app.image = app.scaleImage(snapshotImage, 0.2)
    elif (event.key == 's'):
        app.saveSnapshot()

def redrawAll(app, canvas):
    canvas.create_text(350, 20, text='Press g to getSnapshot', fill='black')
    canvas.create_text(350, 40, text='Press s to saveSnapshot', fill='black')
    canvas.create_rectangle(50, 100, 250, 500, fill='cyan')
    if (app.image != None):
        canvas.create_image(600, 300, image=ImageTk.PhotoImage(app.image))

runApp(width=700, height=600)