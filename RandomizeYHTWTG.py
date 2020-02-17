import fileinput
import random

# First, get the seed
seed = input('Enter seed number: ')
random.seed(int(seed))
seed = str(seed)

#v1.2 code
Treasure=[(-10,3,'xxxx',292,36),#0
          (-9,6,'xXXX',220,84),#1
          (-8,1,'xx11',36,180),(-8,2,'xxxx',160,124),(-8,3,'xXXx',108,44),(-8,5,'xxx1',100,148),(-8,6,'xXXX',236,124),#2-6
          (-7,1,'xxxx',252,180),(-7,2,'xxxx',20,116),(-7,2,'xxxx',236,44),(-7,4,'xxXX',212,68),#7-10
          (-6,3,'xx1x',252,68),(-6,4,'xx1x',244,44),(-6,6,'xx11',244,108),#11-13
          (-5,0,'xx11',276,148),(-5,1,'1xxx',204,68),(-5,2,'xxxx',228,172),(-5,3,'xxxx',44,28),(-5,6,'xx1x',164,132),(-5,6,'xxXX',220,84),#14-19
          (-4,-1,'xx11',164,68),(-4,0,'xx11',44,52),(-4,0,'xxxx',68,148),(-4,3,'xXXX',236,180),(-4,3,'0xxX',268,108),(-4,6,'xXXX',292,84),#20-25
          (-3,-2,'xx11',292,44),(-3,0,'xx1A',44,68),(-3,1,'xx1x',228,180),(-3,2,'XXXX',284,108),(-3,5,'xXXX',160,124),(-3,6,'xx1x',180,172),#26-31
          (-2,-1,'xx1A',124,124),(-2,0,'xx11',20,76),(-2,3,'XXXX',332,68),(-2,4,'EExX',308,76),#32-35
          (-1,0,'xxx1',188,172),(-1,1,'xxx1',36,148),(-1,2,'xxxx',228,52),(-1,3,'XXXX',132,108),#36-39
          (0,0,'xxxx',228,76),(0,3,'xx1x',68,84),(0,4,'11xx',188,132),#40-42
          (1,-1,'xxA1',36,124),(1,-1,'xx11',172,176),(1,0,'xxxx',36,156),(1,2,'1xxx',52,68),(1,4,'x1xx',28,76),#43-47
          (2,0,'1x11',124,172),(2,2,'1xxx',268,84),(2,4,'x1XX',244,76),#48-50
          (3,3,'xxxx',196,60),(3,5,'xx11',76,92),#51-52
          (4,3,'xXXx',212,92),#53
          (5,0,'1xx1',108,84),(5,0,'1x1x',292,180),(5,1,'1x1x',44,84),(5,2,'EEXx',180,60),(5,4,'xx1x',284,108),(5,6,'xxxx',160,124),#54-59
          (6,1,'1x1x',212,84),#60
          (7,-1,'1x11',92,148),(7,0,'1xXX',148,124),(7,3,'1x11',68,100),(7,3,'1x11',252,100),#61-64
          (8,1,'1xXX',160,124),(8,2,'1x1x',300,180)]#65-66
possibleT=[0,3,7,8,9,16,17,22,38,40,45,51,59]
remainingT=[1,2,4,5,6,10,11,12,13,14,15,18,19,20,21,23,25,26,27,28,29,30,31,32,33,34,35,36,37,39,41,42,43,44,46,47,48,49,50,52,53,54,55,56,57,58,60,61,62,63,64,65,66]
unavailableT=[24]

#choose orb order
orbs = [0,1,2,3]
orbs_r = random.sample(orbs, 4)
spots = [-1,-1,-1,-1]
xorb = 0
#print('orbs : ')
#print(orbs_r)

#choose treasure location and check orb isn't needed for location
while(xorb < 4):
#      print('possibleT: ')
#      print(possibleT)
      choiceOfT = random.randint(0,len(possibleT)-1)
      spots[xorb] = possibleT[choiceOfT]
      if(xorb==4):#remove when randomizing win orb
            break
      #add new possibilities
      unavailableT.append(possibleT.pop(choiceOfT))
      additionsT = []
      xT = 0
      while(xT<len(remainingT)):
            valid = (Treasure[remainingT[xT]])[2]
#            print('valid : ' + valid)
            if(valid.count('x',orbs_r[xorb],orbs_r[xorb]+1)>0):
#                  print('x was found at ')
#                  print(remainingT[xT])
                  xT+=1
            elif(valid.count('X',orbs_r[xorb],orbs_r[xorb]+1)>0):
#                  print('X was found at ')
#                  print(remainingT[xT])
                  requiredorbcount = valid.count('1')
                  if(requiredorbcount==0):
                        additionsT.append(remainingT.pop(xT))
                  else:
                        temporb = xorb-1
                        while(temporb >= 0):
                              if(valid.count('1',orbs_r[temporb],orbs_r[temporb]+1)>0):
                                    requiredorbcount-=1
                              temporb -= 1
                        if(requiredorbcount<1):
                              additionsT.append(remainingT.pop(xT))
                        else:
                              xT+=1
            elif(valid.count('1',orbs_r[xorb],orbs_r[xorb]+1)>0):
#                  print('1 was found at ')
#                  print(remainingT[xT])
                  if(valid.count('A')>0):
                        whatorb = valid.find('A')
                        temporb = xorb-1
                        while(temporb >= 0):
                              if(whatorb == temporb):
                                    additionsT.append(remainingT.pop(xT))
                                    break
                              else:
                                    temporb-=1
                        if(temporb < 0):
                              xT+=1
                  else:
                        requiredorbcount = valid.count('1')-1
                        if(valid.count('X')>0):
                              requiredorbcount += 1
                              temporb = xorb-1
                              while(temporb >= 0):
                                    if(valid.count('X',orbs_r[temporb],orbs_r[temporb]+1)>0):
                                          requiredorbcount -= 1
                                          break
                                    temporb -= 1
                        temporb = xorb-1
                        while(temporb >= 0):
                              if(valid.count('1',orbs_r[temporb],orbs_r[temporb]+1)>0):
                                    requiredorbcount -= 1
                              temporb -= 1
                        if(requiredorbcount < 1):
                              additionsT.append(remainingT.pop(xT))
                        else:
                              xT+=1
            elif(valid.count('E',orbs_r[xorb],orbs_r[xorb]+1)>0):
#                  print('E was found at ')
#                  print(remainingT[xT])
                  requiredorbcount = valid.count('E')-1
                  temporb = xorb-1
                  while(temporb >= 0):
                        if(valid.count('E',orbs_r[temporb],orbs_r[temporb]+1)>0):
                              requiredorbcount-=1
                        temporb -= 1
                  if(requiredorbcount<1):
                        additionsT.append(remainingT.pop(xT))
                  else:
                        xT+=1
            elif(valid.count('A',orbs_r[xorb],orbs_r[xorb]+1)>0):
#                  print('A was found at ')
#                  print(remainingT[xT])
                  requiredorbcount = valid.count('1')
                  temporb = xorb-1
                  while(temporb >= 0):
                        if(valid.count('1',orbs_r[temporb],orbs_r[temporb]+1)>0):
                              requiredorbcount-=1
                        temporb -= 1
                  if(requiredorbcount<1):
                        additionsT.append(remainingT.pop(xT))
                  else:
                        xT+=1
            else:
                  print('oops at xT = ')
                  print(xT)
                  print('and remainingT = ')
                  print(remainingT[xT])
                  xT+=1
      #decide which previous locations should stay
      if(len(additionsT) > 8):
            extraorb = random.randint(0,len(possibleT)-1)
            additionsT.append(possibleT.pop(extraorb))
            extraorb = random.randint(0,len(possibleT)-1)
            additionsT.append(possibleT.pop(extraorb))
      else:
            orbsleft = 10 - len(additionsT)
#            print('orbsleft: ')
#            print(orbsleft)
            while(orbsleft > 0):
                  extraorb = random.randint(0,len(possibleT)-1)
                  additionsT.append(possibleT.pop(extraorb))
                  orbsleft -= 1
      unavailableT.extend(possibleT)
      del possibleT
      possibleT = []
      possibleT.extend(additionsT)
      possibleT.sort()
      unavailableT.sort()
      xorb += 1

#used to check that this algroithm works
#print('orbs : ')
#print(orbs_r)
#print('spots: ')
#print(spots)

#once all set, create file and set all orbs and treasure


# Write ROOMS file, setting the orb possitions
writefilename = 'Rooms_random' + seed + '.xml'
readfile = open('Rooms_randomBase.xml')
writefile = open(writefilename, 'w')
t = 0
tcords = 'room x="'+str((Treasure[t])[0])+'" y="'+str((Treasure[t])[1])+'"'
for line in readfile:
      writefile.write(line)
      if(tcords in line):
            if(t in spots):
                  whichorb = orbs_r[spots.index(t)]
                  newline = '<entity template="orb_'
                  if(whichorb==0):
                        newline += 'blue'
                  elif(whichorb==1):
                        newline += 'red'
                  elif(whichorb==2):
                        newline += 'boots'
                  elif(whichorb==3):
                        newline += 'gloves'
                  else:
                        newline += 'lose'
                  newline += '" x="' + str((Treasure[t])[3]) + '" y="' + str((Treasure[t])[4]-4) + '" />\n'
                  writefile.write(newline)
            else:
                  newline = '<entity template="cash" x="' + str((Treasure[t])[3]) + '" y="' + str((Treasure[t])[4]) + '" />\n'
                  writefile.write(newline)
            t += 1
            if(t < 67 and (Treasure[t])[0] == (Treasure[t-1])[0] and (Treasure[t])[1] == (Treasure[t-1])[1]):
                  if(t in spots):
                        whichorb = orbs_r[spots.index(t)]
                        newline = '<entity template="orb_'
                        if(whichorb==0):
                              newline += 'blue'
                        elif(whichorb==1):
                              newline += 'red'
                        elif(whichorb==2):
                              newline += 'boots'
                        elif(whichorb==3):
                              newline += 'gloves'
                        else:
                              newline += 'lose'
                        newline += '" x="' + str((Treasure[t])[3]) + '" y="' + str((Treasure[t])[4]-4) + '" />\n'
                        writefile.write(newline)
                  else:
                        newline = '<entity template="cash" x="' + str((Treasure[t])[3]) + '" y="' + str((Treasure[t])[4]) + '" />\n'
                        writefile.write(newline)
                  t += 1
            if(t < 67):
                  tcords = 'room x="'+str((Treasure[t])[0])+'" y="'+str((Treasure[t])[1])+'"'
readfile.close()
writefile.close()


# Write the GAM file
gamfilename = 'random' + seed + '.gam'
writefile = open(gamfilename, 'w')
gam_text = 'Title: Rand' + seed + '\n'
gam_text += 'FullTitle: Randomizer seed ' + seed +'\n'
gam_text += 'DevTeam: ZZKylie & WtG Speedrun Discord\n'
gam_text += 'DevLogo: phearts.bmp\n'
gam_text += "Author: ZZKylie / ZZKer" + '\n'
gam_text += "URL: ZZKer#1962" + '\n'
gam_text += 'Description: Orb Randomizer version 1.2.007\n'
gam_text += 'MajorVersion: 1\n'
gam_text += 'MinorVersion: 2\n'
gam_text += 'Map: randomBase.map\n'
gam_text += 'Content: DefaultContent.ini\n'
gam_text += 'Rooms: ' + writefilename + '\n'
gam_text += 'StartX: -3\nStartY: 0\n'
writefile.write(gam_text)
writefile.close()

#look into possible bell softlocks









#v2 code for room randomization
#Roomname= [['x','x','Slippery Slope','Nice of You to Drop In','x','x','x','x','x','x'],
#           ['x','x','Hollow King','Foot of the Throne','Welcome to the Underground','Long Way Down','Secret Passage','x','x','x'],
#           ['x','Maps and Legends','Cerulean Aura','Mind the Gap','Rock Transept','Avalon Calling','The Crab Cake Is a Lie','x','x','x'],
#           ['x','Yggdrasil','Covert Operators','I Wonder Where This Goes','Aqueous Humor','Et in Aether ego','Be Seeing You','x','x','x'],
#           ['x','The Grand Vault','The Quarry Hub','Pit Stop','Like Ivy, Twisting',"It's More Scared of You",'Hidden Crevasse','x','x','x'],
#           ['Hydra Is Myth','Artisan Stone Walls','Cave In','Obvious Movie Quote','A Dream of Memory','Mine Shaft','Forgotten Tunnels','A Sickly, Silver Moon','Before the Crash',"Hold On Tight and Don't Look Down"],
#           ['Arcane Vocabulary',"Venn's Banality",'Crawlspace',"Don't Be Hasty",'A Memory of a Dream','Green Man','Descent','This Is Where We Used To Live','A Brief Respite','The Coin and the Courage'],
#           ['You Have To Start The Game','Hops and Skips','Never Could See Any Other Way',"You Definitely Shouldn't Go Left",'Rawr!','Springheel Boots','The Arbitrarium','Catharsis in Catastrophe','Hardcore Prawn','Exit Strategy'],
#           ['KISS Principle','Leaps and Bounds','Pit of Spikes','Tower of Sorrows','Tower of Regrets','Back to the Surface','x','Linchpin','Point of No Return','Playing with Fire'],
#           ["Snake, It's a Snake",'Swimming Upstream','Subterranea','Contrived Lock/Key Mechanisms','Falling Into a Greener Life','Speak Now...','Open Sesame','From Another World'],
#           ['Treasure Hunt','Abstract Bridge','Which Path Will I Take?','Bat Cave','Euclid Shrugged','x','x','Consolation Prize','Eponymous','Harbinger'],
#           ['Danger','Not All Those Who Wander Are Lost','Cognitive Resonance','Functional Spelaeology','Circular Logic','x','x','x','x','Taking the Long Way'],
#           ['Leap of Faith','Stick the Landing','Precarious Footholds','Fungal Forest','Prawn Shot First','x','x','x','x','x'],
#           ['On the Count of Three','Mushroom Staircase','Transplants','The Proper Motivation','Fish Out of Water','Abandoned Alcove','yeah but why u jelly tho','x','x','x'],
#           ['Does Whatever A Spider Does','Eden Maw','Under Construction','Remnants of a Past Unknown','Castle Rock','Observation Deck','Wellspring','x','x','x'],
#           ['Attic Storeroom','Vestibule','Shelter from the Storm','Ghosts','Uncertain Semiotics',"Don't Get Snippy With Me",'Crimson Aura','x','x','x'],
#           ['Clarity Comes in Waves','Great Hall','Cave Painting','The Loneliest Corner','Rough Landing','Bring a Mallet','Dire Crab','x','x','x'],
#           ['The Floor Is Lava','Hollow King Transformed','Worth It?','Secret Cat Level','Feline Foreshadowing','x','x','x','x','An Even 0x80'],
#           ['Brazen Machines','Spider Gloves','Not Worth It!','x','x','x','x','x','x','x']]
