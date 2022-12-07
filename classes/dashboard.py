import random
from classes.button import Button
from classes.popup import PopUp
from functions.drawShapes import drawPin
from functions.strArrayStuff import formatLines
from functions.mouseInBounds import mouseInBounds

# help popUp
def getHelp(app):
    allSteps = ['Find a mystery location in 6 tries!',
    "You're given the type of place it is.",
    'Click and drag to pan the map.',
    'To make a guess, move the cursor where you want to place a pin and press the spacebar.',
    "The closer to red the pin is, the closer you are to the location.",
    'Hover over a pin to reveal the distance and direction you need to go.',
    'As you make more guesses, the name of the location will reveal itself.',
    "Alright. Enough with this silly little text wall.",

    Button('Back', back)]
    app.popUpDisplayed = PopUp(app, allSteps, 'How To Play')
    app.mode = 'popUpMode'


def back(app):
    app.mode = 'gameMode'

class Dashboard:
    def __init__(self, app):
        self.newBlanks(app)
        self.formattedHint = formatLines(self.answerParts, 20)
        margin = 24
        self.buttons = [Button('Help', getHelp, margin, margin)]


    # turn answer into a bunch of underscores, hangman style
    # e.g. "Sutro Tower" to "_____ _____"
    def newBlanks(self, app):
        newS = ''
        for c in app.answer['name']:
            if c.isalnum():
                newS += '_'
            else:
                newS += c
        self.answerParts = newS

    # add letters to fragmented answer
    # e.g. "_____ _____" -> "_u___ ____r"
    def addLetters(self, app):
        ans = app.answer['name']
        if (self.answerParts != ans):
            i = random.randint(0, len(ans) - 1)
            while self.answerParts[i] != '_':
                i = random.randint(0, len(ans) - 1)
            self.answerParts = self.answerParts[:i] + ans[i] + self.answerParts[i+1:]

    # draw name of building and the amenity it is
    def drawHints(self, app, canvas, font, smallerFont, m, w, h):
        cx = app.width/2
        canvas.create_rectangle(cx - w/2, m, cx + w/2, h + m, fill='white', outline='black')
        for i in range(len(self.formattedHint)):
            line = self.formattedHint[i]
            canvas.create_text(cx, m * 2 + (font + 10) * i, text=line, 
                            font=f'Arial {font} bold')
        canvas.create_text(cx, h - m, text=app.answer['category'], 
                        font=f'Arial {smallerFont}', anchor='n')
    
    # draw tutorial instructions
    def drawTutorial(self, app, canvas, h, font, m):
        if len(app.stepsLeft) > 0:
            text = formatLines(app.stepsLeft[0])
            w = len(text[0]) * (font) + 2*m
            rectH = len(text) * (font + 10) + 2*m
            x0 = app.width/2 - w/2
            y0 = h
            x1 = app.width/2 + w/2
            y1 = h + rectH
            canvas.create_rectangle(x0, y0, x1, y1, fill='white', outline='black')
            lineY = h + font
            for line in text:
                canvas.create_text(app.width/2, lineY, text=line, 
                    font=f'Arial {font}', anchor='n')
                lineY += font + 10
    
    # draw guesses left (the pin icon + guesses on the top right)
    def drawGuesses(self, app, canvas, font, smallerFont, m, w, h):
        pinWidth = 10
        guessW = m + 2*pinWidth + 5 * smallerFont
        xPin = app.width - m - guessW
        y = m + h/2
        drawPin(canvas, 'white', xPin + m + pinWidth/2, y + pinWidth * 2, None, 'black')
        text = f'{str(app.guessLimit - app.guessNum)} left'
        canvas.create_text(app.width - 2*m, y, text=text, 
                            font=f'Arial {smallerFont}', anchor='e')
    
    def mousePressed(self, app, mouseX, mouseY):
        # go to next step in tutorial when you click and drag
        if (len(app.stepsLeft) == 5) or (len(app.stepsLeft) == 4) or (len(app.stepsLeft) == 2):
            app.stepsLeft.pop(0)
        for button in self.buttons:
            if button.mouseNearby(mouseX, mouseY):
                button.mousePressed(app)

    def spacePressed(self, app, event):
        # go to next step in tutorial when you place a pin
        if len(app.stepsLeft) == 4:
            app.stepsLeft.pop(0)
            # skip the yelling at you part if you click to press a pin on accident
            app.stepsLeft.pop(0)
        elif len(app.stepsLeft) == 3:
            app.stepsLeft.pop(0)

    # redraw everything
    def redraw(self, app, canvas):
        font = 24
        smallerFont = 18
        m = font
        w = app.width - 2*m
        h = (smallerFont + 10) + (font + 10) * len(self.formattedHint) + 2*m
        self.drawHints(app, canvas, font, smallerFont, m, w, h)
        self.drawGuesses(app, canvas, font, smallerFont, m, w, h)
        self.drawTutorial(app, canvas, h + 2*m, smallerFont - 4, 18)
        for button in self.buttons:
            button.redraw(canvas, button.x, button.y)