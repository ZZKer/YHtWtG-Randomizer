import fileinput
import random

# First, get the seed
seed = input('Enter seed number: ')
random.seed(int(seed))
seed = str(seed)

# Randomize orbs
orbs = [(-8,2),(5,6),(8,1),(-3,5)]
orbs_r = random.sample(orbs,4)

# Set Orb names
ending = ['" toptitle="Cerulean Aura" title="- Activates Blue Ghost Blocks -">\n', '" toptitle="Crimson Aura" title="- Activates Red Ghost Blocks -">\n', '" toptitle="Spider Gloves" title="- Cling to Walls and Leap Off -">\n', '" toptitle="Springheel Boots" title="- Jump Again in Midair -">\n']

# Write ROOMS file, setting the orb possitions
writefilename = 'Rooms_random' + seed + '.xml'
readfile = open('Rooms_Normal.xml')
writefile = open(writefilename, 'w')
for line in readfile:
	if('toptitle' in line):
		activepair = orbs_r.pop(0)
		newline = '<room x="'+str(activepair[0])+'" y="'+str(activepair[1])+ending.pop(0)
		writefile.write(newline)
	else:
		writefile.write(line)
readfile.close()
writefile.close()

# Write the GAM file
gamfilename = 'random' + seed + '.gam'
writefile = open(gamfilename, 'w')
gam_text = 'Title: Rand' + seed + '\n'
gam_text += 'FullTitle: Randomizer seed ' + seed +'\n'
gam_text += "DevTeam: ZZKylie / ZZKer" + '\n'
gam_text += 'DevLogo: phearts.bmp\n'
gam_text += "Author: ZZKylie / ZZKer" + '\n'
gam_text += "URL: ZZKer#1962" + '\n'
gam_text += 'Description: Orb Randomizer version 1.0\n'
gam_text += 'MajorVersion: 1\n'
gam_text += 'MinorVersion: 0\n'
gam_text += 'Map: yhtwtg.map\n'
gam_text += 'Content: DefaultContent.ini\n'
gam_text += 'Rooms: ' + writefilename + '\n'
gam_text += 'StartX: -3\nStartY: 0\n'
writefile.write(gam_text)
writefile.close()
