DEFAULT_SPAWN = "You Have to Start the Game Spawn"
DEFAULT_REDORB = "Crimson Aura Pickup"
DEFAULT_BLUEORB = "Cerulean Aura Pickup"
DEFAULT_BOOTS = "Springheel Boots Pickup"
DEFAULT_GLOVES = "Spider Gloves Pickup"
DEFAULT_LOSE = "Consolation Prize Pickup-1"
DEFAULT_WIN = "Eponymous Pickup"

def reduceReqs(reqs):
    """
    Remove requirement values which represent a superset of another requirement.
    Example: [3 (blue orb, red orb),7 (blue orb, red orb, boots)]
          -> [3] (boots are not needed)

    """
    reducedReqs = []
    reqs.sort()
    for req in reqs:
        add = True
        for newReq in reducedReqs:
            if not newReq & ~ req:
                add = False
                break
            elif not req & ~ newReq:
                add = False
                break
        if add:
            reducedReqs = reducedReqs + [req]
    return reducedReqs

def calculateTotalRequirements(newLocationReqs, currentLocationReqs):
    """
    Combines the requirements needed to reach the current location whith the requirements needed to move along an edge
    in the graph to a new location.

    :param newEdgeReqs: Requirements for moving from the current location to a new one
    :param existingReqs: Requirements for reaching the current location
    :return:
    """
    nrNewReqs = len(newLocationReqs)
    nrOldReqs = len(currentLocationReqs)
    totalReqs = [0]*(nrNewReqs*nrOldReqs)
    for i in range(nrNewReqs):
        for j in range(nrOldReqs):
            totalReqs[i*nrOldReqs+j] = newLocationReqs[i] | currentLocationReqs[j]
    return totalReqs

def iterate(matrix, stateVector):
    """
    Does one iteration of the requirement calculation for all location. Calculating the requirements to reach all
    locations on the map from a given spawn point can be done by using a stateVector with all locations set to [] or [-1] (impossible)
    except for the start location itself, which should be set to [0] (no requirements). Afterwards repeatedly call
    this method to make one movement along all possible edges in the graph simultaneously.
    :param matrix: The matrix representing the logic graph for the game map
    :param stateVector: The current requirement state. Should be initialized with a (...[],[0],[],...) where the [0]
    represents the spawn location
    :return: The updated state vector after moving along the edges of the graph. Feed this back into this method as
    the new state vector to make multiple movements.
    """
    ret = [[] for _ in range(len(stateVector))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            #print(f'{matrix[j][i]}, {stateVector[i]}')
            ret[i] += calculateTotalRequirements(matrix[j][i], stateVector[j])
        #print(ret[i])
        ret[i] = reduceReqs(ret[i])
    return ret

def readTable(file):
    """
    Reads the logic graph matrix and the location labels from a file.
    """
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


def writeTable(writeFile, matrix, locationNames=None):
    """
    Writes a logic graph matrix to a file. Optionally allows writing location names as well.
    """
    if isinstance(locationNames, str):
        stateNames = getStateListFromFile(locationNames)
    with open(writeFile, 'w') as writeFile:
        if len(locationNames) > 0:
            writeFile.write(";" + getTableLine(locationNames))
            writeFile.write("\n")

        for i in range(len(matrix)):
            if len(locationNames) > i:
                line = [locationNames[i]] + matrix[i]
            else:
                line = [""] + matrix[i]
            writeFile.write(getTableLine(line))
            writeFile.write("\n")


def getTableLine(entries):
    """
    Helper for writing the matrix to a file
    """
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
    """
    Helper for writing the matrix to a file
    """
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
    """
    Reads the location names from a file (usually a location graph matrix file).
    Probably not needed anymore since readTable also returns the location names
    """
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

def getInitialState(locationList, startLocation = DEFAULT_SPAWN):
    """
    Creates an initial state for the iterate function
    """
    startLocationPosition = locationList.index(startLocation)
    return [[] for _ in range(startLocationPosition)] + [[0]] + [[] for _ in range(len(locationList)-startLocationPosition-1)]

def findPoIs(locations):
    """
    Returns all locations which are not just room edges
    """
    pois = []
    for loc in locations:

        if not (loc.endswith("Top") or loc.endswith("Right") or loc.endswith("Bottom") or loc.endswith("Left") or loc.endswith("Middle")):
            pois += [loc]

    return pois


def findFinalState(matrix, initialState):
    """
    Calculates requirements to reach all locations on the map from an initial state
    :param matrix: The location graph matrix
    :param initialState: Usually should just have the start location set to [0] and the rest to []
    :return: The complete list of requirements for all locations
    """
    oldState = initialState
    currentState = iterate(matrix,oldState)

    while getTableLine(oldState) != getTableLine(currentState):
        oldState = currentState
        currentState = iterate(matrix, oldState)

    return currentState

def findSubIndex(fullList, subList):
    """
    Helper method to easily select a subset from a row in the matrix
    """
    indices = []

    for i in range(len(fullList)):
        if fullList[i] in subList:
            indices += [i]

    return indices

def reduceRequirementTable(table, labels, reducedLocations = None):
    """
    Calculates requirements to reach any location on the map from any other location and returns the entries for
    the given set of locations. Can be used to precalculate the connections between all pickup locations + other
    relevant locations (spawn, end, teleporter, etc.)
    :param table: Location graph matrix
    :param labels: Full list of Location names
    :param reducedLocations: List of relevant locations
    """
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

