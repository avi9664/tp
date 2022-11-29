import random
from functions.drawShapes import drawPin
from functions.strArrayStuff import formatLines

class Dashboard:
    def __init__(self, app):
        self.newBlanks(app)
        self.formattedHint = formatLines(self.answerParts)


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
    
    # draw guesses left
    def drawGuesses(self, app, canvas, font, smallerFont, m, w, h):
        pinWidth = 10
        guessW = m + 2*pinWidth + 5 * smallerFont
        xPin = app.width - m - guessW
        y = m + h/2
        drawPin(canvas, 'white', xPin + m + pinWidth/2, y + pinWidth * 2, None, 'black')
        text = f'{str(app.guessNum)}/{str(app.guessLimit)}'
        canvas.create_text(app.width - 2*m, y, text=text, 
                            font=f'Arial {smallerFont}', anchor='e')

    def redraw(self, app, canvas):
        font = 24
        smallerFont = 18
        m = font
        w = app.width - 2*m
        h = (smallerFont + 10) + (font + 10) * len(self.formattedHint) + 2*m
        self.drawHints(app, canvas, font, smallerFont, m, w, h)
        self.drawGuesses(app, canvas, font, smallerFont, m, w, h)