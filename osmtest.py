from pyrosm import get_data
from pyrosm import OSM
from cmu_112_graphics import *
import numpy as np
import pandas as pd
# import file code from 
# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder?page=1&tab=scoredesc#tab-top
from functions.extractCoords import findCentroid, extractCoords, findCentroidWithNumPy

# progress bar from https://stackoverflow.com/questions/3160699/python-progress-bar
from tqdm import tqdm


#####
# integrated code from online pyrosm tutorial: 
# https://pyrosm.readthedocs.io/en/latest/basics.html#read-buildings
# pandas:
# https://pandas.pydata.org/docs/user_guide/10min.html 
# numpy:
# https://numpy.org/doc/stable/user/absolute_beginners.html 
#####

def loadData(query):
    fp = get_data(query)
    osm = OSM(fp)

    # the coordinates of all buildings
    buildingCoordList = []

    # the indices of all starting points for each polygon
    buildingIndexList = []
    currentIndex = 0

    buildings = osm.get_buildings()

    # print sample format of a random geopandas entry for future reference
    sampleFormat = buildings.iloc[20]
    print(sampleFormat)
    print(sampleFormat['geometry'])
    print(len(buildings))

    buildings['cx'] = 0
    buildings['cy'] = 0
    buildings['coords'] = 0

    # from https://www.geeksforgeeks.org/python-pandas-dataframe-astype/#:~:text=astype()%20method%20is%20used,type%20to%20another%20data%20type.
    buildings['coords'] = buildings['coords'].astype('object')


    # somehow have a loading screen that says:
    # This will probably take a few minutes.
    # In the meantime, go to the bathroom, get some coffee, stretch, touch grass...

    for i in tqdm(range(len(buildings))):
        entry = buildings.iloc[i]
        polyCoords = np.array(extractCoords(entry['geometry']))
        long, lat = findCentroidWithNumPy(polyCoords)
        buildings.at[i,'cx'] = long
        buildings.at[i,'cy'] = lat
        buildings.at[i,'coords'] = polyCoords

    print(buildings['cx'][20])
    buildings.to_csv(f'{query}.csv')



loadData('SanFrancisco')
