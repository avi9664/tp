# Where On Earth Is That?!
It's a geography game kind of like a reverse Geoguessr- given a map of a city (e.g. your hometown), you have six tries to find a mystery location on a map, like a restaurant, a museum, or a record store.
Just as a caution, the UI is a little snarky. Adds some character.

## Installing modules:
- Download anaconda! (For Pyrosm, installing with pip seems to be a bit tricky. You can try though and let me know if it works.)
- If using Conda, make sure your interpreter is set to `Python 3.9.13 ('base')`. You may have to uninstall regular ol' Python.
- Install numpy, pandas, tqdm (https://github.com/tqdm/tqdm) and pyrosm (https://pyrosm.readthedocs.io/en/latest/installation.html)

## How to run on your local computer:
- Run `loadData.py` to get a csv of a city. The default I'm using is San Francisco, and for the purposes of test-running, should be kept at San Francisco (for now).
- Run `mainApp.py` to play the game!
- The first location that comes up (for testing reasons) is Sutro Tower. It should appear on the center of your map. Click on it to test the win sequence! After that, the game should behave regularly.
