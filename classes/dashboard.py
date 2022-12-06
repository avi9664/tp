import random
from classes.button import Button
from classes.popup import PopUp
from functions.drawShapes import drawPin
from functions.strArrayStuff import formatLines
from functions.mouseInBounds import mouseInBounds

def getHelp(app):
    guide = ['Find a mystery location in 6 tries!',
    "You're given the type of place it is.",
    'Click and drag to pan the map.',
    'To make a guess, move the cursor where you want to place a pin and press the spacebar.',
    "The closer to red the pin is, the closer you are to the location.",
    'Hover over a pin to reveal the distance and direction you need to go.',
    'As you make more guesses, the name of the location will reveal itself.',
    Button('Back', back)]
    app.popUpDisplayed = PopUp(app, guide, 'How To Play')
    app.mode = 'popUpMode'


def back(app):
    app.mode = 'gameMode'

class Dashboard:
    def __init__(self, app):
        self.newBlanks(app)
        self.formattedHint = formatLines(self.answerParts)
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
        for button in self.buttons:
            if button.mouseNearby(mouseX, mouseY):
                button.mousePressed(app)

    # redraw everything
    def redraw(self, app, canvas):
        font = 24
        smallerFont = 18
        m = font
        w = app.width - 2*m
        h = (smallerFont + 10) + (font + 10) * len(self.formattedHint) + 2*m
        self.drawHints(app, canvas, font, smallerFont, m, w, h)
        self.drawGuesses(app, canvas, font, smallerFont, m, w, h)
        for button in self.buttons:
            button.redraw(canvas, button.x, button.y)