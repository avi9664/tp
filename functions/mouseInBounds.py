def mouseInBounds(cx, cy, w, h, mouseX, mouseY):
    if (cx - w/2 <= mouseX <= cx + w/2 and
        cy - h/2 <= mouseY <= cy + h/2):
        return True
    return False