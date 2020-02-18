##THIS IS THE BETA. THERE WILL BE BUGS.

Thank you for trying out the You Have To Win The Game randomizer!
This is version 1.3.
This was created by ZZKylie / ZZKer.
If you have any questions or suggestions, please contact me on Discord @ ZZKer#1962.
If you find any seeds that don't work, please use this github to report it as an Issue.

##Version features

####1.3:
 -  Graphical User Interface for ease of use
 -  Option to require all orbs to win
 -  Option to randomize Lose Orb and include "Consolation Prize" in treasure list
 -  Settings Seed to share your settings with others (will be more helpful as more options are added)
 -  Seed can now be any alpha-numeric string, not just numbers
 -  More treasure locations added (68/70 locations)
 -  Reworked logic when placing items before the drop at the start

####1.2:
 -  Orbs are now randomized with most treasures (66/70 locations)
 -  Special map edit to prevent hardlocks, but not all possible softlocks ;)

####1.1:
 -  Special map edit designed for Randomizer to prevent softlocks.

####1.0:
 -  Orb randomization.
 -  Seeded random.
 -  BUG: Some seeds lead to softlocks if orbs are done in the wrong order. To avoid this, always go right at the beginning.

##Needed files:
 -  [Python 3.8.1 to run program](https://www.python.org/downloads/)
 -  [You Have to Win the Game example map](http://www.piratehearts.com/files/YHtWtG_Campaign.zip)
 -  You Have to Win the Game on Steam (available for free)

##Install:
 1. Make sure Python is installed
 2. Make sure You Have to Win the Game on Steam is installed and played at least once (to initialize folders)
 3. Unzip YHtWtG_Campaign.zip into C:\Users\[your user name]\Documents\my games\You Have to Win the Game\Maps
 4. Place RandomizeYHTWTG.py, randomBase.map, & Rooms_randomBase.xml into the same folder as above
 -  That's it! :D

##To Run:
 1. Double click the .py file to bring up the user interface.
 2. Check the options you want and enter the seed in the "Randomizer Seed" box.
 3. Click the "Randomize" button to create the randomized file.
 4. The new map will appear in your map list in-game.

##Options Explaination:
 -  Require All Orbs: All 4 orbs are required to reach the Win orb.
 -  Randomize Lose Orb: Chooses a random location for the Lose orb and adds the two treasure locations in "Consolation Prize" to possible orb locations.

##The Future:
 - [ ] teleporter randomization
 - [ ] room randomization
 - [ ] start randomization
 - [ ] magic word randomization?
 - [ ] maybe even bell and enemy randomization
 - [ ] Hardmode and glitch logic options
