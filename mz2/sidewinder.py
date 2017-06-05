import random

def grow_north(grid, run, item):
    grow_from = random.choice(run)
    link = grid[(grow_from.row - 1, grow_from.col)]
    if link:
        run[:] = []
    return link, grow_from if link else item

def grow_right(grid, item):
    link = grid[(item.row, item.col + 1)]
    return link

def make(grid, delay=1):
    count = 0
    for row in range(grid.height - 1, -1, -1):
        run = []
        for col in range(grid.width):
            choice = random.choice(['H', 'T'])
            item = grid[(row, col)]
            run.append(item)
            if choice == 'H':
                link, item = grow_north(grid, run, item)
            if choice == 'T' or link is None:
                link = grow_right(grid, item)
            if not link:
                link, item = grow_north(grid, run, item)

            if link:
                count += 1
                if link and count % delay == 0:
                    yield item
                item.link(link)
