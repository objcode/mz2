import random

def make(grid, delay=1):
    current = grid[(random.randint(0, grid.height - 1), random.randint(0, grid.width -1))]
    count = 0
    while current:
        available = [node for node in current.unlinked() if not node.links]
        if available:
            choice = random.choice(available)
            count += 1
            if count % delay == 0:
                yield current
            current.link(choice)
            current = choice
        else:
            current = None # we might be done, but do a hunt to see
            for node in grid.iteritems():
                count += 1
                if count % delay == 0:
                    yield node
                visited = [a for a in node.adjacent() if a.links]
                if not node.links and visited:
                    current = node
                    choice = random.choice(visited)
                    current.link(choice)
                    break
