########
# original code (except for the numpy parts)
# numpy:
# https://numpy.org/doc/stable/user/absolute_beginners.html 
########

import numpy as np

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
