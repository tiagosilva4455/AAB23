import unittest
from MyGraph import MyGraph


class graph_test(unittest.TestCase):

        def test_add_vertex(self):
            g = MyGraph()
            g.add_vertex(1)
            self.assertEqual({1: []}, g.graph)


        def test_add_edge(self):
            g = MyGraph()
            g.add_edge(1, 2)
            self.assertEqual({1: [2],2:[]}, g.graph)

        def test_get_nodes(self):
            g = MyGraph()
            g.add_vertex(1)
            g.add_vertex(2)
            self.assertEqual(g.get_nodes(), [1, 2])

        def test_get_edges(self):
            g = MyGraph()
            g.add_edge(1, 2)
            g.add_edge(1, 3)
            self.assertEqual(g.get_edges(), [(1, 2), (1, 3)])

        def test_size(self):
            g = MyGraph()
            g.add_vertex(1)
            g.add_vertex(2)
            g.add_edge(1, 2)
            self.assertEqual(g.size(), (2, 1))

        def test_get_successors(self):
            g = MyGraph()
            g.add_edge(1, 2)
            g.add_edge(1, 3)
            self.assertEqual(g.get_successors(1), [2, 3])

        def test_get_predecessors(self):
            g = MyGraph()
            g.add_edge(1, 2)
            g.add_edge(3, 2)
            self.assertEqual(g.get_predecessors(2), [1, 3])

        def test_get_adjacents(self):
            g = MyGraph()
            g.add_edge(1, 2)
            g.add_edge(1, 3)
            g.add_edge(3, 2)
            self.assertEqual(g.get_adjacents(1), [2, 3])

        def test_out_degree(self):
            g = MyGraph()
            g.add_edge(1, 2)
            self.assertEqual(g.out_degree(1), 1)

        def test_in_degree(self):
            g = MyGraph()
            g.add_edge(1, 2)
            g.add_edge(3, 2)
            self.assertEqual(g.in_degree(2), 2)

        def test_degree(self):
            g = MyGraph()
            g.add_edge(1, 2)
            g.add_edge(1, 3)
            g.add_edge(3, 2)
            self.assertEqual(g.degree(1), 2)

        def test_reachable_bfs(self):
            g = MyGraph()
            g.add_edge(1, 2)
            g.add_edge(1, 3)
            g.add_edge(3, 2)
            self.assertEqual(g.reachable_bfs(1), [2, 3])


if __name__ == '__main__':
    unittest.main()
