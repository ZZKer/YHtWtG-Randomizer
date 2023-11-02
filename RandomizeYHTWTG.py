import random
import string
import tkinter
from tkinter import ttk

from logic import randomizerlogic as logic
from tkinter import *


# Runs the randomizer code based on the given seed.
#     This should run when the "Randomize" button is pressed
def run_randomizer():
    # First, get the seed
    seed = eseed.get()
    if seed == None or len(seed) == 0:
        random.seed()
        seed = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    random.seed(seed)

    Treasure = [(-10, 3, 'xxxx', 292, 36),  # 0
                (-9, 6, 'xXXX', 220, 84),  # 1
                (-8, 1, 'xx11', 36, 180), (-8, 2, 'xxxx', 160, 124), (-8, 3, 'xXXx', 108, 44),
                (-8, 5, 'xxx1', 100, 148), (-8, 6, 'xXXX', 236, 124),  # 2-6
                (-7, 1, 'xxxx', 252, 180), (-7, 2, 'xxxx', 236, 44), (-7, 2, 'xxxx', 20, 116), (-7, 4, 'xxXX', 212, 68),
                # 7-10
                (-6, 3, 'xx1x', 252, 68), (-6, 4, 'xxXX', 244, 44), (-6, 6, 'xx11', 244, 108),  # 11-13
                (-5, 0, 'xx11', 276, 148), (-5, 1, '1xxx', 204, 68), (-5, 2, 'xxxx', 228, 172), (-5, 3, 'xxxx', 44, 28),
                (-5, 6, 'xxXX', 220, 84), (-5, 6, 'xx1x', 164, 132),  # 14-19
                (-4, -1, 'xx11', 164, 68), (-4, 0, 'xxxx', 68, 148), (-4, 0, 'xx11', 44, 52), (-4, 3, '0xxX', 268, 108),
                (-4, 3, 'xXXX', 236, 180), (-4, 6, 'xXXX', 292, 84),  # 20-25
                (-3, -2, 'xx11', 292, 44), (-3, 0, 'xx11', 44, 68), (-3, 1, 'xx1x', 228, 180),
                (-3, 2, 'XXxX', 284, 108), (-3, 5, 'xXXX', 160, 124), (-3, 6, 'xx1x', 180, 172),  # 26-31
                (-2, -1, 'xX1A', 124, 124), (-2, 0, 'xxA1', 20, 76), (-2, 3, 'XXXX', 256, 68), (-2, 4, 'EExX', 308, 76),
                # 32-35
                (-1, 0, 'xxx1', 188, 172), (-1, 1, 'xxx1', 36, 148), (-1, 2, 'xxxx', 228, 52),
                (-1, 3, 'XxXX', 132, 108),  # 36-39
                (0, -3, 'xx11', 292, 180), (0, -3, 'xx11', 160, 140), (0, 0, 'xxxx', 228, 76), (0, 3, 'xxXX', 68, 84),
                (0, 4, '11xx', 188, 132),  # 40-44
                (1, -1, 'xx11', 172, 176), (1, -1, 'xXA1', 36, 124), (1, 0, 'xxxx', 36, 156), (1, 2, '1xxx', 52, 68),
                (1, 4, 'x1xx', 28, 76),  # 45-49
                (2, 0, '1x11', 124, 172), (2, 2, '1xxx', 268, 84), (2, 4, 'x1XX', 244, 76),  # 50-52
                (3, 3, 'xxxx', 196, 60), (3, 5, 'xx11', 76, 92),  # 53-54
                (4, 3, 'xXXx', 212, 92),  # 55
                (5, 0, '1x1x', 292, 180), (5, 0, '1xx1', 108, 84), (5, 1, '1x1x', 44, 84), (5, 2, 'EEXx', 180, 60),
                (5, 4, 'xx1x', 284, 108), (5, 6, 'xxxx', 160, 124),  # 56-61
                (6, 1, '1x1x', 212, 84),  # 62
                (7, -1, '1x11', 92, 148), (7, 0, '1xXX', 148, 124), (7, 3, '1x11', 252, 100), (7, 3, '1x11', 68, 100),
                # 63-66
                (8, 1, '1xXX', 160, 124), (8, 2, '1x1x', 300, 180)]  # 67-68
    loseorb = 41
    options = logic.RandomizerOptions()
    options.difficultyOptions = diffChoiceDict[diffChoice.get()]
    options.seed = seed
    spots = logic.generateRandomSeed(options)
    for i in range(len(spots)):
        if spots[i] > 27:
            spots[i] -= 1
        if spots[i] > 42:
            spots[i] -= 1
    spots.append(loseorb)

    print(f'spots: {spots}')
    writefilename = 'Rooms_random_' + seed + '.xml'
    readfile = open('Rooms_randomBase.xml')
    writefile = open(writefilename, 'w')
    t = 0
    tcords = 'room x="' + str((Treasure[t])[0]) + '" y="' + str((Treasure[t])[1]) + '"'
    if op_lose.get():
        treasureEntity = 'orb_lose'
    else:
        treasureEntity = 'cash'
    gateforallorbs = op_allorbs.get()
    for line in readfile:
        writefile.write(line)
        if ('room x="-1" y="-2"' in line):
            if (gateforallorbs):
                newline = '<entity template="gate" x="296" y="144" destwx="1" destwy="-2" destrx="24" destry="152" />\n'
            else:
                newline = '<entity template="gate" x="296" y="144" destwx="0" destwy="-2" destrx="24" destry="152" />\n'
            writefile.write(newline)
        elif ('room x="0" y="-3"' in line):
            newline = '<entity template="gate" x="296" y="144" destwx="-3" destwy="0" destrx="24" destry="144" />\n'
            writefile.write(newline)
        if (tcords in line):
            if (t in spots):
                whichorb = spots.index(t)
                newline = '<entity template="orb_'
                if (whichorb == 0):
                    newline += 'blue'
                elif (whichorb == 1):
                    newline += 'red'
                elif (whichorb == 2):
                    newline += 'boots'
                elif (whichorb == 3):
                    newline += 'gloves'
                else:
                    newline += 'lose'
                newline += '" x="' + str((Treasure[t])[3]) + '" y="' + str((Treasure[t])[4] - 4) + '" />\n'
                writefile.write(newline)
            else:
                newline = f'<entity template="{treasureEntity}" x="' + str((Treasure[t])[3]) + '" y="' + str(
                    (Treasure[t])[4]) + '" />\n'
                writefile.write(newline)
            t += 1
            if (t < len(Treasure) and (Treasure[t])[0] == (Treasure[t - 1])[0] and (Treasure[t])[1] ==
                    (Treasure[t - 1])[1]):
                if (t in spots):
                    whichorb = spots.index(t)
                    newline = '<entity template="orb_'
                    if (whichorb == 0):
                        newline += 'blue'
                    elif (whichorb == 1):
                        newline += 'red'
                    elif (whichorb == 2):
                        newline += 'boots'
                    elif (whichorb == 3):
                        newline += 'gloves'
                    else:
                        newline += 'lose'
                    newline += '" x="' + str((Treasure[t])[3]) + '" y="' + str((Treasure[t])[4] - 4) + '" />\n'
                    writefile.write(newline)
                else:
                    newline = f'<entity template="{treasureEntity}" x="' + str((Treasure[t])[3]) + '" y="' + str(
                        (Treasure[t])[4]) + '" />\n'
                    writefile.write(newline)
                t += 1
            if (t < len(Treasure)):
                tcords = 'room x="' + str((Treasure[t])[0]) + '" y="' + str((Treasure[t])[1]) + '"'
    readfile.close()
    # op_allorbs code for rooms
    if (gateforallorbs):
        newline = '\n\n<room x="1" y="-2" title="What Do I Win?" />\n\n'
        newline += '<room x="2" y="-2" title="Only A Transition" />\n\n'
        newline += '<room x="3" y="-2" title="Eponymous">\n'
        newline += '<entity template="orb_win" x="300" y="176" />\n</room>\n'
    else:
        newline = '\n\n<room x="0" y="-2" title="Eponymous">\n'
        newline += '<entity template="orb_win" x="160" y="136" />\n</room>\n'
    writefile.write(newline)
    writefile.close()

    # Write the GAM file
    gamfilename = 'random_' + seed + '.gam'
    writefile = open(gamfilename, 'w')
    gam_text = 'Title: Rand-' + seed + '\n'
    gam_text += 'FullTitle: Randomizer seed ' + seed + '\n'
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

    # look into possible bell softlocks

    # Let user know Randomization is done
    output_label['text'] = 'Randomization complete with seed: "' + seed + '"'


def set_settings():
    settingsstring = str(esettings.get())
    if (settingsstring.find('A') > -1):
        check_allorbs.select()
    else:
        check_allorbs.deselect()
    if (settingsstring.find('L') > -1):
        check_lose.select()
    else:
        check_lose.deselect()


def set_setting_allorbs():
    settingsstring = str(esettings.get())
    if (op_allorbs.get()):
        if (settingsstring.find('A') < 0):
            esettings.insert(0, 'A')
    else:
        settingsstring = settingsstring.replace('A', '')
        esettings.delete(0, tkinter.END)
        esettings.insert(0, settingsstring)


def set_setting_lose():
    settingsstring = str(esettings.get())
    if (op_lose.get()):
        if (settingsstring.find('L') < 0):
            esettings.insert(settingsstring.find('A') + 1, 'L')
    else:
        settingsstring = settingsstring.replace('L', '')
        esettings.delete(0, tkinter.END)
        esettings.insert(0, settingsstring)


def setSettingDifficulty():
    pass


class CustomDifficultyWindow(Toplevel):

    def __init__(self, parent, initialSettings=logic.DifficultyOptions(), onclose=None):
        super().__init__(parent)
        self.title('Custom Difficulty')

        self.onclose = onclose

        self.settings = initialSettings

        self.spikeJumpVar = BooleanVar()
        self.spikeJumpVar.set(self.settings.spikejumps)
        self.tripleJumpVar = BooleanVar()
        self.tripleJumpVar.set(self.settings.triplejumps)
        self.extendedJumpVar = BooleanVar()
        self.extendedJumpVar.set(self.settings.extendedjumps)

        difficultyFrame = Frame(self)
        difficultyFrame.grid(row=0, column=0, sticky=(N, E, S, W), padx=5, pady=5)
        checkSpikeJumps = Checkbutton(difficultyFrame, text='Spikejumps', variable=self.spikeJumpVar, command=self.updateSettings)
        checkSpikeJumps.grid(row=0, column=0, sticky=W)
        checkTripleJumps = Checkbutton(difficultyFrame, text='Ground Grace Storage (aka Triple Jumps)',
                                               variable=self.tripleJumpVar, command=self.updateSettings)
        checkTripleJumps.grid(row=1, column=0, sticky=W)
        checkExtendedJumps = Checkbutton(difficultyFrame, text='Refire Grace Storage (aka Extended Jumps)',
                                                 variable=self.extendedJumpVar, command=self.updateSettings)
        checkExtendedJumps.grid(row=2, column=0, sticky=W)

        closeButton = tkinter.Button(difficultyFrame, text='Close', command=self.close,)
        self.protocol("WM_DELETE_WINDOW", self.close)
        closeButton.grid(row=3, column=0, sticky=(W,E,S))

        self.transient(parent)
        self.wait_visibility()
        self.resizable(False, False)
        self.grab_set()

    def updateSettings(self):
        self.settings.startWithBlueOrb = False
        self.settings.startWithRedOrb = False
        self.settings.startWithBoots = False
        self.settings.startWithGloves = False

        self.settings.spikejumps = self.spikeJumpVar.get()
        self.settings.triplejumps = self.tripleJumpVar.get()
        self.settings.extendedjumps = self.extendedJumpVar.get()

    def close(self):
        if self.onclose != None:
            self.onclose()

        self.grab_release()
        self.destroy()


def openCustomDifficultyWindow():
    customDifficultyWindow = CustomDifficultyWindow(mainwindow, diffOptionCustom, setSettingDifficulty)
    customDifficultyWindow.wait_window()


diffOptionGlitchless = logic.DifficultyOptions()
diffOptionUnrestricted = logic.DifficultyOptions()
diffOptionUnrestricted.spikejumps = True
diffOptionUnrestricted.triplejumps = True
diffOptionUnrestricted.extendedjumps = True
diffOptionCustom = logic.DifficultyOptions()

diffChoiceDict = {'unrestricted': diffOptionUnrestricted, 'glitchless': diffOptionGlitchless,
                  'custom': diffOptionCustom}

# create the gui
mainwindow = Tk()
mainwindow.title('You Have To Randomize The Game v1.3')
mainframe = Frame(mainwindow)
mainframe.grid(column=0, row=0, sticky=(N,W,E), padx=5, pady=5)
# Options
op_allorbs = BooleanVar()  # Option to require all orbs - TODO-------------------------------------------------------------
op_lose = BooleanVar()  # Option to randomize lose orb
op_difficulty = logic.DifficultyOptions()
check_allorbs = Checkbutton(mainframe, text='Require All Orbs', variable=op_allorbs, command=set_setting_allorbs)
check_lose = Checkbutton(mainframe, text='Replace Treasure with Lose', variable=op_lose, command=set_setting_lose)
check_allorbs.grid(row=0, sticky=W)
check_lose.grid(row=1, sticky=W)

difficultySettings = Frame(mainframe)
diffChoice = StringVar()
diffChoice.set('unrestricted')
diffLabel = Label(difficultySettings, text='Difficulty:')
diffLabel.grid(row=0, sticky=W)
diffUnrestricted = Radiobutton(difficultySettings, text='Unrestricted', variable=diffChoice,
                                        value='unrestricted', command=setSettingDifficulty)
diffUnrestricted.grid(row=1, sticky=W, padx=(10,0))
diffGlitchless = Radiobutton(difficultySettings, text='Glitchless', variable=diffChoice, value='glitchless',
                                      command=setSettingDifficulty)
diffGlitchless.grid(row=2, sticky=W, padx=(10,0))
diffCustom = Radiobutton(difficultySettings, text='Custom', variable=diffChoice, value='custom',
                                  command=openCustomDifficultyWindow)
diffCustom.grid(row=3, sticky=W, padx=(10,0))
# diff_custom = tkinter.Radiobutton(difficultySettings, text='Custom', variable=diffChoice, value=2, command=printChoice)
# diff_custom.grid(row=2, sticky=W)
difficultySettings.grid(row=2, column=0, sticky=W)


ttk.Separator(mainwindow).grid(row=1, sticky=(W,E))
seedframe = Frame(mainwindow)
seedframe.grid(row=2, column=0, sticky=(S,W,E), padx=5, pady=5)
# Settings Seed: This is the seed used for your settings
Label(seedframe, text='Settings Seed:').grid(row=0, column=0)
esettings = Entry(seedframe)
esettings.grid(row=0, column=1, sticky=W, padx=5)
settingbutton = tkinter.Button(seedframe, text='Set Settings', width=15, command=set_settings)
settingbutton.grid(row=0, column=2, sticky=W)
# Randomizer Seed: This is the seed used by the randomizer
Label(seedframe, text='Randomizer Seed:').grid(row=1, column=0, sticky=W)
eseed = Entry(seedframe)
eseed.grid(row=1, column=1, sticky=W, padx=5)
gobutton = Button(seedframe, text='Randomize', width=15, command=run_randomizer)
gobutton.grid(row=1, column=2, sticky=W)
# Output: This tells the user what the program is doing
output_label = Label(mainwindow, text='Click "Randomize" to start randomizer')
output_label.grid(row=3, sticky=W)
# main loop
mainwindow.resizable(False, False)
mainwindow.mainloop()

# Teleporters= [(-7,3,120,160,-9,4,304,64),#0
#              (-6,4,192,32,-9,4,304,64),#1
#              (-3,4,80,104,-3,4,176,104),#2
#              (-3,4,160,104,-3,4,64,104),#3
#              (-2,-2,24,160,-1,-3,200,104),#4
#              (-2,5,288,88,0,2,160,112),#5
#              (-1,-3,296,144,0,-3,24,152),#6: lose
#              (-1,-2,296,144,0,-2,24,152),#7: win (vanilla)
#              (2,1,88,104,6,4,24,24),#8
#              (3,5,40,72,0,2,160,112),#9
#              (7,3,160,32,0,2,160,112),#10
#              (8,2,32,32,6,1,16,160)]#11
#
# extraTeleporters= [(-1,-2,296,144,1,-2,24,152),#win if op_allorbs is on
#                   (0,-3,296,144,-3,0,24,144),#teleport from lose
#                   (0,-2,296,144,-3,0,24,144)]#teleport from win


# v2 code for room randomization
# Roomname= [['x','x','Slippery Slope','Nice of You to Drop In','x','x','x','x','x','x'],
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
#
# Roomlocation=[(-10,2),(-10,3),#0-1
#              (-9,2),(-9,3),(-9,4),(-9,5),(-9,6),#2-6
#              (-8,1),(-8,2),(-8,3),(-8,4),(-8,5),(-8,6),#7-12
#              (-7,1),(-7,2),(-7,3),(-7,4),(-7,5),(-7,6),#13-18
#              (-6,1),(-6,2),(-6,3),(-6,4),(-6,5),(-6,6),#19-24
#              (-5,-3),(-5,-2),(-5,-1),(-5,0),(-5,1),(-5,2),(-5,3),(-5,4),(-5,5),(-5,6),#25-34
#              (-4,-3),(-4,-2),(-4,-1),(-4,0),(-4,1),(-4,2),(-4,3),(-4,4),(-4,5),(-4,6),#35-44
#              (-3,-3),(-3,-2),(-3,-1),(-3,0),(-3,1),(-3,2),(-3,3),(-3,4),(-3,5),(-3,6),#45-54
#              (-2,-3),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-2,3),(-2,4),(-2,5),(-2,6),#55-64
#              (-1,-3),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(-1,3),(-1,4),(-1,5),(-1,6),#65-74
#              (0,-3),(0,-2),(0,-1),(0,0),(0,1),(0,2),(0,3),(0,4),#75-82
#              (1,-1),(1,0),(1,1),(1,2),(1,3),(1,4),#83-88
#              (2,0),(2,1),(2,2),(2,3),(2,4),#89-93
#              (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),#94-100
#              (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),#101-107
#              (5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),#108-114
#              (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),#115-121
#              (7,-1),(7,0),(7,1),(7,2),(7,3),(7,4),#122-127
#              (8,0),(8,1),(8,2)]#128-130
