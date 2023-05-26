import unittest
from SuffixTree import SuffixTree


class SuffixTreesTest(unittest.TestCase):
    def test_add_suffix(self):
        st = SuffixTree()
        st.add_suffix("salt",0)
        st.add_suffix("sand",1)
        st.add_suffix("surf",2)
        st.add_suffix("leaf",3)
        self.assertEqual(st.nodes,
                         {0: (-1, {'l': 10, 's': 1}), 1: (-1, {'a': 2, 'u': 7}), 2: (-1, {'l': 3, 'n': 5}),
                             3: (-1, {'t': 4}), 4: (0, {}), 5: (-1, {'d': 6}),
                             6: (1, {}), 7: (-1, {'r': 8}), 8: (-1, {'f': 9}),
                             9: (2, {}), 10: (-1, {'e': 11}), 11: (-1, {'a': 12}),
                             12: (-1, {'f': 13}), 13: (3, {})})


    def test_find_pattern(self):
        st = SuffixTree()
        st.add_suffix("salt",0)
        st.add_suffix("sand",1)
        st.add_suffix("surf",2)
        st.add_suffix("leaf",3)
        self.assertEqual(st.find_pattern("sa"), "")  # nao percebo o que faz aqui


if __name__ == '__main__':
    unittest.main()
