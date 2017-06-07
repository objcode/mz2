
class Distances(object):
    def __init__(self, root):
        self.root = root
        self.store = {}
        self.store[root] = 0 # we found one!

    def __getitem__(self, cell):
        return self.store.get(cell)

    def __setitem__(self, cell, distance):
        self.store[cell] = distance

    def __contains__(self, cell):
        return cell in self.store

    def cells(self):
        return self.store.iterkeys()

    def max(self):
        cur, highest = self.root, 0
        for cell, distance in self.store.iteritems():
            if highest <= distance:
                cur, highest = cell, distance
        return cur, highest

    def get_path(self, destination):
        path = []
        while destination:
            path.append(destination)
            newdest = None
            for cell in destination.links:
                if self.store[cell] < self.store[destination]:
                    newdest = cell
            destination = newdest
        return path

    def compute_all(self):
        frontier = [self.root]
        visited = set()
        while frontier:
            next_frontier = []

            for cell in frontier:
                new_distance = self[cell] + 1
                for link in cell.links:
                    if link not in self.store:
                        next_frontier.append(link)
                        self[link] = new_distance
            frontier = next_frontier
