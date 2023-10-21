from enum import Enum

import requirementCalculations as calc


class TpShuffleMode(Enum):
    NORMAL = 0
    SHUFFLE_EXITS = 1
    SHUFFLE_ENTRYS = 2
    SHUFFLE_BOTH = 3

class TPShuffleAmount(Enum):
    REGULAR = 0
    MORE = 1
    ALL = 2

class RandomizerOptions(object):
    shuffleSpawn = False
    requireAllOrbs = False
    tpMode = TpShuffleMode.NORMAL
    tpAmount = TPShuffleAmount.REGULAR
    hideTps = False
    hidePowerups = False

def selectSpawnLocation(options):
    return (27,112)

def selectOrbLocations():
    return [3, 63, 31, 69]

def selectEndLocation():
    return 43

def getOrbLocations(options):
    if not isinstance(options, RandomizerOptions):
        print(f"options needs to be RandomizerOptions but was {type(options)}, using default options instead")
        options = RandomizerOptions()

    connectionTable, labels = calc.readTable("logic_graphs/reduced.csv")

    spawnLocation = selectSpawnLocation(options)

    orbLocations = selectOrbLocations()

    endLocation = selectEndLocation()

    while True:



        solution = findSolution(connectionTable, spawnLocation, orbLocations, endLocation)
        if solution:
            break

    return solution

def containsEnd(locations, end):
    for loc in locations:
        if loc[0] == end:
            return True

    return False

def getLocationRequirements(locationList, filterList):
    locReqList = []
    for filterIndex in filterList:
        locReqList += [(filterIndex, locationList[filterIndex])]

    return locReqList

def getReachableLocs(locationList, fulfilledRequirements):
    reachableLocs = []
    for loc in locationList:
        requirements = loc[1]
        if fulfillsRequirements(requirements, fulfilledRequirements):
            reachableLocs += [(loc[0], fulfilledRequirements)]

    return reachableLocs

def fulfillsRequirements(reqList, fulfilledReqs):
    for req in reqList:
        if not req & ~ fulfilledReqs:
            return True

    return False

def filterLocs(locList, orbLocs, excludeLocs):
    newLocs = []
    for i in range(len(locList)):
        loc = addPower(locList[i], orbLocs)
        if loc not in excludeLocs:
            newLocs += [loc]
    return newLocs

def addPower(loc, orbLocs):
    for i in range(len(orbLocs)):
        if loc[0] == orbLocs[i]:
            return (loc[0], loc[1] | 2 ** i)
    return loc

def findSolution(table, spawn, orbs, end):
    currentLocations = [spawn]
    visitedLocations = []
    solution = None
    while not containsEnd(currentLocations, end) and len(currentLocations) > 0:
        print(currentLocations)
        loc = currentLocations.pop()
        visitedLocations += loc

        filteredLocs = getLocationRequirements(table[loc[0]], orbs + [end])

        reachableLocs = getReachableLocs(filteredLocs, loc[1])

        currentLocations += filterLocs(reachableLocs, orbs, visitedLocations)

    return len(currentLocations) > 0
