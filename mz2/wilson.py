import random

def make(grid, delay = 1):
    unvisited = set(grid.iteritems())
    first = random.choice(list(unvisited))
    unvisited.discard(first)

    while unvisited:
        cell = random.choice(list(unvisited))
        count = 0
        path = [cell]
        while cell in unvisited:
            count += 1
            if count % delay == 0:
                yield cell
            adjacent = cell.adjacent()
            old_choice = cell
            cell = random.choice(adjacent)
            for pos, item in enumerate(path):
                if item == cell:
                    path = path[:pos + 1]
                    break
            else:
                path.append(cell)


        last_cell = None
        for cell in path:
            if last_cell:
                cell.link(last_cell)
                unvisited.discard(cell)
                unvisited.discard(last_cell)
            last_cell = cell
