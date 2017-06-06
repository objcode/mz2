import random

def gen(selector):
    def make(grid, delay=1):
        active = [grid.random_node()]

        count = 0
        while active:
            cell = selector(active)
            count += 1
            if count % delay == 0:
                yield cell
            adjacent = [i for i in cell.adjacent() if i.is_unconnected()]
            if adjacent:
                choice = random.choice(adjacent);
                cell.link(choice)
                active.append(choice)
            else:
                active.remove(cell)
    return make


LAST = lambda l: l[-1]
FIRST = lambda l: l[0]
RANDOM = random.choice
