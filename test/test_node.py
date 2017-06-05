from mz2 import grid, node
import unittest

class NodeTest(unittest.TestCase):

    def setUp(self):
        self.grid = grid.Grid(3, 3)
        self.subject = self.grid[(1, 1)]

    def test_path(self):
        nodes = [self.grid[(0,1)], self.grid[(1, 2)]]
        for node in nodes:
            node.link(self.subject, bidi=True)
            node.mark_on_path()
        self.subject.mark_on_path()
        self.assertEqual(set(nodes), set(self.subject.path_neighbors()))

    def test_path_im_not_on(self):
        nodes = [self.grid[(0,1)], self.grid[(1, 2)]]
        for node in nodes:
            node.link(self.subject, bidi=True)
            node.mark_on_path()
        self.assertEqual(set([]), set(self.subject.path_neighbors()))

    def test_path_on_other_side_of_wall(self):
        nodes = [self.grid[(0,1)], self.grid[(1, 2)]]
        for node in nodes:
            node.mark_on_path()
        nodes[0].link(self.subject)
        self.subject.mark_on_path()
        self.assertEqual(set([nodes[0]]), set(self.subject.path_neighbors()), "path doesn't jump the wall")
