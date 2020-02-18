import fileinput
import random
import tkinter
from tkinter import *

# Runs the randomizer code based on the given seed.
#     This should run when the "Randomize" button is pressed
def run_randomizer():
      # First, get the seed
      seed = eseed.get()
      random.seed(seed)

      Treasure=[(-10,3,'xxxx',292,36),#0
          (-9,6,'xXXX',220,84),#1
          (-8,1,'xx11',36,180),(-8,2,'xxxx',160,124),(-8,3,'xXXx',108,44),(-8,5,'xxx1',100,148),(-8,6,'xXXX',236,124),#2-6
          (-7,1,'xxxx',252,180),(-7,2,'xxxx',20,116),(-7,2,'xxxx',236,44),(-7,4,'xxXX',212,68),#7-10
          (-6,3,'xx1x',252,68),(-6,4,'xxXX',244,44),(-6,6,'xx11',244,108),#11-13
          (-5,0,'xx11',276,148),(-5,1,'1xxx',204,68),(-5,2,'xxxx',228,172),(-5,3,'xxxx',44,28),(-5,6,'xx1x',164,132),(-5,6,'xxXX',220,84),#14-19
          (-4,-1,'xx11',164,68),(-4,0,'xx11',44,52),(-4,0,'xxxx',68,148),(-4,3,'xXXX',236,180),(-4,3,'0xxX',268,108),(-4,6,'xXXX',292,84),#20-25
          (-3,-2,'xx11',292,44),(-3,0,'xx11',44,68),(-3,1,'xx1x',228,180),(-3,2,'XXxX',284,108),(-3,5,'xXXX',160,124),(-3,6,'xx1x',180,172),#26-31
          (-2,-1,'xX1A',124,124),(-2,0,'xxA1',20,76),(-2,3,'XXXX',256,68),(-2,4,'EExX',308,76),#32-35
          (-1,0,'xxx1',188,172),(-1,1,'xxx1',36,148),(-1,2,'xxxx',228,52),(-1,3,'XxXX',132,108),#36-39
          (0,-3,'xx11',160,140),(0,-3,'xx11',292,180),(0,0,'xxxx',228,76),(0,3,'xxXX',68,84),(0,4,'11xx',188,132),#40-44
          (1,-1,'xXA1',36,124),(1,-1,'xx11',172,176),(1,0,'xxxx',36,156),(1,2,'1xxx',52,68),(1,4,'x1xx',28,76),#45-49
          (2,0,'1x11',124,172),(2,2,'1xxx',268,84),(2,4,'x1XX',244,76),#50-52
          (3,3,'xxxx',196,60),(3,5,'xx11',76,92),#53-54
          (4,3,'xXXx',212,92),#55
          (5,0,'1xx1',108,84),(5,0,'1x1x',292,180),(5,1,'1x1x',44,84),(5,2,'EEXx',180,60),(5,4,'xx1x',284,108),(5,6,'xxxx',160,124),#56-61
          (6,1,'1x1x',212,84),#62
          (7,-1,'1x11',92,148),(7,0,'1xXX',148,124),(7,3,'1x11',68,100),(7,3,'1x11',252,100),#63-66
          (8,1,'1xXX',160,124),(8,2,'1x1x',300,180)]#67-68
      possibleT=[0,3,7,8,9,16,17,22,38,42,47,53,61]
      remainingT=[1,2,4,5,6,10,11,12,13,14,15,18,19,20,21,23,25,26,27,28,29,30,31,32,33,34,35,36,37,39,
                  43,44,45,46,48,49,50,51,52,54,55,56,57,58,59,60,62,63,64,65,66,67,68]
      #unavailableT=[24]
      loseT=[40,41]
      upstairsT=[27,32,33,42,45,47]

      #choose orb order
      orbs = [0,1,2,3]
      spots = [-1,-1,-1,-1]
      orbs_r = random.sample(orbs, 4)
      xorb = 0
      upstairs = True
      loseorb = 40
      #if op_lose is set: Randomize lose orb locations and lose orb
      if(op_lose.get()):
            for losecash in loseT:
                  remainingT.append(losecash)
            remainingT.sort()
            loseorb = random.randint(0,68)
            if(loseorb in possibleT):
                  possibleT.remove(loseorb)
            else:
                  remainingT.remove(loseorb)
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
            if(upstairs and not(possibleT[choiceOfT] in upstairsT)):
                  upstairs = False
            del possibleT[choiceOfT]
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
                        if(valid.count('A')>0 and not upstairs):
                              requiredorbcount += 1
                        if(requiredorbcount==0):
                              additionsT.append(remainingT.pop(xT))
                        else:
                              temporb = xorb-1
                              while(temporb >= 0):
                                    if(valid.count('1',orbs_r[temporb],orbs_r[temporb]+1)>0 or valid.count('A',orbs_r[temporb],orbs_r[temporb]+1)>0):
                                          requiredorbcount-=1
                                    temporb -= 1
                              if(requiredorbcount<1):
                                    additionsT.append(remainingT.pop(xT))
                              else:
                                    xT+=1
                  elif(valid.count('1',orbs_r[xorb],orbs_r[xorb]+1)>0):
      #                  print('1 was found at ')
      #                  print(remainingT[xT])
                        requiredorbcount = valid.count('1')-1
                        if(valid.count('A')>0 and not upstairs):
                              requiredorbcount += 1
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
                              if(valid.count('1',orbs_r[temporb],orbs_r[temporb]+1)>0 or valid.count('A',orbs_r[temporb],orbs_r[temporb]+1)>0):
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
            possibleT.clear()
            possibleT.extend(additionsT)
            possibleT.sort()
            xorb += 1

      #used to check that this algroithm works
      #print('orbs : ')
      #print(orbs_r)
      #print('spots: ')
      #print(spots)

      #include lose orb in orb list
      orbs_r.append(10)
      spots.append(loseorb)

      #once all set, create file and set all orbs and treasure
      # Write ROOMS file, setting the orb possitions
      writefilename = 'Rooms_random_' + seed + '.xml'
      readfile = open('Rooms_randomBase.xml')
      writefile = open(writefilename, 'w')
      t = 0
      tcords = 'room x="'+str((Treasure[t])[0])+'" y="'+str((Treasure[t])[1])+'"'
      gateatlose = op_lose.get()
      for line in readfile:
            writefile.write(line)
            if(gateatlose and ('room x="0" y="-3"' in line)):
                  newline = '<entity template="gate" x="296" y="144" destwx="-3" destwy="0" destrx="24" destry="144" />\n'
                  writefile.write(newline)
                  gateatlose = False
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
                  if(t < len(Treasure) and (Treasure[t])[0] == (Treasure[t-1])[0] and (Treasure[t])[1] == (Treasure[t-1])[1]):
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
                  if(t < len(Treasure)):
                        tcords = 'room x="'+str((Treasure[t])[0])+'" y="'+str((Treasure[t])[1])+'"'
      readfile.close()
      writefile.close()


      # Write the GAM file
      gamfilename = 'random_' + seed + '.gam'
      writefile = open(gamfilename, 'w')
      gam_text = 'Title: Rand-' + seed + '\n'
      gam_text += 'FullTitle: Randomizer seed ' + seed +'\n'
      gam_text += 'DevTeam: ZZKylie & the WtG Discord\n'
      gam_text += 'DevLogo: phearts.bmp\n'
      gam_text += "Author: ZZKylie / ZZKer" + '\n'
      gam_text += "URL: ZZKer#1962" + '\n'
      gam_text += 'Description: Orb Randomizer version 1.3\n'
      gam_text += 'MajorVersion: 1\n'
      gam_text += 'MinorVersion: 3\n'
      gam_text += 'Map: randomBase.map\n'
      gam_text += 'Content: DefaultContent.ini\n'
      gam_text += 'Rooms: ' + writefilename + '\n'
      gam_text += 'StartX: -3\nStartY: 0\n'
      writefile.write(gam_text)
      writefile.close()

      #look into possible bell softlocks

      #Let user know Randomization is done
      output_label['text'] = 'Randomization complete with seed: "' + seed + '"'


def set_settings():
      settingsstring = str(esettings.get())
      if(settingsstring.find('A')>-1):
            check_allorbs.select()
      else:
            check_allorbs.deselect()
      if(settingsstring.find('L')>-1):
            check_lose.select()
      else:
            check_lose.deselect()

def set_setting_allorbs():
      settingsstring = str(esettings.get())
      if(op_allorbs.get()):
            if(settingsstring.find('A')<0):
                  esettings.insert(0, 'A')
      else:
            settingsstring = settingsstring.replace('A', '')
            esettings.delete(0,tkinter.END)
            esettings.insert(0,settingsstring)

def set_setting_lose():
      settingsstring = str(esettings.get())
      if(op_lose.get()):
            if(settingsstring.find('L')<0):
                  esettings.insert(settingsstring.find('A')+1, 'L')
      else:
            settingsstring = settingsstring.replace('L', '')
            esettings.delete(0,tkinter.END)
            esettings.insert(0,settingsstring)

#create the gui
mainwindow=tkinter.Tk()
mainwindow.title('You Have To Randomize The Game v1.3')
#Options
op_allorbs = BooleanVar()   #Option to require all orbs - TODO-------------------------------------------------------------
op_lose = BooleanVar()      #Option to randomize lose orb
check_allorbs = Checkbutton(mainwindow, text='Require All Orbs', variable=op_allorbs, command=set_setting_allorbs)
check_lose = Checkbutton(mainwindow, text='Randomize Lose Orb', variable=op_lose, command=set_setting_lose)
check_allorbs.grid(row=0, sticky=W)
check_lose.grid(row=1, sticky=W)
#Settings Seed: This is the seed used for your settings
tkinter.Label(mainwindow, text='Settings Seed').grid(row=2, column=0, sticky=W)
esettings = tkinter.Entry(mainwindow)
esettings.grid(row=2, column=1, sticky=W)
settingbutton=tkinter.Button(mainwindow, text='Set Settings', width=25, command=set_settings)
settingbutton.grid(row=2, column=2, sticky=W)
#Randomizer Seed: This is the seed used by the randomizer
tkinter.Label(mainwindow, text='Randomizer Seed').grid(row=3, column=0, sticky=W)
eseed = tkinter.Entry(mainwindow)
eseed.grid(row=3, column=1, sticky=W)
gobutton=tkinter.Button(mainwindow, text='Randomize', width=25, command=run_randomizer)
gobutton.grid(row=3, column=2, sticky=W)
#Output: This tells the user what the program is doing
output_label = tkinter.Label(mainwindow, text='Click "Randomize" to start randomizer')
output_label.grid(row=4, sticky=W)
#main loop
mainwindow.mainloop()



Teleporters= [(-7,3,120,160,-9,4,304,64),
              (-6,4,192,32,-9,4,304,64),
              (-3,4,80,104,-3,4,176,104),
              (-3,4,160,104,-3,4,64,104),
              (-2,-2,24,160,-1,-3,200,104),
              (-2,5,288,88,0,2,160,112),
              (-1,-3,296,144,0,-3,24,152),
              (-1,-2,296,144,0,-2,24,152),
              (2,1,88,104,6,4,24,24),
              (3,5,40,72,0,2,160,112),
              (7,3,160,32,0,2,160,112),
              (8,2,32,32,6,1,16,160)]


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
