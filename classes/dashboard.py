import random

class Dashboard:
    def __init__(self, app):
        self.newBlanks(app)
        self.formatLines()

    # account for multiple-lines
    def formatLines(self):
        splitAnswer = self.answerParts.split(' ')
        lines = ['']
        charLength = 0
        for word in splitAnswer:
            charLength += len(word) + 1
            if charLength > 17:
                charLength = 0
                lines = lines + [f'{word} ']
            else:
                lines[-1] += f'{word} '
        self.formattedHint = lines

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
    def drawHints(self, app, canvas):
        font = 24
        smallerFont = 16
        m = font
        w = font * 17 + 2*m
        h = (smallerFont + 10) + (font + 10) * len(self.formattedHint) + 2*m
        cx = app.width/2
        canvas.create_rectangle(cx - w/2, m, cx + w/2, h + m, fill='white', outline='black')
        for i in range(len(self.formattedHint)):
            line = self.formattedHint[i]
            canvas.create_text(cx, m * 2 + (font + 10) * i, text=line, 
                            font=f'Arial {font} bold')
        canvas.create_text(cx, h - m, text=app.answer['category'], 
                        font=f'Arial {smallerFont}') 


    def redraw(app, canvas):
        # drawLabel(app, canvas)
        pass