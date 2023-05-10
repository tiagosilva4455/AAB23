import unittest
from Automata import Automata

class test_automata_finite(unittest.TestCase):

    def test_ApplySeq(self):
        self.assertEqual(Automata("BA", "BAB").applySeq("BAABABBAB"), [0,1,2,0,1,2,3,1,2,3])

    def test_OccurencesPattern(self):
        self.assertEqual(Automata("BA", "BAB").occurencesPattern("BAABABBAB"), [3,6])

suite =unittest.TestLoader().loadTestsFromTestCase(test_automata_finite)
unittest.TextTestRunner(verbosity=3).run(suite)