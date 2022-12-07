import numpy as np

def strToArray(s, toList=False):
    s = stripParens(s)
    splitCoords = s.split('\n ')
    arr = np.zeros((len(splitCoords),2))
    for i in range(len(splitCoords)):
        coords = stripParens(splitCoords[i])
        longlat = coords.split(' ')
        longlat = [longlat[0], longlat[-1]]
        if len(longlat) < 2:
            print(longlat)
        arr[i,0] = longlat[0]
        arr[i,1] = longlat[1]
    if toList:
        # https://www.sharpsightlabs.com/blog/numpy-array-to-list/
        return arr.tolist()
    return arr

# displays the distance in comprehensible units instead of weird wonky longlat units
def friendlyDistString(d):
    return f'{int(d)} ft' if (d < 1000) else f'{round(d/5280, 1)} mi'

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


def stripParens(s):
    while (not s[0].isdigit() and s[0] != '-'):
        s = s[1:]
    while (not s[-1].isdigit() and s[-1] != '.'):
        s = s[:-1]
    return s

def extractCoords(polygon):
    s = str(polygon)
    leftParens = s.find('(')
    coordsOnly = s[leftParens+2:-2]
    coordList = []
    for pair in coordsOnly.split(', '):
        latlong = pair.split(' ')
        long = float(stripParens(latlong[0]))
        lat = float(stripParens(latlong[1]))
        coordList = coordList + [[long, lat]]
    return coordList

# splits a very long string into multiple lines
def formatLines(s, defaultLength = 50):
        splitAnswer = s.split(' ')
        lines = ['']
        charLength = 0
        for word in splitAnswer:
            charLength += len(word) + 1
            if charLength > defaultLength:
                charLength = 0
                lines = lines + [f'{word} ']
            else:
                lines[-1] += f'{word} '
        return lines


def findCentroid(polygon):
    s = str(polygon.centroid)
    stripped = s[7:-1]
    latlong = stripped.split(' ')
    long = float(latlong[0])
    lat = float(latlong[1])
    return long, lat

def findCentroidWithNumPy(longlats):
    centroid = np.mean(longlats, axis=0)
    return centroid[0], centroid[1]
