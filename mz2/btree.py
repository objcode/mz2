import random

def make(grid, delay=1):
    count = 0
    for row in range(grid.height - 1, -1, -1):
        for col in range(grid.width):
            items = [grid[(row, col + 1)], grid[(row - 1, col)]]
            items = [item for item in items if item]
            if items:
                choice = random.choice(items)
                count += 1
                if count % delay == 0:
                    yield choice
                grid[(row, col)].link(choice)
