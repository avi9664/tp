import numpy as np
from functions.extractCoords import stripParens

#####
# numpy:
# https://numpy.org/doc/stable/user/absolute_beginners.html 
#####

## maybe use repr and eval? (eval is dangerous)

def strToArray(s, toList=False):
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
    if toList:
        # https://www.sharpsightlabs.com/blog/numpy-array-to-list/
        return arr.tolist()
    return arr

def toCanvasCoords(coords, bounds, cw, ch, flattened=True):
    minLong, minLat, maxLong, maxLat = bounds[0], bounds[1], bounds[2], bounds[3]
    newCoords = np.zeros(coords.shape)
    newCoords[:,0] = (coords[:,0] - minLong)/(maxLong - minLong)
    newCoords[:,1] = (coords[:,1] - minLat)/(maxLat - minLat)
    newCoords[:,0] = newCoords[:,0] * cw
    newCoords[:,1] = ch - newCoords[:,1] * ch
    # format: long, lat
    if flattened:
        return list(newCoords.flatten())
    return newCoords
    
    
def toMapCoords(coords, bounds, cw, ch, 
    flattened=True):
    minLong, minLat, maxLong, maxLat = bounds[0], bounds[1], bounds[2], bounds[3]
    newCoords = np.zeros(coords.shape)
    newCoords[:,0] = coords[:,0] / cw * (maxLong - minLong) + minLong
    newCoords[:,1] = (ch - coords[:,1]) / ch * (maxLat - minLat) + minLat
    if flattened:
        return list(newCoords.flatten())
    return newCoords
