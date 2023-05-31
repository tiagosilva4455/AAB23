import unittest
from MyGraph import MyGraph
from debruijn import DeBruijnGraph

class test_DeBruijnGraph(unittest.TestCase):

    def test_balancedGraph(self):
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
        db = DeBruijnGraph(frags)
        self.assertEqual(db.check_nearly_balanced_graph(), ("AC", "AA"))
        
    def test_eulerianPath(self):
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
        db = DeBruijnGraph(frags)
        x = db.eulerian_path()
        y = ["AC", "CC", "CA", "AT", "TT", "TT", "TC", "CA", "AT", "TG", "GG", "GC", "CA", "AT", "TA", "AA"]
        for test, truth in zip(x, y):
            self.assertEqual(str(test), truth)

if __name__ == "__main__":
    unittest.main()
