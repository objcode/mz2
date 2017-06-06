import random

def make(grid, delay=1):
    stack = [grid[(0, 0)]]
    count = 1
    while stack:
        item = stack[-1]
        count += 1
        if count % delay == 0:
            yield item
        unlinked = [i for i in item.unlinked() if i.is_unconnected()]
        if not unlinked:
            stack.pop()
            continue
        else:
            neighbor = random.choice(unlinked)
            item.link(neighbor)
            stack.append(neighbor)
