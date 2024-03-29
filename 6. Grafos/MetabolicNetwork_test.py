import unittest
from MyGraph import MyGraph
from MetabolicNetwork import MetabolicNetwork

class test_MetabolicNetwork(unittest.TestCase):

    def test_getNodeType_REACTION(self):
        mn = MetabolicNetwork("metabolite-reaction")
        mn.add_vertex_type("R1", "reaction")
        mn.add_vertex_type("R2", "reaction")
        mn.add_vertex_type("R3", "reaction")
        mn.add_vertex_type("M1", "metabolite")
        mn.add_vertex_type("M2", "metabolite")
        mn.add_vertex_type("M3", "metabolite")
        mn.add_vertex_type("M4", "metabolite")
        mn.add_vertex_type("M5", "metabolite")
        mn.add_vertex_type("M6", "metabolite")
        mn.add_edge("M1", "R1")
        mn.add_edge("M2", "R1")
        mn.add_edge("R1", "M3")
        mn.add_edge("R1", "M4")
        mn.add_edge("M4", "R2")
        mn.add_edge("M6", "R2")
        mn.add_edge("R2", "M3")
        mn.add_edge("M4", "R3")
        mn.add_edge("M5", "R3")
        mn.add_edge("R3", "M6")
        mn.add_edge("R3", "M4")
        mn.add_edge("R3", "M5")
        mn.add_edge("M6", "R3")
        for test, truth in zip(mn.get_nodes_type("reaction"), ["R1", "R2", "R3"]):
            self.assertEqual(str(test), truth)


    def test_getNodeType_METABOLITE(self):
        mn = MetabolicNetwork("metabolite-reaction")
        mn.add_vertex_type("R1", "reaction")
        mn.add_vertex_type("R2", "reaction")
        mn.add_vertex_type("R3", "reaction")
        mn.add_vertex_type("M1", "metabolite")
        mn.add_vertex_type("M2", "metabolite")
        mn.add_vertex_type("M3", "metabolite")
        mn.add_vertex_type("M4", "metabolite")
        mn.add_vertex_type("M5", "metabolite")
        mn.add_vertex_type("M6", "metabolite")
        mn.add_edge("M1", "R1")
        mn.add_edge("M2", "R1")
        mn.add_edge("R1", "M3")
        mn.add_edge("R1", "M4")
        mn.add_edge("M4", "R2")
        mn.add_edge("M6", "R2")
        mn.add_edge("R2", "M3")
        mn.add_edge("M4", "R3")
        mn.add_edge("M5", "R3")
        mn.add_edge("R3", "M6")
        mn.add_edge("R3", "M4")
        mn.add_edge("R3", "M5")
        mn.add_edge("M6", "R3")
        for test, truth in zip(mn.get_nodes_type("metabolite"), ["M1", "M2", "M3", "M4", "M5", "M6"]):
            self.assertEqual(str(test), truth)

if __name__ == '__main__':
    unittest.main()