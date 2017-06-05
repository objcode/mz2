import random

def make(grid, delay=1):
    unvisited = set(grid.iteritems())
    item = grid[(0, 0)]
    adjacent = set(item.adjacent())
    visited = set([item])
    unvisited.remove(item)
    count = 0
    while unvisited:
        trial = random.choice(list(adjacent))
        count += 1
        if count % delay == 0:
            yield trial
        next_to = visited.intersection(trial.adjacent())
        if next_to:
            choice = random.choice(list(next_to))
            choice.link(trial)
        unvisited.remove(trial)
        visited.add(trial)
        adjacent = adjacent.union(trial.adjacent()).intersection(unvisited)
