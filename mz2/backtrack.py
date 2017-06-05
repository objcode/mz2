import random

def make(grid, delay=1):
    item = grid[(0, 0)]
    queue = [item]
    visited = set([item])
    count = 1
    while len(queue):
        item = queue.pop()
        count += 1
        if count % delay == 0:
            yield item
        unlinked = [i for i in item.unlinked() if i not in visited]
        if not unlinked:
            continue
        trial = random.choice(unlinked)
        item.link(trial)
        queue.append(item)
        queue.append(trial)
        visited.add(trial)
        item = trial
