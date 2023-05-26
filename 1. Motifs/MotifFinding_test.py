import unittest
from MotifFinding import MotifFinding
from MySeq import MySeq

class MotifFinding_test(unittest.TestCase):

    def test_exhaustiveSearch(self):
        seq1 = MySeq("ATAGAGCTGA", "dna")
        seq2 = MySeq("ACGTAGATGA", "dna")
        seq3 = MySeq("AAGATAGGGG", "dna")
        mf = MotifFinding(3, [seq1, seq2, seq3])
        x = mf.exhaustiveSearch()
        self.assertEqual(str(x), "[1, 3, 4]")

    def test_score(self):
        seq1 = MySeq("ATAGAGCTGA", "dna")
        seq2 = MySeq("ACGTAGATGA", "dna")
        seq3 = MySeq("AAGATAGGGG", "dna")
        mf = MotifFinding(3, [seq1, seq2, seq3])
        sol = [1, 3, 4]
        x = mf.score(sol)
        self.assertEqual(str(x), "9")

    def test_consensus(self):
        seq1 = MySeq("ATAGAGCTGA", "dna")
        seq2 = MySeq("ACGTAGATGA", "dna")
        seq3 = MySeq("AAGATAGGGG", "dna")
        mf = MotifFinding(3, [seq1, seq2, seq3])
        sol = [1, 3, 4]
        x = mf.createMotifFromIndexes(sol).consensus()
        self.assertEqual(str(x), "TAG")

    def test_heuristicConsensus(self):
        seq1 = MySeq("ATAGAGCTGA", "dna")
        seq2 = MySeq("ACGTAGATGA", "dna")
        seq3 = MySeq("AAGATAGGGG", "dna")
        mf = MotifFinding(3, [seq1, seq2, seq3])
        sol = mf.heuristicConsensus()
        x = mf.score(sol)
        self.assertEqual(str(x),"9")


if __name__ == '__main__':
    unittest.main()
