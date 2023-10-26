from enum import Enum
import random
import requirementCalculations as calc

DEFAULT_SPAWN = 27
DEFAULT_END = 43
DEFAULT_BLUE_ORB = 3
DEFAULT_RED_ORB = 63
DEFAULT_BOOTS = 31
DEFAULT_GLOVES = 69

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
    seed = None

def selectSpawnLocation():
    return (27,112)

def selectOrbLocations(nrLocs = 71, excludeLocs = [27, 43]):
    """
    Selects a random set of unique locations for the orbs.
    :param nrLocs:
    :param excludeLocs: Locations which should be excluded as orb locations (e.g. spawn and end)
    :return:
    """
    orbs = []
    while len(orbs) < 4:
        nextOrb = random.randint(0,nrLocs-1)
        if nextOrb not in excludeLocs and nextOrb not in orbs:
            orbs += [nextOrb]

    return orbs

def selectEndLocation():
    return 43

def generateRandomSeed(options):
    if not isinstance(options, RandomizerOptions):
        print(f"options needs to be RandomizerOptions but was {type(options)}, using default options instead")
        options = RandomizerOptions()

    random.seed(options.seed)

    connectionTable, labels = calc.readTable("logic_graphs/reduced.csv")

    while True:
        spawnLocation = selectSpawnLocation()
        orbLocations = selectOrbLocations()
        endLocation = selectEndLocation()

        solution = findSolution(connectionTable, spawnLocation, orbLocations, endLocation)
        if solution:
            break

    return orbLocations

def isLocationInList(locationList, location):
    for loc in locationList:
        if loc[0] == location:
            return True

    return False

def getLocationRequirements(locationList, filterList):
    """
    Retrieves the requirements to reach a subset of locations
    :param locationList: The full location list
    :param filterList: The subset for which the requirements should be returned
    """
    locReqList = []
    for filterIndex in filterList:
        locReqList += [(filterIndex, locationList[filterIndex])]

    return locReqList

def getReachableLocs(locationList, fulfilledRequirements):
    """
    Returns the locations for which the necessary requirements are fulfilled
    :param locationList: List of locations to check
    :param fulfilledRequirements: Requirements which can be fulfilled
    :return: The reachable locations (combined with the fulfilled requirements)
    """
    reachableLocs = []
    for loc in locationList:
        requirements = loc[1]
        if fulfillsRequirements(requirements, fulfilledRequirements):
            reachableLocs += [(loc[0], fulfilledRequirements)]

    return reachableLocs

def fulfillsRequirements(reqList, fulfilledReqs):
    """
    Checks if a requirement value fulfills any of the requirements in a given list
    :param reqList: The list of possible requirements
    :param fulfilledReqs: The requirement value to check against the list
    """
    for req in reqList:
        if not req & ~ fulfilledReqs:
            return True

    return False

def updateStates(locList, orbLocs, excludeLocs):
    """
    For a given list of location states adds the requirement for a powerup if the location is and orb location
    and removes location in the excluded list
    :param locList: The list of location states
    :param orbLocs: The list of orb locations
    :param excludeLocs: The list of excluded locations
    """
    newLocs = []
    for i in range(len(locList)):
        loc = addPower(locList[i], orbLocs)
        if loc not in excludeLocs:
            newLocs += [loc]
    return newLocs

def addPower(loc, orbLocs):
    """
    Adds the requirement fulfilled by a powerup to the given location state and returns it
    :param loc: The location state to check
    :param orbLocs: The list of orb locations
    :return: The updated location state
    """
    for i in range(len(orbLocs)):
        if loc[0] == orbLocs[i]:
            return (loc[0], loc[1] | 2 ** i)
    return loc

def findSolution(table, spawn, orbs, end):
    """
    Tries to find path from the spawn to the end location by checking repeatedly if either the end is reachable directly
    or a new orb can be reached (and the corresponding powerup is picked up). This is done using depth-first search
    through all states which can be reached that way
    TODO: return the path to the end
    :param table: logic graph
    :param spawn: Index of the spawn location
    :param orbs: Indices of the orb locations
    :param end: Index of the end location
    :return: True if the end can be reached from the spawn, False otherwise
    """
    currentLocations = [spawn]
    visitedLocations = []
    solution = None
    while not isLocationInList(currentLocations, end) and len(currentLocations) > 0:
        print(currentLocations)
        loc = currentLocations.pop()
        visitedLocations += [loc]

        filteredLocs = getLocationRequirements(table[loc[0]], orbs + [end])

        reachableLocs = getReachableLocs(filteredLocs, loc[1])

        currentLocations += updateStates(reachableLocs, orbs, visitedLocations)

    return len(currentLocations) > 0
