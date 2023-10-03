DEFAULT_SPAWN = "You Have to Start the Game Spawn"
DEFAULT_REDORB = "Crimson Aura Pickup"
DEFAULT_BLUEORB ="Cerulean Aura Pickup"
DEFAULT_BOOTS = "Springheel Boots Pickup"
DEFAULT_GLOVES = "Spider Gloves Pickup"
DEFAULT_LOSE = "Consolation Prize Pickup-1"
DEFAULT_WIN = "Eponymous Pickup"

def reduceReqs(reqs):
    reducedReqs = []
    reqs.sort()
    for req in reqs:
        add = True
        for newReq in reducedReqs:
            if not newReq & ~ req:
                add = False
                break
            elif not req & ~ newReq:
                newReq = req
                add = False
                break
        if add:
            reducedReqs = reducedReqs + [req]
    return reducedReqs

def calculateTotalRequirements(newEdgeReqs, existingReqs):
    nrNewReqs = len(newEdgeReqs)
    nrOldReqs = len(existingReqs)
    totalReqs = [0]*(nrNewReqs*nrOldReqs)
    for i in range(nrNewReqs):
        for j in range(nrOldReqs):
            totalReqs[i*nrOldReqs+j] = newEdgeReqs[i] | existingReqs[j]
    return totalReqs

def iterate(matrix, stateVector):
    ret = [[] for _ in range(len(stateVector))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            #print(f'{matrix[j][i]}, {stateVector[i]}')
            ret[i] += calculateTotalRequirements(matrix[j][i], stateVector[j])
        #print(ret[i])
        ret[i] = reduceReqs(ret[i])
    return ret

def readTable(file):
    nrRows = 0
    nrCols = 0
    with open(file) as tableFile:
        nrCols = tableFile.readline().count(";")
        for line in tableFile:
            if line.strip():
                nrRows += 1

    if nrCols != nrRows:
        print("Table has to have the same number of rows and columns")
        return []

    table = [[[] for _ in range(nrRows)] for _ in range(nrCols)]
    labels = ["" for _ in range(nrCols)]

    with open(file) as tableFile:
        tableFile.readline()

        row = 0
        for line in tableFile:
            if not line.strip():
                continue

            lineSplits = line.split(";")
            labels[row] = lineSplits[0]
            lineSplits = lineSplits[1:]
            for col in range(len(lineSplits)):
                entries = lineSplits[col].split(",")
                for entry in entries:
                    if entry.strip() and int(entry) >= 0:
                        table[row][col] += [int(entry)]
            row += 1
    return table, labels


def writeTable(writeFile, states, stateNames=None):
    if isinstance(stateNames, str):
        stateNames = getStateListFromFile(stateNames)
    with open(writeFile, 'w') as writeFile:
        if len(stateNames) > 0:
            writeFile.write(";" + getTableLine(stateNames))
            writeFile.write("\n")

        for i in range(len(states)):
            if len(stateNames) > i:
                line = [stateNames[i]] + states[i]
            else:
                line = [""] + states[i]
            writeFile.write(getTableLine(line))
            writeFile.write("\n")


def getTableLine(entries):
    writeLine = ""
    if len(entries) == 0:
        print("no entries to write")
        return ""

    writeLine += getTableEntry(entries[0])
    if len(entries) > 1:
        for entry in entries[1:]:
            writeLine += ";" + getTableEntry(entry)

    return writeLine


def getTableEntry(entry):
    writeReq = ""
    if len(entry) == 0:
        return ""

    if isinstance(entry, str):
        if entry.startswith("\"") and entry.endswith("\""):
            return entry
        else:
            return "\"" + entry + "\""

    writeReq += str(entry[0])
    if len(entry) == 1:
        return writeReq

    for req in entry[1:]:
        writeReq += "," + str(req)

    return writeReq


def getStateListFromFile(stateNameFile):
    stateNames = []
    with open(stateNameFile) as readFile:
        firstLineSplits = readFile.readline().split(";")
        while len(firstLineSplits) > 0 and not firstLineSplits[0].strip():
            firstLineSplits = firstLineSplits[1:]
        if not (len(firstLineSplits) > 0 and not firstLineSplits[0].isnumeric()):
            return stateNames

        for split in firstLineSplits:
            stateNames = stateNames + [split.replace("\"", "").replace("\n", "")]


    return stateNames

def getInitialState(stateList, startLocation = DEFAULT_SPAWN):
    startLocationPosition = stateList.index(startLocation)
    return [[] for _ in range(startLocationPosition)] + [[0]] + [[] for _ in range(len(stateList)-startLocationPosition-1)]

def findPoIs(locations):
    pois = []
    for loc in locations:

        if not (loc.endswith("Top") or loc.endswith("Right") or loc.endswith("Bottom") or loc.endswith("Left") or loc.endswith("Middle")):
            pois += [loc]

    return pois


def findFinalState(table, initialState):
    oldState = initialState
    currentState = iterate(table,oldState)

    while getTableLine(oldState) != getTableLine(currentState):
        oldState = currentState
        currentState = iterate(table, oldState)

    return currentState

def findSubIndex(fullList, subList):
    indices = []

    for i in range(len(fullList)):
        if fullList[i] in subList:
            indices += [i]

    return indices

def reduceRequirementTable(table, labels, reducedLocations = None):
    if reducedLocations == None:
        reducedLocations = []
        for label in labels:
            if label.startswith("\"Pickup:") or label.startswith("\"Spawn:"):
                reducedLocations += [label]

    reducedTable = [[] for _ in range(len(reducedLocations))]
    reducedIndex = findSubIndex(labels, reducedLocations)

    print(f'(0/{len(reducedLocations)})')
    for i in range(len(reducedLocations)):
        startLocation = reducedLocations[i]
        initialState = getInitialState(labels, startLocation)
        finalState = findFinalState(table, initialState)
        reducedTable[i] = [finalState[x] for x in reducedIndex]
        print(f'({i+1}/{len(reducedLocations)})')

    return reducedTable, reducedLocations

