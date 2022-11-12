import numpy as np
from functions.extractCoords import stripParens

#####
# numpy:
# https://numpy.org/doc/stable/user/absolute_beginners.html 
#####

## maybe use repr and eval? (eval is dangerous)

def strToArray(s):
    s = stripParens(s)
    splitCoords = s.split('\n ')
    arr = np.zeros((len(splitCoords),2))
    for i in range(len(splitCoords)):
        coords = stripParens(splitCoords[i])
        longlat = coords.split('   ')
        if (len(longlat) > 2):
            for string in longlat:
                if string == '':
                    longlat.remove(string)
        arr[i,0] = longlat[0]
        arr[i,1] = longlat[1]
    return arr

def toCanvasCoords(coords, minLat, minLong, maxLat, maxLong, cw, ch):
    newCoords = np.zeros(coords.shape)
    newCoords[:,1] = (coords[:,1] - minLong)/(maxLong - minLong)
    newCoords[:,0] = (coords[:,0] - minLat)/(maxLat - minLat)
    newCoords[:,1] = cw - newCoords[:,1] * cw
    newCoords[:,0] = newCoords[:,0] * ch
    # format: lat, long
    return newCoords
    
