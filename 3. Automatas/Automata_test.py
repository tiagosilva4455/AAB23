import unittest
from Automata import Automata

class test_automata_finite(unittest.TestCase):

    def test_ApplySeq(self):
        automata = Automata("BA", "BAB")
        self.assertEqual(automata.applySeq("BAABABBAB"), [0,1,2,0,1,2,3,1,2,3])
        automata = Automata("ACTG", "ACTG")
        self.assertEqual(automata.applySeq("ACTCTACTG"), [0, 1, 2, 3, 0, 0, 1, 2, 3, 4])

    def test_OccurencesPattern(self):
        automata = Automata("BA", "BAB")
        self.assertEqual(automata.occurencesPattern("BAABABBAB"), [3,6])
        automata = Automata("ACTG", "ACTG")
        self.assertEqual(automata.occurencesPattern("ACTCTACTG"), [5])

if __name__ == '__main__':
    unittest.main()
