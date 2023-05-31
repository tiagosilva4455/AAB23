import unittest
from Trie import Trie

class TriesTest(unittest.TestCase):

    def test_add_pattern(self):
        t = Trie()
        t.add_pattern("salt")
        t.add_pattern("sand")
        t.add_pattern("surf")
        t.add_pattern("leaf")
        self.assertEqual(t.nodes, {0: {'s': 1, 'l': 10}, 1: {'a': 2, 'u': 7}, 2: {'l': 3, 'n': 5},
                                   3: {'t': 4}, 4: {}, 5: {'d': 6}, 6: {}, 7: {'r': 8},
                                   8: {'f': 9}, 9: {}, 10: {'e': 11}, 11: {'a': 12},
                                12: {'f': 13}, 13: {}})

if __name__ == '__main__':
    unittest.main()
