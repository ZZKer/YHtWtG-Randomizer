from enum import Enum
import random
from logic import requirementcalculations as calc

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


class DifficultyOptions(object):
    startWithBlueOrb = False
    startWithRedOrb = False
    startWithBoots = False
    startWithGloves = False
    spikeJumps = False
    tripleJumps = False
    extendedJumps = False

    def __str__(self):
        return (f'Spike Jumps: {self.spikeJumps}\n'
                f'Triple Jumps: {self.tripleJumps}\n'
                f'Extended Jumps: {self.extendedJumps}')

    def toRequirementValue(self):
        return 1 * self.startWithBlueOrb + \
            2 * self.startWithRedOrb + \
            4 * self.startWithBoots + \
            8 * self.startWithGloves + \
            16 * self.spikeJumps + \
            32 * self.tripleJumps + \
            64 * self.extendedJumps

    def setFromRequirementValue(self, value):
        self.startWithBlueOrb = bool(value & 1)
        self.startWithRedOrb = bool(value & 2)
        self.startWithBoots = bool(value & 4)
        self.startWithGloves = bool(value & 8)
        self.spikeJumps = bool(value & 16)
        self.tripleJumps = bool(value & 32)
        self.extendedJumps = bool(value & 64)


class RandomizerOptions(object):
    shuffleSpawn = False  # TODO: Not supported yet
    requireAllOrbs = False  # TODO: Not supported yet
    tpMode = TpShuffleMode.NORMAL  # TODO: Not supported yet
    tpAmount = TPShuffleAmount.REGULAR  # TODO: Not supported yet
    hideTps = False  # TODO: Not supported yet
    hidePowerups = False  # TODO: Not supported yet
    seed = None
    difficultyOptions = DifficultyOptions()  # TODO: Not supported yet


def selectSpawnState(options):
    startRequirements = options.difficultyOptions.toRequirementValue()
    spawnLocation = selectSpawnLocation(options.shuffleSpawn)
    return (spawnLocation, startRequirements)


def selectSpawnLocation(shuffleSpawn):
    """
    Selects a valid spawn location
    TODO: add spawn shuffle functionality
    :param shuffleSpawn: Whether or not the spawn location should be shuffled with treasures
    :return: The spawn location to use
    """
    return DEFAULT_SPAWN


def selectOrbLocations(nrLocs=71, excludeLocs=[27, 43]):
    """
    Selects a random set of unique locations for the orbs.
    :param nrLocs:
    :param excludeLocs: Locations which should be excluded as orb locations (e.g. spawn and end)
    :return:
    """
    orbs = []
    while len(orbs) < 4:
        nextOrb = random.randint(0, nrLocs - 1)
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

    connectionTable, labels = calc.readTable("logic/reduced_map.csv")

    while True:
        spawnState = selectSpawnState(options)
        endLocation = selectEndLocation()
        orbLocations = selectOrbLocations(excludeLocs=[spawnState[0], endLocation])

        solution = findSolution(connectionTable, spawnState, orbLocations, endLocation)
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
        loc = currentLocations.pop()
        visitedLocations += [loc]

        filteredLocs = getLocationRequirements(table[loc[0]], orbs + [end])

        reachableLocs = getReachableLocs(filteredLocs, loc[1])

        currentLocations += updateStates(reachableLocs, orbs, visitedLocations)

    return len(currentLocations) > 0
