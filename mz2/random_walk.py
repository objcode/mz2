import random

def make(grid, delay=20):
    unvisited = set(grid.iteritems())
    item = grid[(0, 0)]
    unvisited.remove(item)
    count = 0
    while unvisited:
        trial = random.choice(item.adjacent())
        count += 1
        if count % delay == 0:
            yield trial
        if trial in unvisited:
            item.link(trial)
            unvisited.remove(trial)
        item = trial
