import node

def make_grid(width, height):
    retval = []
    for row in range(height):
        row_list = []
        retval.append(row_list)
        for col in range(width):
            row_list.append(node.Node(row, col))
    return retval

class Grid(object):
    def __init__(self, width, height):
        self.grid = make_grid(width, height)
        self.width = width
        self.height = height
        self.link_cells()
        self.distances = None

    def link_cells(self):
        for ridx, row in enumerate(self.grid):
            for cidx, col in enumerate(row):
                col.top = self[(ridx - 1, cidx)]
                col.left = self[(ridx, cidx - 1)]
                col.bottom = self[(ridx + 1, cidx)]
                col.right = self[(ridx, cidx + 1)]

    def __getitem__(self, tup):
        row = tup[0]
        col = tup[1]
        if row < 0 or row >= len(self.grid):
            return None
        row = self.grid[row]
        if col < 0 or col >= len(row):
            return None
        return row[col]

    def iterrows(self):
        for row in self.grid:
            yield row

    def iteritems(self):
        for row in self.grid:
            for cell in row:
                yield cell

    def deadends(self):
        for cell in self.iteritems():
            if cell.is_deadend():
                yield node

    def debug_print(self):
        print "debug_print"
        print '\n'.join([', '.join([str(cell) for cell in row]) for row in self.grid])

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        result = ''
        for row in self.grid:
            r1 = ''
            r2 = ''
            r3 = ''
            for col in row:
                vals = col.clean_str().split('\n')
                r1 += vals[0]
                r2 += vals[1]
                r3 += vals[2]
            result += r1 + '\n' + r2 + '\n'
            if r3.strip():
                result += r3 + '\n'
        return result.decode('utf-8')
