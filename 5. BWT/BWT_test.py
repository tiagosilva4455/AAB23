import unittest
from BWT import BWT


class BWT_test(unittest.TestCase):
    def test_build_bwt(self):
        bw = BWT("bioinformatics$")
        self.assertEqual(bw.bwt, "sm$intobriifoca")

        bw = BWT("tiago$")
        self.assertEqual(bw.bwt, "oiatg$")

        bw = BWT("joana$")
        self.assertEqual(bw.bwt, "ano$aj")

    def test_inverse_bwt(self):
        bwt = BWT("bioinformatica$")
        self.assertEqual(bwt.inverse_bwt(), "bioinformatica$")

        bwt = BWT("tiago$")
        self.assertEqual(bwt.inverse_bwt(), "tiago$")

        bwt = BWT("joana$")
        self.assertEqual(bwt.inverse_bwt(), "joana$")

    def test_bw_matching(self):
        bwt = BWT("bioinformatica$")
        self.assertEqual(bwt.bw_matching("o"), [11, 12])

        bwt = BWT("ananas$")
        self.assertEqual(bwt.bw_matching("a"), [1,2,3])

        bwt = BWT("ananas$")
        self.assertEqual(bwt.bw_matching("ana"), [1, 2])

        #tentar com padrao maior, nao estou a perceber como o codigo faz com mais de uma letra


if __name__ == '__main__':
    unittest.main()
