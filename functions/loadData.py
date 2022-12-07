from pyrosm import get_data
from pyrosm import OSM
from cmu_112_graphics import *
import numpy as np
import pandas as pd
# import file code from 
# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder?page=1&tab=scoredesc#tab-top
from functions.strArrayStuff import findCentroid, extractCoords, findCentroidWithNumPy

# progress bar from https://stackoverflow.com/questions/3160699/python-progress-bar
from tqdm import tqdm


def loadData(app, query):
    print('Gathering data from OSM...', end='')
    fp = get_data(query)
    osm = OSM(fp)

    print('Done!')
    print('Extracting buildings...', end='')
    buildings = osm.get_buildings()
    print('Done!')
    # print sample format of a random geopandas entry for future reference
    # sampleFormat = buildings.iloc[20]
    # print(sampleFormat)
    # print(sampleFormat['geometry'])
    print(f'{len(buildings)} buildings will need to be loaded and processed...')

    buildings['cx'] = 0
    buildings['cy'] = 0
    buildings['coords'] = 0

    # from https://www.geeksforgeeks.org/python-pandas-dataframe-astype/#:~:text=astype()%20method%20is%20used,type%20to%20another%20data%20type.
    buildings['coords'] = buildings['coords'].astype('object')



    # somehow have a loading screen that says:
    # This will probably take a few minutes.
    # In the meantime, go to the bathroom, get some coffee, stretch, touch grass...

    # I'm also using a small module called tqdm which basically creates a progress
    # bar in the console for tasks that take a long time, such as processing data.
    # I don't think it really needs a tech demo because all you do is just call
    # it inside a for loop. I'm going to delete it anyways once I have a loading
    # screen. More info at https://github.com/tqdm/tqdm

    for i in tqdm(range(len(buildings))):
        entry = buildings.iloc[i]
        polyCoords = np.array(extractCoords(entry['geometry']))
        long, lat = findCentroidWithNumPy(polyCoords)
        buildings.at[i,'cx'] = long
        buildings.at[i,'cy'] = lat
        buildings.at[i,'coords'] = polyCoords
    print('Done!')
    print('Converting to a .csv file...', end='')
    # https://stackoverflow.com/questions/35384358/how-to-open-my-files-in-data-folder-with-pandas-using-relative-path
    buildings.to_csv(f'{query}.csv')
    print('Done!')
    

