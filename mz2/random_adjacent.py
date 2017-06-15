import random

def make(grid, delay=1):
    item = grid[(0, 0)]
    adjacent = set(item.adjacent())
    count = 0
    while adjacent:
        # start a new run
        trial = random.choice(list(adjacent))
        # join the path to existing if it exists
        linked = [i for i in trial.unlinked() if not i.is_unconnected()]
        if linked:
            trial.link(random.choice(linked))
        while trial:
            count += 1
            if count % delay == 0:
                yield trial
            # look for a previously unvisited neighbor and link to it (walk)
            unlinked = [i for i in trial.unlinked() if i.is_unconnected()]
            if unlinked:
                choice = random.choice(list(unlinked))
                choice.link(trial)
                unlinked.remove(choice)
            else:
                # no neighbors, this path is dead
                choice = None
            #update state for next run
            adjacent.update(unlinked)
            if trial in adjacent:
                adjacent.remove(trial)
            trial = choice
