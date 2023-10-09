import unittest
from unittest.mock import patch
import randomizerlogic as logic


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

    @patch('randomizerlogic.fulfillsRequirements')
    def test_getReachableLocs(self, fulfillsRequirementMock):
        fulfillsRequirementMock.side_effect=[True, False, True, True, False]
        self.assertEquals(logic.fulfillsRequirements([],1), True)
        self.assertEquals(logic.fulfillsRequirements([], 1), False)
        self.assertEquals(logic.fulfillsRequirements([], 1), True)
        self.assertEquals(logic.fulfillsRequirements([], 1), True)
        self.assertEquals(logic.fulfillsRequirements([], 1), False)



if __name__ == '__main__':
    unittest.main()
