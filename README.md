# Where On Earth Is That?!
It's a geography game kind of like a reverse Geoguessr- given a map of a city (e.g. your hometown), you have six tries to find a mystery location on a map, like a restaurant, a museum, or a record store.

Just as a caution, the UI is a little snarky. Adds some character.

## Installing modules:
- I suggest downloading anaconda! (For Pyrosm, installing with pip seems to be a bit tricky. You can try though and let me know if it works.)
- If using Conda, make sure your interpreter is set to `Python 3.9.13 ('base')`. You may have to uninstall regular ol' Python.
- Make sure that you have `numpy`, `pandas`, `glob`, `tqdm` (https://github.com/tqdm/tqdm) and `pyrosm` (https://pyrosm.readthedocs.io/en/latest/installation.html)

## How to run on your local computer:
- Run `mainApp.py` to start the app!
- Before pressing "Play Game", click on "Load Data" and load a .csv file of any city you want. I used San Francisco, and I recommend that you do too. The app may freeze for a few minutes while it's loading the .csv's-- look at the Python console to see how much time the computer needs to load the dataset.
- I highly recommend loading a city because I had insufficient time to figure out how to load an entire country. Processing a gigantic csv file will probably make your computer explode. 
- Finally, after loading your data, you can play the game!

## Here's a sneakpeek at what the game looks like:
![image](https://user-images.githubusercontent.com/32148378/206231866-08cc4ace-6bcc-4671-9466-d5760a909a02.png)
