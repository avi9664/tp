from cmu_112_graphics import *

def drawOval(canvas, cx, cy, r, fill, outline='white', width=2):
    x0 = cx - r
    y0 = cy - r
    x1 = cx + r
    y1 = cy + r
    canvas.create_oval(x0, y0, x1, y1, fill=fill, outline=outline, width=width)

def drawPin(canvas, color, x, y, text=None):
    r = 5
    needleWidth = 3
    h = y - r * 8
    canvas.create_polygon(x - needleWidth, h + 2*r, x, y, x + needleWidth,
                        h + 2*r, fill='white', outline='black', width=2)
    drawOval(canvas, x, h + r, r*2, color)
    if text != None:
        canvas.create_text(x, h + r, text=text, fill='white')