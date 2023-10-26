import unittest
from unittest.mock import patch
import random
import randomizerlogic as logic
import requirementCalculations as calc


class RandomizerLogicTest(unittest.TestCase):

    def test_fulfillsRequirements(self):
        self.assertTrue((logic.fulfillsRequirements([0], 0)))
        self.assertTrue(logic.fulfillsRequirements([0], 127))
        self.assertTrue((logic.fulfillsRequirements([127], 127)))
        self.assertTrue((logic.fulfillsRequirements([3], 19)))
        self.assertTrue((logic.fulfillsRequirements([127, 0], 0)))
        self.assertTrue((logic.fulfillsRequirements([0, 127], 0)))
        self.assertTrue((logic.fulfillsRequirements([3, 127, 5, 16], 37)))
        self.assertTrue((logic.fulfillsRequirements([3, 127, 5, 16], 21)))
        self.assertFalse((logic.fulfillsRequirements([127], 0)))
        self.assertFalse(logic.fulfillsRequirements([], 127))
        self.assertFalse((logic.fulfillsRequirements([-1], 127)))
        self.assertFalse((logic.fulfillsRequirements([3], 126)))
        self.assertFalse((logic.fulfillsRequirements([3, 6, 24], 21)))


    def test_getReachableLocs(self):
        self.assertEqual(logic.getReachableLocs([("loc0",[0])],0), [("loc0",0)])
        self.assertEqual(logic.getReachableLocs([("loc0", [0])], 13), [("loc0", 13)])
        self.assertEqual(logic.getReachableLocs([("loc0", [1])], 0), [])
        self.assertEqual(logic.getReachableLocs([("loc0", [1,2,4])], 8), [])
        self.assertEqual(logic.getReachableLocs([("loc0", [1,2])], 5), [("loc0", 5)])
        self.assertEqual(logic.getReachableLocs([("loc0", [8]),("loc1", [0]),("loc2", [1])], 5), [("loc1", 5), ("loc2", 5)])
        self.assertEqual(logic.getReachableLocs([("loc0", []),("loc1", [-1]),("loc2", [16])], 15), [])

    def test_getLocationsRequirements(self):
        locationList = [[0],[1],[2,3],[4,5,6],[0]]
        self.assertEquals(logic.getLocationRequirements(locationList, [0]),[(0,[0])])
        self.assertEquals(logic.getLocationRequirements(locationList, [1,2]),[(1,[1]),(2,[2,3])])
        self.assertEquals(logic.getLocationRequirements(locationList, [3,4]),[(3,[4,5,6]),(4,[0])])
        self.assertEquals(logic.getLocationRequirements(locationList, [0, 4]), [(0, [0]), (4, [0])])

    def test_addPower(self):
        self.assertEqual(logic.addPower((0,0),[0]),(0,1))
        self.assertEqual(logic.addPower((0,0), [1]), (0,0))
        self.assertEqual(logic.addPower((15,3), [1,2,15,3]), (15,7))
        self.assertEqual(logic.addPower((15,0), [1,2,3,4]), (15,0))

    def test_filterLocs(self):
        self.assertEqual(logic.updateStates([(0,0)],[0],[]),[(0,1)])
        self.assertEqual(logic.updateStates([(0, 0)], [0], [(0,1)]), [])
        self.assertEqual(logic.updateStates([(1, 0)], [0,1], [(1, 0)]), [(1,2)])
        self.assertEqual(logic.updateStates([(15, 3)], [1,2,15,3], []), [(15, 7)])
        self.assertEqual(logic.updateStates([(15,6),(0, 0),(1,1),(3,4)], [0,15,1,4], [(0,1),(2,0),(3,4),(15,8)]), [(15, 6),(1,5)])

    def test_findSolution(self):
        testMap = calc.readTable("logic_graphs/reduced.csv")[0]
        spawnLocation = (logic.DEFAULT_SPAWN,112)
        orbs = [logic.DEFAULT_BLUE_ORB, logic.DEFAULT_RED_ORB, logic.DEFAULT_BOOTS, logic.DEFAULT_GLOVES]
        end = logic.DEFAULT_END

        self.assertEqual(logic.findSolution(testMap, spawnLocation, orbs, end), True)

        orbs = [17,57,21,64]
        self.assertEqual(logic.findSolution(testMap, spawnLocation, orbs, end), True)
        orbs = [17, 57, 22, 64]
        self.assertEqual(logic.findSolution(testMap, spawnLocation, orbs, end), False)

    @patch('randomizerlogic.selectOrbLocations')
    def test_generateRandomSeed(self, orbSelectionMock):
        orbSelectionMock.return_value = [3, 63, 31, 69]
        self.assertEqual(logic.generateRandomSeed(None), [3,63,31,69])
        
    def test_selectOrbLocations(self):
        random.seed(0)
        self.assertEqual(logic.selectOrbLocations(), [49,53,5,33])


if __name__ == '__main__':
    unittest.main()
